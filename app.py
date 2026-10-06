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
    return redirect(url_for('listar_pedidos'))

@app.route("/pedidos")
def listar_pedidos():
    conn = get_db_connection()
    pedidos = conn.execute(
        """
        SELECT p.id,
               p.cantidad,
               p.hora,
               p.estado,
               m.numero || ' - ' || m.ubicacion as mesa,
               pl.nombre as plato
        FROM pedidos p
        JOIN mesas m ON p.mesa_id = m.id
        JOIN platos pl ON p.plato_id = pl.id
        """
    ).fetchall()
    conn.close()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route("/platos")
def listar_platos():
    conn = get_db_connection()
    platos = conn.execute('SELECT * FROM platos').fetchall()
    conn.close()
    return render_template('platos.html', platos=platos)

@app.route('/plato/nuevo', methods=['GET', 'POST'])
def nuevo_plato():
    if request.method == 'POST':
        # Leer contenido del formulario
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        
        conn = get_db_connection()
        conn.execute("INSERT INTO platos (nombre, categoria, precio) VALUES (?,?,?)",
                     (nombre, categoria, precio))
        
        conn.commit()
        conn.close()
        flash('Plato agregado correctamente', 'success')
        return redirect(url_for('listar_platos'))
    return render_template('form_plato.html')

@app.route('/plato/editar/<int:id>', methods=['GET', 'POST'])
def editar_plato(id):
    conn = get_db_connection()
    plato = conn.execute("SELECT * FROM platos WHERE id = ?", (id,)).fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        
        conn.execute("UPDATE platos SET nombre = ?, categoria = ?, precio = ? WHERE id = ?",
                     (nombre, categoria, precio, id))
        conn.commit()
        conn.close()
        flash('Plato actualizado', 'success')
        return redirect(url_for('listar_platos'))
        
    return render_template('form_plato.html', plato=plato)

@app.route('/plato/eliminar/<int:id>')
def eliminar_plato(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM platos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Plato eliminado', 'success')
    return redirect(url_for('listar_platos'))



@app.route("/mesas")
def listar_mesas():
    conn = get_db_connection()
    mesas = conn.execute('SELECT * FROM mesas').fetchall()
    conn.close()
    return render_template('mesas.html', mesas=mesas)

if __name__ == "__main__":
    app.run(debug=True)