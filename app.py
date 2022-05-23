#<link rel="stylesheet" href="{{url_for('static',filename='css/stylus.css')}}">
#<label style="color:red;">
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_bootstrap import Bootstrap
from model.Dao import db, CuentaBancaria, DetallesPedidos, DetallesVenta, Empleado, Especie, Historial,\
    HongosCFructifero, MicelioBolsa, MicelioPlacaPetri, Pedidos, PlacasPetri, Proveedores, SelloEsporada, Usuarios,\
    Venta, VialEspora
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user_erpfungi:erpfungi123@localhost/erpfungi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Cl4v3'
#Implementación de la gestion de usuarios con flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'log_in'
login_manager.login_message = '¡ Tu sesión expiró !'
login_manager.login_message_category = "info"


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)


@app.route("/")
def inicio():
    return render_template('principal.html')


@app.route('/Usuarios/iniciarSesion')
def log_in():
    if current_user.is_authenticated:
        return render_template('principal.html')
    else:
        return render_template('usuarios/login.html')


@login_manager.user_loader
def cargar_usuario(id):
    return Usuarios.query.get(int(id))


@app.route('/Usuarios/nuevo')
def nuevoUsuario():
    if current_user.is_authenticated and not current_user.is_admin():
        return render_template('principal.html')
    else:
        return render_template('Usuarios/registroCuenta.html')


@app.route('/Usuarios/agregar', methods=['post'])
def agregarUsuario():
    try:
        usuario = Usuarios()
        usuario.nombre = request.form['Nombre']
        usuario.apPaterno = request.form['A. Paterno']
        usuario.apMaterno = request.form['A. Materno']
        usuario.sexo = request.form['Sexo']
        usuario.direccion = request.form['Direccion']
        usuario.telefono = request.form['Telefono']
        usuario.email = request.form['E-mail']
        usuario.imagen = request.form['Foto']
        usuario.password_Contra = request.form['password']
        usuario.tipo = request.values.get("tipo", "Comprador")
        usuario.estatus = 'Activo'
        usuario.agregar()
        flash('¡ Usuario registrado con exito')
    except:
        flash('¡ Error al agregar al usuario !')
    return render_template('usuarios/registrarCuenta.html')


@app.route("/Usuarios/validarSesion", methods=['POST'])
def login():
    correo = request.form['correo']
    password = request.form['password']
    usuario = Usuarios()
    user = usuario.validar(correo, password)
    if user!=None:
        login_user(user)
        return render_template('principal.html')
    else:
        flash('Nombre de usuario o contraseña incorrectos')
        return render_template('usuarios/login.html')


@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('log_In'))


@app.route('/Usuarios/verPerfil')
@login_required
def consultarUsuario():
    return render_template('usuarios/editar.html')
#fin del manejo de usuarios


@app.route("/CuentaBancaria")
def consutaCuentaBancaria():
    cb = CuentaBancaria()
    return render_template('CuentaBancaria/consultaGeneralCB.html', cuentabancaria=cb.consultaGeneral())


@app.route('/CuentaBancaria/nueva')
# @login_required
def nuevaCB():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('CuentaBancaria/agregarCB.html')
    # else:
    #     abort(404)


@app.route('/CuentaBancaria/agregar', methods=['post'])
# @login_required
def agregarCB():
    # try:
        # if current_user.is_authenticated:
            # if current_user.is_admin():
                try:
                    cb = CuentaBancaria()
                    cb.idCuentaBancaria = request.form['idCuentaBancaria']
                    cb.nombreTitular = request.form['nombreTitular']
                    cb.noTarjeta = request.form['noTarjeta']
                    cb.saldo = request.form['saldo']
                    cb.banco = request.form['banco']
                    cb.mes = request.form['mes']
                    cb.cvv = request.form['cvv']
                    cb.tipo = request.form['tipo']
                    cb.estatus = 'Activa'
                    cb.agregar()
                    flash('Tarjeta agregada con exito')
                except:
                    flash('Error al agregar la Tarjeta')
                return redirect(url_for('consultaGeneralCB'))
            # else:
            #     abort(404)

        # else:
        #     return redirect(url_for('mostrar_login'))
    # except:
    #     abort(500)


@app.route("/DetallesPedidos")
def detallesPedidos():
    dp = DetallesPedidos()
    return render_template('DetallesPedidos/consultaDetallesPedidos.html', detallesPedidos=dp.consultaGeneral())


@app.route('/DetallesPedidos/nueva')
# @login_required
def nuevaDP():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('DEtallesPedidos/agregarDP.html')
    # else:
    #     abort(404)


