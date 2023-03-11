from Number import Number
from Number import PreDefs
from Number_tests import assert_val_equal

n_ = PreDefs()


"""
Expression = Value, (None | Operation)
Value = Number | Variable
Operation = (Operator, Expression)
"""


class Operation:
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def compare(self, operation2):
        if self.operator != operation2.operator:
            return "not equal"
        if self.expression.compare(operation2.expression) == "not equal":
            return "not equal"
        return "equal"



class Variable:
    def __init__(self, symbol):
        self._symbol = symbol

    def compare(self, var2):
        if self._symbol == var2._symbol:
            return "equal"
        return "not equal"



class Expression:
    """
    An expression is a node with a value and an operation.
    An operation includes an operator and an Expression.
    The operation specifies the next operation in the chain and may be None.

    Some chain examples:
        (value, Operation=None)
        (value, Operation=(Operator, Expression))
            (Number, Operation=(add, Number))
                (three, Operation=(add, three))
        (value, Operation=(Operator, (value, Operation)))
            (Variable, Operation=(mul, (Number, Operation)))
                (Variable, Operation=(mul, (Number, (Operator, Expression)))))
                    (Variable, Operation=(mul, (Number, (add, Variable)))))
                    ('X', Operation=(mul, (three, (add, 'X')))))
    """
    def __init__(self, value, operation):
        self.value = value
        self.operation = operation

    def tail(self):
        curr_expr = self
        while curr_expr.operation is not None:
            if curr_expr.operation.expression is not None:
                curr_expr = curr_expr.operation.expression
            else:
                break
        return curr_expr


    def chain(self, operation):
        self.tail().operation = operation
        return self

    def subst(self, var, replacement):
        #  Allows for substitution of a variable with another variable or number
        curr_term = self
        # Go through operation chain and replace matching vars
        while True:
            if isinstance(curr_term.value, Variable):
                if curr_term.value.compare(var):
                    curr_term.value = replacement
            if isinstance(curr_term.value, Expression):
                curr_term.value.subst(var, replacement)
            elif curr_term.operation is None:
                break
            if isinstance(curr_term.operation.expression, Expression):
                curr_term = curr_term.operation.expression

    @staticmethod
    def can_collapse(value1, operator, value2):
        if isinstance(value1, Number):
            if isinstance(value2, Number):
                if operator in ["add", "mul", "pow", "tetr", "sub"]:
                    return True
        if isinstance(value1, Variable):
            if isinstance(value2, Variable):
                if value1.compare(value2):
                    match operator:
                        case "add" | "mul" |"pow" | "sub" |"div" :
                            return True
                    return False
        return False

    @staticmethod
    def _apply(number, operator, expression):
        if operator == "inc":
            return number.inc()
        if operator == "add":
            return number.add(expression)
        if operator == "mul":
            return number.mul(expression)
        if operator == "pow":
            return number.pow(expression)
        if operator == "tetr":
            return number.tetr(expression)
        if operator == "dec":
            return number.dec()
        if operator == "sub":
            return number.sub(expression)
        if operator == "div":
            return number.div(expression)
        if operator == "log":
            return number.log(expression)
        if operator == "superlog":
            return number.superlog(expression)

        raise Exception(f"Unknown operator: {operator}")

    @staticmethod
    def collapse(first_value, operator, next_value):
        # Apply operators to numbers that result in the same output size, e.g.
        #  add, mul, pow, tetr, sub
        if isinstance(first_value, Number):
            if operator in ["add", "mul", "pow", "tetr", "sub"]:
                return Expression._apply(first_value, operator, next_value)
        # Collapse variables
        if isinstance(first_value, Variable):
            promoters = {"add": "mul",
                         "mul": "pow",
                         "pow": "tetr"}
            if operator in promoters:
                return Expression(first_value, None).chain(Operation(promoters[operator], Expression(n_.two, None)))
            else:
                # otherwise it is an identity
                idents = {"sub": n_.zero,
                          "div": n_.one,
                          "log": n_.one}
                return Expression(idents[operator])
        raise Exception("Collapse called on non-collapsable elements")


    def simplify(self):
        # Evaluation simplifies chains of terms using algebraic rules.
        # First pass adds and multiplies all adjacent numbers.
        # We'll also count the number of variables in case there are none left.
        curr_exp = self
        next_oper = None

        while True:
            # Collapse repeated numeric operations
            if curr_exp.operation is not None:
                if curr_exp.operation.expression is not None:
                    next_exp = curr_exp.operation.expression
                    next_oper = next_exp.operation
                    if self.can_collapse(curr_exp.value, curr_exp.operation.operator, next_exp.value):
                        result = self.collapse(curr_exp.value, curr_exp.operation.operator, next_exp.value)
                        # We've got the replacement for the current node.
                        # Now replace the parent operation to point to the new collpased expression
                        if isinstance(result, Expression):
                            # When an expression is returned, we'll have a new expression formed
                            # in the chain to plug it in, e.g.
                            # x.add(x).mul(3) will collapse to
                            # x.mul(2).mul(3)
                            curr_exp.operation = result.operation
                            curr_exp.operation.expression.operation = next_oper
                        else:
                            curr_exp.operation = next_oper
                            curr_exp.value = result
                        curr_exp = self
                        continue  # since we had a collapse, go through again to try another
                if next_oper is None:
                    break
                curr_exp = next_oper.value
            else:
                break
        return self

    def compare(self, expr2):
        if not isinstance(expr2, Expression):
            raise Exception("You can only compare an expression to another expression")

        # Compare types of expression components
        if not isinstance(self, type(expr2)):
            return "not equal"
        if not isinstance(self.value, type(expr2.value)):
            return "not equal"
        if not isinstance(self.operation, type(expr2.operation)):
            return "not equal"
        # The expression types match, so start comparing
        if isinstance(self.value, Variable):
            if self.value.compare(expr2.value) != "equal":
                return "not equal"
        if isinstance(self.value, Number):
            if self.value.compare(expr2.value) != "equal":
                return "not equal"
        if self.operation is None or expr2.operation is None:
            if self.operation is not expr2.operation:
                return "not equal"
        else:
            if self.operation.compare(expr2.operation) != "equal":
                return "not equal"

        # Everything matches so far, so continue down the chain
        if isinstance(self.value, Expression):
            return self.value.compare(expr2.value)

        # Everything matches, so return True
        return "equal"



