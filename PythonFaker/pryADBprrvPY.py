import random
from faker import Faker
import psycopg2

fake = Faker()

# Número de registros por tabla
num_clientes = 300
num_tiposeguro = 8
num_polizas = 500
num_agentes = 50
num_reclamaciones = 800
num_pagos = 650
num_comisiones = 550

# Generación de datos - Tabla Clientes
clientes = []
for _ in range(num_clientes):
    clientes.append((fake.first_name(), fake.last_name(), fake.date_of_birth(minimum_age=18, maximum_age=90), fake.email(), str(fake.random_number(digits=10)), fake.address()))

# Generación de datos - Tabla TipoSeguro
tiposeguro = []
tipo_seguro_opciones = [
    'Seguro de vida', 'Seguro de salud', 'Seguro de auto', 'Seguro de hogar', 'Seguro de viajes',
    'Seguro de responsabilidad civil', 'Seguro de mascotas', 'Seguro de accidentes personales'
]
for i in range(num_tiposeguro):
    tiposeguro.append((tipo_seguro_opciones[i % len(tipo_seguro_opciones)], fake.sentence()))

# Conexión a la base de datos de PostgreSQL
try:
    connection = psycopg2.connect(
        host='10.10.10.2',
        port=2345,
        user='postgres',
        password='postgres',
        dbname='broker'
    )
    cursor = connection.cursor()

    # Insertar datos en la tabla Clientes
    cursor.executemany("INSERT INTO Clientes (Nombre, Apellido, FechaNacimiento, Email, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s, %s)", clientes)
    connection.commit()
    
    # Obtener los IDs generados para Clientes
    cursor.execute("SELECT ClienteID FROM Clientes")
    cliente_ids = [row[0] for row in cursor.fetchall()]

    # Insertar datos en la tabla TiposDeSeguro
    cursor.executemany("INSERT INTO TiposDeSeguro (Nombre, Descripcion) VALUES (%s, %s)", tiposeguro)
    connection.commit()
    
    # Obtener los IDs generados para TiposDeSeguro
    cursor.execute("SELECT TipoSeguroID FROM TiposDeSeguro")
    tiposeguro_ids = [row[0] for row in cursor.fetchall()]

    # Generación de datos - Tabla Polizas
    polizas = []
    for _ in range(num_polizas):
        polizas.append((str(fake.random_number(digits=5)), random.choice(cliente_ids), random.choice(tiposeguro_ids),
                        fake.date_this_decade(), fake.date_this_decade(), round(random.uniform(20000.00, 1000000.00), 2)))

    # Generación de datos - Tabla Agentes
    agentes = []
    for _ in range(num_agentes):
        agentes.append((fake.first_name(), fake.last_name(), fake.email(), str(fake.random_number(digits=10))))

    # Insertar datos en la tabla Polizas
    cursor.executemany("INSERT INTO Polizas (NumeroPoliza, ClienteID, TipoSeguroID, FechaInicio, FechaFin, Monto) VALUES (%s, %s, %s, %s, %s, %s)", polizas)
    
    # Insertar datos en la tabla Agentes
    cursor.executemany("INSERT INTO Agentes (Nombre, Apellido, Email, Telefono) VALUES (%s, %s, %s, %s)", agentes)
    connection.commit()
    
    # Obtener los IDs generados para Polizas y Agentes
    cursor.execute("SELECT PolizaID FROM Polizas")
    poliza_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT AgenteID FROM Agentes")
    agente_ids = [row[0] for row in cursor.fetchall()]

    # Generación de datos - Tabla Reclamaciones
    reclamaciones = []
    for _ in range(num_reclamaciones):
        reclamaciones.append((random.choice(poliza_ids), fake.date_this_decade(), round(random.uniform(100.00, 100000.00), 2),
                              fake.word(ext_word_list=['Pendiente', 'En revisión', 'Aprobada', 'Rechazada', 'Pagada', 'Cerrada'])))

    # Generación de datos - Tabla Pagos
    pagos = []
    for _ in range(num_pagos):
        pagos.append((random.choice(poliza_ids), fake.date_this_decade(), round(random.uniform(100.00, 100000.00), 2),
                      fake.word(ext_word_list=['Tarjeta de crédito', 'Tarjeta de débito', 'Transferencia bancaria', 'Efectivo',
                                               'Cheque', 'Pago en Línea', 'PayPal', 'Pago móvil'])))

    # Generación de datos - Tabla Comisiones
    comisiones = []
    for _ in range(num_comisiones):
        comisiones.append((random.choice(agente_ids), random.choice(poliza_ids),
                           round(random.uniform(100.00, 100000.00), 2), fake.date_this_decade()))

    # Insertar datos en la tabla Reclamaciones
    cursor.executemany("INSERT INTO Reclamaciones (PolizaID, FechaReclamacion, MontoReclamado, Estado) VALUES (%s, %s, %s, %s)", reclamaciones)

    # Insertar datos en la tabla Pagos
    cursor.executemany("INSERT INTO Pagos (PolizaID, FechaPago, MontoPagado, MetodoPago) VALUES (%s, %s, %s, %s)", pagos)

    # Insertar datos en la tabla Comisiones
    cursor.executemany("INSERT INTO Comisiones (AgenteID, PolizaID, Monto, FechaComision) VALUES (%s, %s, %s, %s)", comisiones)
    
    # Confirmar los cambios
    connection.commit()
    print("Datos insertados correctamente en la base de datos broker.")

except (Exception, psycopg2.Error) as error:
    print("Error inesperado al intentar insertar datos. Error:", error)

finally:
    # Cerrar la conexión
    if connection:
        cursor.close()
        connection.close()
        print("Conexión cerrada.")
