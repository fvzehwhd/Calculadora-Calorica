from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QComboBox, 
                             QStackedWidget, QTableWidget, QTableWidgetItem, 
                             QTabWidget, QListWidget, QFormLayout, QHeaderView)
from PyQt5.QtCore import Qt

ESTILO_OSCURO_NEON = """
QWidget { background-color: #0f0f15; color: #ffffff; font-family: 'Segoe UI', Arial; font-size: 14px; }
QPushButton { background-color: #1a1a24; border: 2px solid #39ff14; border-radius: 5px; color: #39ff14; font-weight: bold; padding: 8px; }
QPushButton:hover { background-color: #39ff14; color: #0f0f15; }
QPushButton#btn_secundario { border: 2px solid #00ffff; color: #00ffff; }
QPushButton#btn_secundario:hover { background-color: #00ffff; color: #0f0f15; }
QPushButton#btn_peligro { border: 2px solid #ff0055; color: #ff0055; }
QPushButton#btn_peligro:hover { background-color: #ff0055; color: #0f0f15; }
QLineEdit, QComboBox { background-color: #1a1a24; border: 1px solid #00ffff; border-radius: 3px; color: #ffffff; padding: 5px; }
QTableWidget, QListWidget { background-color: #1a1a24; border: 1px solid #ff00ff; }
QHeaderView::section { background-color: #20202d; color: #00ffff; border: 1px solid #333333; font-weight:bold; }
QTabBar::tab { background: #1a1a24; border: 1px solid #ff00ff; padding: 8px; color: #ff00ff; }
QTabBar::tab:selected { background: #ff00ff; color: #0f0f15; font-weight: bold; }
QLabel#titulo { font-size: 22px; color: #00ffff; font-weight: bold; margin-bottom: 10px; }
QLabel#resumen { font-size: 18px; color: #39ff14; font-weight: bold; }
"""

