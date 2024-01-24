import sys
from lex import *


class Parser:
    """
    Keeps track of current token and checks if the code matches the grammar.

    () -> grouping
    | -> OR
    {} -> zero or more
    [] -> zero or one
    + -> one or more of what is it to the left
    "TOKEN_NAME" -> a token
    """

    def __init__(self, lexer):
        self.lexer = lexer

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()  # Called twice to initialize current and peek

    def checkToken(self, kind):
        """
        Returns True if the current token matches.

        :param kind:
        :return:
        """

        return kind == self.curToken.kind

    def checkPeek(self, kind):
        """
        Return True if the next token matches.

        :param kind: The token type to check against the peek token type
        :return:
        """

        return kind == self.peekToken.kind

    def match(self, kind):
        """
        Try to match the current token, then seek the next token. If not, raise an error.

        :return:
        """

        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    def nextToken(self):
        """
        Advances the current token.

        :return:
        """

        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error. " + message)

    def program(self):
        """
        program ::= {statement}

        Parse all the statements in the program.
        """

        print("PROGRAM")
        # Grammar requires some newlines, need to skip the excess
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokenType.EOF):
            self.statement()

    def statement(self):
        """
        Rules for statements. Checks the first token to see what kind of statement it is.
        """

        # "PRINT" (expression | string)
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()
            if self.checkToken(TokenType.STRING):
                self.nextToken()
            else:
                self.expression()

        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison

            self.match(TokenType.THEN)
            self.nl()

            # zero or more statements in the body
            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)

        # "WHILE" comparison "REPEAT" nl {statement nl} "ENDWHILE" nl
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

        # "LABEL" ident nl
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()
            self.match(TokenType.IDENT)

        # "GOTO" ident nl
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression nl
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-LET")
            self.nextToken()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident nl
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()
            self.match(TokenType.IDENT)

        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        self.nl()

    def comparison(self):
        """
        comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
        """

        print("COMPARISON")
        self.expression()
        # At least one comparison operator and another expression
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected a comparison operator at: " + self.curToken.text)

        # Can have 0 or more comparison operators and expressions
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    def isComparisonOperator(self):
        """
        Indicates if the current token is a comparison operator

        :return: Boolean
        """

        return (
            self.checkToken(TokenType.EQEQ)
            or self.checkToken(TokenType.NOTEQ)
            or self.checkToken(TokenType.GT)
            or self.checkToken(TokenType.GTEQ)
            or self.checkToken(TokenType.LT)
            or self.checkToken(TokenType.LTEQ)
        )

    def expression(self):
        """
        expression ::= term {( "-" | "+") term}
        """

        print("EXPRESSION")
        self.term()

        # Can have 0 or more of -/+ and expressions
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    def term(self):
        """
        term ::= unary {( "/" | "*" ) unary}
        """

        print("TERM")
        self.unary()

        # Can have or more of //* and expressions
        while self.checkToken(TokenType.SLASH) or self.checkToken(TokenType.ASTERISK):
            self.nextToken()
            self.unary()

    def unary(self):
        """
        unary ::= ["+" | "-"] primary
        """

        print("UNARY")
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    def primary(self):
        """
        primary ::= number | ident
        """

        print("PRIMARY")
        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.curToken.text)

    def nl(self):
        """
        nl ::= '\n'+

        Make sure the current token is a new line. We accumulate as many new line as there are.
        """

        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
