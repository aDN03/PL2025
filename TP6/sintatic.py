from lexer import lexer  # Importa o lexer do arquivo lexer.py

pointer = 0
tokenStore = []  # Lista de tokens para processar no parser

def currentToken():
    if pointer < len(tokenStore):
        return tokenStore[pointer]
    return None  # Retorna None se o pointer estiver fora do intervalo

def nextToken():
    global pointer
    pointer += 1

def match(expected):
    if currentToken() and currentToken()[0] == expected:
        nextToken()
    else:
        raise SyntaxError(f"Expected {expected}, but found {currentToken()}")

def parseExp():
    result = parseTerm()

    while currentToken() and currentToken()[0] in ['PLUS', 'MINUS']:
        if currentToken()[0] == 'PLUS':
            nextToken()
            result += parseTerm()
        elif currentToken()[0] == 'MINUS':
            nextToken()
            result -= parseTerm()
    return result

def parseTerm():
    result = parseFactor()

    while currentToken() and currentToken()[0] in ['MULTIPLY', 'DIVIDE']:
        if currentToken()[0] == 'MULTIPLY':
            nextToken()
            result *= parseFactor()
        elif currentToken()[0] == 'DIVIDE':
            nextToken()
            result /= parseFactor()
    return result

def parseFactor():
    if currentToken() and currentToken()[0] == 'NUMBER':
        result = currentToken()[1]
        nextToken()
        return result

    elif currentToken() and currentToken()[0] == 'LPAREN':
        nextToken()
        result = parseExp()
        match('RPAREN')
        return result

    else:
        raise SyntaxError(f"Expected number or '(' but found {currentToken()}")

def parse():
    result = parseExp()

    if pointer < len(tokenStore):
        raise SyntaxError("Some tokens were not processed")
    return result

if __name__ == "__main__":
    data = '''
    2+3
    67-(2+3*4)
    (9-2)*(13-4)
    '''

    for expr in data.splitlines():
        if not expr.strip():
            continue

        print(f"Expression: {expr}")
        lexer.input(expr)
        tokenStore = []

        while True:
            tok = lexer.token()
            if not tok:
                break
            tokenStore.append((tok.type, tok.value))

        pointer = 0

        try:
            result = parse()
            print(f"Result: {result}\n")
        except SyntaxError as e:
            print(f"Error parsing expression: {e}\n")