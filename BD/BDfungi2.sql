create database erpfungi;
use erpfungi;
drop table CuentaBancaria;
create table CuentaBancaria(
	idCuentaBancaria int auto_increment not null,
    noTarjeta int(16)not null,
    saldo double not null,
    banco varchar(20) not null,
    mes int(2) not null,
    anio int(2) not null,
    cvv int(3) not null,
    tipo varchar(20) not null,
    estatus varchar(20) not null,
    constraint pk_CuentaBancaria primary key(idCuentaBancaria),
    constraint chr_estatus check (estatus in('Activa', 'Inactiva','Saldo insuficiente'))
);
create table DetallesPedidos(
	idDetallesPedidos int auto_increment not null,
	idPedidos int not null,
    cantUnidades int not null,
    precioUnitario float not null,
    subtotal float not null,
    constraint fk_DetallesPedidos_Pedidos foreign key (idPedidos) references Pedidos (idPedidos),
    constraint pk_DetallesPedidos primary key(idDetallesPedidos)
);
create table DetallesVenta(
	idDetallesVenta int auto_increment not null,
    idSelloEsporada int not null,
    idVialEspora int not null,
    idVenta int not null,
    idMicelioPlacaPetri int not null,
    idMicelioBolsa int not null,
    idPlacasPetri int not null,
    idHongosCFructifero int not null,
    cantidad int not null,
    fecha date not null,
    subtotal float not null,
    estatus varchar(20) not null,
    constraint pk_DetallesVenta primary key(idDetallesVenta),
    constraint fk_DetallesVenta_SelloEsporada foreign key (idSelloEsporada) references SelloEsporada (idSelloEsporada),
    constraint fk_DetallesVenta_VialEspora foreign key (idVialEspora) references VialEspora (idVialEspora),
    constraint fk_DetallesVenta_Venta foreign key (idVenta) references Venta (idVenta),
    constraint fk_VDetallesVenta_MicelioPlacaPetri foreign key (idMicelioPlacaPetri) references MicelioPlacaPetri (idMicelioPlacaPetri),
    constraint fk_DetallesVenta_MicelioBolsa foreign key (idMicelioBolsa) references MicelioBolsa (idMicelioBolsa),
	constraint fk_DetallesVenta_PlacasPetri foreign key (idPlacasPetri) references PlacasPetri (idPlacasPetri),
    constraint fk_DetallesVenta_HongosCFructifero foreign key (idHongosCFructifero) references HongosCFructifero (idHongosCFructifero),
    constraint chdv_estatus check (estatus in('Activa', 'Finalizada'))
);
ALTER TABLE Empleado DROP COLUMN passwordContrasenia;
ALTER TABLE Empleado ADD password_hash VARCHAR(40) not null AFTER nombreCompleto;
create table Empleado(
	idEmpleado int auto_increment not null,
    nombreCompleto varchar(60) not null,
    passwordContrasenia varchar(40) not null,
    tipo int not null,
    estatus varchar(20) not null,
    horarioTurno varchar(60),
    foto mediumblob not null,
    constraint pk_Empleado primary key(idEmpleado),
    constraint che_estatus check (estatus in('Activo', 'Inactivo', 'receso vacacional'))
);
create table Especies(
	idEspecies int auto_increment not null,
    nombre varchar(60) not null,
    filo varchar(60) not null,
    procedeciaGeografica varchar(60) not null,
    taxonomia varchar(60) not null,
    estatus varchar(24) not null,
    tipoCuerpoFructifero varchar(140) not null,
    relacionesSimbioticas varchar(140) not null,
    contaminantesAmenazas varchar(140) not null,
    imagen mediumblob not null,
    constraint pk_Especies primary key(idEspecies),
    constraint chs_estatus check (estatus in('Activa', 'Inactiva', 'Protegida','En Peligro de Extincion'))
);
ALTER TABLE Historial ADD estatus VARCHAR(20) not null AFTER horaSalida;
create table Historial(
	idHistorial int auto_increment not null,
    idEmpleado int not null,
    fecha date not null,
    horaEntrada time not null,
    horaSalida time not null,
    constraint pk_Historial primary key(idHistorial),
    constraint fk_Historial_Empleado foreign key (idEmpleado) references Empleado (idEmpleado)
);
create table HongosCFructifero(
	idHongosCFructifero int auto_increment not null,
    idEspecies int not null,
    cantidad int not null,
    pesoNeto float not null,
    precioVentaPublico float not null,
    costoProduccion float not null,
    existencias int not null,
    estatus varchar(13) not null,
    constraint pk_HongosCFructifero primary key(idHongosCFructifero),
    constraint fk_HongosCFructifero_Especies foreign key (idEspecies) references Especies (idEspecies),
    constraint chhcf_estatus check (estatus in('En produccion', 'Inactivo'))
);

