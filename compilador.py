from func import clean_code
import re

#tuplas de terminales
tipos = 'INT','FLOAT','DOUBLE','SHORT','BIGINT'
operadores = '<','<=','>','>=','==','!='
expr_reg = {'VALOR':'(([0-9]+.[0-9]+)|[0-9]+|(\.[0-9]+))','ARR':'\$[a-zA-Z]+[0-9]*( )*(\[[0-9]*\])'}
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
    if(work_file.startswith('DEFINE PROGRAM ')):
        state_code += '✔ '+ 'DEFINE PROGRAM '
        work_file = work_file.lstrip('DEFINE PROGRAM ')
    else:
        state_code += '✘ '+'"'+'DEFINE PROGRAM '+'"'+ ' No encontrado de forma correcta.'
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
        #ver si las variables son correctas y estan bien asignadas
        for i in range(len(work_file[0])):
            match=re.search(r"^"+expr_reg['ARR']+"?( )*("+'|'.join(tipos)+")(( )*=( )*"+expr_reg['VALOR']+")?( )*;$",work_file[0][i].strip()+';')
            if match:
                #revisa si el arreglo esta bien declarado.
                if(re.search(r"^"+expr_reg['ARR']+"( )*("+'|'.join(tipos)+")( )*=",work_file[0][i].strip())):
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
        #print(work_file)
        #print(state_code)
    else:
        state_code = '✘ '+ 'Revise su "DO" y alrededor'
        raise NameError(state_code)
    #revisar las instrucciones dentro del DO WHILE:
    work_file = 'DO '+work_file #por si no hay instrucciones, vamos a dejar opcional el ponerlas.
    match = re.search(r"(O|;)( )*WHILE( )*\(",(work_file))
    if match:
        #print(match.group())
        work_file = list(work_file.partition(work_file[match.start()+1:match.end()-1].strip()))
        work_file[0]=work_file[0].lstrip('DO ') #quitar el DO que se uso para lo anterior
        work_file[0] =  work_file[0].split(';')
        work_file[0].pop()
        for i in range(len(work_file[0])):
            match = re.search(r"^"+expr_reg['ARR']+"?( )*=( )*"+expr_reg['VALOR']+"( )*;$",work_file[0][i].strip()+';')
            # print('np '+work_file[0][i].strip())
            if match:
                #print(match.group())
                #ver si existen las variables
                if re.search(r"\$[a-zA-Z]+[0-9]*",work_file[0][i]).group() in variables:
                    state_code +='\n'+ '✔ '+match.group().strip()
                else:
                    state_code = '✘ '+ work_file[0][i]+ ' esta variable no se declaro antes'
                    raise NameError(state_code)
            else:
                state_code = '✘ '+ work_file[0][i]+ ' esta declaracion hay que revisarla'
                raise NameError(state_code)
        state_code +='\n'+ '✔ '+'WHILE '
        #print(state_code)
        work_file.pop(0)
        work_file = work_file[1].strip()
    else:
        state_code = '✘ '+ 'Revise su "WHILE" y alrededor'
        raise NameError(state_code)
    if (work_file.endswith('END')):
        work_file = work_file.rstrip('END')
        #print(work_file)
        match = re.search(r"^\(( )*((\$[a-zA-Z]+[0-9]*)|"+expr_reg['VALOR']+")( )*("+'|'.join(operadores)+")( )*((\$[a-zA-Z]+[0-9]*)|"+expr_reg['VALOR']+")( )*\)",work_file.strip())
        if match:
            #print(match.group())
            for i in re.findall(r"\$[a-zA-Z]+[0-9]*",work_file):
                if i not in variables:
                    state_code = work_file + 'Esta usando variables no declaradas'
                    raise NameError(state_code)
            state_code +='✔ ' + work_file.strip()
            state_code +='\n✔ ' + 'END'+ '\n¡Su código parece correcto!'
            print(state_code)
        else:
            state_code = '✘ '+ work_file+'Algo puede estar malo en esta Condición'
            raise NameError(state_code)
    else:
        state_code = '"END" '+ 'No encontrado de forma correcta'
        raise NameError(state_code)
except:
    raise
finally:
    #print(", ".join(otros))
    file.close()
