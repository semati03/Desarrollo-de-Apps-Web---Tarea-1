class Region:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class Comuna:
    def __init__(self, region_id, id, nombre):
        self.region_id = region_id
        self.id = id
        self.nombre = nombre

class Contacto:
    def __init__(self, nombre, email, celular, region, comuna):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.celular = celular
        self.region = region
        self.comuna = comuna

class Dispositivo:
    def __init__(self, nombre, tipo, anos, estado, fotos, desc = ''):
        self.id = id
        self.nombre = nombre
        self.desc = desc
        self.tipo = tipo
        self.anos = anos
        self.estado = estado
        self.fotos = fotos

class Pictures:
    def __init__(self, path, name, file):
        self.path = path
        self.name = name
        self.file = file

def getRegiones(c):
    sql = "SELECT id, nombre FROM region"
    cursor = c.cursor()
    cursor.execute(sql)
    c.commit()
    regiones = cursor.fetchall()
    listaRegiones = []
    if len(regiones) > 0:
        for reg in regiones:
            regionDB = Region(reg[0], reg[1])
            listaRegiones.append(regionDB)
    return listaRegiones

def getComunas(c):
    sql = "SELECT region_id, id, nombre FROM comuna"
    cursor = c.cursor()
    cursor.execute(sql)
    c.commit()
    comunas = cursor.fetchall()
    listaComunas = []
    if len(comunas) > 0:
        for co in comunas:
            comunaDB = Comuna(co[0], co[1], co[2])
            listaComunas.append(comunaDB)
    return listaComunas
