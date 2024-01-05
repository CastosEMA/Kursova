import socketio
from aiohttp import web
import json
from loguru import logger

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

clients_sids = {}
clients_passwords = {}

def hash_function(data: str) -> int:
    hash_value = 0
    for character in data:
        hash_value = (hash_value * 31 + ord(character)) % 1000000
    return hash_value

@sio.on("connect")
def connect(sid, environ):
    print("connected " + sid)



@sio.on("disconnect")
async def close(sid):
    print("disconnect " + sid)
    await sio.disconnect(sid)


@sio.on("receive")
async def receive(sid, env):
    decoded_dict = json.loads(env)

    sender_password = decoded_dict.get("sender_password")
    sender_password = str(hash_function(sender_password))
    sender_login = decoded_dict.get("sender_login")
    receiver_login = decoded_dict.get("receiver_login")

    if decoded_dict.get("type") == "message" or decoded_dict.get("type") == "file":
        if sender_login in clients_sids:
            print("Коричтувач є в списку сесій")
            if clients_passwords[sender_login] == sender_password:
                print("Пароль правильний")

                clients_sids[sender_login] = sid

                if receiver_login in clients_sids:
                    print("Перевіряємо чи існує отримувач з т аким логіном")
                    del decoded_dict["sender_password"]

                    await sio.emit("receive", decoded_dict, room=clients_sids[receiver_login])
                else:
                    pass
            else:
                pass
        else:
            clients_passwords[sender_login] = sender_password
            clients_sids[sender_login] = sid
            if receiver_login in clients_sids:
                del decoded_dict["sender_password"]

                await sio.emit("receive", decoded_dict, room=clients_sids[receiver_login])
            print("Щось не так")
    elif decoded_dict.get("type") == "ver" or decoded_dict.get("type") == "verfile":
        if sender_login in clients_sids:  # перевірка чи є він в списку сідів
            print("Коричтувач є в списку сесій")
            if clients_passwords[sender_login] == sender_password:  # перевірка чи правильний пароль
                print("Пароль правильний")
                del decoded_dict["sender_password"]

                clients_sids[sender_login] = sid

                if receiver_login in clients_sids:
                    await sio.emit("ver", decoded_dict, room=clients_sids[receiver_login])

async def callback():
    logger.info("Callback received")


if __name__ == "__main__":
    web.run_app(app, port=25412)
