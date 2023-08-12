import socketio
import pyautogui
import asyncio
import psutil
import ssl
import uuid
import webbrowser

TOKEN = str(uuid.uuid4())
# ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# ssl_context.load_verify_locations('server.cert')  # Provide the path to the server's certificate
#create socket object
sio = socketio.AsyncClient()

#get client generate period and send period for each data
generate_period = float(input("Enter mouse position generate_period (seconds): "))
send_period = float(input("Enter mouse position send_period (seconds): "))
generate_period_2 = float(input("Enter CPU load generate_period (seconds): "))
send_period_2 = float(input("Enter CPU load send_period (seconds): "))

#send mouse data over socket
async def send_data_mouse():
    buffer_mouse = []
    while True:
        buffer_mouse.append(pyautogui.position())
        await asyncio.sleep(generate_period)

        if len(buffer_mouse) * generate_period >= send_period:
            await sio.emit('send_data', {'type': 'mouse', 'data': buffer_mouse, 'token': TOKEN})
            buffer_mouse.clear()

#send cpu data over socket
async def send_data_cpu():
    buffer_cpu = []
    while True:
        buffer_cpu.append(psutil.cpu_percent(interval=1))
        await asyncio.sleep(generate_period_2)

        if len(buffer_cpu) * generate_period_2 >= send_period_2:
            await sio.emit('send_data', {'type': 'cpu', 'data': buffer_cpu, 'token': TOKEN})
            buffer_cpu.clear()


async def main():
    '''
    1.connect to socket
    2.login socket to a specific room
    3.run asyncio eventloop with two function that sends the data
    '''
    await sio.connect('wss://neuro-brave-server-b222fd4c7de9.herokuapp.com')
    await sio.emit('join_room', {'room': TOKEN})
    # You can run both in an asyncio.gather() to make them concurrent.
    await asyncio.gather(send_data_mouse(), send_data_cpu())

#open webrowser with server that deployed on heroku for your conviniece
webbrowser.open(url=f"https://neuro-brave-server-b222fd4c7de9.herokuapp.com/?token={TOKEN}")

# Run the main coroutine using asyncio
asyncio.run(main())






