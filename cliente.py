import argparse
import socket
import sys
import socket
import time

def parser_ip_puerto():
    parse = argparse.ArgumentParser()
    parse.add_argument('-i', '--ipserver', help='Indica el servidor', type=str, action='store', required=True)
    parse.add_argument('-p', '--port', help='Indica el puerto', type=int, action='store', required=True)
    parse.add_argument('-o', '--operacion', help='Indica el tipo de operacion', type=str, action='store', required=True)
    parse.add_argument('-n', '--primeroperando', help='Indica el primer operando', type=int, action='store', required=True)
    parse.add_argument('-m', '--segundooperando', help='Indica el segundo operando', type=int, action='store', required=True)
    return parse.parse_args()

def iniciar_server_socket( server, puerto, args):
    sock_cliente = socket.socket()
    try:
        sock_cliente.connect((server, puerto))
    except:
        print('Puerto o Server erroneos')
        sys.exit()
    lista_oper = [args.operacion, args.primeroperando, args.segundooperando]
    sock_cliente.send(str(lista_oper).encode())
    respuesta = sock_cliente.recv(1024)
    print('Su resultado es: ',respuesta.decode())
    print('Operacion realizada, desconectando...')
    time.sleep(1)
    sock_cliente.close()
                

if __name__ == '__main__':
    args = parser_ip_puerto()
    server = args.ipserver
    puerto = args.port
    iniciar_server_socket( server, puerto, args)
