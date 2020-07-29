import logging
from datetime import datetime
from urllib import response

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from database import db
from models import Cliente, Compra, detalleCompra, Empresa
import re
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Configuración de la base de datos
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'gold'
FULL_URL_BD = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_BD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializacion del objeto db de sqlalchemy
db.init_app(app)

# Configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)


###############################################
# Agregar nuevo cliente
################################################

@app.route('/nuevo-cliente', methods=['POST'], endpoint='nuevo_cliente')
def nuevo_cliente():
    fecha = request.json['fecha']
    cedula = request.json['cedula']
    fecha_expedicion = request.json['fecha_expedicion']
    ciudad_expedicion = request.json['ciudad_expedicion']
    nombres = request.json['nombres']
    apellidos = request.json['apellidos']
    telefono = request.json['telefono']
    direccion = request.json['direccion']
    municipio = request.json['municipio']
    email = request.json['email']

    cliente = Cliente(fechaIngreso=fecha, cedula=cedula, fechaExpedicion=fecha_expedicion,
                      ciudadExpedicion=ciudad_expedicion, nombres=nombres,
                      apellidos=apellidos, telefono=telefono, direccion=direccion,
                      municipioRucom=municipio, email=email)

    db.session.add(cliente)
    db.session.commit()
    return 'recibido'


###############################################
# Buscar clientes
################################################
@app.route('/buscar-cliente/<int:cedula>', endpoint='buscar_cliente')
def buscar_cliente(cedula):
    cliente = Cliente.query.get_or_404(cedula)
    personas = {}
    lista_cliente = []
    personas['cedula'] = cliente.cedula
    personas['nombres'] = cliente.nombres
    personas['apellidos'] = cliente.apellidos
    personas['fecha_expedicion'] = cliente.fechaExpedicion
    personas['telefono'] = cliente.telefono
    personas['direccion'] = cliente.direccion
    personas['municipio'] = cliente.municipioRucom
    lista_cliente.append(personas)
    return jsonify(lista_cliente)


###############################################
# Listar todos los clientes
################################################
@app.route('/lista-clientes', endpoint='lista_cliente')
def lista_cliente():
    clientes = Cliente.query.all()
    personas = {}
    lista_clientes = []
    for c in range(len(clientes)):
        personas['cedula'] = clientes[c].cedula
        personas['nombres'] = clientes[c].nombres
        personas['apellidos'] = clientes[c].apellidos
        personas['fecha_expedicion'] = clientes[c].fechaExpedicion
        personas['telefono'] = clientes[c].telefono
        personas['direccion'] = clientes[c].direccion
        personas['municipio'] = clientes[c].municipioRucom
        lista_clientes.append(personas)
        personas = {}
    return jsonify(lista_clientes)


###############################################
# Editar cliente
################################################
@app.route('/editar-cliente/<int:cedula>', methods=['PUT'], endpoint='editar_cliente')
def editar_cliente(cedula):
    cliente = Cliente().query.get(cedula)
    cedula = request.json['cedula']
    fecha_expedicion = request.json['fecha_expedicion']
    nombres = request.json['nombres']
    apellidos = request.json['apellidos']
    telefono = request.json['telefono']
    direccion = request.json['direccion']
    municipio = request.json['municipio']
    cliente.cedula = cedula
    cliente.fechaExpedicion = fecha_expedicion
    cliente.nombres = nombres
    cliente.apellidos = apellidos
    cliente.telefono = telefono
    cliente.direccion = direccion
    cliente.municipioRucom = municipio
    db.session.commit()
    return 'recibido'


###############################################
# Eliminar cliente
################################################
@app.route('/eliminar-cliente/<int:cedula>', methods=['DELETE'], endpoint='eliminar_cliente')
def eliminar_cliente(cedula):
    cliente = Cliente().query.get(cedula)
    db.session.delete(cliente)

    db.session.commit()
    return 'recibido'


###############################################
# Certificado de afiliación
################################################


###############################################
# Agregar foto
################################################

###############################################
# Agregar huella
################################################


###############################################
# lista empresas
################################################
@app.route('/lista-empresas', methods=['GET'], endpoint='lista_empresas')
def lista_empresas():
    empresas = Empresa.query.add_columns(Empresa.nombreEmpresaRucom, Empresa.nit).all()
    empresa = {}
    lista_empresas = []
    for c in range(len(empresas)):
        empresa['nit'] = empresas[c].nit
        empresa['nombres'] = empresas[c].nombreEmpresaRucom
        lista_empresas.append(empresa)
        empresa = {}
    return jsonify(lista_empresas)


