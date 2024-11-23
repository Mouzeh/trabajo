import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from test import Conexion  
import re
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = Conexion.conectar()

    def execute_query(self, query, values=None):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, values)
                self.connection.commit()
                return cursor
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
                self.connection.rollback()
                return None
            finally:
                cursor.close()
        else:
            print("No hay conexión a la base de datos")
            return None

    def fetch_all(self, query, values=None):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, values)
                return cursor.fetchall()  
            except Error as e:
                print(f"Error al obtener resultados: {e}")
                return []
            finally:
                cursor.close()
        else:
            print("No hay conexión a la base de datos")
            return []

class SistemaGestion:
    def __init__(self, db):
        self.db = db
        

class Empleado(SistemaGestion):
    def __init__(self, db):
        super().__init__(db)
        self.empleados_registrados = []

    def validar_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def validar_telefono(self, telefono):
        return telefono.isdigit() and len(telefono) >= 7

    def registrar_empleado(self, nombre_usuario, nombre, apellido, direccion, telefono, email, fecha_inicio, sueldo, proyecto, departamento, id_departamento):
        if not self.validar_email(email):
            messagebox.showerror("Error", "Email inválido.")
            return
        if not self.validar_telefono(telefono):
            messagebox.showerror("Error", "Teléfono inválido.")
            return
        
        
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Debe ser DD-MM-YYYY.")
            return
        
        query = """
            INSERT INTO Empleado (Nombre_Usuario, Nombre, Apellido, Dirección, Telefono, Email, Fecha_inicio_contrato, Sueldo, Proyecto, Departamento, ID_Departamento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (nombre_usuario, nombre, apellido, direccion, telefono, email, fecha_inicio_dt, sueldo, proyecto, departamento, id_departamento)
        print(f"Valores a insertar: {values}")
        self.db.execute_query(query, values)
        
        self.empleados_registrados.append({
            "Nombre_Usuario": nombre_usuario,
            "Nombre": nombre,
            "Apellido": apellido,
            "Dirección": direccion,
            "Teléfono": telefono,
            "Email": email,
            "Fecha_inicio_contrato": fecha_inicio_dt,
            "Sueldo": sueldo,
            "Proyecto": proyecto,
            "Departamento": departamento,
            "ID_Departamento": id_departamento
        })
        
        print("Empleado registrado exitosamente")

    def mostrar_empleados(self):
        if self.empleados_registrados:
            empleados_str = "\n".join([f"{empleado['Nombre_Usuario']} - {empleado['Nombre']} {empleado['Apellido']}" for empleado in self.empleados_registrados])
            messagebox.showinfo("Empleados Registrados", empleados_str)
        else:
            messagebox.showinfo("Empleados Registrados", "No hay empleados registrados.")

class Departamento(SistemaGestion):
    def crear_departamento(self, nombre_departamento, gerente):
        query = "INSERT INTO Departamento (Nombre_Departamento, Gerente) VALUES (%s, %s)"
        values = (nombre_departamento, gerente)
        self.db.execute_query(query, values)
        print("Departamento creado exitosamente")

    def eliminar_departamento(self, id_departamento):
        query = "DELETE FROM Departamento WHERE ID_Departamento = %s"
        values = (id_departamento,)
        self.db.execute_query(query, values)
        print("Departamento eliminado exitosamente")

    def modificar_departamento(self, id_departamento, nuevo_nombre, nuevo_gerente):
        query = "UPDATE Departamento SET Nombre_Departamento = %s, Gerente = %s WHERE ID_Departamento = %s"
        values = (nuevo_nombre, nuevo_gerente, id_departamento)
        self.db.execute_query(query, values)
        print("Departamento modificado exitosamente")

    def mostrar_departamentos(self):
        query = "SELECT * FROM Departamento"
        departamentos = self.db.fetch_all(query)
        
        if departamentos:
            departamentos_str = "\n".join([f"ID: {d[0]}, Nombre: {d[1]}, Gerente: {d[2]}" for d in departamentos])
            messagebox.showinfo("Departamentos", departamentos_str)
        else:
            messagebox.showinfo("Departamentos", "No hay departamentos registrados.")
            

class Proyecto(SistemaGestion):
    def crear_proyecto(self, nombre_proyecto, descripcion, id_empleado):
        query = "INSERT INTO Proyecto (Nombre_Proyecto, Descripción, Id_Empleado) VALUES (%s, %s, %s)"
        values = (nombre_proyecto, descripcion, id_empleado)
        self.db.execute_query(query, values)
        print("Proyecto creado exitosamente")

    def asignar_empleado_a_proyecto(self, nombre_usuario, id_proyecto):
        query = """
            INSERT INTO Empleado_Proyecto (Id_Empleado, Id_Proyecto)
            VALUES (%s, %s)
        """
        values = (nombre_usuario, id_proyecto)
        self.db.execute_query(query, values)
        print("Empleado asignado al proyecto exitosamente")

    def eliminar_proyecto(self, id_proyecto):
        query = "DELETE FROM Proyecto WHERE ID_Proyecto = %s"
        values = (id_proyecto,)
        self.db.execute_query(query, values)
        print("Proyecto eliminado exitosamente")

    def modificar_proyecto(self, id_proyecto, nuevo_nombre, nueva_descripcion):
        query = "UPDATE Proyecto SET Nombre_Proyecto = %s, Descripción = %s WHERE ID_Proyecto = %s"
        values = (nuevo_nombre, nueva_descripcion, id_proyecto)
        self.db.execute_query(query, values)
        print("Proyecto modificado exitosamente")



class RegistroTiempo(SistemaGestion):
    def registrar_tiempo(self, nombre_usuario, id_proyecto, fecha, horas_trabajadas, descripcion):
        
        try:
            fecha_dt = datetime.strptime(fecha, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Debe ser DD-MM-YYYY.")
            return

        query = """
            INSERT INTO `REGISTRO TIEMPO` (Nombre_Usuario, ID_Proyecto, Fecha, Horas_Trabajadas, Descripción)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (nombre_usuario, id_proyecto, fecha_dt, horas_trabajadas, descripcion)
        self.db.execute_query(query, values)
        print("Registro de tiempo creado exitosamente")

class MainApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Sistema de Gestión de Empleados")
        self.root.geometry("600x400")

        self.empleado = Empleado(db)
        self.departamento = Departamento(db)
        self.proyecto = Proyecto(db)
        self.registro_tiempo = RegistroTiempo(db)

       
        self.crear_botonera()

    def crear_botonera(self):
        tk.Button(self.root, text="Crear Y Gestionar Departamento", command=self.ventana_gestion_departamento).pack(pady=10)
        tk.Button(self.root, text="Crear Usuario", command=self.ventana_crear_usuario).pack(pady=10)
        tk.Button(self.root, text="Registrar Empleado", command=self.ventana_registrar_empleado).pack(pady=10)
        tk.Button(self.root, text="Crear Proyecto", command=self.ventana_crear_proyecto).pack(pady=10)
        tk.Button(self.root, text="Registrar Tiempo", command=self.ventana_registrar_tiempo).pack(pady=10)
        tk.Button(self.root, text="Añadir Empleado a Proyecto", command=self.ventana_asignar_empleado_a_proyecto).pack(pady=10)
        tk.Button(self.root, text="Modificar Departamento", command=self.ventana_modificar_departamento).pack(pady=10)
        tk.Button(self.root, text="Eliminar Departamento", command=self.ventana_eliminar_departamento).pack(pady=10)
        tk.Button(self.root, text="Eliminar Proyecto", command=self.ventana_eliminar_proyecto).pack(pady=10)
        tk.Button(self.root, text="Modificar Proyecto", command=self.ventana_modificar_proyecto).pack(pady=10)

    def ventana_eliminar_proyecto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Eliminar Proyecto")

        tk.Label(ventana, text="ID Proyecto:").grid(row=0, column=0)
        id_proyecto = tk.Entry(ventana)
        id_proyecto.grid(row=0, column=1)

        def eliminar_proyecto():
            if id_proyecto.get():
                self.proyecto.eliminar_proyecto(id_proyecto.get())
                messagebox.showinfo("Info", "Proyecto eliminado correctamente")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Por favor ingrese un ID de proyecto.")

        tk.Button(ventana, text="Eliminar", command=eliminar_proyecto).grid(row=1, column=1)

    def ventana_modificar_proyecto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Modificar Proyecto")

        tk.Label(ventana, text="ID Proyecto:").grid(row=0, column=0)
        tk.Label(ventana, text="Nuevo Nombre:").grid(row=1, column=0)
        tk.Label(ventana, text="Nueva Descripción:").grid(row=2, column=0)

        id_proyecto = tk.Entry(ventana)
        nuevo_nombre = tk.Entry(ventana)
        nueva_descripcion = tk.Entry(ventana)

        id_proyecto.grid(row=0, column=1)
        nuevo_nombre.grid(row=1, column=1)
        nueva_descripcion.grid(row=2, column=1)

        def modificar_proyecto():
            if id_proyecto.get() and nuevo_nombre.get() and nueva_descripcion.get():
                self.proyecto.modificar_proyecto(id_proyecto.get(), nuevo_nombre.get(), nueva_descripcion.get())
                messagebox.showinfo("Info", "Proyecto modificado correctamente")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")

        tk.Button(ventana, text="Modificar", command=modificar_proyecto).grid(row=3, column=1)


    def ventana_eliminar_departamento(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Eliminar Departamento")
        
        tk.Label(ventana, text="ID Departamento:").grid(row=0, column=0)
        id_departamento = tk.Entry(ventana)
        id_departamento.grid(row=0, column=1)

        def eliminar_departamento():
            self.departamento.eliminar_departamento(id_departamento.get())
            messagebox.showinfo("Info", "Departamento eliminado correctamente")
            ventana.destroy()

        tk.Button(ventana, text="Eliminar", command=eliminar_departamento).grid(row=1, column=1)

    def ventana_modificar_departamento(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Modificar Departamento")
        
        tk.Label(ventana, text="ID Departamento:").grid(row=0, column=0)
        tk.Label(ventana, text="Nuevo Nombre:").grid(row=1, column=0)
        tk.Label(ventana, text="Nuevo Gerente:").grid(row=2, column=0)

        id_departamento = tk.Entry(ventana)
        nuevo_nombre = tk.Entry(ventana)
        nuevo_gerente = tk.Entry(ventana)

        id_departamento.grid(row=0, column=1)
        nuevo_nombre.grid(row=1, column=1)
        nuevo_gerente.grid(row=2, column=1)

        def modificar_departamento():
            self.departamento.modificar_departamento(id_departamento.get(), nuevo_nombre.get(), nuevo_gerente.get())
            messagebox.showinfo("Info", "Departamento modificado correctamente")
            ventana.destroy()

        tk.Button(ventana, text="Modificar", command=modificar_departamento).grid(row=3, column=1)


    def ventana_registrar_empleado(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Empleado")
        tk.Label(ventana, text="Nombre Usuario:").grid(row=0, column=0)
        tk.Label(ventana, text="Nombre:").grid(row=1, column=0)
        tk.Label(ventana, text="Apellido:").grid(row=2, column=0)
        tk.Label(ventana, text="Dirección:").grid(row=3, column=0)
        tk.Label(ventana, text="Teléfono:").grid(row=4, column=0)
        tk.Label(ventana, text="Email:").grid(row=5, column=0)
        tk.Label(ventana, text="Fecha inicio contrato (DD-MM-YYYY) ").grid(row=6, column=0)
        tk.Label(ventana, text="Sueldo:").grid(row=7, column=0)
        tk.Label(ventana, text="Proyecto:").grid(row=8, column=0)
        tk.Label(ventana, text="Departamento:").grid(row=9, column=0)
        tk.Label(ventana, text="ID Departamento:").grid(row=10, column=0)

        nombre_usuario = tk.Entry(ventana)
        nombre = tk.Entry(ventana)
        apellido = tk.Entry(ventana)
        direccion = tk.Entry(ventana)
        telefono = tk.Entry(ventana)
        email = tk.Entry(ventana)
        fecha_inicio = tk.Entry(ventana)
        sueldo = tk.Entry(ventana)
        proyecto = tk.Entry(ventana)
        departamento = tk.Entry(ventana)
        id_departamento = tk.Entry(ventana)

        nombre_usuario.grid(row=0, column=1)
        nombre.grid(row=1, column=1)
        apellido.grid(row=2, column=1)
        direccion.grid(row=3, column=1)
        telefono.grid(row=4, column=1)
        email.grid(row=5, column=1)
        fecha_inicio.grid(row=6, column=1)
        sueldo.grid(row=7, column=1)
        proyecto.grid(row=8, column=1)
        departamento.grid(row=9, column=1)
        id_departamento.grid(row=10, column=1)

        def registrar_empleado():
            self.empleado.registrar_empleado(
                nombre_usuario.get(), nombre.get(), apellido.get(),
                direccion.get(), telefono.get(), email.get(),
                fecha_inicio.get(), sueldo.get(), proyecto.get(),
                departamento.get(), id_departamento.get()
            )
            messagebox.showinfo("Info", "Empleado registrado correctamente")
            ventana.destroy()

        tk.Button(ventana, text="Registrar", command=registrar_empleado).grid(row=11, column=1)

    def ventana_crear_usuario(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Usuario")
        
        tk.Label(ventana, text="Nombre Usuario:").grid(row=0, column=0)
        tk.Label(ventana, text="Contraseña:").grid(row=1, column=0)

        nombre_usuario = tk.Entry(ventana)
        contrasena = tk.Entry(ventana, show='*')  

        nombre_usuario.grid(row=0, column=1)
        contrasena.grid(row=1, column=1)

        def crear_usuario():
            user = nombre_usuario.get()
            password = contrasena.get()
            
            if not user or not password:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            
            query = "INSERT INTO Usuario (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
            values = (user, password)
            self.db.execute_query(query, values)
            messagebox.showinfo("Info", "Usuario creado correctamente.")
            ventana.destroy()

        tk.Button(ventana, text="Crear", command=crear_usuario).grid(row=2, column=1)

    def ventana_gestion_departamento(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Gestionar Departamento")
        
        
        tk.Label(ventana, text="Nombre Departamento:").grid(row=0, column=0)
        tk.Label(ventana, text="Gerente:").grid(row=1, column=0)

        nombre_departamento = tk.Entry(ventana)
        gerente = tk.Entry(ventana)

        nombre_departamento.grid(row=0, column=1)
        gerente.grid(row=1, column=1)

        def crear_departamento():
            nombre = nombre_departamento.get()
            gerente_nombre = gerente.get()

            if not nombre or not gerente_nombre:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            self.departamento.crear_departamento(nombre, gerente_nombre)
            messagebox.showinfo("Info", "Departamento creado correctamente.")
            ventana.destroy()

        tk.Button(ventana, text="Crear", command=crear_departamento).grid(row=2, column=1)

        
        tk.Button(ventana, text="Mostrar Departamentos", command=self.departamento.mostrar_departamentos).grid(row=3, column=1)


    def ventana_crear_proyecto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Proyecto")
        tk.Label(ventana, text="Nombre Proyecto:").grid(row=0, column=0)
        tk.Label(ventana, text="Descripción:").grid(row=1, column=0)
        tk.Label(ventana, text="ID Empleado:").grid(row=2, column=0)

        nombre_proyecto = tk.Entry(ventana)
        descripcion = tk.Entry(ventana)
        id_empleado = tk.Entry(ventana)

        nombre_proyecto.grid(row=0, column=1)
        descripcion.grid(row=1, column=1)
        id_empleado.grid(row=2, column=1)

        def crear_proyecto():
            self.proyecto.crear_proyecto(
                nombre_proyecto.get(), descripcion.get(), id_empleado.get()
            )
            messagebox.showinfo("Info", "Proyecto creado correctamente")
            ventana.destroy()

        tk.Button(ventana, text="Crear", command=crear_proyecto).grid(row=3, column=1)

    def ventana_registrar_tiempo(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Tiempo")
        
        tk.Label(ventana, text="Nombre Usuario:").grid(row=0, column=0)
        tk.Label(ventana, text="ID Proyecto:").grid(row=1, column=0)
        tk.Label(ventana, text="Fecha (DD-MM-YYYY):").grid(row=2, column=0)
        tk.Label(ventana, text="Horas Trabajadas:").grid(row=3, column=0)
        tk.Label(ventana, text="Descripción:").grid(row=4, column=0)

        nombre_usuario = tk.Entry(ventana)
        id_proyecto = tk.Entry(ventana)
        fecha = tk.Entry(ventana)
        horas_trabajadas = tk.Entry(ventana)
        descripcion = tk.Entry(ventana)

        nombre_usuario.grid(row=0, column=1)
        id_proyecto.grid(row=1, column=1)
        fecha.grid(row=2, column=1)
        horas_trabajadas.grid(row=3, column=1)
        descripcion.grid(row=4, column=1)

        def registrar_tiempo():
            self.registro_tiempo.registrar_tiempo(
                nombre_usuario.get(), id_proyecto.get(), fecha.get(),
                horas_trabajadas.get(), descripcion.get()
            )
            messagebox.showinfo("Info", "Tiempo registrado correctamente")
            ventana.destroy()

        tk.Button(ventana, text="Registrar", command=registrar_tiempo).grid(row=5, column=1)
        

    def ventana_asignar_empleado_a_proyecto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Asignar Empleado a Proyecto")
        tk.Label(ventana, text="Nombre Usuario:").grid(row=0, column=0)
        tk.Label(ventana, text="ID Proyecto:").grid(row=1, column=0)

        nombre_usuario = tk.Entry(ventana)
        id_proyecto = tk.Entry(ventana)

        nombre_usuario.grid(row=0, column=1)
        id_proyecto.grid(row=1, column=1)

        def asignar_empleado():
                self.proyecto.asignar_empleado_a_proyecto(
                    nombre_usuario.get(), id_proyecto.get()
                )
                messagebox.showinfo("Info", "Empleado asignado al proyecto correctamente")
                ventana.destroy()

        tk.Button(ventana, text="Asignar", command=asignar_empleado).grid(row=2, column=1)

if __name__ == "__main__":
    db = Database()
    root = tk.Tk()
    app = MainApp(root, db)
    root.mainloop()
