from Number import Number, UndefinedError, ComplexUnimplemented
from Number import PreDefs
from typing import Final
import time
from pprint import pprint
from Number import Sign

# short name to reduce clutter
n_ = PreDefs()


def assert_val_equal(a):
    if a != "equal":
        raise AssertionError(f"{a} is not \"equal\"")


def assert_equal(a, b):
    if a != b:
        raise AssertionError(f"{a} is not {b}")


def standard_tests():
    # Base representation
    # Test equality of zeros
    a = n_.zero
    b = n_.zero
    assert_val_equal(a.compare(b))

    # We can't test inequality until we can make a different number!

# Base operation, increment
    # Verify 0 incremented is 1 > 0
    assert_equal(n_.one.compare(n_.zero), "greater")

    assert_equal(n_.zero.compare(n_.one), "less")

# Inc
    negative_zero = n_.neg_one.inc()
    assert_val_equal(negative_zero.compare(Number(n_.zero, Sign.neg)))
    pos_one = negative_zero.inc()
    assert_val_equal(pos_one.compare(n_.one))


# Addition
    print("Running Addition Tests")
    # Basic... 1 + 2 = 3
    one: Final = Number().inc()
    two: Final = Number().inc().inc()
    three: Final = Number().inc().inc().inc()
    assert_val_equal(three.compare(one.add(two)))

    # identity is 0
    one_b = one.add(Number())
    assert_val_equal(one_b.compare(one))

    # Commutivity... 1 + 2 = 2 + 1
    three_fwd = one.add(two)
    three_rev = two.add(one)
    assert_val_equal(three_fwd.compare(three_rev))

    # Associativity... (1 + 2) + 3 = 1 + (2 + 3)
    six = one.add(two).add(three)
    six_b = one.add(two.add(three))
    assert_val_equal(six.compare(six_b))

    #Negative Numbers
    # 1 + -1 = 0
    assert_val_equal(n_.one.add(n_.neg_one).compare(n_.zero))
    # -1 + -1 = -2
    assert_val_equal(n_.neg_one.add(n_.neg_one).compare(Number(n_.two, Sign.neg)))
    # -1 + 4 = 3
    assert_val_equal(n_.neg_one.add(n_.four).compare(Number(n_.three, Sign.pos)))



# Multiplication
    print("Running Multiplication Tests")
    # Verify multiplication... 2 * 3 = 6
    assert_val_equal(n_.two.mul(n_.three).compare(n_.six))

    # Multiplication by Zero... 2 * 0 = 0
    two_times_zero: Final = n_.two.mul(n_.zero)
    assert_val_equal(two_times_zero.compare(n_.zero))

    # identity... 2 * 1 = 2
    two_times_one = two.mul(n_.one)
    assert_val_equal(two_times_one.compare(two))

    # Commutivity... 2 * 6 = 6 * 1
    twelve: Final = n_.two.mul(n_.six)
    twelve_b = n_.six.mul(n_.two)
    assert_val_equal(twelve.compare(twelve_b))

    # Associativity
    thirtysix: Final = n_.two.mul(n_.three).mul(n_.six)
    thirtysix_b = n_.two.mul(n_.three.mul(n_.six))
    assert_val_equal(thirtysix.compare(thirtysix_b))

    # Negative Numbers
    neg_zero: Final = Number(n_.zero, Sign.neg)
    # -0 * 0 = -0
    assert_val_equal(neg_zero.mul(n_.zero).compare(neg_zero))
    # -0 * -0 = 0
    assert_val_equal(neg_zero.mul(neg_zero).compare(n_.zero))
    # 0 * -1 = 0
    assert_val_equal(n_.zero.mul(n_.neg_one).compare(neg_zero))
    # -0 * -1 = 0
    assert_val_equal(neg_zero.mul(n_.neg_one).compare(n_.zero))
    # -1 * 1 = -1
    assert_val_equal(n_.neg_one.mul(n_.one).compare(n_.neg_one))
    # -1 * -1 = 1
    assert_val_equal(n_.neg_one.mul(n_.neg_one).compare(n_.one))
    # -1 * 5 = -5
    assert_val_equal(n_.neg_one.mul(n_.five).compare(Number(n_.five, Sign.neg)))
    # -2 * -5 = 10
    neg_two: Final = n_.neg_one.dec()
    neg_five = n_.five.mul(n_.neg_one)
    assert_val_equal(neg_two.mul(neg_five).compare(Number(n_.ten)))


