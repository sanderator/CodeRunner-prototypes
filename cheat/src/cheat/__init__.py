EXACT_COPIES_ONLY = False
IGNORE_IDENTIFIERS = True  # If true, all non-keyword identifiers are replaced by '###'

# Remaining constants are not intended to be user-configured.

LANGUAGE_EXTENSIONS = {
    'java'  : '.java',
    'python': '.py',
    'c'     : '.c',
    'matlab': '.m'
}

ONE_LINE_COMMENTS = {
    'java'      : '//[^\n]*',
    'python'    : '#[^\n]*',
    'c'         : '//[^\n]*',
    'matlab'    : '%[^\n]*'
}

MULTI_LINE_COMMENTS = {
    'java'      : "/\*.*?\*/|/\*\*.*?\*/",
    'python'    : "'''.*?'''|\"\"\".*?\"\"\"",
    'c'         : "/\*.*?\*/",
    'matlab'    : "%{.*?}%"
}

# Keyword lists are incomplete but that doesn't matter in this context
KEYWORDS = {
    'java'  : ['case', 'switch', 'if', 'for', 'while',
                'void', 'int', 'float', 'double', 'char',
                'do', 'else', 'break', 'long', 'short', 'boolean',
                'byte', 'return', 'class', 'interface', 'enum'],
    'python': ['def', 'for', 'if', 'while', 'class', 'return', 'and',
                'pass', 'in', 'try', 'except', 'print', 'input',
                'and', 'from', 'not', 'or', 'else', 'elif'],
    'c'     : ['case', 'switch', 'if', 'for', 'while', 'struct',
                'void', 'typedef', 'int', 'float', 'double', 'char',
                'do', 'else', 'const', 'break', 'long', 'short',
                'signed', 'include', 'define', 'return'],
    'matlab' : ['break', 'case', 'catch', 'continue', 'for', 'function',
                'if', 'return', 'switch', 'try', 'while', 'else']
}

HEADERS_LANG = {
        'english': {
            'response': 'Response',
            'email': 'Email address',
            'first_name': 'First name',
            'surname': 'Surname'
            },
        'french': {
            'response': 'Réponse',
            'email': 'Adresse de courriel',
            'first_name': 'Prénom',
            'surname': 'Nom'
            }
        }
