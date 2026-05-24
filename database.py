import sqlite3

DB_NAME = "banco.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuentas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_cuenta TEXT UNIQUE NOT NULL,
            propietario TEXT NOT NULL,
            pin TEXT NOT NULL,
            saldo REAL NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


def guardar_cuenta(numero_cuenta, propietario, pin, saldo):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO cuentas (numero_cuenta, propietario, pin, saldo)
        VALUES (?, ?, ?, ?)
    """, (numero_cuenta, propietario, pin, saldo))

    conexion.commit()
    conexion.close()


def buscar_cuenta(numero_cuenta):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT numero_cuenta, propietario, pin, saldo
        FROM cuentas
        WHERE numero_cuenta = ?
    """, (numero_cuenta,))

    cuenta = cursor.fetchone()
    conexion.close()

    return cuenta


def actualizar_saldo(numero_cuenta, nuevo_saldo):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE cuentas
        SET saldo = ?
        WHERE numero_cuenta = ?
    """, (nuevo_saldo, numero_cuenta))

    conexion.commit()
    conexion.close()