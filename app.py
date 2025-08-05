import pymysql
from markupsafe import escape
from flask import Flask, redirect, url_for, session, get_flashed_messages, render_template, request, redirect, \
    url_for, flash
from gettersAndSetters import getRegiones, getComunas, Contacto, Dispositivo, Pictures
from config import getFormConnection
from datetime import datetime
from validations import *
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os


app = Flask(__name__)
app.secret_key = 'KJHGSAFGDTEQQQ'

# Configuración de la carpeta donde se guardarán las imágenes
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Límite de tamaño para las subidas (opcional)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Máximo 16 MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/agregar-donacion', methods=['GET', 'POST'])
def agregar_donacion():
    f = getFormConnection()     # Se establece la conexión con el servidor mysql
    regiones = getRegiones(f)   # Se obtienen las regiones
    comunas = getComunas(f)     # Se obtienen las comunas
    # Si se usa el metodo POST, entonces se recuperan los valores del formulario.
    if request.method == 'POST':
        contacto = Contacto(request.form['nombreContacto'], request.form['emailContacto'],    # Se recupera el contacto de la donación
                            request.form['numeroContacto'], request.form['region'],
                            request.form['comuna'])
        dispositivos, i = ([], 0)   # Se recuperan los dispositivos de la donación
        while(True):
            try:    # Si no se retorna un error, entonces se recuperan los datos del formulario de dispositivos.
                dispositivo = Dispositivo(request.form['nombreDisp' + str(i)], request.form['tipoDisp' + str(i)],
                                          request.form['anosDisp' + str(i)], request.form['estadoDisp' + str(i)],
                                          list(request.files.getlist('fotosDisp') + str(i)), request.form['descripcionDisp' + str(i)],)
                dispositivos.append(dispositivo)
                i += 1
            except:   # Si al solicitar el request se arroja un error, entonces no quedan dispositivos por recuperar.
                    break
        resultado = insertDonation(f, contacto, dispositivos)

        if resultado is False:
            pass    # Se muestra el mensaje indicando que las validaciones no se llevaron a cabo adecuadamente
        else:
            return redirect(url_for('index'), code=0)
    return render_template('agregar_donacion.html', regiones = regiones, comunas = comunas)


@app.route('/ver-dispositivos', methods=['GET', 'POST'])
def ver_dispositivos():
    return render_template('ver_dispositivos.html')

def insertDonation(f, contacto, dispositivos):
    if validationContact(contacto):
        return False
    for dispositivo in dispositivos:
        img = dispositivo.fotos
        if validationDevice(dispositivo):
            return False
        if not validationIMG(img):
            return False
        _filename = hashlib.sha256(
            secure_filename(img.filename)
            .encode('utf-8')
            ).hexdigest()
        _extension = filetype.guess(img).extension
        img_filename = f"{_filename}.{_extension}"

        img.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))
    # Consultas SQL para añadir contactos y dispositivos (1 y 2) y para recuperar el ID de los contactos (Id).
    sql1 = "INSERT INTO contacto (nombre, email, celular, comuna_id, fecha_creacion) VALUES (%s, %s, %s, %s, %s)"
    sqlIdC = "SELECT id FROM contacto WHERE nombre = %s AND email = %s AND celular = %s AND comuna_id = %s AND fecha_creacion = %s LIMIT 1"
    sql2 = "INSERT INTO dispositivo (contacto_id, nombre, descripcion, tipo, anos_uso, estado) VALUES (%s, %s, %s, %s, %s, %s)"
    sqlIdD = "SELECT id FROM dispositivo WHERE contacto_id = %s AND nombre = %s AND descripcion = %s AND tipo = %s AND anos_uso = %s AND estado = %s LIMIT 1"
    sql3 = "INSERT INTO archivo (ruta_archivo, nombre_archivo, dispositivo_id) VALUES (%s, %s, %s)"


    nombredo, email, celular, comuna = contacto.nombre, contacto.email, contacto.celular, contacto.comuna
    hora = datetime.now().replace(microsecond=0)
    resultado1 = f.cursor().execute(sql1, (nombredo, email, celular, comuna, hora))
    f.commit()

    cursor = f.cursor()
    cursor.execute(sqlIdC, (nombredo, email, celular, comuna, hora))
    f.commit()
    rIdC = cursor.fetchone()

    i, resultado2, resultado3 = (0, None, None)
    for dispositivo in dispositivos:
        print(i)
        i += 1
        nombredi, descripcion, img, tipo, anos_uso, estado = (dispositivo.nombre, dispositivo.desc, dispositivo.fotos,
                                                              dispositivo.tipo, dispositivo.anos, dispositivo.estado)
        print(nombredi, descripcion, tipo, anos_uso, estado)
        resultado2 = f.cursor().execute(sql2, (rIdC[0], nombredi, descripcion, tipo, anos_uso, estado))
        f.commit()

        cursor.execute(sqlIdD, (rIdC[0], nombredi, descripcion, tipo, anos_uso, estado))
        f.commit()
        rIdD = cursor.fetchone()

        for img in dispositivo.fotos:
            resultado3 = f.cursor().execute(sql3, (img.path, img.name, rIdD[0]))
            f.commit()
    return True

if __name__ == "__main__":
    app.run(debug=True)