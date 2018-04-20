import func
import re

#tuplas de terminales
tipos = 'INT','FLOAT','DOUBLE','SHORT','BIGINT'
operadores = '<','<=','>','>=','==','!='
otros = 'DEFINE PROGRAM ','()','DO','$',' ','=',';','[',']','WHILE (',') END'
#lectura de archivo
file = open("codigo_fuente.txt")
#variables de trabajo
original_file = file.read()
work_file = func.clean_code(original_file, '\n',chr(9))
#print(work_file)
work_file = work_file.strip()
state_code = ''
try:
    #¿esta bien la parte del 'DEFINE PROGRAM '?
    if(work_file.startswith(otros[0])):
        state_code += '✔ '+ otros[0]
        work_file = work_file.lstrip(otros[0])
    else:
        state_code += '✘ '+'"'+otros[0]+'"'+ ' No encontrado de forma correcta.'
        raise NameError(state_code)
    #Ver si esta bien el patron number y el ()
    work_file = work_file.split(otros[1],1)
    work_file[0] = work_file[0].strip()
    if re.search(r"^[a-zA-Z]+[0-9]*$",work_file[0]):
        state_code += work_file[0]+ otros[1]
        work_file = work_file[1].lstrip()
        print(work_file)
    else:
        state_code = '✘ '+work_file[0]+' y '+ otros[1]+' No encontrado de forma correcta.'
        raise NameError(state_code)
    #Ver que haya un DO bien puesto xD
    if re.search(r"(\)|;)( )*DO( )*(\$|W)",work_file):
        print('DO')
except:
    raise
finally:
    #print(", ".join(otros))
    file.close()