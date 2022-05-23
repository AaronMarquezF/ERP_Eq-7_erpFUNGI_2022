from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, BLOB, ForeignKey, Float, Date, BOOLEAN, TIME
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class CuentaBancaria(db.Model):
    __tablename__ = 'CuentaBancaria'
    idCuentaBancaria = Column(Integer, primary_key=True)
    nombreTitular = Column(String, nullable=False)
    noTarjeta = Column(Integer, nullable=False)
    saldo = Column(Float, nullable=False)
    banco = Column(String, nullable=False)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
    cvv = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    estatus = Column(String, nullable=False)

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return CuentaBancaria.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        cb = self.consultaIndividuall(id)
        db.session.delete(cb)
        db.session.commit()

    def eliminacionLogica(self, id):
        cb = self.consultaIndividuall(id)
        cb.estatus = 'Inactiva'
        cb.editar()


class DetallesPedidos(db.Model):
    __tablename__ = 'DetallesPedidos'
    idDetallesPedidos = Column(Integer, primary_key=True)
    idPedidos = Column(String, ForeignKey('Pedidos.idDetallesPedidos'))
    cantUnidades = Column(Integer, nullable=False)
    precioUnitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    # pedido = relationship('Pedidos')

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return DetallesPedidos.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        dp = self.consultaIndividual(id)
        db.session.delete(dp)
        db.session.commit()

    def eliminacionLogica(self, id):
        dp = self.consultaIndividuall(id)
        dp.estatus = 'Inactiva'
        dp.editar()


class DetallesVenta(db.Model):
    __tablename__ = 'DetallesVenta'
    idDetallesVenta = Column(Integer, primary_key=True)
    idSelloEsporada = Column(String, ForeignKey('SelloEsporada.idSelloEsporada'))
    idVialEspora = Column(String, ForeignKey('VialEspora.idVialEspora'))
    idVenta = Column(String, ForeignKey('Venta.idVenta'))
    idMicelioPlacaPetri = Column(String, ForeignKey('MicelioPlacaPetri.idMicelioPlacaPetri'))
    idMicelioBolsa = Column(String, ForeignKey('MicelioBolsa.idMicelioBolsa'))
    idPlacasPetri = Column(String, ForeignKey('PlacasPetri.idPlacasPetri'))
    idHongosCFructifero = Column(String, ForeignKey('HongosCFructifero.idHongosCFructifero'))
    cantidad = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)
    subtotal = Column(Float, nullable=False)
    estatus = Column(String, nullable=False)

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return DetallesVenta.query.get(id)


    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        dv = self.consultaIndividuall(id)
        db.session.delete(dv)
        db.session.commit()

    def eliminacionLogica(self, id):
        dv = self.consultaIndividuall(id)
        dv.estatus = 'Inactiva'
        dv.editar()


class Empleado(db.Model):
    __tablename__ = 'Empleado'
    idEmpleado = Column(Integer, primary_key=True)
    nombreCompleto = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    tipo = Column(Integer, nullable=False)
    estatus = Column(String, nullable=False)
    horarioTurno = Column(String, nullable=False)
    foto = Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return Empleado.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).foto

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        em = self.consultaIndividuall(id)
        db.session.delete(em)
        db.session.commit()

    def eliminacionLogica(self, id):
        em = self.consultaIndividuall(id)
        em.estatus = 'Inactiva'
        em.editar()


class Especie(db.Model):
    __tablename__ = 'Especies'
    idEspecies = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    procedeciaGeografica = Column(String, nullable=False)
    estatus = Column(String, nullable=False)
    tipoCuerpoFructifero = Column(String, nullable=False)
    relacionesSimbioticas = Column(String, nullable=False)
    contaminantesAmenazas = Column(String, nullable=False)
    imagen = Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return Especie.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        es = self.consultaIndividual(id)
        db.session.delete(es)
        db.session.commit()

    def eliminacionLogica(self, id):
        es = self.consultaIndividual(id)
        es.estatus = 'Inactiva'
        es.editar()