# Power
    print("Running Power Tests")

    # 0^0 = 1
    # In other definitions of power, 0^N is always zero.
    # However, we have defined power to have the value before any iteration be 1.
    # this results in 0^0 = 1.
    assert_val_equal(n_.one.compare(n_.zero.pow(n_.zero)))

    # 0^1 = 0
    assert_val_equal(n_.zero.compare(n_.zero.pow(n_.one)))

    # 1^0 = 1
    assert_val_equal(n_.one.compare(n_.one.pow(n_.zero)))

    # 1^1 = 1
    assert_val_equal(n_.one.compare(n_.one.pow(n_.one)))

    # Basic... 2^3 = 8
    assert_val_equal(n_.eight.compare(n_.two.pow(n_.three)))

    # Zero power... 2^0 = 1
    two_to_zero = n_.two.pow(n_.zero)
    assert_val_equal(two_to_zero.compare(n_.one))

    #negative expoenents
    # -1^2 = 1
    assert_val_equal(n_.neg_one.pow(n_.two).compare(n_.one))
    # -2^3 = -8
    assert_val_equal(Number(n_.two, Sign.neg).pow(n_.three).compare(Number(n_.eight, Sign.neg)))
    # 2^-3 = 1/8
    two_to_neg_three = n_.two.pow(Number(n_.three, Sign.neg))
    one_eighth = n_.one.div(n_.eight)
    assert_val_equal(two_to_neg_three[0].compare(one_eighth[0]))
    assert_val_equal(two_to_neg_three[1].compare(one_eighth[1]))



# Tetration
    print("Running Tetration Tests")
    # 2 ^^ 3 = 16
    sixteen: Final = n_.two.pow(n_.two).pow(n_.two)
    two_tetra_three = n_.two.tetr(n_.three)
    assert_val_equal(sixteen.compare(two_tetra_three))

    # X ^^ 0 = 1, so we'll just use sixteen, 0 = 1
    sixteen_tetrated_zero = sixteen.tetr(n_.zero)
    assert_val_equal(sixteen_tetrated_zero.compare(n_.one))

    # X ^^ (-N) = 1/(X^^N)
    two_tetra_neg_three = n_.two.tetr(n_.three.mul(n_.neg_one))
    assert_val_equal(sixteen.compare(two_tetra_three))



# decrement
    print("Running Decrement Tests")
    assert_val_equal(n_.one.dec().compare(n_.zero))
    assert_val_equal(n_.three.dec().compare(n_.two))
    assert_equal(n_.four.dec().compare(n_.two), "greater")

    neg_one = n_.zero.dec()
    assert_equal(neg_one.compare(n_.neg_one), "equal")


# subtraction
    print("Running Subtraction Tests")
    # 0-0=0
    assert_val_equal(n_.zero.sub(n_.zero).compare(n_.zero))
    # 1-0=1
    assert_val_equal(n_.one.sub(n_.zero).compare(n_.one))
    # 1-1=0
    assert_val_equal(n_.one.sub(n_.one).compare(n_.zero))
    # 2-2=0
    assert_val_equal(n_.one.sub(n_.one).compare(n_.zero))
    # 3-1=2
    assert_val_equal(n_.three.sub(n_.one).compare(n_.two))

    #negative numbers
    # 1-2=-1
    neg_one = n_.one.sub(n_.two)
    assert_val_equal(neg_one.compare(Number(n_.one, Sign.neg)))
    # 0-1=-1
    neg_one = n_.zero.sub(n_.one)
    assert_val_equal(neg_one.compare(Number(n_.one, Sign.neg)))
    # 10-20=-10
    neg_ten = n_.ten.sub(n_.ten.mul(n_.two))
    assert_val_equal(neg_ten.compare(Number(n_.ten, Sign.neg)))


    # inverse operation tests
    # (x + y) - y = x
    # (5 + 3) - 3 = x
    assert_val_equal(n_.five.add(n_.three).sub(n_.three).compare(n_.five))
    # (x + y) - x = y
    # (5 + 3) - 5 = 3
    assert_val_equal(n_.five.add(n_.three).sub(n_.five).compare(n_.three))

