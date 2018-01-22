import time
import pickle


class Cuenta:
    numero = ''
    saldo = 0.0

    def __init__(self, numero, saldo):
        self.numero = numero
        self.saldo = saldo

    def retiro(self, monto):
        if monto > self.saldo:
            raise RuntimeError('Monto mayor al saldo de la cuenta.')
        self.saldo -= monto
        return self.saldo

    def deposito(self, monto):
        self.saldo += monto
        return self.saldo

    def __str__(self):
        return f'\tNumero: {self.numero} \n\tSaldo: {self.saldo}'


class Transaccion:
    tipo = ''
    monto = 0.0

    def __init__(self, tipo, monto, cuenta):
        self.tipo = tipo
        self.monto = monto
        self.cuenta = cuenta

    def ejecutar(self):
        if self.tipo == 'Deposito':
            self.cuenta.deposito(self.monto)
        else:
            self.cuenta.retiro(self.monto)

    def __str__(self):
        return f'Tipo: {self.tipo} \nMonto: {self.monto} \nCuenta: \n{self.cuenta}'


if __name__ == "__main__":
    cuenta1 = Cuenta('1234567890', 750.0)
    transaccion1 = Transaccion('Deposito', 100.0, cuenta1)
    stringtest = ['1', transaccion1]
    test1 = pickle.dumps(stringtest)
    tran = pickle.loads(test1)
    print(tran)
    tran1 = tran[1]
    print(tran1)
    tran1.ejecutar()
    print(tran1.cuenta)
    query = "update cuenta set SALDO = (SALDO + {}) where CEDULA = '{}'".format(tran1.monto, '1234567890')
