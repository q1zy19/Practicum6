#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from SeT import Settings
from threading import Thread
from datetime import datetime
import socket
import logging
from pathlib import Path
from os.path import exists, sep

def get_response(error, text, file_type):
    return f"""HTTP/1.1 {error} {Settings.stat[error]}
    
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GTM')}
Server: {Settings.name}
Content-Type: {Settings.types[file_type]}
Content-Length: {len(text)}
Connection: close
""".encode() + text

def handler(request, addr):
    try:
        current_file = request.split('\n')[0].split()[1][1:]
    except:
        current_file = 'index.html'
    if not current_file:
        current_file = 'index.html'
    main_path = Path(Settings.directory, current_file)
    if exists(main_path):
        file_type = current_file.split(".")[-1]
        if file_type in Settings.types:
            error = '200'
            write_log(error, addr, main_path)
            with open(main_path, "rb") as file:
                text = file.read()
            responce = get_response(error, text, file_type)
            return responce
        else:
            error = '403'
            text = "<h1>403</h1>".encode()
            file_type = 'html'
            write_log(error, addr, main_path)
            responce = get_response(error, text, file_type)
            return responce

    elif not exists(main_path) or current_file == '':  # нет файла
        error = '404'
        text = "<h1>404</h1>".encode()
        file_type = 'html'
        write_log(error, addr, main_path)
        responce = get_response(error, text, file_type)
        return responce

def connection(conn, addr):
    with conn:
        data = conn.recv(Settings.max_size)
        if data == b"":
            conn.close()
        request = data.decode()
        print(request)
        resp = handler(request, addr)
        conn.send(resp)

def write_log(error, addr, text):
        logging.info(f"""IP-address: {addr} File path: {text} Code: {error} """)

def log_inf():
    logging.basicConfig(
        level=logging.DEBUG,
        format="Date: %(asctime)s | %(message)s",
        handlers=[
            logging.FileHandler("logs.log"),
            logging.StreamHandler(),
        ],
    )

def main():
    log_inf()
    sock = socket.socket()
    try:
        sock.bind(('', Settings.port))
        print('Using port: ', Settings.port)
    except OSError:
        sock.bind(('', Settings.other_port))
        print('Using port: ', Settings.other_port)
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        print("Connected", addr)
        Thread(target=connection, args=[conn, addr[0]]).start()

if __name__ == '__main__':
    main()

