from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

ARCHIVO = "colaboradores.txt"

DIAS_SEMANA = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo"
]


def calcular_edad(fecha_nacimiento):
    fecha_nac = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    hoy = datetime.now().date()

    edad = hoy.year - fecha_nac.year

    if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
        edad -= 1

    return edad


def cargar_colaboradores():
    colaboradores = []

    if not os.path.exists(ARCHIVO):
        return colaboradores

    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            if linea == "":
                continue

            datos = linea.split("|")

            if len(datos) == 4:
                colaborador = {
                    "nombre": datos[0],
                    "apellido": datos[1],
                    "fecha_nacimiento": datos[2],
                    "dia": datos[3]
                }

                colaborador["edad"] = calcular_edad(
                    colaborador["fecha_nacimiento"]
                )

                colaboradores.append(colaborador)

    return colaboradores


def resumen_por_dia():
    resumen = {}

    for dia in DIAS_SEMANA:
        resumen[dia] = 0

    colaboradores = cargar_colaboradores()

    for colaborador in colaboradores:
        dia = colaborador["dia"]

        if dia in resumen:
            resumen[dia] += 1

    return resumen


@app.route("/")
def inicio():
    return redirect(url_for("registro"))


@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        fecha_nacimiento = request.form.get("fecha_nacimiento", "").strip()
        dia = request.form.get("dia", "").strip()

        if not nombre or not apellido or not fecha_nacimiento or not dia:
            return render_template(
                "registro.html",
                dias=DIAS_SEMANA,
                error="Todos los campos son obligatorios."
            )

        colaborador = {
            "nombre": nombre,
            "apellido": apellido,
            "fecha_nacimiento": fecha_nacimiento,
            "dia": dia
        }

        with open(ARCHIVO, "a", encoding="utf-8") as archivo:
            archivo.write(
                f"{colaborador['nombre']}|"
                f"{colaborador['apellido']}|"
                f"{colaborador['fecha_nacimiento']}|"
                f"{colaborador['dia']}\n"
            )

        return redirect(url_for("colaboradores"))

    return render_template(
        "registro.html",
        dias=DIAS_SEMANA
    )


@app.route("/colaboradores")
def colaboradores():
    lista_colaboradores = cargar_colaboradores()

    return render_template(
        "colaboradores.html",
        colaboradores=lista_colaboradores
    )


@app.route("/resumen")
def resumen():
    resumen_dias = resumen_por_dia()

    return render_template(
        "resumen.html",
        resumen=resumen_dias
    )


if __name__ == "__main__":
    app.run(debug=True)