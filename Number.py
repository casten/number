"""
The following is a class and set of unit tests related to Hyperoperation.
A number class is implemented with a unary representation.
It implements increment/succession via python list addition of a single value.
Higher order operations are layered above up to and including tetration/hyper-4.

Notes about implementation:
* after inc, (add,mul,pow,tetr) are extremely similar with the exception of their
  initial condition.

References:
https://en.wikipedia.org/wiki/Hyperoperation
"""
from enum import Enum
from enum import auto
import copy


class UnderflowError(ArithmeticError):
    pass


class UndefinedError(ArithmeticError):
    pass


class ComplexUnimplemented(ArithmeticError):
    pass

class Value:
    pass


class Special(Value):
    class special_types(Enum):
        any = auto()
        any_even = auto()
        any_odd = auto()
        pos_even_not_zero = auto()

    def __init__(self, stype):
        if not isinstance(stype, self.special_types):
            raise Exception("To make a special, you must say the type, e.g. Special.types.any")
        self.stype = stype

    def compare(self, value):
        if not isinstance(value, Special):
            return "not equal"
        if value.stype == self.stype:
            return "equal"
        return "not equal"


# Helper with predefined numbers
class PreDefs:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        self.zero = Number()
        self.one = self.zero.inc()
        self.two = self.one.inc()
        self.three = self.one.add(self.two)
        self.four = self.two.add(self.two)
        self.five = self.two.add(self.three)
        self.six = self.three.add(self.three)
        self.six = self.three.add(self.three)
        self.seven = self.three.add(self.four)
        self.eight = self.four.add(self.four)
        self.nine = self.five.add(self.four)
        self.ten = self.five.add(self.five)

        self.neg_one = Number(self.one, Sign.neg)

        self.any = Special(Special.special_types.any)
        self.any_even = Special(Special.special_types.any_even)
        self.any_odd = Special(Special.special_types.any_odd)
        self.pos_even_not_zero = Special(Special.special_types.pos_even_not_zero)



class NumberState:
    def __init__(self, magnitude, sign):
        # default state is non-negative zero
        if isinstance(magnitude, Number):
            self._magnitude = magnitude.state.get_magnitude()
        elif not isinstance(magnitude, list):
            raise Exception("   NumberState requires either a Number or a Number.integer for the magnitude")
        else:
            self._magnitude = magnitude
        self._sign = sign

    def clone(self):
        return NumberState(self._magnitude, self._sign)

    def copy(self, state):
        if not isinstance(state, NumberState):
            raise Exception("You can only copy a NumberState")
        self._magnitude = state._magnitude
        self._sign = state._sign

    def compare_magnitude(self, comparand):
        for _ in iter(self.get_magnitude()):
            try:
                comparand.get_magnitude()[0]
                comparand = NumberState(comparand.get_magnitude()[1:], self._sign)
            except Exception as e:
                return "greater"
        try:
            comparand.get_magnitude()[0]
            return "less"
        except:
            return "equal"

    def compare(self, comparand):
        if not isinstance(comparand, NumberState):
            raise Exception("You can only compare a NumberState")

        if self._sign != comparand._sign:
            if self._sign == Sign.pos:
                return "greater"
            else:
                return "less"

        return self.compare_magnitude(comparand)

    def get_magnitude(self):
        return copy.copy(self._magnitude)

    def get_sign(self):
        return copy.copy(self._sign)


class Sign(Enum):
    pos = auto()
    neg = auto()


