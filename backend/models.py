from datetime import datetime
from app import db


class Cliente(db.Model):
    cedula = db.Column(db.Integer, primary_key=True)
    fechaIngreso = db.Column(db.DateTime, default=datetime.utcnow)
    fechaExpedicion = db.Column(db.DateTime, default=datetime.utcnow)
    ciudadExpedicion = db.Column(db.String(30))
    nombres = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))
    telefono = db.Column(db.String(30))
    direccion = db.Column(db.String(255))
    municipioRucom = db.Column(db.String(45))
    email = db.Column(db.String(100))
    foto = db.Column(db.String(255))
    huella = db.Column(db.String(255))


class Empresa(db.Model):
    nit = db.Column(db.String(80), primary_key=True)
    direccion = db.Column(db.String(255))
    ciudad = db.Column(db.String(30))
    telefono = db.Column(db.String(30))
    representanteLegal = db.Column(db.String(255))
    rucom = db.Column(db.String(30))
    municipioRucom = db.Column(db.String(45))
    departamentoRucom = db.Column(db.String(45))
    logo = db.Column(db.String(255))
    cedulaRepresentante = db.Column(db.Integer)
    cedulaLugaeExpedicion = db.Column(db.String(30))
    nombreEmpresaRucom = db.Column(db.String(45))
    emailEmpresa = db.Column(db.String(45))


class Compra(db.Model):
    idCompra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idEmpresa = db.Column(db.String(80), db.ForeignKey('empresa.nit'))
    ley = db.Column(db.String(255))
    vrGramo = db.Column(db.String(30))
    nota = db.Column(db.String(300))
    estadoCompra = db.Column(db.String(40))
    fechaCompra = db.Column(db.DateTime, default=datetime.utcnow)
    idEmpleado = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleado'))


class Empleado(db.Model):
    idEmpleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    correo = db.Column(db.String(255))
    contrasenia = db.Column(db.String(40))


class detalleCompra(db.Model):
    idDetalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCliente = db.Column(db.Integer, db.ForeignKey('cliente.cedula'))
    idCompra = db.Column(db.Integer, db.ForeignKey('compra.idCompra'))
    gramos = db.Column(db.Float)
    foto = db.Column(db.String(255))
    huella = db.Column(db.String(255))
    estadoCedula = db.Column(db.String(255))
    rut = db.Column(db.String(255))
    antecedentesJuidiciales = db.Column(db.String(255))
    procuraduria = db.Column(db.String(255))
    contraloria = db.Column(db.String(255))
    ofac = db.Column(db.String(255))
    vrGramos = db.Column(db.Float)

