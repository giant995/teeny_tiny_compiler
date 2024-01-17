class Lexer:
    def __init__(self, source):
        """
        Set the current character and current position of the source string then load the first character.

        :param source: Source code to lex as a string. We append a newline to simplify lexing/parsing the last
        token/statement
        """
        self.source = source + "\n"
        self.curChar = ""  # Current character in the string
        self.curPos = -1  # current position in the string
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
        pass

    def skipWhitespace(self):
        """Skip whitespace except newlines, which we use to indicate the end of a statement."""
        pass

    def skipComment(self):
        """Skip comments in the code."""
        pass

    def getToken(self):
        """Return the next token."""
        pass
