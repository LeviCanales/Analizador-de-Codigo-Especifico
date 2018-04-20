import func

#tuplas de terminales
tipos = 'INT','FLOAT','DOUBLE','SHORT','BIGINT'
operadores = '<','<=','>','>=','==','!='
otros = 'DEFINE PROGRAM ','()','DO','$',' ','=',';','[',']','WHILE (',') END'
#lectura de archivo
file = open("codigo_fuente.txt")
#variables de trabajo
original_file = file.read()
work_file = func.clean_code(original_file, '\n',chr(9))
print(work_file)
work_file = work_file.strip()
state_code = ''
try:
    #esta bien la parte del 'DEFINE PROGRAM '?
    if(work_file.startswith(otros[0])):
        state_code += '✔ '+ otros[0]
        work_file = work_file.lstrip(otros[0])
        print(state_code)
    else:
        state_code += '✘ '+'"'+otros[0]+'"'+ ' No encontrado de forma correcta.'
        raise NameError(state_code)
except:
    raise
finally:
    file.close()