# division
    print("Running Division Tests")
    # 0/1 = 0,1
    zero_oneths = n_.zero.div(n_.one)
    assert_val_equal(zero_oneths[0].compare(n_.zero))
    assert_val_equal(zero_oneths[1].compare(n_.zero))
    # 1/1 = 1,0
    one_oneths = n_.one.div(n_.one)
    assert_val_equal(one_oneths[0].compare(n_.one))
    assert_val_equal(one_oneths[1].compare(n_.zero))
    # 1/2 = 0,1
    one_half = n_.one.div(n_.two)
    assert_val_equal(one_half[0].compare(n_.zero))
    assert_val_equal(one_half[1].compare(n_.one))
    # 2/2 = 1,0
    assert_val_equal(n_.two.div(n_.two)[0].compare(n_.one))
    assert_val_equal(n_.two.div(n_.two)[1].compare(n_.zero))
    # 4/2 = 2,0
    assert_val_equal(n_.four.div(n_.two)[0].compare(n_.two))
    assert_val_equal(n_.four.div(n_.two)[1].compare(n_.zero))

    # 4/3 = 1,1
    assert_val_equal(n_.four.div(n_.three)[0].compare(n_.one))
    assert_val_equal(n_.four.div(n_.three)[1].compare(n_.one))

    # 8/3 = 2,2
    assert_val_equal(n_.eight.div(n_.three)[0].compare(n_.two))
    assert_val_equal(n_.eight.div(n_.three)[1].compare(n_.two))

    # 4/5 = 0,4
    five: Final = n_.two.add(n_.two).inc()
    assert_val_equal(n_.four.div(five)[0].compare(n_.zero))
    assert_val_equal(n_.four.div(five)[1].compare(n_.four))

    # 1/8 = 0,1
    assert_val_equal(n_.one.div(n_.eight)[0].compare(n_.zero))
    assert_val_equal(n_.one.div(n_.eight)[1].compare(n_.one))


    # 1/0 = by definition, returns DivideByZeroError
    no_except = True
    try:
        n_.one.div(n_.zero)
    except ZeroDivisionError:
        no_except = False
    assert (not no_except)

    # 1/-1 = -1, 0
    assert_val_equal(n_.one.div(n_.neg_one)[0].compare(n_.neg_one))
    assert_val_equal(n_.one.div(n_.neg_one)[1].compare(n_.zero))

    # -1/-1 = 1, 0
    assert_val_equal(n_.neg_one.div(n_.neg_one)[0].compare(n_.one))
    assert_val_equal(n_.neg_one.div(n_.neg_one)[1].compare(n_.zero))

    # -0/0 = divide_by_zero
    no_except = True
    try:
        n_.neg_one.mul(neg_zero).div(n_.zero)
    except ZeroDivisionError:
        no_except = False
    assert (not no_except)

    # -0/-1 = 0, 0
    assert_val_equal(neg_zero.div(n_.neg_one)[0].compare(n_.zero))
    assert_val_equal(neg_zero.div(n_.neg_one)[0].compare(n_.zero))
    # -0/1 = -0, 0
    assert_val_equal(neg_zero.div(n_.one)[0].compare(neg_zero))
    assert_val_equal(neg_zero.div(n_.one)[1].compare(n_.zero))
    # 0/-1 = -0, 0
    assert_val_equal(n_.zero.div(n_.neg_one)[0].compare(neg_zero))
    assert_val_equal(n_.zero.div(n_.neg_one)[1].compare(n_.zero))

    # inverse operation tests
    # (x * y)/x = y rem 0
    # (5 * 3)/5 = 3 rem 0
    assert_val_equal(n_.five.mul(n_.three).div(n_.five)[0].compare(n_.three))
    assert_val_equal(n_.five.mul(n_.three).div(n_.five)[1].compare(n_.zero))
    # (x * y)/y = x rem 0
    # (5 * 3)/3 = 5 rem 0
    assert_val_equal(n_.five.mul(n_.three).div(n_.three)[0].compare(n_.five))
    assert_val_equal(n_.five.mul(n_.three).div(n_.three)[1].compare(n_.zero))

