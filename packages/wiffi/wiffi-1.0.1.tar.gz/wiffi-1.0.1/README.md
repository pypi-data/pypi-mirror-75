# wiffi

Python 3 package to interface devices from [STALL WIFFI](https://stall.biz).

## Installation

pip3 install wiffi

## Configure the WIFFI device

1. Set "CCU-IP Adresse myCCUIP" to the IP address of Home Assistant.
2. Set port for JSON telegrams to configured server port using parameter "send_json".

## Usage

```python
class WiffiIntegrationApi:
    def __init__(self, hass, config_entry):
        self._server = WiffiTcpServer(8189, self)

    async def __call__(self, device, metrics):
        # device is of type WiffiDevice
        print(f"mac address = {device.mac_address}")

        for metric in metrics:
            # metric is of type WiffiMetric
            print(f"value = {metric.value} {metric.unit_of_measurement")
```
