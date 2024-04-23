from antlr4 import *
from JavaLexer import JavaLexer
from JavaParser import JavaParser


class MyListener(ParseTreeListener):
    def enterBlock(self, ctx):
        print("Entering block:", ctx.getText())


def main():
    code = """
    class MyClass {
        void myMethod() {
            int x = 10;
            if (x > 5) {
                System.out.println("x is greater than 5");
            }
        }
    }
    """
    input_stream = InputStream(code)
    lexer = JavaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParser(token_stream)
    tree = parser.compilationUnit()

    listener = MyListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)


if __name__ == "__main__":
    main()
