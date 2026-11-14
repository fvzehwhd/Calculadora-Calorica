import sys
from PyQt5.QtWidgets import QApplication
from controller import AppController

def main():
    app = QApplication(sys.argv)
    
    # Instanciamos el controlador, que a su vez prepara el modelo y la vista
    controlador = AppController()
    controlador.iniciar()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()