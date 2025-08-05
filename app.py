import pymysql
from markupsafe import escape
from flask import Flask, url_for, session, get_flashed_messages, render_template, request, redirect, jsonify, flash
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

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Máximo 16 MB

currentPage = 0
maxPage = 0
num = 0

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = request.args.get('mensaje')
    return render_template('index.html', mensaje=mensaje)

@app.route('/agregar-donacion', methods=['GET', 'POST'])
def agregar_donacion():
    f = getFormConnection()     # Se establece la conexión con el servidor mysql
    regiones = getRegiones(f)   # Se obtienen las regiones
    comunas = getComunas(f)     # Se obtienen las comunas
    mostrar_confirmacion = False
    error = False
    # Si se usa el metodo POST, entonces se recuperan los valores del formulario.
    if request.method == 'POST':
        if request.form['confirm'] == "yes":

            contacto = Contacto(request.form['nombreContacto'],
                                request.form['emailContacto'],
                                request.form['numeroContacto'],
                                request.form['region'],
                                request.form['comuna'])
            dispositivos, i = ([], 0)   # Se recuperan los dispositivos de la donación
            while True:
                try:    # Si no se retorna un error, entonces se recuperan los datos del formulario de dispositivos.
                    dispositivo = Dispositivo(request.form['nombreDisp' + str(i)],
                                              request.form['tipoDisp' + str(i)],
                                              request.form['anosDisp' + str(i)],
                                              request.form['estadoDisp' + str(i)],
                                              list(request.files.getlist('fotosDisp' + str(i))),
                                              request.form['descripcionDisp' + str(i)])
                    # Se añade el dispositivo actual a una lista
                    dispositivos.append(dispositivo)
                    # Se incrementa el i
                    i += 1
                except:   # Si al solicitar el request se arroja un error, entonces no quedan dispositivos por recuperar.
                    break
            # Se realizan las validaciones y se procede de dos formas distintas
            validated = validation(contacto, dispositivos)
            if validated is False:
                error = True
            else:
                mostrar_confirmacion = True
            resultado = insertDonation(f, contacto, dispositivos)
        else:
            redirect(url_for('agregar_donacion'))
    return render_template('agregar_donacion.html', regiones = regiones,
                           comunas = comunas, mostrar_confirmacion=mostrar_confirmacion,
                           error=error)

@app.route('/ver_dispositivos', methods=['GET', 'POST'])
def ver_dispositivos():
    global currentPage, maxPage, num

    print(currentPage, maxPage, num)
    f = getFormConnection()  # Se establece la conexión con el servidor MySQL
    dispositivos = []  # Lista para almacenar los dispositivos
    archivos = {}  # Diccionario para almacenar los archivos por dispositivo
    error = False  # Variable para manejar errores

    if request.method == 'POST':
        print("post")
        print(f"antes {currentPage}, {maxPage}, {num}")
        backOrNext = request.form['direction']
        if backOrNext == 'back':
            currentPage -= 1 if currentPage > 1 else 1
        elif backOrNext == 'next':
            currentPage += 1 if currentPage < maxPage else maxPage
        print(f"despues {currentPage}, {maxPage}, {num}")
        redirect(url_for('ver_dispositivos'))
    try:
        if currentPage < 1:
            currentPage = 1
        if currentPage > maxPage:
            currentPage = maxPage
        with f.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM dispositivo")
            newNum = cursor.fetchall()[0][0]

            if currentPage == 0 and maxPage == 0 and num == 0 or newNum != num:
                print("inicializacion")
                print(f"antes primer {currentPage}, {maxPage}, {num}")
                num = newNum
                if num % 5 == 0:
                    maxPage = (num // 5)
                else:
                    maxPage = (num // 5) + 1
                currentPage = 1 if currentPage == 0 else currentPage
                print(f"despues primer {currentPage}, {maxPage}, {num}")

            if num - (currentPage * 5 - 5) < 5:
                cursor.execute("SELECT D.id, D.contacto_id, CO.nombre, CO.email, COM.nombre, D.nombre, D.descripcion, D.tipo, D.anos_uso, D.estado "
                               "FROM dispositivo D, contacto CO, comuna COM "
                               "WHERE contacto_id=CO.id AND CO.comuna_id=COM.id "
                               "ORDER BY id DESC LIMIT %s, %s", (currentPage * 5 - 5, num - (currentPage * 5 - 5)))
                dispositivos = cursor.fetchall()
            else:
                cursor.execute("SELECT D.id, D.contacto_id, CO.nombre, CO.email, COM.nombre, D.nombre, D.descripcion, D.tipo, D.anos_uso, D.estado "
                               "FROM dispositivo D, contacto CO, comuna COM "
                               "WHERE contacto_id=CO.id AND CO.comuna_id=COM.id "
                               "ORDER BY id DESC LIMIT %s, %s", (currentPage * 5 - 5, 5))
                dispositivos = cursor.fetchall()
            # Obtener archivos asociados a cada dispositivo
            for dispositivo in dispositivos:
                cursor.execute("SELECT id, ruta_archivo, nombre_archivo FROM archivo WHERE dispositivo_id=%s", (dispositivo[0],))
                archivos[dispositivo[0]] = cursor.fetchall()

    except Exception as e:
        error = True
        print(f"Error al recuperar dispositivos: {e}")
    return render_template('ver_dispositivos.html', dispositivos=dispositivos,
                           archivos=archivos, error=error, currentPage=currentPage, maxPage=maxPage)

def validation(contacto, dispositivos):
    # Validación de contacto
    if not validationContact(contacto):
        return False
    # Se toma cada dispositivo por separado
    for dispositivo in dispositivos:
        # Validación de los datos del dispositivo
        if not validationDevice(dispositivo):
            return False
        # Se toma cada imagen del dispositivo
        for img in dispositivo.fotos:
            # Validación de las imagenes del dispositivo
            if not validationIMG(img):
                return False
    return True

def insertDonation(f, contacto, dispositivos):
    imgClass = []
    for dispositivo in dispositivos:
        for img in dispositivo.fotos:
            _filename = hashlib.sha256(
                secure_filename(img.filename)
                .encode('utf-8')
            ).hexdigest()
            _extension = filetype.guess(img).extension
            img_filename = f"{_filename}.{_extension}"
            imgClass.append(Pictures(app.config["UPLOAD_FOLDER"], img_filename, img))
            img.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))
        dispositivo.fotos = imgClass
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
        i += 1
        nombredi, descripcion, a, tipo, anos_uso, estado = (dispositivo.nombre, dispositivo.desc, dispositivo.fotos,
                                                            dispositivo.tipo, dispositivo.anos, dispositivo.estado)
        resultado2 = f.cursor().execute(sql2, (rIdC[0], nombredi, descripcion, tipo, anos_uso, estado))
        f.commit()

        cursor.execute(sqlIdD, (rIdC[0], nombredi, descripcion, tipo, anos_uso, estado))
        f.commit()
        rIdD = cursor.fetchone()

        for img in dispositivo.fotos:
            resultado3 = f.cursor().execute(sql3, (img.path, img.name, rIdD[0]))
            f.commit()
    return True

