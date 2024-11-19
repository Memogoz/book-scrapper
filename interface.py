import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QLabel, QPushButton, QLineEdit, QProgressBar, QTextEdit
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QThread, pyqtSignal

import multiprocessing
import time
import random #--- temp

from scrapper import scrape_books

class WorkerThread(QThread):


    # Señal para enviar el progreso actualizado a la GUI
    update_progress = pyqtSignal(int)
    update_text = pyqtSignal(str)
    
    def run(self):
        '''
        sampleText = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras congue mattis lorem, sed tincidunt nunc pharetra et. Curabitur non laoreet ante. Integer at tempus magna. Nunc vel fringilla nisi. Sed ut lacinia velit. Sed massa tortor, condimentum in tempus sit amet, elementum sit amet dolor. Nullam ac purus egestas, gravida quam vel, fermentum velit. Morbi nisl libero, dapibus a sem quis, molestie varius lacus. Nam egestas dapibus urna ac aliquam. Sed faucibus vulputate dolor, ac eleifend urna ultrices eget. Vivamus in dolor ut mi feugiat finibus vitae vitae urna. Aliquam sapien velit, dignissim non eros id, finibus egestas purus. Sed. a v f r d a ae'
        textList = sampleText.split()

        # Simulamos una tarea de larga duración
        for i in range(101):  # De 0 a 100 para el progreso de la barra
            time.sleep(0.1*random.randint(1, 3))  # Simula que está trabajando
            # Emite una señal con el valor de progreso para actualizar la GUI
            self.update_progress.emit(i)
            self.update_text.emit(textList[i])  # Envía una porción del texto
        '''

        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=scrape_books,args=(q,))
        p.start()

        rsp = ''
        totalProducts = 0
        prodCount = 1

        while rsp != None:
            time.sleep(0.3*random.randint(1, 5))
            rsp = q.get()

            if type(rsp) == type(1):
                totalProducts = rsp
                continue
            

            self.update_progress.emit((prodCount*100)//totalProducts)
            self.update_text.emit(rsp)

            prodCount += 1
            

        print('terminado')
        p.join()






class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Shopping Web Scrapper")

        self.layout = QVBoxLayout()

        self.layoutTop = QHBoxLayout()
        self.layoutShops = QHBoxLayout()
        self.layoutContent = QHBoxLayout()

        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()

        # Top Layout
        self.layoutTop.addWidget(QLabel('Scrapper           '))
        self.layoutTop.addWidget(QLabel('Producto : '))
        self.inputLine = QLineEdit()
        self.layoutTop.addWidget(self.inputLine)
        self.button = QPushButton('Buscar')
        self.button.clicked.connect(self.start_task)
        self.layoutTop.addWidget(self.button)

        self.layoutShops.addWidget(QLabel('Amazon'))
        self.progressBarAmazon = QProgressBar()
        self.layoutShops.addWidget(self.progressBarAmazon)
        self.layoutShops.addWidget(QLabel('              Aliexpress'))
        self.progressBarAliexpress = QProgressBar()
        self.layoutShops.addWidget(self.progressBarAliexpress)
        self.layoutShops.addWidget(QLabel('        Mercado Libre'))
        self.progressBarMercado = QProgressBar()
        self.layoutShops.addWidget(self.progressBarMercado)

        self.productsBoxAmazon = QTextEdit()
        self.productsBoxAmazon.setReadOnly(True)  # Evitar que el usuario edite el texto
        self.layout1.addWidget(self.productsBoxAmazon)

        self.productsBoxAliexpress = QTextEdit()
        self.productsBoxAliexpress.setReadOnly(True)  
        self.layout2.addWidget(self.productsBoxAliexpress)

        self.productsBoxMercado = QTextEdit()
        self.productsBoxMercado.setReadOnly(True)  
        self.layout3.addWidget(self.productsBoxMercado)

        self.layoutContent.addLayout(self.layout1)
        self.layoutContent.addLayout(self.layout2)
        self.layoutContent.addLayout(self.layout3)

        self.layout.addLayout(self.layoutTop)
        self.layout.addLayout(self.layoutShops)
        self.layout.addLayout(self.layoutContent)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
    


    def start_task(self):
        self.button.setEnabled(False)

        self.thread1 = WorkerThread()
        # Conectar las señales a métodos separados
        self.thread1.update_progress.connect(self.update_progress_amazon)
        self.thread1.update_text.connect(self.update_box_amazon)
        # Reactivar el botón cuando el hilo finalice
        self.thread1.finished.connect(lambda: self.button.setEnabled(True))

        self.thread2 = WorkerThread()
        # Conectar las señales a métodos separados
        self.thread2.update_progress.connect(self.update_progress_aliexpress)
        self.thread2.update_text.connect(self.update_box_aliexpress)

        self.thread3 = WorkerThread()
        # Conectar las señales a métodos separados
        self.thread3.update_progress.connect(self.update_progress_mercado)
        self.thread3.update_text.connect(self.update_box_mercado)


        # Iniciar los hilos
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
    


    def update_progress_amazon(self, value):
        self.progressBarAmazon.setValue(value)
    
    def update_box_amazon(self, message):
        self.productsBoxAmazon.append(message)

    def update_progress_aliexpress(self, value):
        self.progressBarAliexpress.setValue(value)
    
    def update_box_aliexpress(self, message):
        self.productsBoxAliexpress.append(message)

    def update_progress_mercado(self, value):
        self.progressBarMercado.setValue(value)
    
    def update_box_mercado(self, message):
        self.productsBoxMercado.append(message)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