# log
    print("Running Log Tests")

    # Anythig to the zero is one
    # 0^0 = 1
    # logˇ0(1) = 0
    one_log_base_0 = n_.one.log(n_.zero)
    assert_val_equal(one_log_base_0[0].compare(n_.zero))
    assert_val_equal(one_log_base_0[1].compare(n_.zero))

    # 0^(pos number) = 0
    # logˇ0(0) = any pos, mant=0
    zero_log_base_zero = n_.zero.log(n_.zero)
    assert_val_equal(zero_log_base_zero[0].compare(n_.pos_even_not_zero))
    assert_val_equal(zero_log_base_zero[1].compare(n_.zero))


    # 0^x = 1
    # logˇ0(1) = 0, mant=0
    log_one_base_zero = n_.one.log(n_.zero)
    assert_val_equal(log_one_base_zero[0].compare(n_.zero))
    assert_val_equal(log_one_base_zero[1].compare(n_.zero))

    # log base 0 is undefined for every value other than 0
    # logˇ0(2) = undefined
    saw_exception = False
    try:
        n_.two.log(n_.zero)
    except UndefinedError as e:
        saw_exception = True
    assert(saw_exception)

    # logˇ2(0) = undefined
    saw_exception = False
    try:
        n_.zero.log(n_.two)
    except UndefinedError as e:
        saw_exception = True
    assert(saw_exception)


    # logˇ1(1) = any_value!, mant=0
    assert_val_equal(n_.one.log(n_.one)[0].compare(n_.any))
    assert_val_equal(n_.one.log(n_.one)[1].compare(n_.zero))

    # logˇ1(2) = undefined
    saw_exception = False
    try:
        n_.two.log(n_.one)[0].compare(n_.one)
    except UndefinedError as e:
        saw_exception = True
    assert(saw_exception)

    # logˇ2(2) = 1, mant=0
    two_log_two = n_.two.log(n_.two)
    assert_val_equal(two_log_two[0].compare(n_.one))
    assert_val_equal(two_log_two[1].compare(n_.zero))

    # logˇ2(4) = 2, mant=0
    assert_val_equal(n_.four.log(n_.two)[0].compare(n_.two))
    assert_val_equal(n_.four.log(n_.two)[1].compare(n_.zero))

    # logˇ2(8) = 3, mant=0
    assert_val_equal(n_.eight.log(n_.two)[0].compare(n_.three))
    assert_val_equal(n_.eight.log(n_.two)[1].compare(n_.zero))

    # logˇ2(15) = 3, mant=7
    fifteen: Final = n_.two.mul(n_.two).inc().mul(n_.three)
    fifteen_log_2 = fifteen.log(n_.two)
    assert_val_equal(fifteen_log_2[0].compare(n_.three))
    assert_val_equal(fifteen_log_2[1].compare(n_.seven))

    # logˇ3(15) = 2, mant=6
    assert_val_equal(fifteen.log(n_.three)[0].compare(n_.two))
    assert_val_equal(fifteen.log(n_.three)[1].compare(n_.six))

    # logˇ4(15) = 1, mant=11
    assert_val_equal(fifteen.log(n_.four)[0].compare(n_.one))
    assert_val_equal(fifteen.log(n_.four)[1].compare(n_.ten.inc()))


    # -0^x = 0
    # logˇ-0(0) = x, mant=0
    # x = any pos even except 0
    zero_log_base_neg_zero = n_.zero.log(neg_zero)
    assert_val_equal(zero_log_base_neg_zero[0].compare(n_.pos_even_not_zero))
    assert_val_equal(zero_log_base_neg_zero[1].compare(n_.zero))

    # 0^x = -0
    # logˇ0(-0) = x
    # x is undefined
    saw_exception = False
    try:
        neg_zero.log(n_.zero)
    except UndefinedError as e:
        saw_exception = True
    assert(saw_exception)


    # logˇ2(0) = undefined
    saw_exception = False
    try:
        n_.two.log(n_.zero)
    except UndefinedError as e:
        saw_exception = True
    assert(saw_exception)


    # logˇ-1(1) = any_even, mant=0
    log_one_base_neg_one = n_.one.log(n_.neg_one)
    assert_val_equal(log_one_base_neg_one[0].compare(n_.any_even))
    assert_val_equal(log_one_base_neg_one[1].compare(n_.zero))

    # logˇ-1(-1) = any_odd, mant=0
    log_neg_one_base_neg_one = n_.neg_one.log(n_.neg_one)
    assert_val_equal(log_neg_one_base_neg_one[0].compare(n_.any_odd))
    assert_val_equal(log_neg_one_base_neg_one[1].compare(n_.zero))

    # logˇ-2(4) = 2, mant=0
    log_b_neg_two_of_four = n_.four.log(neg_two)
    assert_val_equal(log_b_neg_two_of_four[0].compare(n_.two))
    assert_val_equal(log_b_neg_two_of_four[1].compare(n_.zero))

    # logˇ-2(8) = complex (not handled.. yet?!?!)
    threw_correct = False
    try:
        n_.eight.log(neg_two)
    except ComplexUnimplemented:
        threw_correct = True
    assert threw_correct




    # inverse operation test
    # general - logˇX(pow(X,Y) = Y, mant=0
    # logˇ5(pow(5,3) = 3, mant=0
    assert_val_equal(n_.three.pow(n_.five).log(n_.three)[0].compare(n_.five))
    assert_val_equal(n_.three.pow(n_.five).log(n_.three)[1].compare(n_.zero))

