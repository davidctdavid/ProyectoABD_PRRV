--Creación de la tabla Clientes
CREATE TABLE Clientes (
    ClienteID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    FechaNacimiento DATE,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefono VARCHAR(15),
    Direccion VARCHAR(255)
);
--Creación de la tabla TipoDeSeguro
CREATE TABLE TiposDeSeguro (
    TipoSeguroID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(100)
);
--Creación de la tabla Polizas
CREATE TABLE Polizas (
    PolizaID SERIAL PRIMARY KEY,
    NumeroPoliza VARCHAR(50) UNIQUE NOT NULL,
    ClienteID INT,
    TipoSeguroID INT,
    FechaInicio DATE,
    FechaFin DATE,
    Monto DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID),
    FOREIGN KEY (TipoSeguroID) REFERENCES TiposDeSeguro(TipoSeguroID)
);
--Creación de la tabla Agentes
CREATE TABLE Agentes (
    AgenteID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefono VARCHAR(15)
);
--Creación de la tabla Reclamaciones
CREATE TABLE Reclamaciones (
    ReclamacionID SERIAL PRIMARY KEY,
    PolizaID INT,
    FechaReclamacion DATE NOT NULL,
    MontoReclamado DECIMAL(10, 2) NOT NULL,
    Estado VARCHAR(50) NOT NULL,
    FOREIGN KEY (PolizaID) REFERENCES Polizas(PolizaID)
);
--Creación de la tabla Pagos
CREATE TABLE Pagos (
    PagoID SERIAL PRIMARY KEY,
    PolizaID INT,
    FechaPago DATE NOT NULL,
    MontoPagado DECIMAL(10, 2) NOT NULL,
    MetodoPago VARCHAR(50) NOT NULL,
    FOREIGN KEY (PolizaID) REFERENCES Polizas(PolizaID)
);
--Creación de la tabla Comisiones
CREATE TABLE Comisiones (
    ComisionID SERIAL PRIMARY KEY,
    AgenteID INT,
    PolizaID INT,
    Monto DECIMAL(10, 2) NOT NULL,
    FechaComision DATE NOT NULL,
    FOREIGN KEY (AgenteID) REFERENCES Agentes(AgenteID),
    FOREIGN KEY (PolizaID) REFERENCES Polizas(PolizaID)
);
