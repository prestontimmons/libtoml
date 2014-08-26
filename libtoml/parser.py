from datetime import datetime

from rply import LexerGenerator, ParserGenerator

ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

lg = LexerGenerator()

lg.ignore(r"\s+")
lg.ignore(r"\# .*")

lg.add("COLON", r":")
lg.add("LCURLY", r"\{")
lg.add("RCURLY", r"\}")
lg.add("LBRACKET", r"\[")
lg.add("RBRACKET", r"\]")
lg.add("COMMA", r",")
lg.add("EQUALS", r"=")
lg.add("BOOLEAN", r"true|false")
lg.add("DATETIME", r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
lg.add("FLOAT", r"-?\d+\.\d+")
lg.add("INTEGER", r"-?\d+")
lg.add("STRING", r'"(\\"|[^"])*"')
lg.add("KEY", r"[a-zA-Z_][a-zA-Z0-9_#\?\.]*")

lexer = lg.build()
pg = ParserGenerator([rule.name for rule in lg.rules], cache_id="libtoml")

@pg.production("main : statements")
def main(p):
    return p[0]

@pg.production("statements : statements statement")
def statements(p):
    return p[0] + [p[1]]

@pg.production("statements : statement")
def statements_single(p):
    return [p[0]]

@pg.production("statement : expr")
def statement_expr(p):
    return p[0]

@pg.production("statement : assign")
def statement_assign(p):
    return p[0]

@pg.production("assign : KEY EQUALS arg")
def assignment(p):
    return (p[0].getstr(), p[2])

@pg.production("args : arg")
@pg.production("args : arg COMMA")
def args_single(p):
    return [p[0]]

@pg.production("args : arg COMMA args")
def args(p):
    return [p[0]] + p[2]

@pg.production("dictkey : arg COLON arg")
@pg.production("dictkey : arg COLON arg COMMA")
def dictkey_single(p):
    return {p[0]: p[2]}

@pg.production("dictkeys : dictkey")
def dictkeys(p):
    return p[0]

@pg.production("dictkeys : dictkey dictkeys")
def dictkeys_many(p):
    d = p[0]
    d.update(p[1])
    return d

@pg.production("arg : LCURLY dictkeys RCURLY")
def dict_arg(p):
    return p[1]

@pg.production("arg : LBRACKET args RBRACKET")
def list_arg(p):
    return p[1]

@pg.production("arg : STRING")
def string_arg(p):
    return p[0].getstr()[1:-1]

@pg.production("arg : DATETIME")
def date_arg(p):
    return datetime.strptime(p[0].getstr(), ISO8601_FORMAT)

@pg.production("arg : FLOAT")
def float_arg(p):
    return float(p[0].getstr())

@pg.production("arg : INTEGER")
def integer(p):
    return int(p[0].getstr())

@pg.production("arg : BOOLEAN")
def boolean_arg(p):
    val = p[0].getstr()
    if val == "true":
        return True
    if val == "false":
        return False

@pg.production("expr : LBRACKET LBRACKET KEY RBRACKET RBRACKET")
def table_expr(p):
    return ("table", p[2].getstr())

@pg.production("expr : LBRACKET KEY RBRACKET")
def key_expr(p):
    return ("keygroup", p[1].getstr())

@pg.error
def error_handler(token):
    if token.value == "$end":
        raise EmptyError()
    msg = "Error on line %s. Ran into a %s where it wasn't expected."
    raise ValueError(msg % (token.source_pos.lineno, token.gettokentype()))

class EmptyError(ValueError):
    pass

parser = pg.build()

def parse_toml(value):
    tokens = lexer.lex(value)
    try:
        return parser.parse(tokens)
    except EmptyError:
        return {}
