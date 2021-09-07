from yapl_lexer import *
from yapl_parser import *
import sys

# other global variables
variables = [{}]
defs = {'func': {}, 'struct': {}}


def expEval(p, level):  # evaluate expression
    if p[0] == "STR":
        for x in range(level, -1, -1):
            if p[1] in variables[x]:
                if p[2] in variables[x][p[1]]:
                    return variables[x][p[1]][p[2]]
                else:
                    print('Attribute Error :', p[2])
                    exit()
        print('Variable doesnt exist', p[1])
        exit()
    if(p[0] == 'INT' or p[0] == 'FLOAT' or p[0] == 'BOOL' or p[0] == 'CHAR' or p[0] == 'STRING'):
        return p
    elif (p[0] == 'NAME'):
        for x in range(level, -1, -1):
            if p[1] in variables[x]:
                return variables[x][p[1]]
        print('Error Variable doesnt exist:', p[1])
        exit()

    operator = p[0]
    if operator == 'FUN':
        ret = funcEval(p, level)
        return ret
    if len(p) == 3:
        try:
            a = expEval(p[1], level)
            b = expEval(p[2], level)
            if operator == 'EXPS':
                if a[0] == 'INT' or a[0] == 'FLOAT':
                    a = ('STRING', str(a[1]))
                if b[0] == 'INT' or b[0] == 'FLOAT':
                    b = ('STRING', str(b[1]))
                if a[1] == True:
                    a = ('STRING', 'TRUE')
                elif a[1] == False:
                    a = ('STRING', 'FALSE')
                if b[1] == True:
                    b = ('STRING', 'TRUE')
                elif b[1] == False:
                    b = ('STRING', 'FALSE')
                ret = ('STRING', a[1]+' ' + b[1])

            elif operator == '+':
                if ((a[0] == "FLOAT" and (b[0] == "FLOAT" or b[0] == "INT")) or (b[0] == "FLOAT" and (a[0] == "FLOAT" or a[0] == "INT"))):
                    ret = ("FLOAT", a[1]+b[1])
                elif a[0] == "STRING" and b[0] == "STRING":
                    ret = ("STRING", a[1]+b[1])
                elif a[0] != b[0]:
                    print('TypeError')
                    exit()
                else:
                    ret = (a[0], a[1]+b[1])
            elif operator == '-':
                if ((a[0] == "FLOAT" and (b[0] == "FLOAT" or b[0] == "INT")) or (b[0] == "FLOAT" and (a[0] == "FLOAT" or a[0] == "INT"))):
                    ret = ("FLOAT", a[1]-b[1])
                elif a[0] != b[0]:
                    print('TypeError')
                    exit()
                else:
                    ret = (a[0], a[1]-b[1])
            elif operator == '*':
                if ((a[0] == "FLOAT" and (b[0] == "FLOAT" or b[0] == "INT")) or (b[0] == "FLOAT" and (a[0] == "FLOAT" or a[0] == "INT"))):
                    ret = ("FLOAT", a[1]*b[1])
                elif a[0] != b[0]:
                    print('TypeError', a, b)
                    exit()
                else:
                    ret = (a[0], a[1]*b[1])
            elif operator == '/':
                if ((a[0] == "FLOAT" and (b[0] == "FLOAT" or b[0] == "INT")) or (b[0] == "FLOAT" and (a[0] == "FLOAT" or a[0] == "INT"))):
                    if b[1] == 0:
                        print("Zero division Error")
                        exit()
                    ret = ("FLOAT", a[1]/b[1])
                elif a[0] != b[0]:
                    print('TypeError')
                    exit()
                else:
                    ret = (a[0], a[1]/b[1])
            elif operator == '%':
                if ((a[0] == "FLOAT" and (b[0] == "FLOAT" or b[0] == "INT")) or (b[0] == "FLOAT" and (a[0] == "FLOAT" or a[0] == "INT"))):
                    ret = ("FLOAT", a[1] % b[1])
                elif a[0] != b[0]:
                    print('TypeError')
                    exit()
                else:
                    ret = (a[0], a[1] % b[1])
            elif operator == '^':
                if ((a[0] == "FLOAT" and (b[0] == "FLOAT" or b[0] == "INT")) or (b[0] == "FLOAT" and (a[0] == "FLOAT" or a[0] == "INT"))):
                    ret = ("FLOAT", a[1]**b[1])
                elif a[0] != b[0]:
                    print('TypeError')
                    exit()
                else:
                    ret = (a[0], a[1]**b[1])
            elif operator == '==':
                ret = ("BOOL", a[1] == b[1])
            elif operator == '!=':
                ret = ("BOOL", a[1] != b[1])
            elif operator == '<':
                ret = ("BOOL", a[1] < b[1])
            elif operator == '<=':
                ret = ("BOOL", a[1] <= b[1])
            elif operator == '>':
                ret = ("BOOL", a[1] > b[1])
            elif operator == '>=':
                ret = ("BOOL", a[1] >= b[1])
            elif operator == 'AND':
                ret = ("BOOL", a[1] and b[1])
            elif operator == 'OR':
                ret = ("BOOL", a[1] or b[1])
            return ret
        except TypeError:
            print('TypeError')

    elif len(p) == 2:
        var = ''
        ret = ''
        if p[1][1][0] == 'NAME':
            var = p[1][1][1]
        a = expEval(p[1], level)
        if operator == '++' and (a[0] == 'INT' or a[0] == 'FLOAT'):
            ret = (a[0], a[1]+1)
        elif operator == '--' and (a[0] == 'INT' or a[0] == 'FLOAT'):
            ret = (a[0], a[1]-1)
        elif operator == 'MIN' and (a[0] == 'INT' or a[0] == 'FLOAT'):
            ret = (a[0], -a[1])
        elif operator == 'NOT' and a[0] != 'INT' and a[0] != 'FLOAT':
            ret = (a[0], not a[1])
        elif operator == "EXP" and var != '':
            variables[level][var] = a
            pass
        else:
            print('TypeError')
            exit()
        return ret


