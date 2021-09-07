import ply.lex as lex

tokens = [
    "INT",
    "FLOAT",
    "CHAR",
    "STRING",
    "BOOL",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "MOD",
    "POW",
    "EQUAL",
    "EQ",
    "NEQ",
    "GT",
    "LE",
    "GTE",
    "LEE",
    "END",
    "NOT",
    "AND",
    "OR",
    "LROUND",
    "RROUND",
    "PRINT",
    "INCREMENT",
    "DECREMENT",
    "IF",
    "EL",
    "ELS",
    "FOR",
    "STRUCT",
    "DOT",
    "FUNC",
    "RET",
    "COMMENTS",
    "NAME",
    "COMMA",
    "VAR",
    "LAST",
    "COL"
]
t_COL = r'\:'
t_LAST = r'\:\>'
t_EQUAL = r'\-\>'
t_COMMA = r'\,'
t_POW = r'\^'
t_PLUS = r'\+'
t_DOT = r'\.'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'
t_GT = r'\>'
t_LE = r'\<'
t_GTE = r'\>\='
t_LEE = r'\<\='
t_EQ = r'\=\='
t_NEQ = r'\!\='
t_END = r'\;'
t_LROUND = r'\('
t_RROUND = r'\)'
t_ignore = ' \t\r\n\f\v'  # these we are ignoring
t_ignore_COMMENT = r'\#.*'


def t_BOOL(t):
    r'TRUE|FALSE'
    if(t.value == "TRUE"):
        t.value = True
    elif(t.value == "FALSE"):
        t.value = False
    return t


def t_FLOAT(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CHAR(t):
    r'\'[^\']\''
    t.value = t.value[1]
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1: -1]
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == "PRINT":
        t.type = 'PRINT'
    elif t.value == "FLOAT":
        t.type = 'VAR'
    elif t.value == "INT":
        t.type = 'VAR'
    elif t.value == "CHAR":
        t.type = 'VAR'
    elif t.value == "STRING":
        t.type = 'VAR'
    elif t.value == "BOOL":
        t.type = 'VAR'
    elif t.value == "NOT":
        t.type = 'NOT'
    elif t.value == "AND":
        t.type = 'AND'
    elif t.value == "OR":
        t.type = 'OR'
    elif t.value == "IF":
        t.type = 'IF'
    elif t.value == "EL":
        t.type = 'EL'
    elif t.value == "ELS":
        t.type = 'ELS'
    elif t.value == "FOR":
        t.type = 'FOR'
    elif t.value == "STRUCT":
        t.type = 'STRUCT'
    elif t.value == "FUNC":
        t.type = 'FUNC'
    elif t.value == "RET":
        t.type = 'RET'
    else:
        t.type = 'NAME'
    return t


def t_lineno(t):
    r'\n'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print('[Lexer Error] Line', t.lineno)
    print(f"Illegal character: {t.value}")
    t.lexer.skip(1)


lexer = lex.lex()

# while True:
#     print("YAPL_LEXER>>", end='')
#     lexer.input(input())

#     while True:
#         tokenEntered = lexer.token()
#         if not tokenEntered:
#             break
#         print(tokenEntered)
