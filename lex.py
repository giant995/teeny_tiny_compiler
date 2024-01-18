import enum


class Token:
    """
    Token contains the original text and the type of token.
    """

    def __init__(self, tokenText, tokenKind):
        """
        :param tokenText: The token's actual text. Used for identifiers, strings and numbers
        :param tokenKind: The TokenType that this token is classified as.
        """
        self.text = tokenText
        self.kind = tokenKind


class TokenType(enum.Enum):
    """Enum for all the types of tokens."""
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class Lexer:
    def __init__(self, source):
        """
        Set the current character and current position of the source string then load the first character.

        :param source: Source code to lex as a string. We append a newline to simplify lexing/parsing the last
        token/statement
        :param curChar: The current character in the string
        :param curPos: The current position in the string
        """
        self.source = source + "\n"
        self.curChar = ""
        self.curPos = -1
        self.next_char()

    def next_char(self):
        """Process the next character."""
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = "\0"  # EOF
        else:
            self.curChar = self.source[self.curPos]

    def peek(self):
        """Return the lookahead character."""
        if self.curPos + 1 >= len(self.source):
            return "\0"
        return self.source[self.curPos + 1]

    def abort(self, message):
        """Invalid token found, print error message and exit."""
        pass

    def skipWhitespace(self):
        """Skip whitespace except newlines, which we use to indicate the end of a statement."""
        pass

    def skipComment(self):
        """Skip comments in the code."""
        pass

    def getToken(self):
        """
        Return the next token. Check the first character of this token to see if it can decide what it is.
        If it is a multiple character operator (e.g.: !=), number, identifier or keyword then we will process the rest.
        """
        token = None

        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == "\0":
            token = Token(self.curChar, TokenType.EOF)
        else:  # unknown token
            pass

        self.next_char()
        return token