@app.route('/DetallesPedidos/agregar', methods=['post'])
# @login_required
def agregarDP():
    # try:
        # if current_user.is_authenticated:
            # if current_user.is_admin():
                try:
                    dp = DetallesPedidos()
                    dp.idDetallesPedidos = request.form['idDetallesPedidos']
                    dp.idPedidos = request.form['idPedidos']
                    dp.cantUnidades = request.form['cantUnidades']
                    dp.precioUnitario = request.form['precioUnitario']
                    dp.subtotal = request.form['subtotal']
                    dp.estatus = 'Activa'
                    dp.agregar()
                    flash('Detalles de pedido agregados con éxito')
                except:
                    flash('Error al agregar los detalles del pedido')
                return redirect(url_for('consultaDetallesPedidos'))
            # else:
            #     abort(404)

        # else:
        #     return redirect(url_for('mostrar_login'))
    # except:
    #     abort(500)


@app.route("/DetallesVenta")
def consultaDetallesVenta():
    dv = DetallesVenta()
    return render_template('DetallesVenta/consultaDetallesVenta.html', detallesVenta=dv.consultaGeneral())


@app.route('/DetallesVenta/nueva')
# @login_required
def nuevaDV():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('DetallesVenta/agregarDV.html')
    # else:
    #     abort(404)


@app.route('/DetallesVenta/agregar', methods=['post'])
# @login_required
def agregarDV():
    # try:
        # if current_user.is_authenticated:
            # if current_user.is_admin():
                try:
                    dv = DetallesVenta()
                    dv.idDetallesVenta = request.form['idDetallesVenta']
                    dv.idSelloEsporada = request.form['idSelloEsporada']
                    dv.idVialEspora = request.form['idVialEspora']
                    dv.idVenta = request.form['idVenta']
                    dv.idMicelioPlacaPetri = request.form['idMicelioPlacaPetri']
                    dv.idMicelioBolsa = request.form['idMicelioBolsa']
                    dv.idPlacasPetri = request.form['idPlacasPetri']
                    dv.idHongosCFructifero = request.form['idHongosCFructifero']
                    dv.cantidad = request.form['cantidad']
                    dv.fecha = request.form['fecha']
                    dv.subtotal = request.form['subtotal']
                    dv.estatus = 'Activa'
                    dv.agregar()
                    flash('Detalles de venta agregados con éxito')
                except:
                    flash('Error al agregar detalles de venta')
                return redirect(url_for('consultaDetallesVenta'))
            # else:
            #     abort(404)

        # else:
        #     return redirect(url_for('mostrar_login'))
    # except:
    #     abort(500)


@app.route("/Empleado")
def empleado():
    em = Empleado()
    return render_template('Empleado/consultaGeneralEm.html', empleado=em.consultaGeneral())


@app.route('/Empleado/nueva')
# @login_required
def nuevaEm():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('Empleado/agregarEm.html')
    # else:
    #     abort(404)


@app.route('/Empleado/agregar', methods=['post'])
# @login_required
def agregarEm():
    # try:
        # if current_user.is_authenticated:
            # if current_user.is_admin():
                try:
                    em = Empleado()
                    em.idEmpleado = request.form['idEmpleado']
                    em.nombreCompleto = request.form['nombreCompleto']
                    em.password_hash = request.form['password_hash']
                    em.tipo = request.form['tipo']
                    em.estatus = 'Activa'
                    em.horarioTurno = request.form['horarioTurno']
                    em.foto = request.files['foto'].stream.read()
                    em.agregar()
                    flash('Empleado agregado con exito')
                except:
                    flash('Error al agregar Empleado')
                return redirect(url_for('consultaGeneralEm'))
            # else:
            #     abort(404)

        # else:
        #     return redirect(url_for('mostrar_login'))
    # except:
    #     abort(500)


@app.route('/Empleado/consultarImagen/<int:id>')
def consultarImagenEmpleado(id):
    em = Empleado()
    return em.consultarImagen(id)


@app.route("/Especies")
def consultaEspecies():
    es = Especie()
    return render_template('Especies/consultaGeneralEsp.html', especies=es.consultaGeneral())


@app.route('/Especies/consultarImagen/<int:id>')
def consultarImagenEspecies(id):
    es = Especie()
    return es.consultarImagen(id)


@app.route('/Especies/nueva')
def nuevaEs():
    return render_template('Especies/agregarEs.html')


@app.route("/Historial")
def historial():
    hi = Historial()
    return render_template('Historial/consultarHistorial.html', historial=hi.consultaGeneral())


@app.route('/Historial/nueva')
# @login_required
def nuevaHi():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('Historial/agregarH.html')
    # else:
    #     abort(404)