###############################################
# Agregar nueva compra
################################################
@app.route('/nueva-compra', methods=['POST'], endpoint='nueva_compra')
def nueva_compra():
    fechaCompra = request.json['fechaCompra']
    idEmpresa = request.json['idEmpresa']
    ley = request.json['ley']
    vrGramo = request.json['vrGramo']
    nota = request.json['nota']
    estadoCompra = request.json['estadoCompra']
    idEmpleado = request.json['idEmpleado']

    compra = Compra(fechaCompra=fechaCompra, idEmpresa=idEmpresa, ley=ley,
                    vrGramo=vrGramo, nota=nota,
                    estadoCompra=estadoCompra, idEmpleado=idEmpleado)
    db.session.add(compra)
    db.session.commit()
    return 'recibido'


###############################################
# Consultar compra
################################################
@app.route('/consultar-compra/<int:idCompra>', endpoint='consultar_compra')
def consultar_compra(idCompra):
    compras = Compra.query.join(Empresa, Compra.idEmpresa == Empresa.nit) \
        .add_columns(Compra.fechaCompra,
                     Compra.nota, Compra.idCompra,
                     Empresa.nombreEmpresaRucom, Compra.vrGramo,
                     Compra.idEmpresa, Compra.ley,
                     Compra.vrGramo, Compra.idEmpleado). \
        filter(Compra.idCompra == idCompra)
    compra = {}
    lista_compra = []
    for c in compras:
        compra['idCompra'] = c.idCompra
        compra['empresa'] = c.nombreEmpresaRucom
        compra['fecha'] = c.fechaCompra
        compra['nota'] = c.nota
        compra['gramos'] = c.vrGramo
        compra['idEmpresa'] = c.idEmpresa
        compra['ley'] = c.ley
        compra['vrGramo'] = c.vrGramo
        compra['idEmpleado'] = c.idEmpleado
        lista_compra.append(compra)
        compra = {}
    return jsonify(lista_compra)


###############################################
# listar Compras
################################################

@app.route('/lista-compras', endpoint='lista_compras')
def lista_compras():
    compras = Compra.query.join(Empresa, Compra.idEmpresa == Empresa.nit) \
        .add_columns(Compra.fechaCompra,
                     Compra.nota, Empresa.nombreEmpresaRucom, Compra.idCompra, Compra.estadoCompra). \
        filter(Compra.estadoCompra == "abierto")
    compra = {}
    lista_compras = []
    for c in compras:
        compra['idCompra'] = c.idCompra
        compra['estadoCompra'] = c.estadoCompra
        compra['fecha'] = c.fechaCompra
        compra['empresa'] = c.nombreEmpresaRucom
        compra['nota'] = c.nota
        lista_compras.append(compra)
        compra = {}
    return jsonify(lista_compras)


###############################################
# Eliminar   Compra
################################################
@app.route('/eliminar-compra/<int:idCompra>', methods=['DELETE'], endpoint='eliminar_compra')
def eliminar_compra(idCompra):
    compra = Compra().query.get(idCompra)
    db.session.delete(compra)
    db.session.commit()
    return 'recibido'


###############################################
# Certificado Agrupacion Compra
################################################


###############################################
# Agregar cliente a Agrupacion Compra
################################################
@app.route('/cliente-compra', methods=['POST'], endpoint='cliente_compra')
def cliente_compra():
    idDetalle = request.json['idDetalle']
    cedula = request.json['cedula']
    idCompra = request.json['idCompra']
    gramos = request.json['gramos']
    compra_cliente = detalleCompra(idDetalle=idDetalle, idCliente=cedula, idCompra=idCompra,
                                   gramos=gramos)
    db.session.add(compra_cliente)
    db.session.commit()
    return 'recibido'


###############################################
# Tota gramos
################################################
@app.route('/suma-gramos/<int:idCompra_>', methods=['GET'], endpoint='suma_gramos')
def suma_gramos(idCompra_):
    detalle_compra = detalleCompra.query.join(Cliente, detalleCompra.idCliente == Cliente.cedula) \
        .join(Compra, detalleCompra.idCompra == Compra.idCompra) \
        .add_columns(detalleCompra.gramos). \
        filter(Compra.idCompra == idCompra_)
    detalle = {}
    lista = []
    suma = 0
    for c in detalle_compra:
        suma += c.gramos
    detalle['suma_gramos'] = suma
    lista.append(detalle)
    return jsonify(lista)


