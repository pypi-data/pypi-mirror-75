import boto3
import datetime
import json
import time,os,subprocess
import botocore.exceptions
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class AWSIoTOperation:

    '''
    AWS IoT Core Error Code and Error Message
    400: Bad Request - ．Invalid JSON
                       ．Missing required node: state
                       ．State node must be an object
                       ．Desired node must be an object
                       ．Reported node must be an object
                       ．Invalid version
                       ．Invalid clientToken
                       ．JSON contains too many levels of nesting; maximum is 6
                       ．State contains an invalid node
    401: Unauthorized
    403: Forbidden
    404: Not Found
    409: Conflict
    410: Limit Exceeded
    413: Payload Too Large - The payload exceeds the maximum size allowed
    415: Unsupported Media Type - Unsupported documented encoding; supported encoding is UTF-8
    422: Failed to Process Request
    429: Too Many Requests - The Device Shadow service will generate this error message when there are more than 10 in-flight requests
    500: Internal Server Error
    503: Service Unavailable
    '''

    def __init__(self, setting=None):
        self.setting = setting
        self.fleet_indexing = False
        if 'fleet_indexing' in self.setting:
            if self.setting['fleet_indexing'] == 'true':
                self.fleet_indexing = True
        # login by cli for update "~/.aws/credentials"
        if os.path.exists("~/.aws/credentials") == False:
            os.system("mkdir -p ~/.aws")
            os.system("echo \"{}\" > ~/.aws/credentials".format("""[default]
aws_access_key_id={}
aws_secret_access_key={}""".format(self.setting['access_key_id'], self.setting['secret_access_key'])))

        # os.system("AWS_ACCESS_KEY_ID={} AWS_SECRET_ACCESS_KEY={} aws ecr get-login --no-include-email --region {}".format(
        #         self.setting['access_key_id'],
        #         self.setting['secret_access_key'],
        #         self.setting['region_name']))

        self.iot = boto3.client(
            'iot',
            region_name=self.setting['region_name'],
            aws_access_key_id=self.setting['access_key_id'],
            aws_secret_access_key=self.setting['secret_access_key']
        )

        self.shadow = boto3.client('iot-data', region_name=self.setting['region_name'])
        self.account_id = boto3.client('sts').get_caller_identity()['Account']
        self.things_content = []
        self.myAWSIoTMQTTClient = None

    def search_devices(self):
        if self.fleet_indexing == True:
            response = self.iot.search_index(
                indexName='AWS_Things',
                queryString='thingName: *',
                maxResults=250,
                queryVersion='2017-09-30'
            )
        else:
            response = self.iot.list_things()

        devices = []
        for device in response['things']:
            new_dev = {
                'name': device['thingName'],
                'desired': {}, 'reported': {}, 'timestamp': 0,
                'connected': False,
            }

            if 'connectivity' in device:
                new_dev['connected'] = device['connectivity']['connected']
                new_dev['timestamp'] = device['connectivity']['timestamp']

            if 'shadow' not in device:
                devices.append(new_dev)
                continue

            shadow = json.loads(device['shadow'])
            if 'desired' in shadow:
                new_dev['desired'] = shadow['desired']
            if 'reported' in shadow:
                new_dev['reported'] = shadow['reported']

            devices.append(new_dev)
        self.things_content = devices
        return self.things_content

    def search_device(self, name):
        stream_body = self.shadow.get_thing_shadow(thingName=name)["payload"]
        shadows_data = json.loads(stream_body.read())
        response = {
            'things': [
                {
                    'thingName': name,
                    'connectivity': {'connected': False},
                    'shadow': json.dumps(shadows_data['state']),
                },
            ]
        }

        if self.fleet_indexing == True:
            index = self.iot.search_index(
                indexName='AWS_Things',
                queryString='thingName: '+name,
                maxResults=250,
                queryVersion='2017-09-30'
            )
            if len(index) > 0:
                response['things'][0]['connectivity']['connected'] = index['things'][0]['connectivity']['connected']
                response['things'][0]['connectivity']['timestamp'] = index['things'][0]['connectivity']['timestamp']

        devices = []
        for device in response['things']:
            new_dev = {
                'name': device['thingName'],
                'desired': {}, 'reported': {}, 'timestamp': 0,
                'connected': device['connectivity']['connected'],
            }
            if 'shadow' not in device:
                devices.append(new_dev)
                continue
            
            shadow = json.loads(device['shadow'])
            if 'desired' in shadow:
                new_dev['desired'] = shadow['desired']
            if 'reported' in shadow:
                new_dev['reported'] = shadow['reported']
            if 'timestamp' in device['connectivity']:
                new_dev['timestamp'] = device['connectivity']['timestamp']
            devices.append(new_dev)
        return devices

    def  get_properties(self, name):
        for device in self.things_content:
            if device['name'] == name:
                return {'desired': device['desired'], 'reported': device['reported']}
        return {'desired': {}, 'reported': {}}

    def desired(self, device_name, desired_payload):
        desired_dict = json.loads(desired_payload)
        data = {"state": {"desired": desired_dict}}
        response = self.shadow.update_thing_shadow(
            thingName=device_name,
            payload=json.dumps(data).encode("utf-8")
        )
        return response['ResponseMetadata']['HTTPStatusCode']

    def message_callback(self, client, userdata, message):
        print(message.topic)
        print(message.payload.decode('utf-8'))
        self.callback(message.topic, message.payload.decode('utf-8'))

    def unsubscribe_messages(self, topic):
        if self.myAWSIoTMQTTClient == None:
            return
        self.myAWSIoTMQTTClient.unsubscribe(topic)
        self.myAWSIoTMQTTClient.disconnect()

    def subscribe_messages(self, callback, topic='#', second=-1):
        self.callback = callback
        self.myAWSIoTMQTTClient = None
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient('', useWebsocket=True)
        self.myAWSIoTMQTTClient.configureIAMCredentials(self.setting['access_key_id'], self.setting['secret_access_key'])
        self.myAWSIoTMQTTClient.configureEndpoint(self.setting['host'], 443)
        self.myAWSIoTMQTTClient.configureCredentials(self.setting['root_ca_path'])
        if self.myAWSIoTMQTTClient.connect() == False:
            print('connect failed')
            self.myAWSIoTMQTTClient = None
            return

        print('connect:ok, subscribe topic[%s] %d sec\n' % (topic, second))

        self.myAWSIoTMQTTClient.subscribe(topic, 1, self.message_callback)
        if second <=0:
            return

        time.sleep(second)
        self.myAWSIoTMQTTClient.unsubscribe(topic)
        self.myAWSIoTMQTTClient.disconnect()
        self.myAWSIoTMQTTClient = None
    
    def open_tunnel(self, device_id, service, port):
        p = subprocess.Popen([
            'aws', 'iotsecuretunneling', 'open-tunnel',
            '--destination-config', 'thingName={},services={}'.format(device_id, service),
            '--timeout-config', 'maxLifetimeTimeoutMinutes=30',
            '--region', self.setting['region_name']], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if rc != 0:
            return err

        token = json.loads(output)['sourceAccessToken']
        # setup tunnel conf
        os.system("mkdir -p /data")
        os.system("echo \"{}\" > /data/.aws_tunnel.ini".format("""region = {}
source-listen-port = {}
access-token = {}""".format(self.setting['region_name'], port, token)))
        # start tunnel service
        # os.system("docker kill aws-tunnel 2> /dev/null")
        # os.system("docker rm -f aws-tunnel 2> /dev/null")
        # os.system(
        #     'docker run -d --network host -v /tmp/:/tmp/ --name aws-tunnel bibbylong/aws-localproxy-cli:1.0.1-amd64 sh -c "localproxy --config /tmp/.aws_tunnel.ini"')
        return ''

    def command(self, device_id, name, payload, retry_time=10):
        job_id = "{}_{}".format(device_id, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
        status, response = self.create_jobs([device_id], name, payload, job_id)
        if status <200 or status > 299:
            return status, {'error':'create command failed'}

        for i in range(retry_time):
            try:
                job_info = self.get_job_exec_status(device_id, job_id)
                if job_info['status'] != 'IN_PROGRESS' and job_info['status'] != 'QUEUED':
                    break
                time.sleep(1)
            except:
                time.sleep(1)

        if job_info['status'] == 'IN_PROGRESS' or job_info['status'] == 'QUEUED':
            return 400, {'error':'command panding'}
        elif job_info['status'] == 'SUCCEEDED':
            try:
                json_object = json.loads(job_info['statusDetails']['detailsMap']['data'])
                return 200, json_object
            except ValueError as e:
                return 200, {'data':job_info['statusDetails']['detailsMap']['data']}
        else:
            return 400, {'error':'process command failed'}

    def get_shadow(self, device_id):
        response = self.shadow.get_thing_shadow(
            thingName=device_id
        )
        status = response['ResponseMetadata']['HTTPStatusCode']
        result = json.loads(response['payload'].read().decode('utf-8'))
        result.pop('metadata', None)
        return status, result

    def update_shadow(self, device_id, data):
        # data format example:
        # data = {'state': {'desired': {'general': {'description': 'new name'}}}}
        try:
            response = self.shadow.update_thing_shadow(
                thingName=device_id,
                payload=json.dumps(data).encode('utf-8')
            )
            status = response['ResponseMetadata']['HTTPStatusCode']
            result = json.loads(response['payload'].read().decode('utf-8'))
        except botocore.exceptions.ClientError as err:
            status = err.response['ResponseMetadata']['HTTPStatusCode']
            result = err.response
        return status, result

    def get_application_list(self, device_id):
        status, shadow = self.get_shadow(device_id)
        list = []
        if 'state' in shadow and 'reported' in shadow['state']:
            reported = shadow['state']['reported']
            if 'applications' in reported and 'list' in reported['applications']:
                list = reported['applications']['list']
        return status, list

    def install_application(self, device_id, app_url):
        params = json.dumps({'url': app_url})
        status, response = self.create_jobs(
            [device_id], 'thingspro-applications-installation', params, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        )
        return status, response

    def application_control(self, device_id, app_name, action):
        if action in ['start', 'stop', 'restart']:
            params = json.dumps({'appName': app_name, 'command': action})
            status, response = self.create_jobs(
                [device_id], 'thingspro-applications-control', params, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            )
            return status, response
        else:
            return 400, None

    def create_jobs(self, device_id_list, method, params, job_id):
        body = json.dumps({
            'name': method,
            'payload': params
        })
        target_list = []
        for device_id in device_id_list:
            target_string = 'arn:aws:iot:%s:%s:thing/%s' % (
                self.setting['region_name'], self.account_id, device_id)
            target_list.append(target_string)
        try:
            response = self.iot.create_job(
                jobId=job_id,
                targets=target_list,
                document=body,
                description='create a new job',
                targetSelection='SNAPSHOT'
            )
            status = response['ResponseMetadata']['HTTPStatusCode']
        except botocore.exceptions.ClientError as err:
            print(err)
            status = err.response['ResponseMetadata']['HTTPStatusCode']
            response = err.response
        return status, response

    def reboot(self, device_id_list):
        status, response = self.create_jobs(
            device_id_list, 'system-reboot', '{}', datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
        return status, response

    def get_all_jobs(self, count):
        if count > 250:
            count = 250
        response = self.iot.list_jobs(
            maxResults=count
        )
        return response['jobs']

    def get_device_jobs(self, device_id, count=250):
        if count > 250:
            count = 250
        response = self.iot.list_job_executions_for_thing(
            thingName=device_id,
            maxResults=count
        )
        return response['executionSummaries']

    def get_job(self, job_id):
        response = self.iot.describe_job(
            jobId=job_id
        )
        return response['job']

    def get_job_exec_status(self, device_id, job_id):
        response = self.iot.describe_job_execution(
            jobId=job_id,
            thingName=device_id,
        )
        return response['execution']

    def get_job_payload(self, job_id):
        response = self.iot.get_job_document(
            jobId=job_id
        )
        return response['document']
