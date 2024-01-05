import json
import base64
import os
import sys
import ctime
import socketio

HOST = "localhost"
PORT = 25412
login = None
password = None

sio = socketio.Client()


@sio.on("ver")
def ver(env):
    if env.get("type") == "ver":
        message_text = env.get("message")
        sender_login = env.get("sender_login")
        sended_str = f"Повідомленя з текстом {message_text}  \n успішно надійшло користувачу {sender_login} "
        print(sended_str)
    elif env.get("type") == "verfile":
        message_text = env.get("message")
        sender_login = env.get("sender_login")
        sended_str = f"Повідомленя з файлом {message_text}  \n успішно надійшло користувачу {sender_login} "
        print(sended_str)


@sio.on("receive")
def receive(env):
    global login
    global password
    message_type = env.get("type")
    if message_type == "message":
        message_text = env.get("message")
        message_time = env.get("time")

        sended_str = f"\nВам повідомлення від: {env.get('sender_login')} \n Текст повідомлення: {message_text} \nЧас " \
                     f"відправлення: {message_time.get('hour')}:{message_time.get('min')}"

        send_to_server(message_type="ver", message=message_text, sender_login=login, sender_password=password,
                       receiver_login=env.get('sender_login'))

        print(sended_str)
    elif message_type == "file":
        message_text = env.get("message")
        env.get("time")
        message_text = json.loads(message_text)

        file_data = base64.b64decode(message_text.get("file_data"))  # Decode Base64 string to bytes

        with open("new " + message_text.get("file_name"), "wb") as new_file:  # Open file in binary write mode
            new_file.write(file_data)  # Write the decoded bytes to the file

        send_to_server(message_type="verfile", message=message_text.get("file_name"), sender_login=login,
                       sender_password=password,
                       receiver_login=env.get('sender_login'))


def hash_function(data: str) -> int:
    hash_value = 0
    for character in data:
        hash_value = (hash_value * 31 + ord(character)) % 1000000
    return hash_value


def send_file(file_path, sender_login, sender_password, receiver_login):
    with open(file_path, 'rb') as file:
        byte_data = file.read()
        encoded_data = base64.b64encode(byte_data).decode('utf-8')

        data = {
            "file_name": os.path.basename(file.name),
            "file_data": encoded_data
        }
        sended_data = json.dumps(data)

    send_to_server(message_type="file",
                   message=sended_data,
                   sender_login=sender_login,
                   sender_password=sender_password,
                   receiver_login=receiver_login)


def send_to_server(message_type, message, sender_login, sender_password, receiver_login):
    message_dict = {
        "type": message_type,
        "message": message,
        "sender_login": sender_login,
        "sender_password": sender_password,
        "receiver_login": receiver_login,
        "time": ctime.Time().dict_ret()
    }

    message_for_send = json.dumps(message_dict)
    sio.emit("receive", message_for_send.encode())


def main():
    sio.connect(f'http://{HOST}:{PORT}')
    global login
    global password
    login = input("Введіть ваш логін: ")
    password = input("Введіть пароль: ")
    send_to_server(message_type="message", message="sdfkghbgfh", sender_login=login, sender_password=password,
                   receiver_login="sdfjklnjgfn")

    while True:
        receiver_login = input("Введіть логін користувача, якому хочете відправити повідомлення: ")
        if receiver_login == "stop":
            sys.exit()
        message_type = input("Введіть тип повідомлення (текст, файл): ")
        if message_type == "stop":
            sys.exit()
        if message_type == "текст":
            message_text = input("Введіть текст повідомлення: ")
            send_to_server(message_type="message", message=message_text, sender_login=login, sender_password=password,
                           receiver_login=receiver_login)

        elif message_type == "файл":
            try:
                file_path = input("Введіть шлях до файлу: ")
                send_file(file_path=file_path,
                          sender_login=login,
                          sender_password=password,
                          receiver_login=receiver_login
                          )

            except Exception as e:
                print(f"Помилка: {e}")

        elif message_type == "консоль":
            send_to_server(message_type="console", message="", sender_login="", sender_password="", receiver_login="")

        else:
            print("Щось не так")
        print("")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        sio.disconnect()