###############################################
# Editar Compra
################################################
@app.route('/editar-compra/<int:idCompra>', methods=['PUT'], endpoint='editar_compra')
def editar_compra(idCompra):
    compra = Compra().query.get(idCompra)

    fechaCompra = request.json['fechaCompra']
    idEmpresa = request.json['idEmpresa']
    ley = request.json['ley']
    nota = request.json['nota']
    vrGramo = request.json['vrGramo']
    estadoCompra = request.json['estadoCompra']
    idEmpleado = request.json['idEmpleado']

    compra.fechaCompra = fechaCompra
    compra.idEmpresa = idEmpresa
    compra.ley = ley
    compra.nota = nota
    compra.vrGramo = vrGramo
    compra.estadoCompra = estadoCompra
    compra.idEmpleado = idEmpleado
    db.session.commit()
    return 'recibido'


###############################################
# Listas clientes en compra
################################################
@app.route('/lista-cliente-compra/<int:idCompra_>', methods=['GET'], endpoint='lista_cliente_compra')
def lista_cliente_compra(idCompra_):
    detalle_compra = detalleCompra.query.join(Cliente, detalleCompra.idCliente == Cliente.cedula) \
        .join(Compra, detalleCompra.idCompra == Compra.idCompra) \
        .add_columns(Compra.fechaCompra, Compra.idCompra, Cliente.cedula,
                     Cliente.nombres, Cliente.apellidos,
                     detalleCompra.gramos, detalleCompra.foto, detalleCompra.huella). \
        filter(Compra.idCompra == idCompra_)
    lista_clientes = []
    detalle = {}
    for c in detalle_compra:
        detalle['fecha'] = c.fechaCompra
        detalle['no_doc'] = c.idCompra
        detalle['cedula'] = c.cedula
        detalle['nombres'] = c.nombres
        detalle['apellidos'] = c.apellidos
        detalle['gramos'] = c.gramos
        detalle['foto'] = c.foto
        detalle['huella'] = c.huella
        lista_clientes.append(detalle)
        detalle = {}
    return jsonify(lista_clientes)


###############################################
# Agregar foto en cliente compra
################################################

###############################################
# Agregar huella en cliente compra
################################################

###############################################
# Editar  cliente compra
################################################

@app.route('/editar-cliente-compra/<int:cedula>', methods=['PUT'], endpoint='editar_cliente_compra')
def editar_cliente_compra(cedula):
    detalle_compra = detalleCompra().query.get()
    cedula = request.json['cedula']
    nombres = request.json['nombres']
    apellidos = request.json['apellidos']
    gramos = request.json['gramos']
    detalle_compra.cedula = cedula
    detalle_compra.nombres = nombres
    detalle_compra.apellidos = apellidos
    detalle_compra.gramos = gramos
    db.session.commit()
    return 'recibido'


###############################################
# Eliminar  cliente compra
################################################

@app.route('/eliminar-cliente-compra/<int:cedula>/<int:idCompra>', methods=['DELETE'],
           endpoint='eliminar_cliente_compra')
def eliminar_cliente_compra(cedula, idCompra):
    cliente_compra = detalleCompra().query. \
        filter(detalleCompra.idCliente == cedula).filter(detalleCompra.idCompra == idCompra)
    cliente_detalle_compra = detalleCompra().query.get(cliente_compra[0].idDetalle)
    db.session.delete(cliente_detalle_compra)
    db.session.commit()
    return 'Eliminado'


