import base64
import hashlib
import hmac
import json
import requests
import time
import urllib
import asyncio
import threading
from azure.eventhub import TransportType
from azure.eventhub import EventHubConsumerClient

class AzureIoTOperation:
    API_VERSION = "2018-06-30"
    TOKEN_VALID_SECS = 365 * 24 * 60 * 60
    TOKEN_FORMAT = "SharedAccessSignature sr=%s&sig=%s&se=%s&skn=%s"

    def __init__(self, setting=None):
        self.setting = setting
        if self.setting['connection_string'] != None:
            host, key, value = [sub[sub.index("=") + 1:] for sub in self.setting['connection_string'].split(";")]
            self.iot_host = host
            self.key_name = key
            self.key_value = value

    def _build_expiry_on(self):
        return "%d" % (time.time() + self.TOKEN_VALID_SECS)
    
    def _build_sas_token(self):
        target_uri = self.iot_host.lower()
        expiry_time = self._build_expiry_on()
        to_sign = "%s\n%s" % (target_uri, expiry_time)
        key = base64.b64decode(self.key_value.encode("utf-8"))
        signature = urllib.parse.quote(
            base64.b64encode(
                hmac.HMAC(key, to_sign.encode("utf-8"), hashlib.sha256).digest()
            )
        ).replace("/", "%2F")
        return self.TOKEN_FORMAT % (target_uri, signature, expiry_time, self.key_name)

    def get_module_twin(self, device_id, module_id):
        connected = False
        token = self._build_sas_token()
        url = "https://%s/twins/%s/modules/%s?api-version=%s" % (self.iot_host, device_id, module_id, self.API_VERSION)
        r = requests.get(url, headers={"Content-Type": "application/json", "Authorization": token})
        if r.status_code < 200 or r.status_code > 299:
            print('get device twin failed')
            return {
                'connected': False, 
                'desired': {},
                'reported': {},
                'timestamp': '0001-01-01T00:00:00Z'
            }
        response = json.loads(r.text)
        if '$metadata' in response['properties']['desired']:
            del response['properties']['desired']['$metadata']
        if '$version' in response['properties']['desired']:
            del response['properties']['desired']['$version']
        if '$metadata' in response['properties']['reported']:
            del response['properties']['reported']['$metadata']
        if '$version' in response['properties']['reported']:
            del response['properties']['reported']['$version']
        if response['connectionState'] == 'Connected':
            connected = True
        return {
            'connected': connected, 
            'desired': response['properties']['desired'],
            'reported': response['properties']['reported'],
            'timestamp': response['lastActivityTime']
        }

    def get_device_twin(self, device_id):
        connected = False
        token = self._build_sas_token()
        url = "https://%s/twins/%s?api-version=%s" % (self.iot_host, device_id, self.API_VERSION)
        r = requests.get(url, headers={"Content-Type": "application/json", "Authorization": token})
        if r.status_code < 200 or r.status_code > 299:
            print('get device twin failed')
            return {
                'connected': False, 
                'desired': {},
                'reported': {},
                'timestamp': '0001-01-01T00:00:00Z'
            }
        response = json.loads(r.text)
        if '$metadata' in response['properties']['desired']:
            del response['properties']['desired']['$metadata']
        if '$version' in response['properties']['desired']:
            del response['properties']['desired']['$version']
        if '$metadata' in response['properties']['reported']:
            del response['properties']['reported']['$metadata']
        if '$version' in response['properties']['reported']:
            del response['properties']['reported']['$version']
        if response['connectionState'] == 'Connected':
            connected = True
        return {
            'connected': connected, 
            'desired': response['properties']['desired'],
            'reported': response['properties']['reported'],
            'timestamp': response['lastActivityTime']
        }

    def search_devices(self):
        token = self._build_sas_token()
        url = "https://%s/devices?api-version=%s" % (self.iot_host, self.API_VERSION)
        r = requests.get(url, headers={"Content-Type": "application/json", "Authorization": token})
        if r.status_code < 200 or r.status_code > 299:
            print('list iot device failed')
            return []
        response = json.loads(r.text)
        devices = []
        for device in response:
            new_dev = {
                'name': device['deviceId'],
                'desired': {}, 'reported': {}, 'timestamp': 0,
                'connected': False,
                'timestamp': device['lastActivityTime'],
            }
            if device['connectionState'] == 'connected':
                new_dev['connected'] = True
            devices.append(new_dev)
        self.things_content = devices
        return self.things_content

    def search_device(self, name):
        names = name.split("?module=")
        if len(names) > 1:
            prop = self.get_module_twin(names[0], names[1])
        else:
            prop = self.get_device_twin(names[0])
        prop['name'] = name
        return [prop]

    def device_desired(self, device_name, desired_payload):
        properties = {"properties": {"desired": json.loads(desired_payload)}}
        token = self._build_sas_token()
        url = "https://%s/twins/%s?api-version=%s" % (self.iot_host, device_name, self.API_VERSION)
        r = requests.patch(url, headers={"Content-Type": "application/json", "Authorization": token, "If-Match": "*"}, data=json.dumps(properties))
        if r.status_code == 429:
            waiting = r.headers['Retry-After'] if r.headers['Retry-After'] <= 10 else 10
            time.sleep(waiting)
            return 998
        return r.status_code

    def module_desired(self, device_name, module_name, desired_payload):
        properties = {"properties": {"desired": json.loads(desired_payload)}}
        token = self._build_sas_token()
        url = "https://%s/twins/%s/modules/%s?api-version=%s" % (self.iot_host, device_name, module_name, self.API_VERSION)
        r = requests.patch(url, headers={"Content-Type": "application/json", "Authorization": token, "If-Match": "*"}, data=json.dumps(properties))
        if r.status_code == 429:
            waiting = r.headers['Retry-After'] if r.headers['Retry-After'] <= 10 else 10
            time.sleep(waiting)
            return 998
        return r.status_code

    def desired(self, name, desired_payload):
        names = name.split("?module=")
        if len(names) > 1:
            return self.module_desired(names[0], names[1], desired_payload)
        else:
            return self.device_desired(names[0], desired_payload)

    def on_event_batch(self, partition_context, events):
        for event in events:
            data = {
                'telemetry': event.body_as_str(),
                'properties': event.properties,
            }
            if b'iothub-connection-device-id' in event.system_properties:
                if event.system_properties[b'iothub-connection-device-id'].decode('utf-8') != self.sub_device and self.sub_device != "#":
                    continue
                data['deviceID'] = event.system_properties[b'iothub-connection-device-id'].decode('utf-8')
            if b'iothub-connection-module-id' in event.system_properties:
                data['moduleID'] = event.system_properties[b'iothub-connection-module-id'].decode('utf-8')
            self.callback(self.sub_device, json.dumps(data))
        partition_context.update_checkpoint()

    def on_error(self, partition_context, error):
        # Put your code here. partition_context can be None in the on_error callback.
        if partition_context:
            print("An exception: {} occurred during receiving from Partition: {}.".format(
                partition_context.partition_id,
                error
            ))
        else:
            print("An exception: {} occurred during the load balance process.".format(error))

    def unsubscribe_messages(self, topic):
        self.client.close()
        self.clientt.join()
        print('sub exit success')

    def sub_routine(self):
        try:
            with self.client:
                self.client.receive_batch(
                    on_event_batch=self.on_event_batch,
                    on_error=self.on_error
                )
        finally:
            return

    def subscribe_messages(self, callback, topic='#', second=-1):
        self.sub_device = topic
        self.callback = callback
        self.client = EventHubConsumerClient.from_connection_string(
            conn_str=self.setting['eventhub_connection_string'],
            consumer_group="$default",
        )

        self.clientt = threading.Thread(target = self.sub_routine)
        self.clientt.start()

        print('connect:ok, subscribe device[%s] %d sec\n' % (self.sub_device, second))

        if second <=0:
            return

        time.sleep(second)
        self.client.close()
        self.clientt.join()
        print('sub exit success')

    def open_tunnel(self, device_id, service, port):
        return "unsupport"

    def device_command(self, device_id, name, payload, retry_time=10):
        token = self._build_sas_token()
        url = "https://%s/twins/%s/methods?api-version=%s" % (self.iot_host, device_id, self.API_VERSION)
        body = json.dumps({
            "methodName": name,
            "payload": json.loads(payload)
        })
        r = requests.post(url, headers={"Content-Type": "application/json", "Authorization": token}, data=body)
        if r.status_code == 429:
            waiting = r.headers['Retry-After'] if r.headers['Retry-After'] <= 10 else 10
            time.sleep(waiting)
            return 998, "Too many requests."
        
        response = json.loads(r.text)
        return 200, response['payload']
    
    def module_command(self, device_id, module_id, name, payload, retry_time=10):
        token = self._build_sas_token()
        url = "https://%s/twins/%s/modules/%s/methods?api-version=%s" % (self.iot_host, device_id, module_id, self.API_VERSION)
        body = json.dumps({
            "methodName": name,
            "payload": json.loads(payload)
        })
        r = requests.post(url, headers={"Content-Type": "application/json", "Authorization": token}, data=body)
        if r.status_code == 429:
            waiting = r.headers['Retry-After'] if r.headers['Retry-After'] <= 10 else 10
            time.sleep(waiting)
            return 998, "Too many requests."
        
        response = json.loads(r.text)
        return 200, response['payload']
    
    def command(self, device_id, name, payload, retry_time=10):
        names = device_id.split("?module=")
        if len(names) > 1:
            return self.module_command(names[0], names[1], name, payload, retry_time=retry_time)
        else:
            return self.device_command(names[0], name, payload, retry_time=retry_time)