def expression_unit_test():
    # Expression with one number, no operation
    # Subst should do nothing
    ex = Expression(n_.zero, None)
    ex.subst(Variable("X"), n_.one)
    assert_val_equal(ex.value.compare(n_.zero))

    # Expression with one variable, no operation
    # Define a term with just X and replace X with 1.
    ex = Expression(Variable("X"), None)
    ex.subst(Variable("X"), n_.one)
    assert_val_equal(ex.value.compare(n_.one))

    # Basic Eval test
    ex = Expression(Variable("X"), None)
    ex.subst(Variable("X"), n_.one)
    assert_val_equal(ex.simplify().value.compare(n_.one))

    # X + 1, x=1
    ex = Expression(Variable("X"), Operation("add", Expression(n_.one, None)))
    ex.subst(Variable("X"), n_.one)
    assert_val_equal(ex.simplify().value.compare(n_.two))

    # Using chain syntax to attach separate expressions with an operation
    # X + X, x=1
    ex = Expression(Variable("X"), None)
    ex2 = Expression(Variable("X"), None)
    oper_add_ex2 = Operation("add", ex2)
    ex.chain(oper_add_ex2)
    # This will simply the expression by merging the X+X to become a single X * 2
    ex.simplify()
    # Verify simplification
    assert_val_equal(ex.compare(Expression(Variable("X"), Operation("mul", Expression(n_.two, None)))))
    ex.subst(Variable("X"), n_.one)
    ex.simplify()
    assert_val_equal(ex.value.compare(n_.two))
