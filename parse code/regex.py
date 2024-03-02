import re


def separate_code_blocks(file_path):
    functions = []
    comments = []
    other_definitions = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        block = ''
        in_block = False
        for line in lines:
            line = line.strip()
            if line.startswith("/*"):  # Multi-line comment start
                in_block = True
                block += line + '\n'
            elif line.startswith("//"):  # Single-line comment
                comments.append(line)
            elif line.startswith("*/"):  # Multi-line comment end
                in_block = False
                block += line
                comments.append(block)
                block = ''
            elif in_block:  # Inside a multi-line comment
                block += line + '\n'
            elif re.match(r'(public|private|protected)\s', line):  # Function definition
                functions.append(line)
            elif line:  # Other definitions
                other_definitions.append(line)

    return functions, comments, other_definitions


if __name__ == "__main__":
    file_path = "code2.java"  # Replace this with the path to your Java file
    functions, comments, other_definitions = separate_code_blocks(file_path)

    print("Functions:")
    for function in functions:
        print(function)

    print("\nComments:")
    for comment in comments:
        print(comment)

    print("\nOther Definitions:")
    for definition in other_definitions:
        print(definition)
