import asyncio
from websockets import connect

async def hello(uri):
    async with connect(uri) as websocket:
        message = await websocket.recv()
        print(message)

        login_msg ='{"requestId": "1234-45653-343454","login": {"username": "rpi3","password": "A80cV"}}'
        print(login_msg)
        await websocket.send(login_msg)
        print("login sent")
        message = await websocket.recv()
        print(message)

        # beacon_msg = '{"context": "atons.urn:mrn:imo:mmsi:123456789","updates": ' \
        #             '[{"values": [{"path": "navigation.position.longitude","value": 14.99},' \
        #             '{"path": "navigation.position.latitude","value": 31.99},{"path": "name","value": "BeaconPy"},' \
        #             '{"path": "virtual","value": "true"},{"path": "atonType.name","value": "BLE Beacon Py"}]}]}'

        # await websocket.send(beacon_msg)
        # print("beacon sent:",beacon_msg)
        # message = await websocket.recv()
        # print(message)

asyncio.run(hello("ws://192.168.68.103/:3000/signalk/v1/stream?subscribe=none"))