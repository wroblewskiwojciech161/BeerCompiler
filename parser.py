
# Wojciech Wróblewski parser 
# jftt projekt 

from lexer import OneBeerLexer
from sly import Parser
from key_words import KeyWords


class OneBeerParser(Parser):
    

    tokens = OneBeerLexer.tokens
    
    ############################################
    # PROGRAM
    ############################################

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        return(KeyWords.key['start'], p.declarations, p.commands)

    @_('BEGIN commands END')
    def program(self, p):
        return(KeyWords.key['start'], p.declarations, p.commands)
    ############################################
    # DECLARATIONS
    ############################################

    @_('declarations COMMA PID')
    def declarations(self, p):
        return (p.declarations, KeyWords.key['var'], p.PID, p.lineno)

    @_('declarations COMMA PID LEFT_B NUMBER COLON NUMBER RIGHT_B')
    def declarations(self, p):  
        return (p.declarations, KeyWords.key['tab'],  p.PID, p.NUMBER0, p.NUMBER1, p.lineno)

    @_('PID')
    def declarations(self, p):  
        return (KeyWords.key['var'], p.PID, p.lineno)

    @_('PID LEFT_B NUMBER COLON NUMBER RIGHT_B')
    def declarations(self, p): 
        return ('table', p.PID, p.NUMBER0, p.NUMBER1, p.lineno)

    ############################################
    # COMMANDS
    ############################################

    @_('commands command')
    def commands(self, p):
        x = p.commands
        x.append(p.command)
        return x

    @_('command')
    def commands(self, p):
        return [p.command]

    @_('id ASSIGN expression SEMICOLON')
    def command(self, p):
        return (KeyWords.key[':='], p.id, p.expression, p.lineno)

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return (KeyWords.key['if'], p.condition, p.commands, p.lineno)

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return (KeyWords.key['else'], p.condition, p.commands0, p.commands1, p.lineno)


    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return (KeyWords.key['while'], p.condition, p.commands, p.lineno)

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        return (KeyWords.key['repeat'], p.commands, p.condition, p.lineno)

    @_('FOR PID FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        return (KeyWords.key['for_down'], p[1], p.value0, p.value1, p.commands ,p.lineno)

    @_('FOR PID FROM value TO value DO commands ENDFOR')
    def command(self, p):
        return (KeyWords.key['for_to'], p[1], p.value0, p.value1, p.commands ,p.lineno)

    @_('READ value SEMICOLON')
    def command(self, p):
        return (p[0], p.value, p.lineno)

    @_('WRITE value SEMICOLON')
    def command(self, p):
        return (KeyWords.key['write'], p.value, p.lineno)

    ############################################
    # EXPRESSIONS
    ############################################

    @_('value')
    def expression(self, p):
        return p.value

    @_('value ADD value','value SUB value',
       'value MULT value','value DIV value',
       'value MOD value',)
    def expression(self, p):
        return (p[1], p.value0, p.value1, p.lineno)

    ############################################
    # CONDITIONS
    ############################################

    @_('value EQ value','value NOT_EQ value','value GREATER value',
       'value LESS_EQ value','value GREATER_EQ value','value LESS value')
    def condition(self, p):
        return (p[1], p.value0, p.value1, p.lineno)
    
    ############################################
    #  VALUE
    ############################################

    @_('NUMBER')
    def value(self, p):
        return (KeyWords.key['n'], p[0] ,p.lineno)

    @_('id')
    def value(self, p):
        return p.id

    ############################################
    # PID
    ############################################

    @_('PID')
    def id(self, p):
        return (KeyWords.key['var'], p[0], p.lineno)

    @_('PID LEFT_B PID RIGHT_B')
    def id(self, p):
        return (KeyWords.key['tab'], p[0], (KeyWords.key['var'], p[2]), p.lineno)

    @_('PID LEFT_B NUMBER RIGHT_B')
    def id(self, p):
        return (KeyWords.key['tab'], p[0], (KeyWords.key['n'], p[2]), p.lineno)


    def error(self,p):
        print("Error: error in line",str(p.lineno)," unknown or wrong token/inscription")
        exit(0)
