from aws import AWSIoTOperation
from az import AzureIoTOperation

class IoTOperation:
    def __init__(self, target, setting):
        if target == 'aws':
            self.client = AWSIoTOperation(setting)
        elif target == 'azure':
            self.client = AzureIoTOperation(setting)

    def search_devices(self):
        return self.client.search_devices()

    def search_device(self, device_name):
        return self.client.search_device(device_name)

    def desired(self, device_name, desired_payload):
        return self.client.desired(device_name, desired_payload)

    def unsubscribe_messages(self, topic):
        self.client.unsubscribe_messages(topic)

    def message_callback(self, topic, payload):
        print('Received a new message from topic: '+topic)
        print(payload)
        print('--------------\n\n')

    def subscribe_messages(self, topic='', second=-1, callback=None, userdata=None):
        user_callback = self.message_callback
        if callback != None:
            user_callback = callback
        self.userdata = userdata
        self.client.subscribe_messages(user_callback, topic, second)

    def open_tunnel(self, device_id, service, port):
        return self.client.open_tunnel(device_id, service, port)

    def command(self, device_id, command_name, payload, retry_time=10):
        return self.client.command(device_id, command_name, payload, retry_time)
