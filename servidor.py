from flask import Flask, jsonify, redirect
import requests
app = Flask(__name__)

import mysql.connector

conexion = mysql.connector.connect(
    user='Edgar',
    password='12345',
    database='oferta_academica'
)
cursor = conexion.cursor()


@app.route("/api/v1/public/seccion")
def hello():
    query = "SELECT * FROM seccion"
    cursor.execute(query)
    secciones = cursor.fetchall()
    dicc_secciones = {}
    lista_seccion = []
    for s in secciones:
        c = {"nrc": s[0],
             "seccion": s[1],
             "cupos": s[2],
             "disponibles": s[3],
             "id_periodo": s[4],
             "clave_materia": s[5],
             "id_profesor": s[6]
             }
        lista_seccion.append(c)

    dicc_secciones['secciones'] = lista_seccion

    return jsonify(dicc_secciones)

@app.route("/api/v1/public/materia")
def materia():
    query = "SELECT * FROM materia"
    cursor.execute(query)
    materias = cursor.fetchall()
    dicc_materias = {}
    lista_materia = []
    for s in materias:
        c = {"clave": s[0],
             "nombre": s[1],
             "creditos": s[2]
             }
        lista_materia.append(c)

    dicc_materias['materias'] = lista_materia

    return jsonify(dicc_materias)

@app.route("/api/v1/public/horario")
def horario():
    query = "SELECT * FROM horario"
    cursor.execute(query)
    horarios = cursor.fetchall()
    dicc_horario = {}
    lista_horario = []
    for s in horarios:
        c = {"id": s[0],
             "sesion": s[1],
             "hora": s[2],
             "dias": s[3],
             "edificio": s[4],
             "aula": s[5],
             "nrc_Seccion": s[6]
             }
        lista_horario.append(c)

    dicc_horario['horarios'] = lista_horario

    return jsonify(dicc_horario)

@app.route("/api/v1/public/profesor")
def profesor():
    query = "SELECT * FROM profesor"
    cursor.execute(query)
    profesores = cursor.fetchall()
    dicc_profesores = {}
    lista_profesores = []
    for s in profesores:
        c = {"id": s[0],
             "nombre": s[1]
             }
        lista_profesores.append(c)

    dicc_profesores['profesores'] = lista_profesores

    return jsonify(dicc_profesores)

@app.route("/api/v1/public/seccion-completa")
def seccion_completa():
    query = "SELECT * FROM seccion"
    cursor.execute(query)
    secciones = cursor.fetchall()
    dicc_secciones = {}
    lista_seccion = []
    for s in secciones:
        query = "SELECT * FROM materia WHERE clave = %s"
        cursor.execute(query, (s[5],))
        materia = cursor.fetchall()

        query = "SELECT * FROM profesor WHERE id = %s"
        cursor.execute(query, (s[6],))
        profesor = cursor.fetchall()

        query = "SELECT * FROM horario WHERE nrc_Seccion = %s"
        cursor.execute(query, (s[0],))
        horarios = cursor.fetchall()
        datos = []

        for h in horarios:
            h1 = {"sesion": h[1],
                  "hora": h[2],
                  "dias": h[3],
                  "edificio": h[4],
                  "aula": h[5],
                  }
            datos.append(h1)

        c = {"clave_materia": s[5],
             "materia": materia[0][1],
             "creditos": materia[0][2],
             "nrc": s[0],
             "seccion": s[1],
             "cupos": s[2],
             "disponibles": s[3],
             "id_periodo": s[4],
             "horario": datos,
             "profesor": profesor[0][1]
             }
        lista_seccion.append(c)

    dicc_secciones['secciones'] = lista_seccion

    return jsonify(dicc_secciones)


app.run()