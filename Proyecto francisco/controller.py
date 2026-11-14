from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from model import CaloriasModel
from view import AppView

class AppController:
    def __init__(self):
        self.model = CaloriasModel()
        self.view = AppView()
        self.datos_json = self.model.cargar_datos_estaticos()
        
        self.conectar_senales()
        self.cargar_interfaz_estatica()

    def iniciar(self):
        self.view.show()

    def conectar_senales(self):
        # Login y Configuración
        self.view.btn_login.clicked.connect(self.login)
        self.view.btn_registro_nav.clicked.connect(lambda: self.view.stacked.setCurrentIndex(4))
        self.view.btn_cancelar_registro.clicked.connect(lambda: self.view.stacked.setCurrentIndex(0))
        self.view.btn_guardar_registro.clicked.connect(self.procesar_registro_fisico)
        
        # Dashboard
        self.view.btn_agregar_comida.clicked.connect(self.agregar_comida)
        self.view.btn_cerrar_sesion.clicked.connect(lambda: self.view.stacked.setCurrentIndex(0))
        
        # Navegación hacia otras vistas
        self.view.btn_ver_alimentos.clicked.connect(lambda: self.view.stacked.setCurrentIndex(2))
        self.view.btn_ver_rutinas.clicked.connect(self.abrir_rutinas)
        self.view.btn_ver_historial.clicked.connect(self.abrir_historial) # <-- Abre el historial
        
        # Evento cuando el usuario cambia el filtro semanal/mensual
        self.view.combo_filtro_historial.currentIndexChanged.connect(self.cargar_datos_historial)
        
        # Botones para volver al Dashboard
        self.view.btn_volver_food.clicked.connect(lambda: self.view.stacked.setCurrentIndex(1))
        self.view.btn_volver_workout.clicked.connect(lambda: self.view.stacked.setCurrentIndex(1))
        self.view.btn_volver_historial.clicked.connect(lambda: self.view.stacked.setCurrentIndex(1))

    # -------- FUNCIONES DEL HISTORIAL --------
    def abrir_historial(self):
        # Selecciona por defecto los últimos 7 días y carga la tabla
        self.view.combo_filtro_historial.setCurrentIndex(0) 
        self.cargar_datos_historial()
        self.view.stacked.setCurrentIndex(5)

    def cargar_datos_historial(self):
        # Determinar cuántos días extraer según el ComboBox
        idx = self.view.combo_filtro_historial.currentIndex()
        if idx == 0:
            dias = 7
        elif idx == 1:
            dias = 30
        else:
            dias = 9999 # Todo el histórico

        registros = self.model.obtener_historial(dias)
        
        # Llenar la tabla
        self.view.tabla_historial.setRowCount(len(registros))
        for row, reg in enumerate(registros):
            fecha, des, alm, cen = reg
            total = des + alm + cen
            self.view.tabla_historial.setItem(row, 0, QTableWidgetItem(str(fecha)))
            self.view.tabla_historial.setItem(row, 1, QTableWidgetItem(f"{des}"))
            self.view.tabla_historial.setItem(row, 2, QTableWidgetItem(f"{alm}"))
            self.view.tabla_historial.setItem(row, 3, QTableWidgetItem(f"{cen}"))
            self.view.tabla_historial.setItem(row, 4, QTableWidgetItem(f"{total} kcal"))
    # -----------------------------------------

    def procesar_registro_fisico(self):
        usr = self.view.reg_usuario.text().strip()
        pwd = self.view.reg_pass.text().strip()
        obj = self.view.reg_obj.currentText()
        sexo = self.view.reg_sexo.currentText()
        
        if not usr or not pwd:
            QMessageBox.warning(self.view, "Error", "El usuario y contraseña son obligatorios.")
            return

        try:
            edad = int(self.view.reg_edad.text().strip())
            altura = float(self.view.reg_altura.text().strip())
            peso = float(self.view.reg_peso.text().strip())
            dias = int(self.view.reg_dias.text().strip())
        except ValueError:
            QMessageBox.warning(self.view, "Error", "La Edad, Altura, Peso y Días deben ser valores numéricos.")
            return
            
        exito = self.model.registrar_usuario(usr, pwd, obj, peso, altura, edad, sexo, dias)
        
        if exito:
            QMessageBox.information(self.view, "Éxito", "Perfil y meta calórica calculados. Ya puedes iniciar sesión.")
            self.view.reg_usuario.clear()
            self.view.reg_pass.clear()
            self.view.reg_edad.clear()
            self.view.reg_altura.clear()
            self.view.reg_peso.clear()
            self.view.reg_dias.clear()
            self.view.stacked.setCurrentIndex(0)
        else:
            QMessageBox.warning(self.view, "Error", "El nombre de usuario ya existe.")

    def login(self):
        usr = self.view.input_usuario.text().strip()
        pwd = self.view.input_pass.text().strip()
        if self.model.login(usr, pwd):
            self.actualizar_dashboard()
            self.view.stacked.setCurrentIndex(1)
            self.view.input_usuario.clear()
            self.view.input_pass.clear()
        else:
            QMessageBox.warning(self.view, "Error", "Credenciales incorrectas.")

    def actualizar_dashboard(self):
        usr_data = self.model.usuario_actual
        self.view.lbl_bienvenida.setText(f"Hola, {usr_data['usuario']} | Objetivo: {usr_data['objetivo']}")
        
        meta = self.model.calcular_meta_calorias()
        self.view.lbl_meta.setText(f"Meta Diaria Calculada: {meta} kcal")
        
        desayuno, almuerzo, cena = self.model.obtener_registro_hoy()
        total = desayuno + almuerzo + cena
        self.view.lbl_consumido.setText(f"Consumido Hoy: {total} kcal\n(D: {desayuno} | A: {almuerzo} | C: {cena})")

    def agregar_comida(self):
        comida = self.view.combo_comida.currentText()
        calorias_txt = self.view.input_calorias.text().strip()
        if not calorias_txt.isdigit():
            QMessageBox.warning(self.view, "Error", "Ingresa un número válido de calorías.")
            return
        
        self.model.agregar_calorias(comida, int(calorias_txt))
        self.view.input_calorias.clear()
        self.actualizar_dashboard()
        QMessageBox.information(self.view, "Agregado", f"Se sumaron {calorias_txt} kcal al {comida}.")

    def cargar_interfaz_estatica(self):
        alimentos = self.datos_json["alimentos"]
        self.view.tabla_alimentos.setRowCount(len(alimentos))
        for row, item in enumerate(alimentos):
            self.view.tabla_alimentos.setItem(row, 0, QTableWidgetItem(item["nombre"]))
            self.view.tabla_alimentos.setItem(row, 1, QTableWidgetItem(str(item["calorias"])))
            
        rutinas = self.datos_json["rutinas"]
        self.view.lista_masa.addItems(rutinas["aumento_muscular"])
        self.view.lista_grasa.addItems(rutinas["reduccion_grasa"])

    def abrir_rutinas(self):
        if self.model.usuario_actual['objetivo'] == 'Déficit Calórico':
            self.view.tabs.setCurrentIndex(1)
        else:
            self.view.tabs.setCurrentIndex(0)
        self.view.stacked.setCurrentIndex(3)