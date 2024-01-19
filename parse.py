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
        Try to match the current token. If not, error.

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

        self.nl()

    def nl(self):
        """
        nl ::= '\n'+

        Make sure the current token is a new line. We accumulate as many new line as there are.
        """

        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
