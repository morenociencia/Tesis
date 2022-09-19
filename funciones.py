import decimal as dc
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as sql



# Estableciendo un error de 1e-101
dc.getcontext().prec = 110


# Valor de euler con 100 decimales
# A001113, list -99
eulerPre = dc.Decimal('1').exp()

euler = eulerPre.quantize(
    dc.Decimal('.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'),
    rounding = dc.ROUND_DOWN)


# Valor de pi con 100 decimales
# A000796, list -99
pi = dc.Decimal('3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214')



def funcionCoordenadas():

    """Devuelve los valores calculados en formato texto, en un array,
    [punto de corte xa, constante t, punto de corte xb, punto de corte yb]"""

    try:

        return np.load('coor_de_corte.npy')

    except FileNotFoundError:

        print("Ejecute primero bisección.py")



def crearBBDD():

    """Crea una base de datos"""
    conexion = sql.connect("Datos.db")
    conexion.commit()
    conexion.close()



def tableSummary():

    """Crea una tabla de información general en la BBDD"""
    conexion = sql.connect("Datos.db")
    cursor = conexion.cursor()
    cursor.execute("""CREATE TABLE Summary 
        (
            Particion_X text,
            VectoresLog_Y text,
            MediaLog text,
            SdLog text,
            VectoresExp_Y text,
            MediaExp text,
            SdExp text
        )
        """ )
    conexion.commit()
    conexion.close()



def insertSummary(lista):

    """Recibe una lista que contiene tuplas, inserta dichos datos en la BBDD (summary)"""
    conexion = sql.connect("Datos.db")
    cursor = conexion.cursor()
    instruccion = f"INSERT INTO Summary VALUES (?,?,?,?,?,?,?)"
    cursor.executemany(instruccion, lista)
    conexion.commit()
    conexion.close()



def convertTupleSummary(array):

    """Recibe un array y convierte los valores internos a un tupla,
    la idea es generar una lista aceptable para sql.
    Devuelve un objeto, recuerde convertirlo a lista."""
    for i in range(len(array)):
        
        #Se convierten a string los valores internos
        yield tuple([str(array[i][0]), str(array[i][1]),
                     str(array[i][2]), str(array[i][3]),
                     str(array[i][4]), str(array[i][5]),
                     str(array[i][6])]) 



def crearTabla(civil,i):

    """Crea una tabla en la BBDD"""
    conexion = sql.connect("Datos.db")
    cursor = conexion.cursor()
    cursor.execute("""CREATE TABLE Civilización%s_%s 
        (
            Particion text,
            Camino text
        )
        """ %(civil,i) )
    conexion.commit()
    conexion.close()



def insertarDatos(lista, civil, i):

    """Recibe una lista que contiene tuplas, inserta dichos datos en la BBDD"""
    conexion = sql.connect("Datos.db")
    cursor = conexion.cursor()
    instruccion = f"INSERT INTO Civilización{civil}_{i} VALUES (?,?)"
    cursor.executemany(instruccion, lista)
    conexion.commit()
    conexion.close()



def conversionTupla(lista):

    """Recibe una lista y convierte los valores internos a un tupla,
    la idea es generar una lista aceptable para sql.
    Devuelve un objeto, recuerde convertirlo a lista."""
    for i in range(len(lista)):
        
        #Se convierten a string los valores internos
        yield tuple([str(lista[i][0]), str(lista[i][1])]) 



def constante():

    """Retorna el valor de una constante, se encuentra en un archivo externo."""
    return dc.Decimal(((np.load('coor_de_corte.npy'))[1]))



def evaluarErrores(nombre, x, funcion0, funcion1):

    """Esta función examina la coordenada x en un punto donde 2 funciones se cruzan,
    devuelve si la aproximación fue correcta o erronea junto con su nivel de error."""
    yFuncion0 = funcion0(x)
    yfuncion1 = funcion1(x)

    yTotal = np.abs(yFuncion0) - np.abs(yfuncion1)

    if yTotal == 0:

        print("\nLa ejecución fue correcta para: " + str(nombre))
        print("El nivel de error es: %s" %yTotal)

        return True

    else:

        print("\nHubo un error en la ejecución.")
        print("El nivel de error es: %s" %yTotal)

        return False