class Number(Value):
    """
    A number class with unary internal representation that attempts to implement
    arithmatic operations with minimal external functions.

    Member functions attempt to be functional in intent, but are implemented in an
    imperative style. (Because that is how I learned how to program?)
    """

    def __init__(self, copy_state=None, sign=Sign.pos):
        if not isinstance(sign, Sign):
            raise Exception("If you pass a second param, it must be a Sign")
        if None is copy_state:
            self._state = NumberState([], Sign.pos)  # Unary zero
        else:
            if isinstance(copy_state, Number):
                self._state = NumberState(copy_state._state.get_magnitude(), copy_state.state.get_sign())
                if sign is not None:
                    self.state._sign = sign
                return
            if not isinstance(copy_state, NumberState):
                raise Exception("Object passed into Number() must be a NumberState.")
            self._state = copy_state.clone()



    def clone(self):
        return copy.deepcopy(self)


    # Use a property to ensure the state is immutable
    @property
    def state(self):
        return self._state

    def inc(self):
        # Make a new number that is the previous list + a new element
        # (conscious effort to not use the + operator here even if it
        #  is just a cosmetic distinction)
        # special case 0.  0.inc() is always +1 independent of zero sign
        if len(self.state.get_magnitude()) == 0:
            return Number(NumberState(['x'], Sign.pos))
        if self.state.get_sign() == Sign.neg:
            return Number(NumberState(self.state.get_magnitude()[1:], Sign.neg))
        return Number(NumberState([*self.state.get_magnitude(), 'x'], Sign.pos))

    def add(self, b):
        if not isinstance(b, Number):
            raise Exception("You can only add by Numbers!")
        # 0th iteration is identity
        result = self.clone()
        for _ in b.state.get_magnitude():
            if b.state.get_sign() == Sign.pos:
                result = result.inc()
            else:
                result = result.dec()
        return result

    def mul(self, b):
        # 0th iteration is 0
        copy_self = self.clone()
        if not isinstance(b, Number):
            raise Exception("You can only mul by Numbers!")
        result = n_.zero.clone()
        for _ in b.state.get_magnitude():
            result = result.add(copy_self)
        if self._state.get_sign() == b.state.get_sign():
            result.state._sign = Sign.pos
        else:
            result.state._sign = Sign.neg
        return result

    def pow(self, b):
        if not isinstance(b, Number):
            raise Exception("You can only pow by Numbers!")
        result = n_.one.clone()
        for _ in b.state.get_magnitude():
            result = result.mul(self)
        if b.state.get_sign() == Sign.neg:
            return n_.one.div(result)
        return result

    def tetr(self, b):
        if not isinstance(b, Number):
            raise Exception("You can only tetr by Numbers!")
        # Stupid piecewise definition
        if b.compare(n_.zero) == "equal":
            # 0th iteration is 1
            return n_.one
        result = self.clone()
        once = True
        # For the non-zero tetration case, you loop b - 1 times.
        for _ in b.state.get_magnitude():
            if once:  # Skip the first so do one less
                once = False
                continue
            result = result.pow(self)
        return result

    def dec(self):
        self_copy = self.clone()
        if self.compare(n_.zero) == "equal":
            return n_.neg_one.clone()
        if self.state.get_sign() == Sign.pos:
            return Number(NumberState(self.state.get_magnitude()[1:], Sign.pos))
        else:
            return Number(NumberState(Number(self_copy, Sign.pos).inc(), Sign.neg))

    def sub(self, s):
        if not isinstance(s, Number):
            raise Exception("You can only subtract by Numbers!")
        result = self.clone()
        for _ in s.state.get_magnitude():
            if result.compare(n_.zero) == "equal":
                # We've exhausted the minuend, so flip the sign and start adding
                result = Number(NumberState(n_.one._state.get_magnitude(), Sign.neg))
                continue
            if s.state.get_sign() == Sign.pos:
                result = result.dec()
            else:
                result = result.inc()
        return result

    def div(self, denominator):
        if not isinstance(denominator, Number):
            raise Exception("You can only divide by Numbers!")
        numerator = Number(self.clone(), Sign.pos)
        divisions = n_.zero.clone()
        if denominator.compare(n_.zero) == "equal":
            raise ZeroDivisionError()
        sign = Sign.pos if self.state.get_sign() == denominator.state.get_sign() else Sign.neg
        while True:
            progress = n_.zero.clone()
            if numerator.state.compare_magnitude(n_.zero.state) == "equal":
                return Number(divisions, sign), progress
            for _ in denominator.state.get_magnitude():
                if numerator.state.compare_magnitude(n_.zero.state) == "equal":
                    return Number(divisions, sign), progress
                numerator = numerator.dec()
                progress = progress.inc()
            divisions = divisions.inc()

    #  This returns (magnitude, mantissa)
    #  But the currently returned mantissa may not be the best representation.
    #  It is the integer remainder of the next higher magnitude.
    #  As this is a closed form solution, it seems complete enough.
    def log(self, base):
        if not isinstance(base, Number):
            raise Exception("You can only log by base Numbers!")
        self_copy = self.clone()
        numerator = self.clone()
        if base.state.compare_magnitude(n_.zero.state) == "equal":
            if self.state.compare_magnitude(n_.zero.state) == "equal":
                if self.state.get_sign() == Sign.neg:
                    raise UndefinedError()
                else:
                    return n_.pos_even_not_zero, n_.zero
            if self.state.compare_magnitude(n_.one.state) == "equal":
                return n_.zero, n_.zero
            raise UndefinedError("0^N where N!=[0,1] is always zero, so log base N cannot be calculated.")
        if base.compare(n_.one) == "equal":
            if self.compare(n_.one) == "equal":
                return n_.any, n_.zero
            if self.compare(n_.neg_one) == "equal":
                raise ComplexUnimplemented
            raise UndefinedError()
        if base.compare(n_.neg_one) == "equal":
            if self.compare(n_.one) == "equal":
                return n_.any_even, n_.zero
            if self.compare(n_.neg_one) == "equal":
                return n_.any_odd, n_.zero
        if self.state.compare_magnitude(n_.zero.state) == "equal":
            # For log N for base B other than 0,1 (handled above)
            # given b^x=N  with N=0, there is no value for x where b^x can be 0
            raise UndefinedError()
        magnitude = n_.zero.clone()
        while True:
            if numerator.compare(n_.one) == "equal":
                remainder = self_copy.sub(base.pow(magnitude))
                return magnitude, remainder
            numerator, _ = numerator.div(base)
            if numerator.state.compare_magnitude(n_.zero.state) == "equal":
                pow_result = base.pow(magnitude)
                remainder = self_copy.sub(pow_result)
                if pow_result.state.get_sign() == Sign.neg:
                    raise ComplexUnimplemented
                return magnitude, remainder
            magnitude = magnitude.inc()


    def superlog(self, base):
        if not isinstance(base, Number):
            raise Exception("You can only superlog by base Numbers!")
        self_copy = self.clone()
        if base.compare(n_.zero) == "equal":
            if self.compare(n_.zero) == "equal":
                return n_.any, n_.zero
            raise UndefinedError()
        if base.state.compare_magnitude(n_.one.state) == "equal":
            if self.compare(n_.one) == "equal":
                if base.state.get_sign() == Sign.pos:
                    return n_.any, n_.zero
                else:
                    return n_.any_even, n_.zero
            raise UndefinedError()
        height = n_.one
        log_progress = self.clone()
        curr_base = base
        while True:
            log_progress, _ = log_progress.log(curr_base)
            if log_progress.compare(n_.zero) == "equal":
                remainder = self_copy.sub(base.tetr(height))
                return height, remainder
            height = height.inc()
            curr_base = curr_base.mul(curr_base)

    def compare(self, b):
        if isinstance(b, Special):
            return "not equal"
        if not isinstance(b, Number):
            raise Exception("You can only compare with Specials and Numbers!")
        return self._state.compare(b._state)

    def repr_standard(self):
        return str(len(self._state.get_magnitude()))

# short name to reduce clutter
n_ = PreDefs()
