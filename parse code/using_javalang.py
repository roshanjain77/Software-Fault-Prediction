import javalang


def extract_code_blocks(file_path):
    functions = []
    comments = []
    other_definitions = []

    with open(file_path, 'r') as file:
        code = file.read()

    tree = javalang.parse.parse(code)

    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        print(path, node)
        print('-'*50)

    return None, None, None


if __name__ == "__main__":
    file_path = "code2.java"  # Replace this with the path to your Java file
    functions, comments, other_definitions = extract_code_blocks(file_path)

    print("Functions:")
    for function in functions:
        print(function)

    print("\nComments:")
    for comment in comments:
        print(comment)

    print("\nOther Definitions:")
    for definition in other_definitions:
        print(definition)
