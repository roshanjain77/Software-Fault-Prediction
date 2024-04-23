# Generated from Java.g by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser

# This class defines a complete listener for a parse tree produced by JavaParser.
class JavaListener(ParseTreeListener):

    # Enter a parse tree produced by JavaParser#compilationUnit.
    def enterCompilationUnit(self, ctx:JavaParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by JavaParser#compilationUnit.
    def exitCompilationUnit(self, ctx:JavaParser.CompilationUnitContext):
        pass


    # Enter a parse tree produced by JavaParser#packageDeclaration.
    def enterPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#packageDeclaration.
    def exitPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#importDeclaration.
    def enterImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#importDeclaration.
    def exitImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:JavaParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:JavaParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#classDeclaration.
    def enterClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#classDeclaration.
    def exitClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceDeclaration.
    def enterInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceDeclaration.
    def exitInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#classBody.
    def enterClassBody(self, ctx:JavaParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#classBody.
    def exitClassBody(self, ctx:JavaParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceBody.
    def enterInterfaceBody(self, ctx:JavaParser.InterfaceBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceBody.
    def exitInterfaceBody(self, ctx:JavaParser.InterfaceBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#classBodyDeclaration.
    def enterClassBodyDeclaration(self, ctx:JavaParser.ClassBodyDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#classBodyDeclaration.
    def exitClassBodyDeclaration(self, ctx:JavaParser.ClassBodyDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceBodyDeclaration.
    def enterInterfaceBodyDeclaration(self, ctx:JavaParser.InterfaceBodyDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceBodyDeclaration.
    def exitInterfaceBodyDeclaration(self, ctx:JavaParser.InterfaceBodyDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#fieldDeclaration.
    def exitFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#parameterList.
    def enterParameterList(self, ctx:JavaParser.ParameterListContext):
        pass

    # Exit a parse tree produced by JavaParser#parameterList.
    def exitParameterList(self, ctx:JavaParser.ParameterListContext):
        pass


    # Enter a parse tree produced by JavaParser#parameter.
    def enterParameter(self, ctx:JavaParser.ParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#parameter.
    def exitParameter(self, ctx:JavaParser.ParameterContext):
        pass


    # Enter a parse tree produced by JavaParser#dataType.
    def enterDataType(self, ctx:JavaParser.DataTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#dataType.
    def exitDataType(self, ctx:JavaParser.DataTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#block.
    def enterBlock(self, ctx:JavaParser.BlockContext):
        pass

    # Exit a parse tree produced by JavaParser#block.
    def exitBlock(self, ctx:JavaParser.BlockContext):
        pass


    # Enter a parse tree produced by JavaParser#statement.
    def enterStatement(self, ctx:JavaParser.StatementContext):
        pass

    # Exit a parse tree produced by JavaParser#statement.
    def exitStatement(self, ctx:JavaParser.StatementContext):
        pass


    # Enter a parse tree produced by JavaParser#expression.
    def enterExpression(self, ctx:JavaParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#expression.
    def exitExpression(self, ctx:JavaParser.ExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#declarationStatement.
    def enterDeclarationStatement(self, ctx:JavaParser.DeclarationStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#declarationStatement.
    def exitDeclarationStatement(self, ctx:JavaParser.DeclarationStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#expressionStatement.
    def enterExpressionStatement(self, ctx:JavaParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#expressionStatement.
    def exitExpressionStatement(self, ctx:JavaParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#ifStatement.
    def enterIfStatement(self, ctx:JavaParser.IfStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#ifStatement.
    def exitIfStatement(self, ctx:JavaParser.IfStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#whileStatement.
    def enterWhileStatement(self, ctx:JavaParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#whileStatement.
    def exitWhileStatement(self, ctx:JavaParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#forStatement.
    def enterForStatement(self, ctx:JavaParser.ForStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#forStatement.
    def exitForStatement(self, ctx:JavaParser.ForStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#forControl.
    def enterForControl(self, ctx:JavaParser.ForControlContext):
        pass

    # Exit a parse tree produced by JavaParser#forControl.
    def exitForControl(self, ctx:JavaParser.ForControlContext):
        pass


    # Enter a parse tree produced by JavaParser#returnStatement.
    def enterReturnStatement(self, ctx:JavaParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#returnStatement.
    def exitReturnStatement(self, ctx:JavaParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:JavaParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:JavaParser.AssignmentExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#variableDeclarators.
    def enterVariableDeclarators(self, ctx:JavaParser.VariableDeclaratorsContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclarators.
    def exitVariableDeclarators(self, ctx:JavaParser.VariableDeclaratorsContext):
        pass


    # Enter a parse tree produced by JavaParser#variableDeclarator.
    def enterVariableDeclarator(self, ctx:JavaParser.VariableDeclaratorContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclarator.
    def exitVariableDeclarator(self, ctx:JavaParser.VariableDeclaratorContext):
        pass


    # Enter a parse tree produced by JavaParser#qualifiedName.
    def enterQualifiedName(self, ctx:JavaParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by JavaParser#qualifiedName.
    def exitQualifiedName(self, ctx:JavaParser.QualifiedNameContext):
        pass


