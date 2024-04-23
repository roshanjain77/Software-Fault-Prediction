import javalang


def parse_expression(expression):
    """ Recursively parse and format expressions into readable Java code. """
    if isinstance(expression, javalang.tree.BinaryOperation):
        return f"{parse_expression(expression.operandl)} {expression.operator} {parse_expression(expression.operandr)}"
    elif isinstance(expression, javalang.tree.Literal):
        return expression.value
    elif isinstance(expression, javalang.tree.MemberReference):
        return expression.member
    elif isinstance(expression, javalang.tree.MethodInvocation):
        args = ", ".join(parse_expression(arg) for arg in expression.arguments)
        return f"{expression.member}({args})"
    elif isinstance(expression, javalang.tree.Assignment):
        return f"{parse_expression(expression.expressionl)} {expression.type} {parse_expression(expression.value)}"
    elif expression:
        return str(expression)
    return ""


def parse_statement(statement):
    """ Convert statements into a formatted string of Java code. """
    if isinstance(statement, javalang.tree.ReturnStatement):
        return f"return {parse_expression(statement.expression)};" if statement.expression else "return;"
    elif isinstance(statement, javalang.tree.LocalVariableDeclaration):
        type_name = statement.type.name
        declarations = ", ".join(
            [f"{decl.name} = {parse_expression(decl.initializer)}" if decl.initializer else decl.name for decl in statement.declarators])
        return f"{type_name} {declarations};"
    elif isinstance(statement, javalang.tree.StatementExpression):
        return parse_expression(statement.expression) + ";"
    elif isinstance(statement, javalang.tree.BlockStatement):
        return ' '.join(parse_statement(stmt) for stmt in statement.statements)
    else:
        return str(statement)


def parse_java_code(code):
    """ Parse Java code to extract methods, classes, and global variables. """
    tree = javalang.parse.parse(code)
    functions = []
    classes = []
    globals = []

    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        class_name = node.name
        class_methods = []
        class_fields = []
        for member in node.body:
            if isinstance(member, javalang.tree.MethodDeclaration):
                body_content = ' '.join(parse_statement(stmt)
                                        for stmt in member.body) if member.body else ""
                method_details = {
                    "return_type": str(member.return_type),
                    "function_name": member.name,
                    "function_body": body_content
                }
                class_methods.append(method_details)
            elif isinstance(member, javalang.tree.FieldDeclaration) and 'static' in member.modifiers:
                type_name = member.type.name
                for declarator in member.declarators:
                    globals.append(f"{type_name} {declarator.name}")

        classes.append({"class_name": class_name,
                       "methods": class_methods, "fields": class_fields})

    return functions, classes, globals


# Example usage
java_code = """
public class MyClass {
    static int count = 0;  // Static field, global variable

    public void method() {
        int x = 10;
        // This is a comment
        return;
    }

    public void method2() {
        int x = 10;
        y = 20;  // Another variable
        return;
    }
}

public class AnotherClass {
    public MyClass add(int a, int b) {
        return new MyClass();
    }
}
"""

# java_code = open("code.java").read()
functions, classes, globals = parse_java_code(java_code)
print("Functions:", functions)
print("Classes:", classes)
print("Global Variables:", globals)