def newEval(p, level):
    for x in range(level, -1, -1):
        if p[2] in variables[x]:
            print('Redecelaration Error variable:', p[2])
            exit()
    val = expEval(p[3], level)
    if val[0] == p[1] or (val[0] in ["FLOAT", "INT"] and p[1] in ["FLOAT", "INT"]):
        variables[level][p[2]] = val
    else:
        print("TypeError i", val, p[1])
        exit()


def printEval(p, level):
    result = expEval(p[1], level)
    if result[0] == 'BOOL' and result[1] == True:
        print('TRUE')
    elif result[0] == 'BOOL' and result[1] == False:
        print('FALSE')
    else:
        print(result[1])


def loopEval(p, level):
    stype = p[0]  # node type of parse tree
    name = p[1]
    st = p[2]
    end = p[3]
    step = p[4]
    for x in range(level, -1, -1):
        if name in variables[x]:
            print('Redecelaration Error', name)
            exit()
    for counter_ in range(st, end, step):
        ret = ''
        variables[level][name] = ('INT', counter_)
        variables.append({})
        runProgram(p[5], level+1)
        variables.pop()


def structEval(p, level):
    if p[1] == "new":
        if p[2] in defs['struct']:
            print('Struct Redecelaration Error')
            exit()
        temp = dict()
        for deff in p[3]:
            if deff[1] == "STR":
                print('STR keyword cannot be used')
                exit()
            temp[deff[1]] = deff[0]
        defs['struct'][p[2]] = temp
    elif p[1] == "ini":
        if p[2] not in defs['struct']:
            print('Struct not declared:', p[2])
            exit()
        for x in range(level, -1, -1):
            if p[3] in variables[x]:
                print('Redecelaration Error', p[3])
                exit()
        variables[level][p[3]] = {'STR': p[2]}
    elif p[1] == "def":
        for x in range(level, -1, -1):
            if p[2] in variables[x]:
                if p[4][0] == defs['struct'][variables[x][p[2]]['STR']][p[3]]:
                    variables[x][p[2]][p[3]] = p[4]
                    return
                else:
                    print('Attribute error of struct',
                          variables[x][p[2]]['STR'])
                    exit()
        print('Variable doesnt exist', p[2])
        exit()


def funcEval(p, level):
    if p[1] == "new":
        if p[2] in defs['func']:
            print('Struct Redecelaration Error')
            exit()
        defs['func'][p[2]] = {'param': p[3], 'body': p[4]}
    elif p[1] == "FC":
        if p[2] not in defs['func']:
            print('Function not declared:', p[2])
            exit()
        if len(p[3]) != len(defs['func'][p[2]]['param']):
            print('Arguments mismatch of function', p[2])
            exit()
        temp = {}
        for n in range(len(p[3])):
            val = expEval(p[3][n], level)
            if val[0] == defs['func'][p[2]]['param'][n][0]:
                temp[defs['func'][p[2]]['param'][n][1]] = val
            else:
                print('Argument type error', p[2], )
                exit()
        variables.append(temp)
        ret = ''
        ret = runProgram(defs['func'][p[2]]['body'], level+1)
        variables.pop()
        if ret != '':
            return ret


func = {
    'PRINT': printEval,
    'NEW': newEval,
    'EXP': expEval,
    'LOOP': loopEval,
    'STR': structEval,
    'FUN': funcEval,

}


def stmtEval(p, level):  # p is the parsed statement subtree / program
    stype = p[0]  # node type of parse tree
    func[p[0]](p, level)


def runProgram(p, level):  # p[0] == 'Program': a bunch of statements
    check = 0
    start = 0
    for stmt in p:  # statements in proglist
        ret = ''
        if stmt == None:
            return
        if stmt[0] == 'IF':
            start = 1
            if (expEval(stmt[1], level)[1]):
                check = 1
                ret = runProgram(stmt[2], level)
                if ret != '':
                    return ret
        elif start == 1 and check == 1 and (stmt[0] == "EL" or stmt[0] == "ELS"):
            continue
        elif start == 1 and check == 0 and stmt[0] == "EL":
            if (expEval(stmt[1], level)[1]):
                check = 1
                ret = runProgram(stmt[2], level)
                if ret != '':
                    return ret
        elif start == 1 and check == 0 and stmt[0] == "ELS":
            check = 0
            start = 0
            ret = runProgram(stmt[1], level)
            if ret != '':
                return ret
        elif start == 0 and (stmt[0] == "EL" or stmt[0] == "ELS"):
            print('ERROR: IF expected')
            exit()
        elif stmt[0] == 'RET':
            ret = expEval(stmt[1], level)
            return ret
        elif check == 1 or start == 1:
            check = 0
            start = 0
            stmtEval(stmt, level)
        else:
            stmtEval(stmt, level)  # statement subtree as tuple


if len(sys.argv) == 1:
    print('File name/path not provided as cmd arg.')
    exit(1)

while True:
    fileHandler = open('./test_cases/'+sys.argv[1], "r")
    userin = fileHandler.read()
    fileHandler.close()

    print("Welcome to your YAPL's Interpreter!")
    parsed = parser.parse(userin)
    if not parsed:
        continue

    for line in userin.split('\n'):
        print(line)
    print("=========================================")
    try:
        runProgram(parsed, 0)
    except Exception as e:
        print(e)

    # input("Press any key to run code again.")
    break


exit()
