class SaldoEfectivoInsuficiente(Exception):
    pass

class SaldoCuentaInsuficiente(Exception):
    pass

class CajeroAutomatico:
    def __init__(self):
        self.efectivo_disponible = 100000
        self.cuentas = {
            '1234': {'pin': '0000', 'saldo': 5000},
            '5678': {'pin': '1111', 'saldo': 10000}
        }
        self.usuario_actual = None

    def autenticar(self, numero_cuenta, pin):
        if numero_cuenta in self.cuentas and self.cuentas[numero_cuenta]['pin'] == pin:
            self.usuario_actual = numero_cuenta
            print("Autenticación exitosa.")
        else:
            print("Número de cuenta o PIN incorrectos.")

    def mostrar_saldo(self):
        if self.usuario_actual:
            print(f"Saldo actual: {self.cuentas[self.usuario_actual]['saldo']}")
        else:
            print("Debe autenticarse primero.")

    def deposito_propio(self, monto):
        if self.usuario_actual:
            self.cuentas[self.usuario_actual]['saldo'] += monto
            print(f"Depósito exitoso. Saldo actual: {self.cuentas[self.usuario_actual]['saldo']}")
        else:
            print("Debe autenticarse primero.")

    def deposito_otra_cuenta(self, numero_cuenta, monto):
        if self.usuario_actual:
            if numero_cuenta in self.cuentas:
                self.cuentas[numero_cuenta]['saldo'] += monto
                print(f"Depósito a cuenta {numero_cuenta} exitoso.")
            else:
                print("Número de cuenta no existe.")
        else:
            print("Debe autenticarse primero.")

    def transferencia(self, numero_cuenta, monto):
        if self.usuario_actual:
            if monto > self.cuentas[self.usuario_actual]['saldo']:
                raise SaldoCuentaInsuficiente("Saldo en la cuenta insuficiente para la transferencia.")
            if numero_cuenta in self.cuentas:
                self.cuentas[self.usuario_actual]['saldo'] -= monto
                self.cuentas[numero_cuenta]['saldo'] += monto
                print(f"Transferencia a cuenta {numero_cuenta} exitosa.")
            else:
                print("Número de cuenta no existe.")
        else:
            print("Debe autenticarse primero.")

    def retiro(self, monto):
        if self.usuario_actual:
            if monto > self.cuentas[self.usuario_actual]['saldo']:
                raise SaldoCuentaInsuficiente("Saldo en la cuenta insuficiente para el retiro.")
            if monto > self.efectivo_disponible:
                raise SaldoEfectivoInsuficiente("Efectivo insuficiente en el cajero.")
            self.cuentas[self.usuario_actual]['saldo'] -= monto
            self.efectivo_disponible -= monto
            print(f"Retiro exitoso. Saldo actual: {self.cuentas[self.usuario_actual]['saldo']}")
        else:
            print("Debe autenticarse primero.")

# Ejemplo de uso
cajero = CajeroAutomatico()

# Autenticación
cajero.autenticar('1234', '0000')

# Mostrar saldo
cajero.mostrar_saldo()

# Depósito en cuenta propia
cajero.deposito_propio(500)

# Depósito en otra cuenta
cajero.deposito_otra_cuenta('5678', 300)

# Transferencia
try:
    cajero.transferencia('5678', 7000)
except SaldoCuentaInsuficiente as e:
    print(e)

# Retiro de efectivo
try:
    cajero.retiro(2000)
except (SaldoCuentaInsuficiente, SaldoEfectivoInsuficiente) as e:
    print(e)