class Historial(db.Model):
    __tablename__ = 'Historial'
    idHistorial = Column(Integer, primary_key=True)
    idEmpleado = Column(Integer, ForeignKey('Empleado.idEmpleado'))
    fecha = Column(Date, nullable=False)
    horaEntrada = Column(TIME, nullable=False)
    horaSalida = Column(TIME, nullable=False)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return Historial.query.get(id)


    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        hi = self.consultaIndividuall(id)
        db.session.delete(hi)
        db.session.commit()

    def eliminacionLogica(self, id):
        hi = self.consultaIndividuall(id)
        hi.estatus = 'Inactiva'
        hi.editar()


class HongosCFructifero(db.Model):
    __tablename__ = 'HongosCFructifero'
    idHongosCFructifero = Column(Integer, primary_key=True)
    idEspecies = Column(Integer, ForeignKey('Especies.idEspecies'))
    nombreComun = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    pesoNeto = Column(Float, nullable=False)
    precioVentaPublico = Column(Float, nullable=False)
    costoProduccion = Column(Float, nullable=False)
    existencias = Column(Integer, nullable=False)
    estatus = Column(String, nullable=False)
    imagen = Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return HongosCFructifero.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        hcf = self.consultaIndividual(id)
        db.session.delete(hcf)
        db.session.commit()

    def eliminacionLogica(self, id):
        hcf = self.consultaIndividual(id)
        hcf.estatus = 'Inactiva'
        hcf.editar()


class MicelioBolsa(db.Model):
    __tablename__ = 'MicelioBolsa'
    idMicelioBolsa = Column(Integer, primary_key=True)
    idEspecies = Column(Integer, ForeignKey('Especies.idEspecies'))
    presioPublico = Column(Float, nullable=False)
    costoProduccion = Column(Float, nullable=False)
    fechaInoculacion = Column(Date, nullable=False)
    estatus = Column(String, nullable=False)
    imagen = Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return MicelioBolsa.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        mb = self.consultaIndividuall(id)
        db.session.delete(mb)
        db.session.commit()

    def eliminacionLogica(self, id):
        mb = self.consultaIndividuall(id)
        mb.estatus = 'Inactiva'
        mb.editar()


class MicelioPlacaPetri(db.Model):
    __tablename__ = 'MicelioPlacaPetri'
    idMicelioPlacaPetri = Column(Integer, primary_key=True)
    idEspecies = Column(Integer, ForeignKey('Especies.idEspecies'))
    fechaInoculacion = Column(Date, nullable=False)
    precioPublico = Column(Float, nullable=False)
    costoProduccion = Column(Float, nullable=False)
    estatus = Column(String, nullable=False)
    existencias = Column(Integer, nullable=False)
    imagen = Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return MicelioPlacaPetri.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        mpp = self.consultaIndividuall(id)
        db.session.delete(mpp)
        db.session.commit()

    def eliminacionLogica(self, id):
        mpp = self.consultaIndividuall(id)
        mpp.estatus = 'Inactiva'
        mpp.editar()


class Pedidos(db.Model):
    __tablename__ = 'Pedidos'
    idPedidos = Column(Integer, primary_key=True)
    idProveedores = Column(Integer, ForeignKey('Proveedores.idProveedores'))
    idEmpleado = Column(Integer, ForeignKey('Empleado.idEmpleado'))
    concepto = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    tatalPagar = Column(Float, nullable=False)
    estatus = Column(String, nullable=False)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return Pedidos.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        pe = self.consultaIndividuall(id)
        db.session.delete(pe)
        db.session.commit()

    def eliminacionLogica(self, id):
        pe = self.consultaIndividuall(id)
        pe.estatus = 'Inactiva'
        pe.editar()


