#importando modulos
import matplotlib.pyplot as plt
from numpy import arange
from secrets import choice
from funciones import alturaProbabilidad, funcionNormal, funcionNormalBiModal
from decimal import Decimal, getcontext



class MonteCarlo():


    def __init__(self, particion, iteraciones):
        
        """Existen tres grupos de variables generales,
        las mismas están organizadas de NO encapsuladas a encapsuladas."""

        """Variables de Ingreso"""
        #self.distancia1 = Decimal('3.45')
        self.distancia0 = -Decimal('3.45')
        self.iteraciones = iteraciones
        self.__particion = Decimal(str(particion))

        """Variables Estadísticas y Numéricas"""
        #Desviación
        self.sd = Decimal('1')
        #Media
        self.m = Decimal('0')
        #Ajuste de altura
        self.adj_h = Decimal('1')
        #altura rectangulo
        self.__h = Decimal('0.5')

        self.__limites_de_Probabilidad = None

        self.__verificadora = Decimal('0')



        """Variables de Matrices y Listas"""
        self.listaIndex = []

        self.__matrizX = None
        self.__matrizY = None

        self.__matriz_de_Coordenadas = []

        self.__listaX_on = []
        self.__listaY_on = []

        self.__listaX_out = []
        self.__listaY_out = []


        """Variables adicionales para usar una distribución bimodal"""
        #Desviación 1
        self.sd1 = Decimal('1')
        #Media 1
        self.m1 = Decimal('6.9')
        self.distancia1 = Decimal('10.35')


    #Limpiador de Variables de Matrices y Listas
    def __set_matriz_de_coordenadas(self):

        """Modifica la matriz_de_coordenadas a su valor por defecto."""
        self.__matriz_de_Coordenadas = []

    def __set_listas_on(self):

        """Modifica las listas que almacenan las coordenadas de 
        los valores al azar adentro de una distribución de probabilidad,
        a su valor por defecto."""
        self.__listaX_on = []
        self.__listaY_on = []

    def __set_listas_out(self):


        """Modifica las listas que almacenan las coordenadas de 
        los valores al azar que están FUERA de una distribución de probabilidad,
        a su valor por defecto."""
        self.__listaX_out = []
        self.__listaY_out = []

    def __set_matriz_x_y(self):

        """Modifica las matrices que almacenan la partición regular del
        eje de ordenadas y abscisas a su valor por defecto."""
        self.__matrizX = None
        self.__matrizY = None

    def __set_verificadora(self):

        self.__verificadora = Decimal('0')


    def get_matriz_de_coordenadas(self):

        return self.__matriz_de_Coordenadas


    def toString(self, x):

        """Muestra el estado del objeto en un momento determinado."""
        
        if x==1 or x==0:
            
            """Devuelve el estado del primer grupo de variables."""
            #Variables de Ingreso
            print("\nSu partición regular es: " + str(self.__particion))
            print("Su distancia de inicio es: " + str(self.distancia0))
            print("Su ditancia final es:  " + str(self.distancia1))
            print("La cantidad de iteraciones es: " + str(self.iteraciones))


        if x==2 or x==0:

            """Devuelve el estado del segundo grupo de variables."""
            #Variables Estadísticas y Numéricas
            print("\nSu desviación estándar es: " + str(self.sd))
            print("Su media es: " + str(self.m))
            print("El ajuste de altura es: " + str(self.adj_h))
            print("La altura de su rectangulo es: " + str(self.__h))

            print("Sus límites de probabilidad son: " + str(self.__limites_de_Probabilidad))

            print("La variable verificadora es: " + str(self.__verificadora))


        if x==3 or x==0:

            """Devuelve el estado del tercer grupo de variables."""
            #Variables de Matrices y Listas
            print("\nla lista index es: " + str(self.listaIndex))

            print("Su matriz X es: " + str(self.__matrizX))
            print("Su matriz Y es: " + str(self.__matrizY))

            print("Su matriz de coordenadas es: " + str(self.__matriz_de_Coordenadas))

            print("Su lista Xon es: " + str(self.__listaX_on))
            print("Su lista Yon es: " + str(self.__listaY_on))

            print("Su lista Xout es: " + str(self.__listaX_out))
            print("Su lista Yout es: " + str(self.__listaY_out))


        if x!=0 and x!=1 and x!=2 and x!=3:

            """En caso de que los valores ingresados no correspondan a ninguna
            opción, se le recuerda al usuario las opciones."""
            print("Recuerde las siguientes opciones:")
            print("Escriba 1 para visualizar el primer grupo de variables.")
            print("Escriba 2 para visualizar el segundo grupo de variables.")
            print("Escriba 3 para visualizar el tercer grupo de variables.")
            print("Escriba 0 para visualizar todos los grupos de variables.")


    #Creando métodos
    #Generar función de probabilidad
    #Se usa la distribución normal con la ecuación de Gauss


    def __funcion0(self):
        
        #self.__h = alturaProbabilidad(self.sd)
        self.__h = alturaProbabilidad(self.sd1)


    def __funcion(self, x):

        #self.__limites_de_Probabilidad = funcionNormal(x, self.m, self.sd)
        
        self.__limites_de_Probabilidad = funcionNormalBiModal(x, self.m, self.m1, self.sd, self.sd1)



    #Creando matriz de coordenadas
    def __matrizCoordenadas(self):

        """Guarda todos los puntos como coordenadas o vectores que se encuentran 
        adentro de la distribución de probabilidad en un matriz."""
        for i in range(len(self.__listaX_on)):

            self.__matriz_de_Coordenadas.append([self.__listaX_on[i],self.__listaY_on[i]])



    #Evaluador de repeticiones
    def __repeticiones(self):

        """verifica que no existan coordenadas repetidas."""
        #Comparando los valores para ver si hay repetidos
        for i in range(len(self.__matriz_de_Coordenadas)):

            for l in range(1+i,len(self.__matriz_de_Coordenadas)):

                if self.__matriz_de_Coordenadas[i] == self.__matriz_de_Coordenadas[l]:

                    #print("Hay igual")
                    #print("Indice: " + str(i))
                    #print("Indice: " + str(l))

                    self.listaIndex.append(l)
                    self.__verificadora += 1

        if self.listaIndex == []:

            self.__set_verificadora()



    def calcular(self):

        # self.__set_tipo_media()

        self.__set_matriz_de_coordenadas()

        self.__set_listas_on()

        self.__set_listas_out()

        self.__set_matriz_x_y()

        #self.toString(0)


        self.__funcion0()
    

        #arange genera valores más precisos que linspace
        self.__matrizX = arange(self.distancia0, self.distancia1, self.__particion)
        self.__matrizY = arange(Decimal('0'), ((self.__h + self.__particion ) * self.adj_h ), self.__particion)


        for i in range(self.iteraciones):

            #Se deben generar dos cifras aleatorias para tener una coordenada
            coordenadaX = choice(self.__matrizX)
            coordenadaY = choice(self.__matrizY)
            
            #Se debe evaluar la coordenada x en la función de probabilidad.
            #Recordar que los valores devueltos por la función son los limites.
            self.__funcion(coordenadaX)
            
            #Estableciendo si los valores están dentro o fuera de la distribución
            #Los límites de "x" no importan, porque en un inicio son de menos infinito
            #hasta infinito, por eso se evalua y.
            if self.__limites_de_Probabilidad >= coordenadaY : 

                self.__listaX_on.append(coordenadaX)
                self.__listaY_on.append(coordenadaY)

            else:

                self.__listaX_out.append(coordenadaX)
                self.__listaY_out.append(coordenadaY)


        self.__matrizCoordenadas()


        self.__repeticiones()


        if self.__verificadora > 0:

            print("Existen: " + str(self.__verificadora) + " valores repetidos.")


            #Eliminar valores repetidos
            self.listaIndex = list(set(self.listaIndex))
            #Ordenar de mayor a menor
            self.listaIndex = sorted(self.listaIndex, reverse=True)


            while len(self.listaIndex) > 0:

                #se puede usar el método pop para quitar indice
                self.__matriz_de_Coordenadas.pop(self.listaIndex[0])

                self.listaIndex.pop(0)


            #Verificando que no hay valores repetidos
            self.__repeticiones()


            if self.__verificadora == 0 and self.listaIndex == []:

                print("\nLa eliminación de valores repetidos fue exitosa.")

            else:

                print("Hubo un error en la eliminación.")
                print("Verificadora: " + str(self.__verificadora))
                print("Lista Index: " + str(self.listaIndex))
                input()


        #ordenando valores resultantes
        self.__matriz_de_Coordenadas.sort()



    def grafica(self):

        plt.title("Simulación de Monte Carlo", fontsize = 15)
        plt.xlabel("Nivel de Desarrollo", fontsize = 12)
        plt.ylabel("Probabilidad de Caminos", fontsize = 12)

        plt.xlim(self.distancia0, self.distancia1)
        plt.ylim(0, ((self.__h + self.__particion ) * self.adj_h ) )

        plt.scatter(self.__listaX_on,self.__listaY_on, color="blue", marker="o")
        plt.scatter(self.__listaX_out,self.__listaY_out, color="black", marker="o")

        plt.show()


    def azar(self):

        azar = choice(self.__matriz_de_Coordenadas)

        #print("\nSu valor al azar es: " + str(azar))
        return azar


#objeto = MonteCarlo(0.001, 700)

#objeto.calcular()

# for i in range(5):

#     a = objeto.azar()

#     print("Su valor al azar es: ", a)

#objeto.grafica()