class AppView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Fitness - NeoTrack")
        self.resize(550, 700) # Un poco más ancho para la tabla de historial
        self.setStyleSheet(ESTILO_OSCURO_NEON)
        
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        
        self.init_login_view()
        self.init_dashboard_view()
        self.init_food_ref_view()
        self.init_workout_view()
        self.init_setup_view()
        self.init_history_view() # <--- Nueva vista
        
        self.stacked.addWidget(self.view_login)      # Indice 0
        self.stacked.addWidget(self.view_dashboard)  # Indice 1
        self.stacked.addWidget(self.view_food_ref)   # Indice 2
        self.stacked.addWidget(self.view_workout)    # Indice 3
        self.stacked.addWidget(self.view_setup)      # Indice 4
        self.stacked.addWidget(self.view_historial)  # Indice 5

    def init_login_view(self):
        self.view_login = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        lbl_titulo = QLabel("INICIO DE SESIÓN")
        lbl_titulo.setObjectName("titulo")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Nombre de usuario")
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Contraseña")
        self.input_pass.setEchoMode(QLineEdit.Password)
        
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_registro_nav = QPushButton("Registrar Nuevo Perfil")
        self.btn_registro_nav.setObjectName("btn_secundario")
        
        layout.addWidget(lbl_titulo)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_pass)
        layout.addSpacing(10)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_registro_nav)
        self.view_login.setLayout(layout)

    def init_setup_view(self):
        self.view_setup = QWidget()
        layout = QVBoxLayout()
        lbl_titulo = QLabel("Configuración de Perfil Físico")
        lbl_titulo.setObjectName("titulo")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        
        form_layout = QFormLayout()
        self.reg_usuario = QLineEdit()
        self.reg_pass = QLineEdit()
        self.reg_pass.setEchoMode(QLineEdit.Password)
        self.reg_obj = QComboBox()
        self.reg_obj.addItems(["Déficit Calórico", "Ganancia Muscular"])
        self.reg_sexo = QComboBox()
        self.reg_sexo.addItems(["Hombre", "Mujer"])
        self.reg_edad = QLineEdit()
        self.reg_edad.setPlaceholderText("Ej. 45")
        self.reg_altura = QLineEdit()
        self.reg_altura.setPlaceholderText("Centímetros (Ej. 180)")
        self.reg_peso = QLineEdit()
        self.reg_peso.setPlaceholderText("Kilogramos (Ej. 94)")
        self.reg_dias = QLineEdit()
        self.reg_dias.setPlaceholderText("Días (0 si no entrenas)")
        
        form_layout.addRow("Usuario:", self.reg_usuario)
        form_layout.addRow("Contraseña:", self.reg_pass)
        form_layout.addRow("Tu Objetivo:", self.reg_obj)
        form_layout.addRow("Sexo biológico:", self.reg_sexo)
        form_layout.addRow("Edad (años):", self.reg_edad)
        form_layout.addRow("Altura (cm):", self.reg_altura)
        form_layout.addRow("Peso (kg):", self.reg_peso)
        form_layout.addRow("Días de entreno/semana:", self.reg_dias)
        
        self.btn_guardar_registro = QPushButton("Calcular Meta y Finalizar")
        self.btn_cancelar_registro = QPushButton("Cancelar")
        self.btn_cancelar_registro.setObjectName("btn_secundario")
        
        layout.addWidget(lbl_titulo)
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addWidget(self.btn_guardar_registro)
        layout.addWidget(self.btn_cancelar_registro)
        self.view_setup.setLayout(layout)

    def init_dashboard_view(self):
        self.view_dashboard = QWidget()
        layout = QVBoxLayout()
        
        self.lbl_bienvenida = QLabel("Panel Principal")
        self.lbl_bienvenida.setObjectName("titulo")
        self.lbl_meta = QLabel("Meta Diaria: 0 kcal")
        self.lbl_consumido = QLabel("Consumido Hoy: 0 kcal")
        self.lbl_consumido.setObjectName("resumen")
        
        layout.addWidget(self.lbl_bienvenida)
        layout.addWidget(self.lbl_meta)
        layout.addWidget(self.lbl_consumido)
        
        form_layout = QFormLayout()
        self.combo_comida = QComboBox()
        self.combo_comida.addItems(["desayuno", "almuerzo", "cena"])
        self.input_calorias = QLineEdit()
        self.input_calorias.setPlaceholderText("Ej. 350")
        
        self.btn_agregar_comida = QPushButton("Añadir Calorías")
        
        form_layout.addRow("Momento del día:", self.combo_comida)
        form_layout.addRow("Calorías a sumar:", self.input_calorias)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_agregar_comida)
        layout.addSpacing(20)
        
        # Nuevos botones del Dashboard
        self.btn_ver_historial = QPushButton("Ver Historial Semanal/Mensual") # <--- NUEVO BOTÓN
        self.btn_ver_historial.setObjectName("btn_secundario")
        
        self.btn_ver_alimentos = QPushButton("Ver Calorías de Comidas Básicas")
        self.btn_ver_alimentos.setObjectName("btn_secundario")
        
        self.btn_ver_rutinas = QPushButton("Ver Rutinas de Entrenamiento")
        self.btn_ver_rutinas.setObjectName("btn_secundario")
        
        self.btn_cerrar_sesion = QPushButton("Cerrar Sesión")
        self.btn_cerrar_sesion.setObjectName("btn_peligro")
        
        layout.addWidget(self.btn_ver_historial)
        layout.addWidget(self.btn_ver_alimentos)
        layout.addWidget(self.btn_ver_rutinas)
        layout.addWidget(self.btn_cerrar_sesion)
        
        self.view_dashboard.setLayout(layout)

    def init_food_ref_view(self):
        self.view_food_ref = QWidget()
        layout = QVBoxLayout()
        lbl_titulo = QLabel("Calorías de Comidas Básicas")
        lbl_titulo.setObjectName("titulo")
        self.tabla_alimentos = QTableWidget(0, 2)
        self.tabla_alimentos.setHorizontalHeaderLabels(["Alimento", "Calorías"])
        self.tabla_alimentos.horizontalHeader().setStretchLastSection(True)
        self.btn_volver_food = QPushButton("Volver al Panel")
        layout.addWidget(lbl_titulo)
        layout.addWidget(self.tabla_alimentos)
        layout.addWidget(self.btn_volver_food)
        self.view_food_ref.setLayout(layout)

    def init_workout_view(self):
        self.view_workout = QWidget()
        layout = QVBoxLayout()
        lbl_titulo = QLabel("Recomendaciones de Entrenamiento")
        lbl_titulo.setObjectName("titulo")
        
        self.tabs = QTabWidget()
        self.tab_masa = QWidget()
        self.tab_grasa = QWidget()
        self.lista_masa = QListWidget()
        layout_masa = QVBoxLayout()
        layout_masa.addWidget(self.lista_masa)
        self.tab_masa.setLayout(layout_masa)
        self.lista_grasa = QListWidget()
        layout_grasa = QVBoxLayout()
        layout_grasa.addWidget(self.lista_grasa)
        self.tab_grasa.setLayout(layout_grasa)
        self.tabs.addTab(self.tab_masa, "Aumento Muscular")
        self.tabs.addTab(self.tab_grasa, "Reducción de Grasa")
        
        self.btn_volver_workout = QPushButton("Volver al Panel")
        layout.addWidget(lbl_titulo)
        layout.addWidget(self.tabs)
        layout.addWidget(self.btn_volver_workout)
        self.view_workout.setLayout(layout)

    # -------- NUEVA VENTANA DE HISTORIAL --------
    def init_history_view(self):
        self.view_historial = QWidget()
        layout = QVBoxLayout()
        
        lbl_titulo = QLabel("Historial de Consumo Calórico")
        lbl_titulo.setObjectName("titulo")
        
        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Mostrar:"))
        self.combo_filtro_historial = QComboBox()
        self.combo_filtro_historial.addItems(["Últimos 7 días (Semanal)", "Últimos 30 días (Mensual)", "Todo el histórico"])
        filtro_layout.addWidget(self.combo_filtro_historial)
        
        # Tabla de 5 columnas
        self.tabla_historial = QTableWidget(0, 5)
        self.tabla_historial.setHorizontalHeaderLabels(["Fecha", "Desayuno", "Almuerzo", "Cena", "Total"])
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.btn_volver_historial = QPushButton("Volver al Panel")
        
        layout.addWidget(lbl_titulo)
        layout.addLayout(filtro_layout)
        layout.addWidget(self.tabla_historial)
        layout.addWidget(self.btn_volver_historial)
        self.view_historial.setLayout(layout)
    # ---------------------------------------------