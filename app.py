from flask import Flask, render_template, request, redirect, session
from models import CuentaBancaria
from database import crear_tabla, guardar_cuenta, buscar_cuenta, actualizar_saldo

app = Flask(__name__)
app.secret_key = "clave_secreta"
crear_tabla()

cuentas = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/crear_cuenta", methods=["GET", "POST"])
def crear_cuenta():
    if request.method == "POST":
        numero = request.form["numero"]
        propietario = request.form["propietario"]
        pin = request.form["pin"]
        saldo = float(request.form["saldo"])

        guardar_cuenta(numero, propietario, pin, saldo)

        return redirect("/login")

    return render_template("crear_cuenta.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "POST":
        numero = request.form["numero"]
        pin = request.form["pin"]

        cuenta = buscar_cuenta(numero)

        if cuenta:
            pin_guardado = cuenta[2]

            if pin_guardado == pin:
                session["cuenta"] = numero
                return redirect("/panel")
            else:
                mensaje = "PIN incorrecto"
        else:
            mensaje = "La cuenta no existe"

    return render_template("login.html", mensaje=mensaje)


@app.route("/panel")
def panel():
    if "cuenta" not in session:
        return redirect("/login")

    datos = buscar_cuenta(session["cuenta"])

    cuenta = CuentaBancaria(
        datos[0],
        datos[1],
        datos[2],
        datos[3]
    )   

    return render_template("panel.html", cuenta=cuenta)


@app.route("/transferir", methods=["GET", "POST"])
def transferir():
    if "cuenta" not in session:
        return redirect("/login")

    mensaje = ""

    if request.method == "POST":
        destino = request.form["destino"]
        monto = float(request.form["monto"])

        cuenta_origen = cuentas[session["cuenta"]]

        if destino in cuentas:
            cuenta_destino = cuentas[destino]

            if cuenta_origen.transferir(cuenta_destino, monto):
                mensaje = "Transferencia realizada correctamente"
            else:
                mensaje = "Saldo insuficiente"
        else:
            mensaje = "La cuenta destino no existe"

    return render_template("transferir.html", mensaje=mensaje)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/logout")

@app.route("/depositar", methods=["GET", "POST"])
def depositar():
    if "cuenta" not in session:
        return redirect("/login")

    mensaje = ""

    if request.method == "POST":
        monto = float(request.form["monto"])
        numero = session["cuenta"]

        datos = buscar_cuenta(numero)

        if datos:
            saldo_actual = datos[3]

            if monto > 0:
                nuevo_saldo = saldo_actual + monto
                actualizar_saldo(numero, nuevo_saldo)
                mensaje = "Depósito realizado correctamente"
            else:
                mensaje = "El monto debe ser mayor a cero"

    return render_template("depositar.html", mensaje=mensaje)


@app.route("/retirar", methods=["GET", "POST"])
def retirar():
    if "cuenta" not in session:
        return redirect("/login")

    mensaje = ""

    if request.method == "POST":
        monto = float(request.form["monto"])
        numero = session["cuenta"]

        datos = buscar_cuenta(numero)

        if datos:
            saldo_actual = datos[3]

            if monto <= 0:
                mensaje = "El monto debe ser mayor a cero"
            elif monto <= saldo_actual:
                nuevo_saldo = saldo_actual - monto
                actualizar_saldo(numero, nuevo_saldo)
                mensaje = "Retiro realizado correctamente"
            else:
                mensaje = "Saldo insuficiente"

    return render_template("retirar.html", mensaje=mensaje)
if __name__ == "__main__":
    app.run(debug=True)