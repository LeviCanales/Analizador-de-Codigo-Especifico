from func import clean_code
import re

#tuplas de terminales
tipos = 'INT','FLOAT','DOUBLE','SHORT','BIGINT'
operadores = '<','<=','>','>=','==','!='
otros = 'DEFINE PROGRAM ','WHILE (',') END'
#lectura de archivo
file = open("codigo_fuente.txt")
#variables de trabajo
original_file = file.read()
work_file = clean_code(original_file, '\n',chr(9))
work_file = work_file.strip()
state_code = ''
#Guardar variables
variables = []
try:
    #¿esta bien la parte del 'DEFINE PROGRAM '?
    if(work_file.startswith(otros[0])):
        state_code += '✔ '+ otros[0]
        work_file = work_file.lstrip(otros[0])
    else:
        state_code += '✘ '+'"'+otros[0]+'"'+ ' No encontrado de forma correcta.'
        raise NameError(state_code)
    #Ver si esta bien el patron number y el ()
    work_file = work_file.split('()',1)
    work_file[0] = work_file[0].strip()
    if re.search(r"^[a-zA-Z]+[0-9]*$",work_file[0]):
        state_code += work_file[0]+ '()'
        work_file = work_file[1].lstrip()
        #print(state_code)
    else:
        state_code = '✘ '+work_file[0]+' y '+ '()'+' No encontrado de forma correcta.'
        raise NameError(state_code)
    #Ver que haya un DO bien puesto xD
    match = re.search(r"(\)|;)( )*DO( )*(\$|W)",work_file)
    if match:
        # print(work_file[:match.start()+1])
        # print(work_file[match.end()-1:])
        work_file = work_file.split(work_file[match.start()+1:match.end()-1],1)
        work_file[0] =  work_file[0].split(';')
        work_file[0].pop()
        #print(work_file[0])
        for i in range(len(work_file[0])):
            match=re.search(r"^\$[a-zA-Z]+[0-9]*( )*(("+'|'.join(tipos)+")|(\[[0-9]*\]( )*("+'|'.join(tipos)+")))(( )*=( )*[0-9]*(\.[0-9]+)?)?( )*;$",work_file[0][i].strip()+';')
            if match:
                #print(match.group())
                if(re.search(r"^\$[a-zA-Z]+[0-9]*( )*(\[[0-9]*\]( )*("+'|'.join(tipos)+"))( )*=",work_file[0][i].strip())):
                    state_code = '✘ '+ work_file[0][i]+ ' El arreglo no se asigna de esta forma.'
                    raise NameError(state_code)
                else:
                    state_code +='\n'+ '✔ '+match.group().strip()
                    variables.append(re.search(r"\$[a-zA-Z]+[0-9]*",work_file[0][i]).group())
            else:
                state_code = '✘ '+ work_file[0][i]+ ' esta declaracion hay que revisarla'
                raise NameError(state_code)
        variables=tuple(variables)
        #print(variables)
        state_code +='\n'+ '✔ '+'DO'
        work_file = work_file[1].lstrip()
        print(work_file)
        print(state_code)
    else:
        state_code = '✘ '+ 'Revise su "DO" y alrededor'
        raise NameError(state_code)
except:
    raise
finally:
    #print(", ".join(otros))
    file.close()
