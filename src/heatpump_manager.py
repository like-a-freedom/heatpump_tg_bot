import asyncio
from typing import Optional
from greeclimate.discovery import Discovery
from greeclimate.device import Device


async def device_discovery() -> Optional[Device]:
    discovery = Discovery()

    for device_info in await discovery.scan(wait_for=5):
        try:
            print("DEVICE INFO", device_info)
            device = Device(device_info)
            await device.bind()  # Device will auto bind on update if you omit this step
            print(
                f"Adding Gree device at {device.device_info.ip},{device.device_info.port},{device.device_info.name}"
            )
            return device
        except Exception:
            print(f"Unable to bind to gree device: {device_info}")
            continue


def get_device():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(device_discovery())
    loop.close()
    return result
