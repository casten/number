from Number import Number
from Number import PreDefs
from Number_tests import assert_val_equal
import copy


n_ = PreDefs()

"""
Expression = Value, (None | Operation)
Value = Number | Variable
Operation = (Operator, Expression)
"""



class Operator:
    operators = {
        "inc": Number.inc,
        "add": Number.add,
        "mul": Number.mul,
        "pow": Number.pow,
        "tetr": Number.tetr,
        "dec": Number.dec,
        "sub": Number.sub,
        "div": Number.div,
        "log": Number.log,
        "superlog": Number.superlog
    }
    standard_map = {
        "add": "+",
        "mul": "*",
        "pow": "^",
        "tetr": "^^",
        "sub": "-",
        "div": "/",
        "log": "log",
        "superlog": "slog"
    }

    def apply(self, number, expression):
        return self.operators[self.name](number, expression)

    def __init__(self, operator):
        self.name = operator

    def compare(self, operator):
        return "equal" if self.name == operator.name else "not equal"

    def repr_standard(self):
        return self.standard_map[self.name]


class Operation:
    def __init__(self, operator, expression):
        if not isinstance(operator, Operator):
            raise Exception("The first param of Operation must be an Operator")
        if not isinstance(expression, Expression):
            raise Exception("The second param of Operation must be an Expression")
        self.operator = operator
        self.expression = expression

    def compare(self, operation2):
        if self.operator.name != operation2.operator.name:
            return "not equal"
        if self.expression.compare(operation2.expression) == "not equal":
            return "not equal"
        return "equal"

    def repr_standard(self):
        if isinstance(self.expression, Expression) and self.expression.operation is not None:
            if self.expression.operation.expression is not None:
                return f" {self.operator.repr_standard()} ({self.expression.repr_standard()})"
        return f" {self.operator.repr_standard()} {self.expression.repr_standard()}"


class Variable:
    def __init__(self, symbol):
        self._symbol = symbol

    def compare(self, var2):
        if self._symbol == var2._symbol:
            return "equal"
        return "not equal"

    def repr_standard(self):
        return self._symbol



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
    def __init__(self, value, operation=None):
        self.value = value
        self.operation = operation

    def copy(self):
        return copy.deepcopy(self)

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
        new_exp = Expression(self.value, None)
        new_exp.tail().operation = operation
        return new_exp

    def subst(self, var, replacement):
        #  Allows for substitution of a variable with another variable or number
        curr_term = self_copy = self.copy()
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
        return self_copy

    @staticmethod
    def can_collapse(value1, operator, value2):
        if isinstance(value1, Number):
            if isinstance(value2, Number):
                if operator.name in ["add", "mul", "pow", "tetr", "sub"]:
                    return True
        if isinstance(value1, Variable):
            if isinstance(value2, Variable):
                if value1.compare(value2):
                    match operator.name:
                        case "add" | "mul" | "pow" | "sub" | "div" :
                            return True
                    return False
        return False


    @staticmethod
    def collapse(first_value, operator, next_value):
        # Apply operators to numbers that result in the same output size, e.g.
        #  add, mul, pow, tetr, sub
        if isinstance(first_value, Number):
            if operator.name in ["add", "mul", "pow", "tetr", "sub"]:
                return operator.apply(first_value, next_value)
        # Collapse variables
        if isinstance(first_value, Variable):
            promoters = {"add": "mul",
                         "mul": "pow",
                         "pow": "tetr"}
            if operator.name in promoters:
                new_operator = Operator(promoters[operator.name])
                return Expression(first_value, None).chain(Operation(new_operator, Expression(n_.two)))
            else:
                # otherwise it is an identity
                idents = {"sub": n_.zero,
                          "div": n_.one,
                          "log": n_.one}
                return Expression(idents[operator.name])
        raise Exception("Collapse called on non-collapsable elements")


    def simplify(self):
        # Evaluation simplifies chains of terms using algebraic rules.
        # First pass adds and multiplies all adjacent numbers.
        # We'll also count the number of variables in case there are none left.

        curr_exp = self_copy = self.copy()
        next_operation = None

        while True:
            # If no operation, we're done
            if curr_exp.operation is None:
                break
            # Look for and collapse adjacent numeric operations
            if curr_exp.operation.expression is None:
                raise Exception("Error! Operation has no expression.")
            # Get the next expression to check for possible simplification
            next_exp = curr_exp.operation.expression
            next_operation = next_exp.operation
            if self_copy.can_collapse(curr_exp.value, curr_exp.operation.operator, next_exp.value):
                result = self_copy.collapse(curr_exp.value, curr_exp.operation.operator, next_exp.value)
                # We've got the replacement for the current node.
                # Now replace the parent operation to point to the new collpased expression
                if isinstance(result, Expression):
                    # When an expression is returned, we'll have a new expression formed
                    # in the chain to plug it in, e.g.
                    # x.add(x).mul(3) will collapse to
                    # x.mul(2).mul(3)
                    curr_exp.operation = result.operation
                    curr_exp.operation.expression.operation = next_operation
                else:
                    curr_exp.operation = next_operation
                    curr_exp.value = result
                # since we had a collapse, reset to begin and try again
                curr_exp = self_copy
                continue
            if next_operation is None:
                break  # No more operations, so we've reached the end
            # We weren't able to collapse the current and next values, so march onward!
            if isinstance(next_operation.expression, Expression):
                curr_exp = next_operation.expression
            else:
                curr_exp = next_operation.value
        return self_copy

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

    def repr_standard(self):
        if self.operation is None:
            return self.value.repr_standard()
        else:
            return self.value.repr_standard() + self.operation.repr_standard()


