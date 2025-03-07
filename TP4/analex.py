import re

def tokenize_sparql(code):
    token_specification = [
        ('KW',      r'\b(?:SELECT|WHERE|LIMIT)\b'),
        ('VAR',     r'\?[a-zA-Z_]\w*'),
        ('PREFIX',  r'[a-zA-Z_]\w*:'),
        ('ID',      r'[a-zA-Z_]\w*'),
        ('STRING',  r'"(?:[^"\\]|\\.)*"(@[a-z]{2})?'),
        ('NUM',     r'\d+'),
        ('DOT',     r'\.'),
        ('BRACE',   r'[{}]'),
        ('WS',      r'[ \t]+'),
        ('UNKNOWN', r'.')
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % (name, pattern) for name, pattern in token_specification)

    regex_compiled = re.compile(tok_regex, re.IGNORECASE)

    tokens = []
    for match in regex_compiled.finditer(code):
        token_name = match.lastgroup
        value = match.group()

        if token_name == 'WS':
            continue 

        tokens.append((token_name, value))
    
    return tokens

query = '''SELECT ?nome ?desc WHERE {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000'''

tokens = tokenize_sparql(query)

for token in tokens:
    print(token)
