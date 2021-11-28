from threading import Thread
from tasks import suma, resta, multiplicar, dividir
import argparse
import socket


#redis.Redis(host='localhost', port=6379, db=0)
def operaciones(con,adr):
    tarea = eval(con.recv(1024).decode())
    if tarea[0].lower() == 'suma':
        resultadoSum = suma.delay(tarea[1], tarea[2])
        con.send(str(resultadoSum.get()).encode())
    elif tarea[1].lower() == 'resta':
        resultadoRes = resta.delay(tarea[1], tarea[2])
        con.send(str(resultadoRes.get()).encode())
    elif tarea[1].lower() == 'multiplicar':
        resultadoMul = multiplicar.delay(tarea[2], tarea[2])
        con.send(str(resultadoMul.get()).encode())
    elif tarea[1].lower() == 'dividir':
        resultadoDiv = dividir.delay(tarea[1], tarea[2])
        con.send(str(resultadoDiv.get()).encode())
    else:
        con.send('Error')
    print(f'La operacion se ha consumado, el cliente {adr} se ha desconectado')
    
def parser_ip_puerto():
    parse = argparse.ArgumentParser()
    parse.add_argument('-i', '--ipserver', help='Ip del cliente', required=True, action='store')
    parse.add_argument('-p', '--port', help='Puerto del cliente', required=True, action='store')
    args = parse.parse_args()
    return args.port, args.ipserver

def iniciar_server_socket( server, puerto, cola):
    sock_server = socket.socket()
    sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_server.bind(((server), int(puerto)))
    sock_server.listen(cola)
    while True:
        con, adr = sock_server.accept()
        print('Se ha establecido conexion con el cliente: ', adr)
        thr = Thread(target=operaciones, args=(con,adr))
        thr.start()


if __name__ == '__main__':
    PORT, SERVER = parser_ip_puerto()
    print(f'Conexion levantada en -puerto {PORT}, ip {SERVER}-')
    print(f'iniciando socket server con una cola de {5}')
    iniciar_server_socket( SERVER, PORT, 5)