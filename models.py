class CuentaBancaria :
    def __init__(self, numero_cuenta, propietario, pin, saldo):
        self.__numero_cuenta = numero_cuenta
        self.__propietario = propietario
        self.__pin = pin
        self.__saldo = saldo

    def validar_pin(self, pin):
        return self.__pin == pin

    def get_numero_cuenta(self):
        return self.__numero_cuenta

    def get_propietario(self):
        return self.__propietario

    def get_saldo(self):
        return self.__saldo

    def depositar(self, monto):
        self.__saldo += monto

    def retirar(self, monto):
        if monto <= self.__saldo:
            self.__saldo -= monto
            return True
        return False

    def transferir(self, cuenta_destino, monto):
        if self.retirar(monto):
            cuenta_destino.depositar(monto)
            return True
        return False