# superlog
    print("Running Superlog Tests")

    # superlogˇ0(0) = any, 0
    assert_val_equal(n_.zero.superlog(n_.zero)[0].compare(n_.any))
    assert_val_equal(n_.zero.superlog(n_.zero)[1].compare(n_.zero))

    # superlogˇ0(1) = UndefinedError
    saw_exception = False
    try:
        n_.one.superlog(n_.zero)
    except UndefinedError as e:
        saw_exception = True
    assert(saw_exception)

    # superlogˇ1(1) = any, 0
    one_superlog_base_one = n_.one.superlog(n_.one)
    assert_val_equal(one_superlog_base_one[0].compare(n_.any))
    assert_val_equal(one_superlog_base_one[1].compare(n_.zero))

    # superlogˇ1(-1) = any, 0
    saw_exception = False
    try:
        neg_one.superlog(n_.one)
    except UndefinedError as e:
        saw_exception = True
    assert(saw_exception)


    # superlogˇ-1(1) = n_.any_even, 0
    one_superlog_base_neg_one = n_.one.superlog(neg_one)
    assert_val_equal(one_superlog_base_neg_one[0].compare(n_.any_even))
    assert_val_equal(one_superlog_base_neg_one[1].compare(n_.zero))


    # superlogˇ1(3) = Undefined Error
    saw_exception = False
    try:
        n_.three.superlog(n_.one)
    except UndefinedError as e:
        saw_exception = True
    assert(saw_exception)


    # superlogˇ2(16) = 3, 0 (2^2^2 = 2^4 = 16)
    sixteen: Final = fifteen.inc()
    assert_val_equal(sixteen.superlog(n_.two)[0].compare(n_.three))
    assert_val_equal(sixteen.superlog(n_.two)[1].compare(n_.zero))

    # superlogˇ2(255) = 3, 23  (2^2^2 = 2^4 = 16... 255-16 = 239
    twofiftyfive: Final = sixteen.mul(sixteen).dec()
    twothirtynine: Final = twofiftyfive.sub(sixteen)
    assert_val_equal(twofiftyfive.superlog(n_.two)[0].compare(n_.three))
    assert_val_equal(twofiftyfive.superlog(n_.two)[1].compare(twothirtynine))