def funcionExp(x):

    """La función cálcula euler elevado a x,
    el método power de numpy es más eficiente que el pow de math.
    se le pasan objetos dc.Decimal"""
    return np.power(euler, dc.Decimal(str(x)))



def funcionLog(x):

    """Cálcula logaritmo natural de x,
    Es más preciso al acudir a la propiedad de cambio de base."""
    return np.divide(dc.Decimal(str(x)).log10(), dc.Decimal(euler).log10())



def funcionSolucionA(x):

    """Relación deducida de un sistema de ecuaciones.
    Ayuda a encontrar el punto de corte en a."""
    par0 = np.add((funcionExp(x)), (funcionLog(x)))

    return par0



def cortar(a,b):

    """Función usada especialmente por el método de bisección."""
    par0 = np.add(dc.Decimal(str(a)), dc.Decimal(str(b)))
    par1 = np.divide( par0, dc.Decimal('2') )
        
    return par1



def funcionExpConstante(x):

    """La función le agrega a la exponencial de euler,
    la constante de ajuste del tiempo. La constante debe ser negativa"""
    return np.add(funcionExp(x), - constante())



def funcionLogConstante(x):

    """La función le agrega a la logaritmica,
    la constante de ajuste del tiempo. la constante es positiva."""
    return np.add(funcionLog(x), constante())



def funcionSolucionB(x):

    """La función tiene forma de parabola y representa
    los puntos donde las funciones se cruzan. Para poder ser usada
    es necesario haber encontrado el punto a (constante t)."""
    par0 = np.add(funcionExp(x), - (funcionLog(x)))
    par1 = np.add(par0, - (np.multiply(constante(), dc.Decimal('2'))))

    return par1



def puntoPendiente(x):

    """Ayuda a calcular la recta punto pendiente que pasa por los puntos a y b,
    recordar que y-y1 = m(x-x1)"""


    coordenadas = funcionCoordenadas()


    y2 = dc.Decimal(coordenadas[3])
    y1 = dc.Decimal('0')
    x2 = dc.Decimal(coordenadas[2])
    x1 = dc.Decimal(coordenadas[0])

    #y2-y1 / x2-x1
    pendiente = np.divide(y2, np.add(x2,-x1))

    pendienteX1 = -(pendiente * x1)

    #y = mx +b
    b = pendienteX1+y1

    return (pendiente*x + (b))



def alturaProbabilidad(sd):

    """Devuelve el punto máximo de la distribución de probabilidad"""
    raiz = np.sqrt(np.multiply(dc.Decimal('2'), pi))
    denom = np.multiply(dc.Decimal(str(sd)), raiz)
    return (np.divide(dc.Decimal('1'), denom))



def valorZ(x, m, sd):

    """Normaliza una función devolviendo el valor z, y también es útil
    para construir la función de distribución normal dada por la formula de Gauss."""
    num = np.add(dc.Decimal(str(x)), - dc.Decimal(str(m)))
    return np.divide(num, dc.Decimal(str(sd)))



def valorSd(x, m, z):

    """Devuelve el valor de la desviación estándar par un z determinado."""
    return valorZ(x, m, z)



def funcionNormal(x, m, sd):

    """Función de distribución normal dada por la ecuación de Gauss."""
    par0 = np.power(dc.Decimal(valorZ(x, m, sd)), dc.Decimal('2'))
    par1 = np.multiply(dc.Decimal(np.divide(dc.Decimal('1'), dc.Decimal('2'))), dc.Decimal('-1'))
    par2 = np.multiply(dc.Decimal(par0), dc.Decimal(par1))
    par3 = np.power(dc.Decimal(str(euler)), dc.Decimal(str(par2)))
    par4 = np.multiply(alturaProbabilidad(sd), par3)

    return par4