###############################################
# Buscar Cliente Compra
################################################
@app.route("/bucar-cliente-compra/<parametro>", endpoint='bucar_cliente_compra')
def bucar_cliente_compra(parametro=None):
    nombre_empresa = []
    empresa = Empresa.query.all()
    for e in empresa:
        nombre_empresa.append(e.nombreEmpresaRucom)

    if re.search("[0-9]{5,}", parametro) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Cliente.cedula == int(parametro)).all()

    elif re.search("[0-9]{4}\-[0-9]{2}\-[0-9]{2}", parametro) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Compra.fechaCompra == parametro).all()

    elif parametro in nombre_empresa:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            join(Empresa, Compra.idEmpresa == Empresa.nit). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Empresa.nombreEmpresaRucom == parametro).all()

    elif re.search("[a-zA-Z]+", parametro) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            join(Empresa, Compra.idEmpresa == Empresa.nit). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Empresa.municipioRucom == parametro).all()

    elif re.search("[0-9]+-[0-9]+-[0-9]+ [a-zA-Z]+", parametro) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Compra.idCompra == parametro).all()
    """
    elif re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", parametro1) is not None and re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                                                                                       parametro2) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Compra.fechaCompra >= parametro1, Compra.fechaCompra <= parametro2).all()
    """
    detalle = {'fecha': [], 'cedula': [], 'nombres': [],
               'estado_cedula': [], 'rut': [],
               'judiciales': [], 'procuraduria': [], 'contraloria': [], 'ofac': []}

    for c in detalle_compra:
        detalle['fecha'].append(c.fechaCompra)
        detalle['cedula'].append(c.cedula)
        detalle['nombres'].append(c.nombres + c.apellidos)
        detalle['estado_cedula'].append(c.estadoCedula)
        detalle['rut'].append(c.rut)
        detalle['judiciales'].append(c.antecedentesJuidiciales)
        detalle['procuraduria'].append(c.procuraduria)
        detalle['contraloria'].append(c.contraloria)
        detalle['ofac'].append(c.ofac)

    return detalle


if __name__ == "__main__":
    app.run(debug=True)


###############################################
# vigencia cedula
################################################

###############################################
# Estado Rut
################################################

###############################################
# Antecedentes judiciales
################################################

###############################################
# antecedentes procuraduria
################################################

###############################################
# contraloria
################################################

###############################################
# ofac
################################################

###############################################
# datos documentos cliente
################################################


@app.route("/documentos-compra/<parametro>", endpoint='documentos_compra')
@app.route('/documentos-compra/<parametro1>/<parametro2>', endpoint='documentos_compra')
def documentos_compra(parametro=None, parametro1=None, parametro2=None):
    nombre_empresa = []
    empresa = Empresa.query.all()
    for e in empresa:
        nombre_empresa.append(e.nombreEmpresaRucom)

    if re.search("[0-9]{5,}", parametro) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Cliente.cedula == int(parametro)).all()

    elif re.search("[0-9]{4}\-[0-9]{2}\-[0-9]{2}", parametro) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Compra.fechaCompra == parametro).all()

    elif parametro in nombre_empresa:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            join(Empresa, Compra.idEmpresa == Empresa.nit). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Empresa.nombreEmpresaRucom == parametro).all()

    elif re.search("[a-zA-Z]+", parametro) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            join(Empresa, Compra.idEmpresa == Empresa.nit). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Empresa.municipioRucom == parametro).all()

    elif re.search("[0-9]+-[0-9]+-[0-9]+ [a-zA-Z]+", parametro) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, Cliente.apellidos, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Compra.idCompra == parametro).all()
    """
    elif re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", parametro1) is not None and re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                                                                                       parametro2) is not None:
        detalle_compra = detalleCompra.query. \
            join(Cliente, detalleCompra.idCliente == Cliente.cedula). \
            join(Compra, detalleCompra.idCompra == Compra.idCompra). \
            add_columns(Compra.fechaCompra, Cliente.cedula,
                        Cliente.nombres, detalleCompra.estadoCedula, detalleCompra.rut,
                        detalleCompra.antecedentesJuidiciales, detalleCompra.procuraduria,
                        detalleCompra.contraloria, detalleCompra.ofac). \
            filter(Compra.fechaCompra >= parametro1, Compra.fechaCompra <= parametro2).all()
    """
    detalle = {'fecha': [], 'cedula': [], 'nombres': [],
               'estado_cedula': [], 'rut': [],
               'judiciales': [], 'procuraduria': [], 'contraloria': [], 'ofac': []}

    for c in detalle_compra:
        detalle['fecha'].append(c.fechaCompra)
        detalle['cedula'].append(c.cedula)
        detalle['nombres'].append(c.nombres + c.apellidos)
        detalle['estado_cedula'].append(c.estadoCedula)
        detalle['rut'].append(c.rut)
        detalle['judiciales'].append(c.antecedentesJuidiciales)
        detalle['procuraduria'].append(c.procuraduria)
        detalle['contraloria'].append(c.contraloria)
        detalle['ofac'].append(c.ofac)

    return detalle


if __name__ == "__main__":
    app.run(debug=True)