def time_tetration():
    results = {}
    count = 0
    height = n_.zero
    while True:
        start = time.time_ns()
        result = n_.two.tetr(height)
        duration = time.time_ns() - start
        results[count] = (duration, len(result.state))
        if count > 4:
            # Stop at 64K.  64K outside of debug mode is ~12s on my laptop.
            # Next would be 4GB.  Assuming runtime is linear vs size as this is just
            # adding more unary digits, that is ~5K un-digits/s.  4GB is ~850K seconds/
            # ~14K minutes/~238 hours/~4 days.  Small differences in implementations can push
            # this time down to barely measurable or unreasonably long for a unit test.
            break
        count += 1
        height = height.inc()
    print(f"Tetration stats:")
    pprint.pprint(results)


def algebraic_rules():
    X = n_.one
    Y = n_.two
    Z = n_.three

# Commutivity
    if True:
    # Commutivity over addition
        # X.add(Y) = Y.add(X)
        assert_val_equal(X.add(Y).compare(Y.add(X)))
    # Commutvity over multiplication
        # X.mul(Y) = Y.mul(X)
        assert_val_equal(X.mul(Y).compare(Y.mul(X)))

# Associativity
    if True:
    # Associativity over addition
        # X+Y+Z = X+Z+Y
        # X.add(Y).add(Z) =  X.add(Z).add(Y)
        assert_val_equal(X.add(Y).add(Z).compare(X.add(Z).add(Y)))
    # Associativity over multiplication
        # X*Y*Z = X*Z*Y
        # X.mul(Y).mul(Z) =  X.mul(Z).mul(Y)
        assert_val_equal(X.mul(Y).mul(Z).compare(X.mul(Z).mul(Y)))
    # Associativity over pow (conversion from chain application to inner application)
        # (X^Y)^Z = X^(Y*Z)
        # X.pow(Y).pow(Z) =  X.pow(Y.mul(Z))
        assert_val_equal(X.pow(Y).pow(Z).compare(X.pow(Z.mul(Y))))


# Distributivity
    if True:
    # Distributivity of addition and multiplication
        # (X+Y)Z = X*Z + Y*Z
        # X.add(Y).mul(Z) = X.mul(Z).add(Y.mul(Z))
        assert_val_equal(X.add(Y).mul(Z).compare(X.mul(Z).add(Y.mul(Z))))
    # Distributivity of addition and multiplication
        # (X*Y)^Z = X^Z * Y^Z
        # X.mul(Y).pow(Z) = X.pow(Z).mul(Y.pow(Z))
        assert_val_equal(X.mul(Y).pow(Z).compare(X.pow(Z).mul(Y.pow(Z))))

# Identities
    if True:
    # addition identity
        # X+0 = X
        # X.add(n_.zero) = X
        assert_val_equal(X.add(n_.zero).compare(X))
    # multiplication identity
        # X*1 = X
        # X.mul(n_.one) = X
        assert_val_equal(X.mul(n_.one).compare(X))
    # power identity
        # X^1 = X
        # X.pow(n_.one) = X
        assert_val_equal(X.pow(n_.one).compare(X))


if __name__ == '__main__':
    standard_tests()
    algebraic_rules()
    # time_tetration()
