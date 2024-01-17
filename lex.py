class Lexer:
    def __init__(self, source):
        pass

    def nextChar(self):
        """Process the next character."""

    def peek(self):
        """Return the lookahead characters."""
        pass

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
