from flask import Flask, request, redirect, render_template, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'UnaClaveSecretaRestaurante' 

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect("restaurante.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return "Sistema de Gestión de Restaurante" 

if __name__ == "__main__":
    app.run(debug=True)