def expression_unit_test():

    # Expression with one number, no operation
    # Subst should do nothing
    ex = Expression(n_.zero, None)
    ex = ex.subst(Variable("X"), n_.one)
    print(ex.repr_standard())
    assert_val_equal(ex.value.compare(n_.zero))

    # Expression with one variable, no operation
    # Define a term with just X and replace X with 1.
    ex = Expression(Variable("X"), None)
    ex = ex.subst(Variable("X"), n_.one)
    print(ex.repr_standard())
    assert_val_equal(ex.value.compare(n_.one))

    # Basic Eval test
    ex = Expression(Variable("X"), None)
    ex = ex.subst(Variable("X"), n_.one)
    print(ex.repr_standard())
    assert_val_equal(ex.simplify().value.compare(n_.one))

    # X + 1, x=1
    ex = Expression(Variable("X"), Operation(Operator("add"), Expression(n_.one)))
    ex = ex.subst(Variable("X"), n_.one)
    print(ex.repr_standard())
    assert_val_equal(ex.simplify().value.compare(n_.two))

    # Using chain syntax to attach separate expressions with an operation
    # X + X, x=1
    ex = Expression(Variable("X"))
    ex2 = Expression(Variable("X"))
    oper_add_ex2 = Operation(Operator("add"), ex2)
    ex = ex.chain(oper_add_ex2)
    print(ex.repr_standard())
    # This will simply the expression by merging the X+X to become a single X * 2
    ex = ex.simplify()
    # Verify simplification
    ex2 = Expression(Variable("X"), Operation(Operator("mul"), Expression(n_.two)))
    assert_val_equal(ex.compare(ex2))
    ex = ex.subst(Variable("X"), n_.one)
    ex = ex.simplify()
    assert_val_equal(ex.value.compare(n_.two))
    print(ex.repr_standard())

    # Using chain syntax to attach separate expressions with an operation
    # X + 2 * (X+1)
    ex_x = Expression(Variable("X"))
    ex_xadd1 = Expression(Variable("X"), Operation(Operator("add"), Expression(n_.one)))
    ex_2times_ex_xadd1 = Expression(n_.two, Operation(Operator("mul"), ex_xadd1))
    ex_x = ex_x.chain(Operation(Operator("add"), ex_2times_ex_xadd1))
    print(ex_x.repr_standard())


if __name__ == "__main__":
    expression_unit_test()

