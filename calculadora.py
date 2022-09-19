from monteCarlo import *
from particionado import *
import matplotlib.pyplot as plt
from funciones import *
import numpy as np



if __name__ == "__main__":
    


    pd.options.display.max_columns = None


    #particion de particionado determina que tan cercanos estan los puntos unos de otros
    #particionado de monte carlo determina el tamaño de los puntos.
    #iteraciones determinan la cantidad de puntos por simulación

    #Creando objeto de particionado
    #Deseable 0.001
    objetoParticionado = Particionado(0.01)

    objetoParticionado.generador()

    objetoParticionado.grafica()

    df = objetoParticionado.dataFrame()

    #creando tabla que almacenará el df
    tableSummary()

    #Insertando datos en BBDD
    insertSummary(list(convertTupleSummary(np.array(df))))

    print("\nSe han insertado correctamente las particiones.")

    #--------FALTA COMPROBACIÓN DE MEDIA Y LÍMITES DE SD---------------

    print("\nExisten " + str(len(df)) + " datos por civilización.")

    #creando objeto de monteCarlo
    #civilización 1 0.0001,10000
    objetoMonteCarlo0 = MonteCarlo(0.001, 1000)
    print("\nCivilización 1.")
    dfValoresAzar0 = np.array(list(valorAzar(objetoMonteCarlo0, df,1)))
    
    #civilización 2
    objetoMonteCarlo1 = MonteCarlo(0.001, 1000)
    print("\nCivilización 2.")
    dfValoresAzar1 = np.array(list(valorAzar(objetoMonteCarlo1, df,2)))
    


    #Extraer valores al azar
    valoresDeX = np.array(df.loc[:,"Particion (x)"])



    #Gráfica
    plt.title("Modelo", fontsize=15)
    plt.xlabel("Clase t", fontsize=12)
    plt.ylabel("Explotación Material", fontsize=12)

    plt.grid()

    plt.plot(valoresDeX, funcionVectorizadaLog(valoresDeX), color="#E67E22")
    plt.plot(valoresDeX, funcionVectorizadaLin(valoresDeX), "--", color="red")
    plt.plot(valoresDeX,funcionVectorizadaExp(valoresDeX), color="#3498DB")
    #graficanto puntos al azar
    #civilización 1
    plt.plot(valoresDeX, (funcionVectorizadaExp(valoresDeX)+dfValoresAzar0), "--", color="#27AE60")
    #civilización 2
    plt.plot(valoresDeX, (funcionVectorizadaExp(valoresDeX)+dfValoresAzar1), "--", color="#8E44AD")


    plt.show()