create table MicelioBolsa(
	idMicelioBolsa int auto_increment not null,
    idEspecies int not null,
    presioPublico float not null,
    costoProduccion float not null,
    fechaInoculacion date not null,
    estatus varchar(10) not null,
    imagen mediumblob not null,
    constraint pk_MicelioBolsa primary key(idMicelioBolsa),
    constraint fk_MicelioBolsa_Especies foreign key (idEspecies) references Especies (idEspecies),
    constraint chmb_estatus check (estatus in('En proceso', 'Colonizado'))
);
create table MicelioPlacaPetri(
	idMicelioPlacaPetri int auto_increment not null,
    idEspecies int not null,
    fechaInoculacion date not null,
    precioPublico float not null,
    costoProduccion float not null,
    estatus varchar(20) not null,
    existencias int not null,
    imagen mediumblob not null,
    constraint pk_MicelioPlacaPetri primary key(idMicelioPlacaPetri),
    constraint fk_MicelioPlacaPetri_Especies foreign key (idEspecies) references Especies (idEspecies),
    constraint chmpp_estatus check (estatus in('Activa', 'Colonizado'))
);
create table Pedidos(
	idPedidos int auto_increment not null,
    idProveedores int not null,
    idEmpleado int not null,
    concepto varchar(140) not null,
    cantidad int not null,
    tatalPagar float not null,
    estatus varchar(20) not null,
    constraint pk_Pedidos primary key(idPedidos),
    constraint fk_Pedidos_Proveedores foreign key (idProveedores) references Proveedores (idProveedores),
    constraint fk_Pedidos_Empleado foreign key (idEmpleado) references Empleado (idEmpleado),
    constraint chped_estatus check (estatus in('Activa', 'Inactiva'))
);

ALTER TABLE PlacasPetri DROP COLUMN color;
ALTER TABLE PlacasPetri ADD color VARCHAR(35) not null AFTER existencias;
create table PlacasPetri(
	idPlacasPetri int auto_increment not null,
    idEspecies int not null,
    fechaCreacion date not null,
    composicionIngredientes varchar(140) not null,
    existencias int not null,
    color int not null,
    estatus varchar(25) not null,
    precioPublico float not null,
    costoProduccion float not null,
    imagen mediumblob not null,
    constraint pk_PlacasPetri primary key(idPlacasPetri),
    constraint fk_PlacasPetri_Especies foreign key (idEspecies) references Especies (idEspecies),
    constraint chpp_estatus check (estatus in('En inventario', 'En espera de ingredientes'))
);
ALTER TABLE Proveedores ADD logo mediumblob not null AFTER estatus;
create table Proveedores(
	idProveedores int auto_increment not null,
    nombre varchar(60)not null,
    direccion varchar(60) not null,
    telefono int(15) not null,
    eMail varchar(60) not null,
    pais varchar(20) not null,
    estado varchar(20) not null,
    ciudad varchar(60) not null,
    codigoPostal int(5) not null,
    estatus varchar(8) not null,
    constraint pk_Proveedores primary key(idProveedores),
    constraint chp_estatus check (estatus in('Activo', 'Inactivo'))
);
create table SelloEsporada(
	idSelloEsporada int auto_increment not null,
    idEspecies int not null,
    existencias int not null,
    estatus varchar(20) not null,
    fechaImpresion date not null,
    precioPublico float not null,
    costoProduccion float not null,
    imagen mediumblob not null,
    constraint pk_SelloEsporada primary key(idSelloEsporada),
    constraint fk_SelloEsporada_Especies foreign key (idEspecies) references Especies (idEspecies),
    constraint chse_estatus check (estatus in('En Inventario', 'Agotada', 'En espera'))
);

