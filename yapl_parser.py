from yapl_lexer import *
import ply.yacc as yacc
import sys

precedence = (
    ('left',  'MINUS', 'PLUS'),
    ('left', 'MUL', 'DIV'),
    ('left', 'GTE', 'GT'),
    ('left', 'LE', 'LEE'),
    ('left', 'INCREMENT', 'DECREMENT'),
    ('left', 'LROUND', 'RROUND'),
    ('left', 'AND', 'OR'),
    ('left', 'POW'),
)

start = 'S'


def p_start(p):  # non-terminal, starting
    """
    S : stmt S
    """
    p[0] = [p[1]] + p[2]  # list comprehension used to solve recursive grammar, added/appending as well


def p_start_empty(p):
    """
    S :
    """
    p[0] = []


def p_print_stmt(p):
    """
    stmt : PRINT EQUAL exp END
    """
    p[0] = ('PRINT', p[3])


def p_assign_int(p):
    """
    stmt : VAR NAME EQUAL exp 
    """
    p[0] = ('NEW', p[1], p[2], p[4])


def p_if(p):
    """
    stmt : IF LROUND exp RROUND EQUAL S LAST
    """
    p[0] = ('IF', p[3], p[6])


def p_elif(p):
    """
    stmt : EL LROUND exp RROUND EQUAL S LAST
    """
    p[0] = ('EL', p[3], p[6])


def p_else(p):
    """
    stmt : ELS EQUAL S LAST
    """
    p[0] = ('ELS', p[3])


def p_loop(p):
    """
    stmt : FOR NAME LROUND INT EQUAL INT COMMA INT RROUND EQUAL S LAST
    """
    p[0] = ('LOOP', p[2], p[4], p[6], p[8], p[11])


def p_struct(p):
    """
    stmt : STRUCT NAME EQUAL defs LAST
    """
    p[0] = ("STR", "new", p[2], p[4])


def p_struct_ini(p):
    """
    stmt : STRUCT NAME NAME
    """
    p[0] = ("STR", "ini", p[2], p[3])


def p_struct_def(p):
    """
    stmt : NAME DOT NAME EQUAL exp
    """
    p[0] = ("STR", "def", p[1], p[3], p[5])


def p_func_def(p):
    """
    stmt : FUNC NAME LROUND defs RROUND EQUAL S LAST
    """
    p[0] = ("FUN", "new", p[2], p[4], p[7])


def p_return(p):
    """
    stmt : RET exp
    """
    p[0] = ("RET", p[2])


def p_empt(p):
    """
    stmt : 
    """
    p[0] - []


def p_defs(p):
    """
    defs : VAR NAME defs
    """
    p[0] = [(p[1], p[2])] + p[3]


def p_defs_emo(p):
    """
    defs : 
    """
    p[0] = []


def p_exp(p):
    """
    stmt : exp
    """
    p[0] = ('EXP', p[1])


def p_func_call(p):
    """
    exp : NAME COL args COL
    """
    p[0] = ('FUN', 'FC', p[1], p[3])


def p_arg_emp(p):
    """
    args :  
    """
    p[0] = []


def p_arg_exp(p):
    """
    args : exp args
    """
    p[0] = [(p[1])] + p[2]


def p_exp_struct(p):
    """
    exp : NAME DOT NAME
    """
    p[0] = ('STR', p[1], p[3])


def p_print_mul(p):
    """
    exp : exp COMMA exp
    """
    p[0] = ('EXPS', p[1], p[3])


def p_exp_brak(p):
    """
    exp : LROUND exp RROUND
    """
    p[0] = (p[2])


def p_exp_name(p):
    """
    exp : NAME
    """
    p[0] = ('NAME', p[1])


def p_exp_bin(p):
    """
    exp : exp PLUS exp
        | exp MINUS exp
        | exp DIV exp
        | exp MUL exp
        | exp MOD exp
        | exp POW exp
    """
    p[0] = (p[2], p[1], p[3])  # '1+2' -> ('+', '1', '2')


def p_exp_log(p):
    """
    exp : exp EQ exp
        | exp NEQ exp
        | exp GT exp
        | exp GTE exp
        | exp LE exp
        | exp LEE exp
        | exp AND exp
        | exp OR exp
    """
    p[0] = (p[2], p[1], p[3])


def p_exp_unary(p):
    """
    exp : exp INCREMENT
        | exp DECREMENT
        | NOT exp
        | MINUS exp
    """
    if (p[2] == '++' or p[2] == '--'):
        p[0] = (p[2], p[1])
    elif(p[1] == 'NOT'):
        p[0] = (p[1], p[2])
    else:
        p[0] = ('MIN', p[2])


def p_exp_char(p):
    """
    exp : CHAR
    """
    p[0] = ('CHAR', p[1])


def p_exp_vals(p):
    """
    exp : INT
        | FLOAT
        | STRING
        | BOOL
    """
    if type(p[1]) == int:
        p[0] = ('INT', p[1])
    elif type(p[1]) == float:
        p[0] = ('FLOAT', p[1])
    elif type(p[1]) == str:
        p[0] = ('STRING', p[1])
    else:
        p[0] = ('BOOL', p[1])


def p_error(p):
    print("Syntax error at token", p.value, p.type, p.lexpos)
    exit(1)


parser = yacc.yacc()  # start parsing, yacc object created
