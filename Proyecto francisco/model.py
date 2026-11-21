import sqlite3
import json
import os
from datetime import date

class CaloriasModel:
    def __init__(self):
        self.conn = sqlite3.connect('app_data.db')
        self.crear_tablas()
        self.usuario_actual = None

    def crear_tablas(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                          (id INTEGER PRIMARY KEY, usuario TEXT, password TEXT, objetivo TEXT,
                           peso REAL, altura REAL, edad INTEGER, sexo TEXT, dias_entrenamiento INTEGER,
                           meta_calorias INTEGER)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS registros
                          (id INTEGER PRIMARY KEY, usuario_id INTEGER, fecha TEXT,
                           desayuno INTEGER, almuerzo INTEGER, cena INTEGER)''')
        self.conn.commit()

    def registrar_usuario(self, usuario, password, objetivo, peso, altura, edad, sexo, dias):
        if sexo == 'Hombre':
            tmb = (10 * peso) + (4.5 * altura) - (5 * edad) + 5
        else:
            tmb = (10 * peso) + (4.5 * altura) - (5 * edad) - 161

        if dias == 0:
            factor_actividad = 1.0
        elif 1 <= dias <= 2:
            factor_actividad = 1.2
        elif 3 <= dias <= 5:
            factor_actividad = 1.55
        else:
            factor_actividad = 1.725

        tdee = tmb * factor_actividad 

        if objetivo == 'Déficit Calórico':
            meta_calorias = int(tdee - 500)
        else:
            meta_calorias = int(tdee + 300)

        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario=?", (usuario,))
        if cursor.fetchone():
            return False 
            
        cursor.execute('''INSERT INTO usuarios 
                          (usuario, password, objetivo, peso, altura, edad, sexo, dias_entrenamiento, meta_calorias) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (usuario, password, objetivo, peso, altura, edad, sexo, dias, meta_calorias))
        self.conn.commit()
        return True

    def login(self, usuario, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, objetivo, meta_calorias FROM usuarios WHERE usuario=? AND password=?", (usuario, password))
        user = cursor.fetchone()
        if user:
            self.usuario_actual = {'id': user[0], 'usuario': usuario, 'objetivo': user[1], 'meta': user[2]}
            return True
        return False

    def obtener_registro_hoy(self):
        hoy = str(date.today())
        cursor = self.conn.cursor()
        cursor.execute("SELECT desayuno, almuerzo, cena FROM registros WHERE usuario_id=? AND fecha=?",
                       (self.usuario_actual['id'], hoy))
        reg = cursor.fetchone()
        if reg:
            return reg
        else:
            cursor.execute("INSERT INTO registros (usuario_id, fecha, desayuno, almuerzo, cena) VALUES (?, ?, 0, 0, 0)",
                           (self.usuario_actual['id'], hoy))
            self.conn.commit()
            return (0, 0, 0)

    def agregar_calorias(self, comida, calorias):
        hoy = str(date.today())
        cursor = self.conn.cursor()
        query = f"UPDATE registros SET {comida} = {comida} + ? WHERE usuario_id=? AND fecha=?"
        cursor.execute(query, (calorias, self.usuario_actual['id'], hoy))
        self.conn.commit()

    def calcular_meta_calorias(self):
        return self.usuario_actual['meta']

    def cargar_datos_estaticos(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.join(base_dir, 'datos.json'))

        with open('datos.json', 'r', encoding='utf-8') as f:
                    return json.load(f)

    # --- NUEVA FUNCIÓN PARA EL HISTORIAL ---
    def obtener_historial(self, limite_dias):
        cursor = self.conn.cursor()
        # Buscamos en SQLite los registros usando modificadores de fecha ('-7 days', '-30 days', etc)
        modificador = f'-{limite_dias} days'
        query = '''SELECT fecha, desayuno, almuerzo, cena 
                   FROM registros 
                   WHERE usuario_id=? AND fecha >= date('now', ?) 
                   ORDER BY fecha DESC'''
        cursor.execute(query, (self.usuario_actual['id'], modificador))
        return cursor.fetchall()