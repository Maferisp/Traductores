"""
    Analizador Lexicografico del Lenguaje GuardedUSB
    Primera fase del proyecto
    Traductores e Interpretadores (CI-3725)
    Maria Fernanda Magallanes (13-10787)
    Maria Fernanda Machado (13-10780)
    Septiembre - Diciembre 2019
"""
from ply import lex
from sys import argv

# Palabras reservadas 
reserved = {
    #Generales del lenguaje
    'declare' : 'TkDeclare',

    #Tipos de datos
    'int' : 'TkInt',
    'bool' : 'TkBool',
    'inter' : 'TkInter',
    'array' : 'TkArray',

    #Condicionales
    'if' : 'TkIf',
    'fi' : 'Tkfi',
    'else' : 'TkElse',
    'then' : 'TkThen',

    #Iteraciones
    'for' : 'TkFor',
    'rof' : 'TkRof',
    'while' : 'TkWhile',

    #Auxiliares de Codicionales e iteraciones
    'do' : 'TkDo',
    'od' : 'TkOd',
    'of' : 'TkOf',


    #Entrada y salida
    'read' : 'TkRead',
    'print' : 'TkPrint',
    'println' : 'TkPrintln',

    # funciones de conversión de tipos y embebidas
    'atoi' : 'TkAtoi',
    'size' : 'TkSize',
    'max' : 'TkMax',
    'min' : 'TkMin',

    #Postcondicion
    'Post' : 'TkPost',
    'forall' : 'TkForall',
    'exists' : 'TkExists',

    #Operadores
    'in' : 'TkIn',

    #Para los valores Booleanos
    'true' : 'TkTrue',
    'false' : 'TkFalse',
}

# Lista de Tokens
tokens = [
    # Para las variables
    'TkId',

    #  Numeros enteros
    'TkNum',

    # Cadenas de Caracteres
    'TkString',

    # Simbolos utilizados para denotar separadores
    'TkOBlock',
    'TkCBlock',
    'TkSoForth',
    'TkComma',
    'TkCOpenPar',
    'TkClosePar',
    'TkAsig',
    'TkSemicolon',
    'TkArrow',

    # Simbolos utiliados para denotar operadores
    'TkPlus',
    'TkMinus',
    'TkMult',
    'TkDiv',
    'TkMod',
    'TkOr',
    'TkAnd',
    'TkNot',
    'TkLess',
    'TkLeq',
    'TkGeq',
    'TkGreater',
    'TkEqual',
    'TkNEqual',
    'TkOBracket',
    'TkCBracket',
    'TkTwoPoints',
    'TkConcat',
] + list(reserved.values())

# Especificaciones de los tokens
t_TkOBlock = r'\|\['
t_TkCBlock = r'\]\|'
t_TkSoForth = r'\.\.'
t_TkComma = r'\,'
t_TkCOpenPar = r'\(' 
t_TkClosePar = r'\)'
t_TkAsig = r':='
t_TkSemicolon = r';'
t_TkArrow = r'==>'

t_TkPlus = r'\+'
t_TkMinus = r'\-'
t_TkMult = r'\*'
t_TkDiv = r'\/'
t_TkMod = r'\%'
t_TkOr = r'\/'
t_TkAnd = r'\/\\'
t_TkNot = r'\!'
t_TkLess = r'<'
t_TkLeq = r'<='
t_TkGeq = r'>='
t_TkGreater = r'>'
t_TkEqual = r'=='
t_TkNEqual = r'!='
t_TkOBracket = r'\['
t_TkCBracket = r'\]'
t_TkTwoPoints = r':'
t_TkConcat = r'\|\|'

# Reglas Ignoradas
t_ignore_Space = r'\s'             # Espacio en blanco 
t_ignore_Comment = r'\//.*'        # Comentarios 
t_ignore_Line = r' \n'             # Salto de linea
t_ignore_Tab = r' \t'              # Tabuladores


TOKENS_VALIDOS = []  #Coleccion de tokens validos
TOKENS_INVALIDOS = [] #Coleccion de tokens invalidos


# Funciones Regulares
def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TkId(identificar):
    r'[a-zA-Z]+[a-zA-Z_0-9]*'
    identificar.type =  reserved.get(identificar.value, 'TkId')
    return identificar

def t_TkString(string):
    r'"([^"\\\n]|\\"|\\\\|\\n)*"'
    return string

# Numero de lineas
def t_newLine(line):
    r'\n+'
    line.lexer.lineno += len(line.value)

# Manejador de errores
def t_error(invalido):
    """ Funcion por "default" cuando encuentra un token que no pertenece a la lista de tokens """
    error = 'Error: Unexpected character "' + str(invalido.value[0]) + '" in row ' \
        + str(invalido.lineno) + ', column ' + str(invalido.lexpos+1)
    TOKENS_INVALIDOS.append(error)
    invalido.lexer.skip(1)

## Leer el archivo
lexer = lex.lex()  #Construccion del lexer 
"""Main"""

#Verificamos si se paso el argumento correctamente
if len(argv) < 2:
    print("Uso del programa: python3 lexer.py <Nombre del archivo>.")
    sys.exit()

#abrimos la ruta pasada por argumento
filepath = argv[1]

#Guardamos la extension del archivo
ext = filepath.split('.')

#Verificamos si la extension es la correcta
if ext[-1] != 'pusb':
    print("Error al leer el archivo: Extension incorrecta.")
    sys.exit()

#Abrimos el contenido del la ruta
file = open(filepath, 'r')
#Guardamos las lineas de cada
data = file.readline()

while data and len(TOKENS_INVALIDOS)<1:
    #pasamos la linea como data al lexer
    #Esto es con el fin de calcular bien la columna de los tokens
    lexer.input(data)


    #Iteramos sobre el la entrada para extraer los tokens
    #for tok in lexer:
    #    print(tok.type, tok.value, tok.lineno)
    tok = lexer.token()
    
    while tok :
        if (tok.type == 'TkNum' or tok.type == 'TkId' or tok.type == 'TkString'):
            token_info = str(tok.type) + ' ("' + str(tok.value) + '") '\
            + str(tok.lineno) + ' ' + str(tok.lexpos+1)
        else:
            token_info = str(tok.type) + ' ' + str(tok.lineno) + ' ' + str(tok.lexpos+1)

        TOKENS_VALIDOS.append(token_info)
        tok = lexer.token()

    #leemos otra linea
    data = file.readline()

# Cuando hay un error
if(len(TOKENS_INVALIDOS)>0):
    print( TOKENS_INVALIDOS[0])
else: 
    for x in TOKENS_VALIDOS:
        print(x)