ALTER TABLE Usuarios ADD password_hash VARCHAR(256) not null AFTER passwd;
ALTER TABLE Usuarios DROP COLUMN passwd;
create table Usuarios(
	idUsuarios int auto_increment not null,
    nombre varchar(30) not null,
    apPaterno varchar(30) not null,
    apMaterno varchar(30) not null,
    password_Contra varchar(40) not null,
    sexo boolean not null,
    direccion varchar(60) not null,
    telefono int(10) not null,
    eMail varchar(60) not null,
    imagen mediumblob not null,
    estatus varchar(20) not null,
    constraint pk_Usuarios primary key(idUsuarios),
    constraint chu_estatus check (estatus in('Activo', 'Inactivo','Bloqueado'))
);
create table Venta(
	idVenta int auto_increment not null,
	idCuentaBancaria int not null,
    idUsuarios int not null,
    idEmpleado int not null,
    fecha date not null,
    total float not null,
    estatus varchar(10) not null,
    constraint pk_Venta primary key(idVenta),
    constraint fk_Venta_CuentaBancaria foreign key (idCuentaBancaria) references CuentaBancaria (idCuentaBancaria),
    constraint fk_Venta_Usuarios foreign key (idUsuarios) references Usuarios (idUsuarios),
    constraint fk_Venta_Empleado foreign key (idEmpleado) references Empleado (idEmpleado),
    constraint chvnt_estatus check (estatus in('En proceso', 'Finalizada'))
);
create table VialEspora(
	idVialEspora int auto_increment not null,
    idEspecies int not null,
    existencias int not null,
    precioPublico float not null,
    costoProduccion float not null,
	estatus varchar(20) not null,
    imagen mediumblob not null,
    constraint pk_VialEspora primary key(idVialEspora),
    constraint fk_VialEspora_Especies foreign key (idEspecies) references Especies (idEspecies),
    constraint chv_estatus check (estatus in('En Inventario', 'Agotada'))
);
/*Crear un usuario para la conexion con la app*/
drop user user_erpfungi;
create user user_erpfungi identified by 'erpfungi123';
grant select, insert, update, delete on erpfungi.CuentaBancaria to user_erpfungi;
grant select, insert, update, delete on erpfungi.DetallesVenta to user_erpfungi; 
grant select, insert, update, delete on erpfungi.DetallesPedidos to user_erpfungi; 
grant select, insert, update, delete on erpfungi.Empleado to user_erpfungi; 
grant select, insert, update, delete on erpfungi.Especies to user_erpfungi; 
grant select, insert, update, delete on erpfungi.Historial to user_erpfungi; 
grant select, insert, update, delete on erpfungi.MicelioBolsa to user_erpfungi;
grant select, insert, update, delete on erpfungi.HongosCFructifero to user_erpfungi;
grant select, insert, update, delete on erpfungi.Pedidos to user_erpfungi;
grant select, insert, update, delete on erpfungi.PlacasPetri to user_erpfungi;
grant select, insert, update, delete on erpfungi.MicelioPlacaPetri to user_erpfungi; 
grant select, insert, update, delete on erpfungi.Proveedores to user_erpfungi; 
grant select, insert, update, delete on erpfungi.SelloEsporada to user_erpfungi; 
grant select, insert, update, delete on erpfungi.Usuarios to user_erpfungi; 
grant select, insert, update, delete on erpfungi.Venta to user_erpfungi; 
grant select, insert, update, delete on erpfungi.VialEspora to user_erpfungi;
