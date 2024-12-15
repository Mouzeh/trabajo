#Contexto:
#Imagina que un grupo de empresarios está iniciando una nueva agencia de viajes llamada "Viajes Aventura". Quieren crear un sistema de reserva en línea para ofrecer a sus clientes la posibilidad de planificar y reservar sus vacaciones de manera conveniente. El sistema debe gestionar diferentes destinos, paquetes turísticos y permitir a los clientes personalizar sus viajes.#
# 
#Requerimientos del Cliente:
#La agencia de viajes tiene varios requisitos clave que desean que se aborden en el sistema:#
#
#1.	Gestión de Destinos:
#•	Cada destino tiene información como nombre, descripción, actividades disponibles y costo.
#•	Debe ser posible agregar, mostrar todos, modificar y eliminar destinos.
#
#2.	Paquetes Turísticos:
#•	Los paquetes turísticos consisten en combinaciones de destinos con fechas específicas.
#•	Cada paquete tiene un precio total que se calcula en función de los destinos seleccionados y las fechas de viaje.
#•	Los clientes pueden ver la disponibilidad de los paquetes para las fechas deseadas.

#3.	Reservas:
#•	Los clientes pueden seleccionar y reservar paquetes turísticos disponibles.
#•	Se requiere un sistema de autenticación para que los clientes puedan realizar reservas y acceder a sus detalles personales.
#•	Cada reserva debe registrarse en una base de datos para su posterior gestión.


 #   Mi código en SQL 
    
-- Crear la base de datos ViajesAventura
CREATE DATABASE IF NOT EXISTS ViajesAventura;
USE ViajesAventura;

-- Tabla Usuarios
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL,
    contraseña VARCHAR(50) NOT NULL,
    rol VARCHAR(45) NOT NULL
);

-- Tabla Destinos
CREATE TABLE Destinos (
    id_destino INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    actividades VARCHAR(45) NOT NULL,
    costo FLOAT NOT NULL
);

-- Tabla Paquetes
CREATE TABLE Paquetes (
    id_paquete INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    precio FLOAT NOT NULL
);

-- Tabla Paquete_Destinos (relación muchos a muchos entre Paquetes y Destinos)
CREATE TABLE Paquete_Destinos (
    paquetes_id_paquete INT NOT NULL,
    destino_id_destino INT NOT NULL,
    PRIMARY KEY (paquetes_id_paquete, destino_id_destino),
    FOREIGN KEY (paquetes_id_paquete) REFERENCES Paquetes (id_paquete) ON DELETE CASCADE,
    FOREIGN KEY (destino_id_destino) REFERENCES Destinos (id_destino) ON DELETE CASCADE
);

-- Tabla Reservas
CREATE TABLE Reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    fecha_reserva DATE NOT NULL,
    estado VARCHAR(45) NOT NULL,
    paquetes_id_paquete INT NOT NULL,
    usuarios_id_usuario INT NOT NULL,
    FOREIGN KEY (paquetes_id_paquete) REFERENCES Paquetes (id_paquete) ON DELETE CASCADE,
    FOREIGN KEY (usuarios_id_usuario) REFERENCES Usuarios (id_usuario) ON DELETE CASCADE
);

SELECT * FROM reservas;
