from decimal import Decimal, getcontext
from funciones import *
from numpy import array, add, save, multiply, divide, absolute, append


def biseccion(a, b, funcion):
    
    """Aplicación del método de bisección para encontrar la constante de tiempo."""


    while True:

        n = int(1)

        lista = []


        while True:

            print("iteracion--------------"+str(n))

            c = cortar(a,b)
            # print("\n su xr es de: " + str(c))
            lista.append(c)

            d = funcion(c)
            e1 = multiply(funcion(a), funcion(c))
            # print("\nxr*xa es: " + str(e1))

            error = None

            if n > Decimal('1'):

                error = absolute(multiply(divide(add(lista[n - 1 ], - lista[n - 2 ] ), lista[n - 1 ] ), Decimal('100' ) ) )
                print("\n su error es: " + str(error))


            if error == Decimal('0'):

                return c
                break


            if e1 > Decimal('0'):
                a = c
              

            elif e1 < Decimal('0'):
                b = c


            n += 1


        break
    


if __name__ == '__main__':

    #Las funciones se encuentran cerca de 0.2 y 0.4
    #Método de bisección para encontrar punto x1=0
    coordenada_de_corte_x = biseccion(0.2, 0.4, funcionSolucionA)


    errorA = evaluarErrores("a", coordenada_de_corte_x, funcionExp, funcionLog)


    if errorA == True:

        #Guardando coordenadas en un array
        coordenadas = array([
                            str(coordenada_de_corte_x), str(funcionExp(coordenada_de_corte_x))
                            ])


        #Guardando en un archivo externo, este va a ser usado por funciones
        save('coor_de_corte', coordenadas)


        input("\n Presione enter para continuar")
        #Método de bisección para encontrar x2=0 en funcionSolucionB
        coordenada_b = biseccion(0.8, 1.0, funcionSolucionB)
        errorB = evaluarErrores("b", coordenada_b, funcionExpConstante, funcionLogConstante)
    

        if errorB == True:

            #Guardando todas las coordenadas
            coordenadas = append(coordenadas, [str(coordenada_b), str(funcionExpConstante(coordenada_b))])

            #Guardando todos los datos en un archivo externo
            save('coor_de_corte', coordenadas)

            #crwando BBDD que después será usada
            crearBBDD()

            #Grafica
            graficaFunciones()
