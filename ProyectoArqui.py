
from ctypes import sizeof
import string
import sys


if __name__ == '__main__':
    instruccion = input()
    tokens = instruccion.split()
    s = int(tokens[1])
    bp = int(tokens[3])
    gh = int(tokens[5])
    lh = int(tokens[7])
    counter_pred = 0
    branch_tot = 0
    branch_tomado_cor = 0
    branch_tomado_incor = 0
    branch_no_tomado_cor = 0
    branch_no_tomado_incor = 0
    tabla = [[0 for i in range(2)]for j in range(2**s)]
    sizeTabla = 2**s
    patternTableEntries = 2**lh
    with open(r"Trazo_de_saltos.trace.txt",'r') as f:
        print("Parametros")
        print("Tipo de predictor: {}".format(bp))
        print("Entradas en el history table: {}".format(sizeTabla))
        print("Tamaño de los registros de historia local: {}".format(lh))
        print("Entradas en el pattern table: {}".format(patternTableEntries))
        if bp == 0:
            mask = (2**s)-1
            for line in f:
                next = line.split()
                direction = int(next[0])
                pred = next[1]
                index = direction & mask

                if((tabla[index][0] == 1) and (tabla[index][1] == 1) ): #Caso 11 
                    if (pred == 'T'): #acierto
                        branch_tomado_cor += 1 #predice correctamente
                    elif(pred == 'N'): #fallo
                        tabla[index][1] = 0 #actualiza tabla
                        branch_tomado_incor += 1 #predice incorrectamente
                elif((tabla[index][0] == 1) and (tabla[index][1] == 0)): #Caso 10
                    if (pred == 'T'): #acierto
                        branch_tomado_cor += 1 #predice correctamente
                        tabla[index][1] = 1 
                    elif(pred == 'N'): #fallo
                        tabla[index][0] = 0
                        branch_tomado_incor += 1 #predice incorrectamente
                elif((tabla[index][0] == 0) and (tabla[index][1] == 0)): #Caso 00
                    if (pred == 'T'): # fallo
                        branch_no_tomado_incor += 1 #predice incorrecto
                        tabla[index][1] = 1                       
                    elif(pred == 'N'):   #acierto
                        branch_no_tomado_cor += 1  #predice correcto              
                elif((tabla[index][0] == 0) and (tabla[index][1] == 1)): #Caso 01
                    if(pred == 'T'): #fallo
                        branch_no_tomado_incor += 1 #predice incorrecto
                        tabla[index][0] = 1 
                    elif(pred == 'N'): #acierto
                        tabla[index][1] = 0
                        branch_no_tomado_cor += 1 #predice correcto

        elif bp == 1:
            print("Not implemented")
        elif bp == 2:
            print("Not implemented")
        elif bp == 3:   
            print("Not implemented")
        else:
            print("Error, wrong data input for -bp, please use '0', '1', '2' or '3'")
            exit()
        branch_tot = branch_tomado_cor + branch_tomado_incor + branch_no_tomado_incor + branch_no_tomado_cor
        branch_cor = branch_tomado_cor+branch_no_tomado_cor
        print("# branches: {}".format(branch_tot))
        print("# branches tomados predichos correctamente: {}".format(branch_tomado_cor))
        print("# branches tomados predichos incorrectamente: {}".format(branch_tomado_incor))
        print("# branches no tomados predichos correctamente: {}".format(branch_no_tomado_cor))
        print("# branches no tomados predichos incorrectamente: {}".format(branch_no_tomado_incor))
        print("% predicciones correctas: {}%".format((branch_cor*100)/branch_tot))