@app.route("/HongosCFructifero")
def consultaHongosCFructifero():
    hcf = HongosCFructifero()
    return render_template('HongosCFructifero/consultaGeneralHCF.html', hongosCFructifero=hcf.consultaGeneral())


@app.route('/HongosCFructifero/consultarImagen/<int:id>')
def consultarImagenHCF(id):
    hcf = HongosCFructifero()
    return hcf.consultarImagen(id)


@app.route('/HongosCFructifero/nueva')
# @login_required
def nuevaHCF():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('HongosCFructifero/agregarHCF.html')
    # else:
    #     abort(404)


@app.route("/MicelioBolsa")
def micelioBolsa():
    mb = MicelioBolsa()
    return render_template('MicelioBolsa/consultaGeneralMicBol.html', micelioBolsa=mb.consultaGeneral())


@app.route('/MicelioBolsa/consultarImagen/<int:id>')
def consultarImagenMicBol(id):
    mb = MicelioBolsa()
    return mb.consultarImagen(id)


@app.route('/MicelioBolsa/nueva')
def nuevaMB():
    return render_template('MicelioBolsa/agregarMB.html')


@app.route("/MicelioPlacaPetri")
def micelioPlacaPetri():
    mpp = MicelioPlacaPetri()
    return render_template('MicelioPlacaPetri/consultaGeneralMPP.html', micelioPlacaPetri=mpp.consultaGeneral())


@app.route('/MicelioPlacaPetri/consultarImagen/<int:id>')
def consultarImagenMicPP(id):
    mpp = MicelioPlacaPetri()
    return mpp.consultarImagen(id)


@app.route('/MicelioPlacaPetri/nueva')
def nuevaMPP():
    return render_template('MicelioPlacaPetri/agregarMPP.html')


@app.route("/Pedidos")
def pedidos():
    pe = Pedidos()
    return render_template('Pedidos/consultaGeneralPe.html', pedidos=pe.consultaGeneral())


@app.route('/Pedidos/nueva')
# @login_required
def nuevaPe():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('Pedidos/AgregarPe.html')
    # else:
    #     abort(404)


@app.route("/PlacasPetri")
def placasPetri():
    pp = PlacasPetri()
    return render_template('PlacasPetri/consultaGeneralPP.html', PlacasPetri=pp.consultaGeneral())


@app.route('/PlacasPetri/consultarImagen/<int:id>')
def consultarImagenPP(id):
    pp = PlacasPetri()
    return pp.consultarImagen(id)


@app.route('/PlacasPetri/nueva')
def nuevaPP():
    return render_template('PlacasPetri/agregarPP.html')


@app.route("/Proveedores")
def proveedores():
    pr = Proveedores()
    return render_template('Proveedores/consultaGeneralPr.html', Proveedores=pr.consultaGeneral())


@app.route('/Proveedores/consultarImagen/<int:id>')
def consultarImagenPr(id):
    pr = Proveedores()
    return pr.consultarImagen(id)


@app.route('/Proveedores/nueva')
# @login_required
def nuevaPr():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('Proveedores/agregarPr.html')
    # else:
    #     abort(404)


@app.route("/SelloEsporada")
def selloEsporada():
    se = SelloEsporada()
    return render_template('SelloEsporada/consultaGeneralSE.html', SelloEsporada=se.consultaGeneral())


@app.route('/SelloEsporada/consultarImagen/<int:id>')
def consultarImagenSE(id):
    se = SelloEsporada()
    return se.consultarImagen(id)


@app.route('/SelloEsporada/nueva')
# @login_required
def nuevaSE():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('SelloEsporada/agregarSE.html')
    # else:
    #     abort(404)


@app.route("/Usuarios")
def usuarios():
    return "¡¡¡Hola Mundo!!!"


@app.route("/Venta")
def venta():
    ve = Venta()
    return render_template('Venta/consultaVenta.html', Venta=ve.consultaGeneral())


@app.route('/Venta/nueva')
# @login_required
def nuevaVe():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('Venta/agregarVe.html')
    # else:
    #     abort(404)


@app.route("/VialEspora")
def vialEspora():
    ves = VialEspora()
    return render_template('VialEspora/consultaGeneralVE.html', VialEspora=ves.consultaGeneral())


@app.route('/VialEspora/nueva')
# @login_required
def nuevaVEs():
    # if current_user.is_authenticated and current_user.is_admin():
            return render_template('VialEspora/agregarVEs.html')
    # else:
    #     abort(404)


@app.route('/VialEspora/consultarImagen/<int:id>')
def consultarImagenVialEsp(id):
    ves = VialEspora()
    return ves.consultarImagen(id)


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
