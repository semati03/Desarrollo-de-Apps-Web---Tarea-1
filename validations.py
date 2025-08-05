import pymysql
import re
from gettersAndSetters import Contacto, Dispositivo
import filetype

def validationContact(contacto):
    name, email, number, region, commune = contacto.nombre, contacto.email, contacto.celular, contacto.region, contacto.comuna
    try:
        assert(name != '' and email != '' and number != '' and region != '' and commune != '')
    except AssertionError:
        print("a")
        return False
    if not validationName(name, "donator"):
        print("b")
        return False
    if not validationEmail(email):
        print("c")
        return False
    if not validationNumber(number):
        print("d")
        return False
    return True

def validationDevice(dispositivo):
    deviceName, deviceType, useTime, status = dispositivo.nombre, dispositivo.tipo, dispositivo.anos, dispositivo.estado
    try:
        assert(deviceName != '' and deviceType != '' and useTime != '' and status != '')
    except AssertionError:
        return False
    if not validationName(deviceName, "device"):
        return False
    return True

def validationIMG(conf_img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}
    if conf_img is None:
        return False

    if conf_img.filename == "":
        return False

    ftype_guess = filetype.guess(conf_img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False

    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validationName(name, arg):
    try:
        if arg == "donator":
            assert(3 < len(name) < 80)
        if arg == "device":
            assert(3 < len(name))
    except AssertionError:
        return False
    return True

def validationEmail(email):
    a = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(a, email):
        return True
    else:
        return False

def validationNumber(number):
    try:
        assert(type(int(number)) == int and len(number) == 9)
    except AssertionError:
        return False
    return True