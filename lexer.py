from sly import Lexer

# Wojciech Wróblewski lexer 
# jftt projekt  kompilatora

class OneBeerLexer(Lexer):
    tokens = {
    ADD, SUB, MULT, DIV, MOD,
    NOT_EQ, GREATER_EQ, LESS_EQ, GREATER, LESS, EQ,
    DOWNTO, TO, FROM,ENDWHILE,
    ENDFOR, ENDIF, WHILE, DO, FOR,
    IF, END, BEGIN, DECLARE,
    THEN, ELSE, READ, WRITE,
    LEFT_B, RIGHT_B, COLON, SEMICOLON, ASSIGN,
    NUMBER, PID, COMMA,REPEAT,UNTIL}

    
    ADD = r'\+'
    SUB = r'-'
    MULT = r'\*'
    DIV = r'/'
    MOD = r'%'
    ASSIGN = r':='
    NOT_EQ = r'!='
    GREATER_EQ = r'>='
    LESS_EQ = r'<='
    GREATER = r'>'
    LESS = r'<'
    EQ = r'='
    DOWNTO = r'DOWNTO'
    TO = r'TO'
    FROM = r'FROM'
    ENDWHILE = r'ENDWHILE'
    ENDFOR = r'ENDFOR'
    ENDIF = r'ENDIF'
    WHILE = r'WHILE'
    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'
    DO = r'DO'
    FOR = r'FOR'
    IF = r'IF'
    END = r'END'
    BEGIN = r'BEGIN'
    DECLARE = r'DECLARE'
    THEN = r'THEN'
    ELSE = r'ELSE'
    READ = r'READ'
    WRITE = r'WRITE'
    LEFT_B = r'\('
    RIGHT_B = r'\)'
    COLON = r':'
    SEMICOLON = r';'
    COMMA = r','
    NUMBER = r'[0-9]+'
    PID = r'[_a-z]+'

    ignore = ' \t\r'
  
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    @_(r'\[[^\]]*\]')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        msg = " Error, syntax error in line " + str(self.lineno) + " unexpected token : "+str(t.value)
        print(msg)
        self.index += 1
        exit(0)