@app.route('/informacion_dispositivos', methods=['GET', 'POST'])
def informacion_dispositivos():
    dispositivo_id = request.args.get('id')
    f = getFormConnection()
    archivos = {}
    comentarios = []
    cursor = f.cursor()

    # Si se lanza una solicitud POST, se inserta el comentario
    if request.method == 'POST':
        name = request.form.get('CommentName')
        text = request.form.get('CommentText')

        # Validación de datos del comentario
        if len(name) < 3 or len(name) > 80:
            flash("El largo del nombre debe ser de entre 3 y 80 caracteres", "validationError")
            return redirect(url_for('informacion_dispositivos', id=dispositivo_id))
        elif len(text) < 5:
            flash("El largo del comentario debe ser mayor a 5 caracteres", "validationError")
            return redirect(url_for('informacion_dispositivos', id=dispositivo_id))
        else:
            # Insertar el comentario en la base de datos
            t = datetime.now().replace(microsecond=0)
            cursor.execute("INSERT INTO comentario (nombre, texto, fecha, dispositivo_id) VALUES (%s, %s, %s, %s)",
                           (name, text, t, dispositivo_id))
            f.commit()  # Confirmar los cambios en la base de datos
            flash("Comentario agregado exitosamente!", "success")  # Mensaje de éxito después de insertar

    # Consultar los detalles del dispositivo
    cursor.execute("SELECT D.id, CO.nombre, CO.email, CO.celular, COM.nombre, REG.nombre, D.nombre, D.anos_uso, D.tipo, D.estado "
                   "FROM dispositivo D "
                   "JOIN contacto CO ON D.contacto_id = CO.id "
                   "JOIN comuna COM ON CO.comuna_id = COM.id "
                   "JOIN region REG ON COM.region_id = REG.id "
                   "WHERE D.id = %s", dispositivo_id)
    dispositivo = cursor.fetchone()

    # Consultar los archivos asociados al dispositivo
    cursor.execute("SELECT id, ruta_archivo, nombre_archivo FROM archivo WHERE dispositivo_id=%s", dispositivo[0])
    archivos[dispositivo[0]] = cursor.fetchall()

    # Consultar los comentarios del dispositivo
    cursor.execute("SELECT C.nombre, C.texto, C.fecha "
                   "FROM comentario C "
                   "WHERE C.dispositivo_id = %s", dispositivo_id)
    comentarios = cursor.fetchall()

    f.close()

    # Renderizar el template, pasando los comentarios actualizados
    return render_template('informacion-dispositivos.html', dispositivo=dispositivo,
                           archivos=archivos, comentarios=comentarios, dispositivo_id=dispositivo_id)

@app.route('/tipo_dispositivos', methods=['GET'])
def tipo_dispositivos():
    return render_template('tipo-dispositivos.html')

@app.route('/get_data_tipo_dispositivos', methods=['GET'])
def get_data_tipo_dispositivos():
    f = getFormConnection()
    cursor = f.cursor()
    cursor.execute("SELECT tipo, COUNT(*) AS total FROM dispositivo GROUP BY tipo")
    dispositivos_por_tipo = cursor.fetchall()
    f.close()

    # Convertir datos a JSON
    data = [{"tipo": tipo, "total": total} for (tipo, total) in dispositivos_por_tipo]
    return jsonify(data)

@app.route('/contactos_comuna', methods=['GET'])
def contactos_comuna():
    return render_template('contactos-comuna.html')

@app.route('/get_data_contactos_comuna', methods=['GET'])
def get_data_contactos_comuna():
    f = getFormConnection()
    cursor = f.cursor()
    cursor.execute("SELECT comuna.nombre, COUNT(*) AS total FROM contacto JOIN comuna ON contacto.comuna_id = comuna.id GROUP BY comuna.nombre")
    contactos_por_comuna = cursor.fetchall()
    f.close()

    # Convertir datos a JSON
    data = [{"comuna": comuna, "total": total} for (comuna, total) in contactos_por_comuna]
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=3306)
    app.run(debug=True)