grammar Java;

compilationUnit : packageDeclaration? importDeclaration* typeDeclaration*;

packageDeclaration : 'package' qualifiedName ';';

importDeclaration : 'import' qualifiedName ';';

typeDeclaration : classDeclaration | interfaceDeclaration;

classDeclaration : 'class' Identifier classBody;

interfaceDeclaration : 'interface' Identifier interfaceBody;

classBody : '{' classBodyDeclaration* '}';

interfaceBody : '{' interfaceBodyDeclaration* '}';

classBodyDeclaration : methodDeclaration | fieldDeclaration;

interfaceBodyDeclaration : methodDeclaration | fieldDeclaration;

methodDeclaration : Identifier '(' parameterList? ')' block;

fieldDeclaration : dataType Identifier ('=' expression)? ';';

parameterList : parameter (',' parameter)*;

parameter : dataType Identifier;

dataType : Identifier;

block : '{' (statement | block)* '}';

statement : declarationStatement
          | expressionStatement
          | ifStatement
          | whileStatement
          | forStatement
          | returnStatement
          ;

expression : assignmentExpression;

declarationStatement : dataType variableDeclarators ';';

expressionStatement : expression ';';

ifStatement : 'if' '(' expression ')' statement ('else' statement)?;

whileStatement : 'while' '(' expression ')' statement;

forStatement : 'for' '(' forControl ')' statement;

forControl : (variableDeclarators | expression)? ';' expression? ';' expression?;

returnStatement : 'return' expression? ';';

assignmentExpression : Identifier '=' expression;

variableDeclarators : variableDeclarator (',' variableDeclarator)*;

variableDeclarator : Identifier ('=' expression)?;

qualifiedName : Identifier ('.' Identifier)*;

Identifier : [a-zA-Z_] [a-zA-Z_0-9]*;
