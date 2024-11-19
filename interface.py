import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QLabel, QPushButton, QLineEdit, QProgressBar, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal

import multiprocessing
import time
import random #--- temp

from scrapper import scrape_books

class WorkerThread(QThread):

    def __init__(self, category):
        super().__init__()
        self.category = category

    # Señal para enviar el progreso actualizado a la GUI
    update_progress = pyqtSignal(int)
    update_text = pyqtSignal(str)
    
    def run(self):
        
        

        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=scrape_books,args=(q,self.category))
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

        self.setWindowTitle("Book Web Scrapper")

        self.layout = QVBoxLayout()

        self.layoutTop = QHBoxLayout()
        self.layoutShops = QHBoxLayout()
        self.layoutContent = QHBoxLayout()

        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()

        # Top Layout
        self.layoutTop.addWidget(QLabel('Book Scrapper           '))
        self.button = QPushButton('Search')
        self.button.clicked.connect(self.start_task)
        self.layoutTop.addWidget(self.button)
        
        self.LabelA = QLabel('A')
        self.layoutShops.addWidget(self.LabelA)
        self.progressBarAmazon = QProgressBar()
        self.layoutShops.addWidget(self.progressBarAmazon)
        self.LabelB = QLabel('              B')
        self.layoutShops.addWidget(self.LabelB)
        self.progressBarAliexpress = QProgressBar()
        self.layoutShops.addWidget(self.progressBarAliexpress)
        self.LabelC = QLabel('        C')
        self.layoutShops.addWidget(self.LabelC)
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

        booksCategorys = ['travel_2','mystery_3','historical-fiction_4','sequential-art_5','classics_6','philosophy_7','romance_8','womens-fiction_9','fiction_10','childrens_11','religion_12','nonfiction_13','music_14','default_15','science-fiction_16','sports-and-games_17','add-a-comment_18','fantasy_19','new-adult_20','young-adult_21','science_22','poetry_23','paranormal_24','art_25','psychology_26']
        chosenCategory1 = booksCategorys[random.randint(0, 24)]
        chosenCategory2 = booksCategorys[random.randint(0, 24)]
        chosenCategory3 = booksCategorys[random.randint(0, 24)]

        self.update_title_A(chosenCategory1)
        self.update_title_B(chosenCategory2)
        self.update_title_C(chosenCategory3)

        self.thread1 = WorkerThread(chosenCategory1)
        # Conectar las señales a métodos separados
        self.thread1.update_progress.connect(self.update_progress_amazon)
        self.thread1.update_text.connect(self.update_box_amazon)
        # Reactivar el botón cuando el hilo finalice
        self.thread1.finished.connect(lambda: self.button.setEnabled(True))

        self.thread2 = WorkerThread(chosenCategory2)
        # Conectar las señales a métodos separados
        self.thread2.update_progress.connect(self.update_progress_aliexpress)
        self.thread2.update_text.connect(self.update_box_aliexpress)

        self.thread3 = WorkerThread(chosenCategory3)
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

    def update_title_A(self, title):
        self.LabelA.setText(title)

    def update_progress_aliexpress(self, value):
        self.progressBarAliexpress.setValue(value)
    
    def update_box_aliexpress(self, message):
        self.productsBoxAliexpress.append(message)

    def update_title_B(self, title):
        self.LabelB.setText(title)

    def update_progress_mercado(self, value):
        self.progressBarMercado.setValue(value)
    
    def update_box_mercado(self, message):
        self.productsBoxMercado.append(message)

    def update_title_C(self, title):
        self.LabelC.setText(title)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
