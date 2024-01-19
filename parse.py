import sys
from lex import *


class Parser:
    """
    Keeps track of current token and checks if the code matches the grammar.
    """

    def __init__(self):
        pass

    def checkToken(self, lexer):
        """
        Returns True if the current token matches.

        :param lexer:
        :return:
        """

        pass

    def checkPeek(self, kind):
        """
        Return True if the next token matches.

        :param kind:
        :return:
        """

        pass

    def match(self):
        """
        Try to match the current token. If not, error.

        :return:
        """

        pass

    def nextToken(self):
        """
        Advances the current token.

        :return:
        """

        pass

    def abort(self, message):
        sys.exit("Error. " + message)