def funcionNormalBiModal(x, m0, m1, sd0, sd1):

    """Función de disttribución bi-modal, es decir con 2 modas,
    su base se encuentra en la distribución normal."""
    return np.add(funcionNormal(x, m0, sd0), funcionNormal(x, m1, sd1))



def valorAzar(objetoMonteCarlo, dataf, civil):

    """Devuelve un objeto con los valores al azar,
    Las iteraciones indican la cantidad de valores azar a devolver,
    correspondida con la creación de objetos."""


    for l in range(len(dataf)):

        print("Creando objeto: ",l)

        #ingresando la coordenada del vector modulo
        objetoMonteCarlo.distancia0 = dc.Decimal('0')
        #objetoMonteCarlo.distancia1 = dataf.iat[l,1]

        #sumo los vectores y me dan la distancia total
        objetoMonteCarlo.distancia1 = dataf.iat[l,1] + dataf.iat[l,4]
        
        #Atributos de tipo Estadístico
        objetoMonteCarlo.m = dataf.iat[l,2]
        objetoMonteCarlo.sd = dataf.iat[l,3]

        #Atributos adicionales
        objetoMonteCarlo.m1 = dataf.iat[l,5] + dataf.iat[l,1]
        objetoMonteCarlo.sd1 = dataf.iat[l,6]

        #calculando, generando distribución normal y frecuencia acumulada.
        objetoMonteCarlo.calcular()


        #Extrayendo datos según los valores al azar obtenidos (Tener en cuenta que hay 2 medias)
        matrizDeCoordenadas = objetoMonteCarlo.get_matriz_de_coordenadas()
        
        #preparando el formato de lista/tupla
        listaAux = list(conversionTupla(matrizDeCoordenadas))

        #Creando tabla
        crearTabla(civil, l)
        #insertando datos
        insertarDatos(listaAux, civil, l)


        #Mostrar gráfica
        #objetoMonteCarlo.grafica()

        #Extrayendo un valor al azar de la frecuencia acumulada.
        #Por el momento extraer sólo la coordenada x
        a = (objetoMonteCarlo.azar())[0]
        #print(a)
        yield a


funcionVectorizadaLog = np.vectorize(funcionLogConstante)
funcionVectorizadaLin = np.vectorize(puntoPendiente)
funcionVectorizadaExp = np.vectorize(funcionExpConstante)
funcionVectorizadaSolB = np.vectorize(funcionSolucionB)

coordenadas = funcionCoordenadas()


def graficaFunciones():

    """Gráfica general del modelo."""
    x = np.arange(dc.Decimal("0.001"),dc.Decimal("1.001"),dc.Decimal("0.001"))


    plt.grid()

    plt.title("Gráfica General", fontsize=15)

    plt.ylabel("Nivel de Desarrollo", fontsize=12)
    plt.xlabel("Clase t", fontsize=12)

    plt.ylim(-0.5,1.5)
    plt.xlim(0,1)

    plt.plot(x,funcionVectorizadaExp(x), label='e^x - t', color="#3498DB")
    plt.plot(x,funcionVectorizadaLog(x), label='ln(x) + t', color="#E67E22")
    plt.plot(x,funcionVectorizadaSolB(x), ":",label='e^x - ln(x) - 2*t', color="green")
    plt.plot(x,funcionVectorizadaLin(x), "--", label="y = mx + b", color="red")
    plt.plot(dc.Decimal(coordenadas[0]),0, marker="o", markersize=7,color="#8E44AD", label='a, b')
    plt.plot(dc.Decimal(coordenadas[2]), dc.Decimal(coordenadas[3]), marker="o", markersize=7,color="#8E44AD")

    plt.legend()


    plt.show()



#graficaFunciones()