# Cloud Device Management Toolkit

## Support
* azure iotedge
    * list/get device/module info
    * list/get/edit device/module twin
    * subscribe device D2C message
    * invoke device/module direct command
* azure iot device
    * list/get device info
    * list/get/edit device twin
    * subscribe device D2C message
    * invoke device direct command
* aws iot device
    * list/get thing info
    * list/get/edit thing shadow
    * subscribe device D2C message
    * invoke thing job
* aws greengrass (TODO)
* aliyun (TODO)

## Setup
1. git clone this repo
2. cd to this folder
3. edit auth configuration ***(setting.ini)*** :
    ```ini
    #--------------------------------------------------------------------------------
    # aws credentials help
    # - access_key_id, secret_access_key
    #   * https://aws.amazon.com/tw/premiumsupport/knowledge-center/create-access-key/
    # - root_ca_path
    #   * https://www.amazontrust.com/repository/AmazonRootCA1.pem
    #--------------------------------------------------------------------------------
    [aws]
    region_name = ap-northeast-1
    host = test.iot.ap-northeast-1.amazonaws.com
    access_key_id = test
    secret_access_key = test
    fleet_indexing = true
    root_ca_path = ./aws/awsRootCA.crt

    #--------------------------------------------------------------------------------------------------------------------------
    # azure credentials help  (using the Azure CLI from cloud shell, https://docs.microsoft.com/zh-tw/azure/cloud-shell/quickstart)
    # - connection_string
    #   * az iot hub show-connection-string --name MyIotHub
    # - eventhub_connection_string
    #   * Endpoint
    #      - az iot hub show --query properties.eventHubEndpoints.events.endpoint --name {your IoT Hub name}
    #   * EntityPath
    #      - az iot hub show --query properties.eventHubEndpoints.events.path --name {your IoT Hub name}
    #   * SharedAccessKey for the SharedAccessKeyName="service"
    #      - az iot hub policy show --name service --query primaryKey --hub-name {your IoT Hub name}
    #--------------------------------------------------------------------------------------------------------------------------
    [azure]
    connection_string = HostName=${HostName};SharedAccessKeyName=${SharedAccessKeyName};SharedAccessKey=${SharedAccessKey}
    eventhub_connection_string = Endpoint=${Endpoint};SharedAccessKeyName=${SharedAccessKeyName};SharedAccessKey=${SharedAccessKey};EntityPath=${EntityPath}
    consumer_group = $default
    ```
4. enter env
    ```bash
    docker run -it --rm --name sample-cli \
        -v $(pwd):/data --net host \
        bibbylong/device-mgmt:1.0.9-amd64 bash
    ```
    ```bash
    python3 ./sample.py -h
    ```
5. or run by docker-compose
    ```bash
    docker-compose run --rm sample -h
    ```
## Sample
* [source](https://github.com/GaryHsu77/cloud-iot-toolkit/blob/master/sample.py)
* help
    ```bash
    ~ python3 ./sample.py -h
    usage: sample.py [-h] [-t TARGET] [-m MODE] [-T TOPIC] [-D DEVICE]
                     [-C COMMAND_NAME] [-P COMMAND_PAYLOAD] [-S DESIRED_PAYLOAD]
                     [--pretty]
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TARGET, --target TARGET
                            connection target
      -m MODE, --mode MODE  Operation modes: ['subscribe', 'list', 'command',
                            'device', 'desired']
      -T TOPIC, --topic TOPIC
                            Targeted topic
      -D DEVICE, --device DEVICE
                            control device
      -C COMMAND_NAME, --command COMMAND_NAME
                            control command name
      -P COMMAND_PAYLOAD, --payload COMMAND_PAYLOAD
                            control command payload
      -S DESIRED_PAYLOAD, --desired_payload DESIRED_PAYLOAD
                            desired payload
      --pretty              pretty json output
    ```

* list devices
    ```bash
    ~ python3 ./sample.py --pretty \
        -t azure \
        -m list
    [
      {
        "name": "mydev1",
        "desired": {},
        "reported": {},
        "timestamp": "0001-01-01T00:00:00Z",
        "connected": false
      }
    ]
    ```

* get device
    ```bash
    ~ python3 ./sample.py --pretty \
        -t azure \
        -m device \
        -D mydev1
    {
      "name": "mydev1",
      "desired": {},
      "reported": {},
      "timestamp": "0001-01-01T00:00:00Z",
      "connected": false
    }
    ```

    > get module under device (azure)
    > ```bash
    > ~ python3 ./sample.py --pretty \
    >     -t azure \
    >     -m device \
    >     -D mydev1?module=myModule
    > {
    >   "name": "mydev1?module=myModule",
    >   "desired": {},
    >   "reported": {},
    >   "timestamp": "0001-01-01T00:00:00Z",
    >   "connected": false
    > }
    > ```

* update device twin
    ```bash
    ~ python3 ./sample.py \
        -t azure \
        -m desired \
        -D mydev1 \
        --desired_payload '{"enable":true}'
    200
    ```
    > update module twin (azure)
    > ```bash
    > python3 ./sample.py \
    >   -t azure \
    >   -m desired \
    >   -D mydev1?module=myModule \
    >   --desired_payload '{"enable":true}'
    > ```

* subscribe D2C message
    #### all message
    ```bash
    ~ python3 ./sample.py -t azure -m subscribe -T '#'
    ```
    
    #### specify topic
    ```bash
    ~ python3 ./sample.py -t azure -m subscribe -T 'test'
    ```
    
    #### specify device (azure)
    ```bash
    ~ python3 ./sample.py -t azure -m subscribe -T 'mydev'
    ```

* invoke method
    ```bash
    ~ python3 ./sample.py --pretty \
        -t azure \
        -m command \
        -D mydev1 \
        -C api-v1 \
        -P '{"path":"/device/ethernets","method":"GET"}'
    code: 200
    response: {
        "data": [
            {
                "id": 1,
                "enable": true,
                "ip": "192.168.3.3"
            },
            {
                "id": 2,
                "enable": true,
                "ip": "192.168.3.4"
            }
        ]
    }
    ```

    > module under device (azure)
    > ```bash
    > ~ python3 ./sample.py --pretty \
    >     -t azure \
    >     -m command \
    >     -D mydev1?module=myModule \
    >     -C api-v1 \
    >     -P '{"path":"/device/ethernets","method":"GET"}'
    > ```

## Cloud Device Management Console

```bash
docker-compose run --rm device-mgmt -t aws
```
![](https://i.imgur.com/nHeLukh.png)