class PlacasPetri(db.Model):
    __tablename__ = 'PlacasPetri'
    idPlacasPetri = Column(Integer, primary_key=True)
    idEspecies = Column(Integer, ForeignKey('Especies.idEspecies'))
    fechaCreacion = Column(Date, nullable=False)
    composicionIngredientes = Column(String, nullable=False)
    existencias = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    estatus = Column(String, nullable=False)
    precioPublico = Column(Float, nullable=False)
    costoProduccion = Column(Float, nullable=False)
    imagen = Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return PlacasPetri.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        pp = self.consultaIndividuall(id)
        db.session.delete(pp)
        db.session.commit()

    def eliminacionLogica(self, id):
        pp = self.consultaIndividuall(id)
        pp.estatus = 'Inactiva'
        pp.editar()


class Proveedores(db.Model):
    __tablename__ = 'Proveedores'
    idProveedores = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(Integer, nullable=False)
    eMail = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    codigoPostal = Column(Integer, nullable=False)
    estatus = Column(String, nullable=False)
    logo = Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return Proveedores.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).logo

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        pr = self.consultaIndividuall(id)
        db.session.delete(pr)
        db.session.commit()

    def eliminacionLogica(self, id):
        pr = self.consultaIndividuall(id)
        pr.estatus = 'Inactiva'
        pr.editar()


class SelloEsporada(db.Model):
    __tablename__ = 'SelloEsporada'
    idSelloEsporada = Column(Integer, primary_key=True)
    idEspecies = Column(Integer, nullable=False)
    existencias = Column(Integer, nullable=False)
    estatus = Column(String, nullable=False)
    fechaImpresion = Column(Date, nullable=False)
    precioPublico = Column(Float, nullable=False)
    costoProduccion = Column(Float, nullable=False)
    imagen = Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return SelloEsporada.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        se = self.consultaIndividuall(id)
        db.session.delete(se)
        db.session.commit()

    def eliminacionLogica(self, id):
        se = self.consultaIndividuall(id)
        se.estatus = 'Inactiva'
        se.editar()


class Usuarios(UserMixin, db.Model):
    __tablename__ = 'Usuarios'
    idUsuarios = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apPaterno = Column(String, nullable=False)
    apMaterno = Column(String, nullable=False)
    sexo = Column(BOOLEAN, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    eMail = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    imagen = Column(String, nullable=False)
    estatus = Column(String, nullable=False)

    @property
    def password(self):
        raise AttributeError('No Fué posible acceder a password')

    # def validarPassword(self, password):
    #     return check_passwd(self.passwd, password)

    def is_authenticated(self):
        return True

class Venta(db.Model):
    __tablename__ = 'Venta'
    idVenta = Column(Integer, primary_key=True)
    idCuentaBancaria = Column(Integer, ForeignKey('CuentaBancaria.idCuentaBancaria'))
    idUsuarios = Column(Integer, ForeignKey('Usuarios.idUsuarios'))
    idEmpleado = Column(Integer, ForeignKey('Empleado.idEmpleado'))
    fecha = Column(Date, nullable=False)
    total = Column(Float, nullable=False)
    estatus = Column(String, nullable=False)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return Venta.query.get(id)


    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        ve = self.consultaIndividuall(id)
        db.session.delete(ve)
        db.session.commit()

    def eliminacionLogica(self, id):
        ve = self.consultaIndividuall(id)
        ve.estatus = 'Inactiva'
        ve.editar()


class VialEspora(db.Model):
    __tablename__ = 'VialEspora'
    idVialEspora = Column(Integer, primary_key=True)
    idEspecies = Column(Integer, ForeignKey('Especies.idEspecies'))
    existencias = Column(Integer, nullable=False)
    precioPublico = Column(Float, nullable=False)
    costoProduccion = Column(Float, nullable=False)
    estatus = Column(String, nullable=False)
    imagen = Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        # return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividual(self, id):
        return VialEspora.query.get(id)

    def consultarImagen(self, id):
        return self.consultaIndividual(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        ves = self.consultaIndividuall(id)
        db.session.delete(ves)
        db.session.commit()

    def eliminacionLogica(self, id):
        ves = self.consultaIndividuall(id)
        ves.estatus = 'Inactiva'
        ves.editar()
