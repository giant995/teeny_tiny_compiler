from lex import *


def main():
    source = "+- */"
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()


if __name__ == "__main__":
    main()
