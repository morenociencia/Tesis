#Tomar la función de distancia de cada variable
#Generar la particion, valores de x (a => b).
#Como todos los vectores comienzan en cero, el modulo de los mismos, es 
#reemplazando los valores de partición en la función base.
#Se saca media, no es más que el vector dividido a la mitad.
#Se elige un punto z extremo de 3.45 por default para calcular las desviaciones.



#Importando modulos
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from funciones import *
import decimal as dc



class Particionado():



    #El constructor, variables de la instancia
    def __init__(self, particion):
        

        self.__particion = dc.Decimal(str(particion))

        #punto de corte con el eje x b
        self.b = np.add(dc.Decimal(coordenadas[2]), -self.__particion)

        #punto de inicio
        self.inicio = np.add(dc.Decimal(coordenadas[0]), self.__particion)


        self.particionBase = np.arange(self.inicio, np.add(self.b, self.__particion), self.__particion)

        
        #generando vectores modulo
        self.vectoresModuloLog = np.array(np.add(funcionVectorizadaLog(self.particionBase), - funcionVectorizadaLin(self.particionBase)))

        self.vectoresModuloExp = np.array(np.add(funcionVectorizadaLin(self.particionBase), - funcionVectorizadaExp(self.particionBase)))

        self.vectoresModuloExp1 = np.array(np.add(funcionVectorizadaExp(self.particionBase), - funcionVectorizadaLin(self.particionBase)))



        #listas para la función log
        self.__mediasLog = []

        self.__desviacionesLog = []

        #listas para la funcion exp
        self.__mediasExp = []

        self.__desviacionesExp = []


        self.z = dc.Decimal('3.45')



    def generador(self):

        """Ayuda a calcular las desviaciones y las medias."""
        for i in range(len(self.particionBase)):
    
             self.__mediasLog.append( np.divide((self.vectoresModuloLog[i]), dc.Decimal('2')))

             self.__mediasExp.append( np.divide((self.vectoresModuloExp[i]), dc.Decimal('2')))


        for i in range(len(self.particionBase)):

            self.__desviacionesLog.append(np.divide((self.__mediasLog[i]), self.z))

            self.__desviacionesExp.append(np.divide((self.__mediasExp[i]), self.z))


    def dataFrame(self):

        """Guarda en un dataframe información de cada función, como el particionado general,
        el tamaño de los vectores, las medias y las desviaciones."""
        df = pd.DataFrame(data = {
        "Particion (x)" : self.particionBase,
        "Vectores log (y)"  : self.vectoresModuloLog,
        "Media log"         : self.__mediasLog, 
        "Desviación log"    : self.__desviacionesLog,
        "Vectores Exp(y)"   : self.vectoresModuloExp,
        "Media Exp"         : self.__mediasExp, 
        "Desviación Exp"    : self.__desviacionesExp } )

        return df


    def grafica(self):

        """genera una gráfica de los vectores modulos, pueder verse como una
        comprobación geométrica de que la función log es más grande que exp."""

        plt.grid()
        
        plt.title("Vectores Modulo", fontsize=15)
        plt.xlabel("Clase t", fontsize=12)
        plt.ylabel("Magnitud del vector", fontsize=12)

        plt.plot(self.particionBase, self.vectoresModuloLog, label='ln(x) + t', color="#E67E22")
        plt.plot(self.particionBase, self.vectoresModuloExp, label='e^x - t', color="#3498DB")
        plt.plot(self.particionBase, self.vectoresModuloExp1, "--", color="#3498DB")

        plt.legend()

        plt.show()



#objeto = Particionado(0.001)

#objeto.generador()

#objeto.grafica()