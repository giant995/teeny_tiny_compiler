import enum
import sys


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

    @staticmethod
    def checkIfKeyword(tokenText):
        """
        Decides if a token text is a keyword or not.

        :param tokenText: The token text to analyze
        :return: The TokenType if it is a keyword, None otherwise
        """
        for kind in TokenType:
            if kind.name == tokenText and 100 <= kind.value < 200:
                return kind
        return None


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
        self.nextChar()

    def nextChar(self):
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
        sys.exit("Lexing error. " + message)

    def skipWhitespace(self):
        """Skip whitespace except newlines, which we use to indicate the end of a statement."""
        while self.curChar == " " or self.curChar == "\t" or self.curChar == "\r":
            self.nextChar()

    def skipComment(self):
        """Skip comments in the code."""
        if self.curChar == "#":
            while self.curChar != "\n":
                self.nextChar()

    def getToken(self):
        """
        Return the next token. Check the first character of this token to see if it can decide what it is.
        If it is a multiple character operator (e.g.: !=), number, identifier or keyword then we will process the rest.
        """
        self.skipWhitespace()
        self.skipComment()
        token = None

        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == "=":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == ">":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == "<":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == "!":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == "\"":
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != "\"":
                # Don't allow special characters in the string. No escape characters, newlines, tab or %.
                if (
                        self.curChar == "\r" or self.curChar == "\n" or self.curChar == "\t"
                        or self.curChar == "\\" or self.curChar == "%"
                ):
                    self.abort("Illegal")
                self.nextChar()

            subtext = self.source[startPos:self.curPos]
            token = Token(subtext, TokenType.STRING)
        elif self.curChar.isdigit():
            # Get every digit and the optional decimal point
            startPos = self.curPos

            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == ".":
                self.nextChar()

                if not self.peek().isdigit():
                    self.abort("Illegal character in number")
                while self.peek().isdigit():
                    self.nextChar()

            number = self.source[startPos:self.curPos + 1]
            token = Token(number, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier
            # Get all consecutive alphanumeric characters
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            tokText = self.source[startPos:self.curPos+1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword is None:  # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)
        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == "\0":
            token = Token(self.curChar, TokenType.EOF)
        else:  # unknown token
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token
