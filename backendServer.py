import pymysql
import pickle
import socket


class Transaccion:
    usuario = ''
    monto = 0.0

    def __init__(self, usuario, monto):
        self.usuario = usuario
        self.monto = monto


if __name__ == "__main__":
    HOST = ''
    PORT = 8869
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        SERVER_SOCKET.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    SERVER_SOCKET.listen(10)
    while 1:
        connection, address = SERVER_SOCKET.accept()
        data = connection.recv(4096)
        if not data:
            break
        else:
            datos = pickle.loads(data)
            conexion = pymysql.connect(host='172.31.99.13', user='banco', passwd='banco', db='bancopython')
            cur = conexion.cursor()

            if len(datos) > 1:
                usuario = ''
                if datos[0] == "1":
                    usuario = datos[1]
                else:
                    tran = datos[1]
                    usuario = tran.usuario
                    query = "select CEDULA from cliente where USUARIO = '{}'".format(usuario)
                    cur.execute(query)
                    conexion.commit()
                    cedula = cur._rows[0][0]
                    if datos[0] == "2":
                        query = "update cuenta set SALDO = (SALDO + {}) where CEDULA = '{}'".format(tran.monto, cedula)
                    else:
                        query = "update cuenta set SALDO = (SALDO - {}) where CEDULA = '{}'".format(tran.monto, cedula)
                    cur.execute(query)
                    conexion.commit()
                query = ("select SALDO from cuenta cu join cliente cl on (cu.cedula = cl.cedula) where USUARIO = '%s'" % usuario)
                cur.execute(query)
                conexion.commit()
                connection.send(pickle.dumps(str(cur._rows[0][0])))
                conexion.close()
            else:
                query = "select USUARIO from cliente where USUARIO = '{}'".format(datos[0])
                cur.execute(query)
                conexion.commit()
                if cur._rows:
                    connection.send(pickle.dumps(str(cur._rows[0][0])))
                else:
                    connection.send(pickle.dumps("error"))
                conexion.close()

    SERVER_SOCKET.close()
