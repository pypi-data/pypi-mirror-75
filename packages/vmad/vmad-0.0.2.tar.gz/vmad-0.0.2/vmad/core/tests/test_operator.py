from __future__ import print_function

from pprint import pprint
from vmad.core.operator import operator, ZeroGradient
from vmad.core.model import Builder
import pytest

@operator
class error_on_grad:
    ain = 'x'
    aout = 'y'

    def apl(node, x):
        return x

    def vjp(node, _y):
        raise AssertionError("shall not reach here")

    def jvp(node, x_):
        raise AssertionError("shall not reach here")

@operator
class error:
    ain = 'x'
    aout = 'y'

    def apl(node, x):
        raise AssertionError("shall not reach here")

    def vjp(node, _y):
        raise AssertionError("shall not reach here")

    def jvp(node, x_):
        raise AssertionError("shall not reach here")

def test_operator_zero():

    with Builder() as m:
        a = m.input('a')
        t1 = error_on_grad(x=a)
        m.output(c=t1)

    init = dict(a=3)

    c, tape = m.compute(init=init, vout='c', return_tape=True)
    assert c == 3

    vjp = tape.get_vjp()
    init = dict(_c=ZeroGradient)
    _a = vjp.compute(init=init, vout='_a', monitor=print)
    assert _a == 0

    jvp = tape.get_jvp()
    init = dict(a_=ZeroGradient)
    c_ = jvp.compute(init=init, vout='c_', monitor=print)
    assert c_ == 0

def test_operator_multiple():
    @operator
    class with_defaults:
        ain = [('x', '*')]
        aout = 'y'

        def apl(node, x): return x
        def vjp(node, _y): return _y
        def jvp(node, x_): return x_

    @operator
    class with_defaults:
        ain = [('x', '*'), 'y']
        aout = 'y'

        def apl(node, x, y): return x
        def vjp(node, _y): return _y, _y
        def jvp(node, x_, y_): return x_, y_

    @operator
    class with_defaults:
        ain = 'x', 'y'
        aout = 'y'

        def apl(node, x, y): return x
        def vjp(node, _y): return _y, _y
        def jvp(node, x_, y_): return x_, y_


def test_operator_defaults():
    @operator
    class with_defaults:
        ain = 'x'
        aout = 'y'

        def apl(node, x, defaults=False):
            assert defaults == False
            return x

        def vjp(node, _y, defaults=False):
            assert defaults == False
            return _y

        def jvp(node, x_, defaults=False):
            assert defaults == False
            return x_

    with Builder() as m:
        a = m.input('a')
        t1 = with_defaults(x=a)
        m.output(c=t1)

    init = dict(a=3)

    c, tape = m.compute(init=init, vout='c', return_tape=True)
    assert c == 3

    vjp = tape.get_vjp()
    init = dict(_c=1)
    _a = vjp.compute(init=init, vout='_a', monitor=print)
    assert _a == 1

    jvp = tape.get_jvp()
    init = dict(a_=1)
    c_ = jvp.compute(init=init, vout='c_', monitor=print)
    assert c_ == 1

def test_operator_skip_unused():

    with Builder() as m:
        a = m.input('a')
        t1 = error(x=a)
        m.output(c=a)

    init = dict(a=3)

    c, tape = m.compute(init=init, vout='c', return_tape=True)
    assert c == 3

    vjp = tape.get_vjp()
    init = dict(_c=0)
    _a = vjp.compute(init=init, vout='_a', monitor=print)
    assert _a == 0

    jvp = tape.get_jvp()
    init = dict(a_=0)
    c_ = jvp.compute(init=init, vout='c_', monitor=print)
    assert c_ == 0

import numpy
@operator
class split:
    ain = 'x'
    aout = 'args'

    def apl(node, x, axis):
        return [numpy.take(x, i, axis=axis) for i in range(numpy.shape(x)[axis])]

    def vjp(node, _args, axis):
        return numpy.stack(_args, axis=axis)

    def jvp(node, x_, axis):
        return [numpy.take(x_, i, axis=axis) for i in range(numpy.shape(x_)[axis])]

@operator
class stack:
    ain = 'args'
    aout = 'y'

    def apl(node, args, axis):
        return numpy.stack(args, axis=axis)

    def vjp(node, _y, args, axis):
        return [numpy.take(_y, i, axis=axis) for i in range(numpy.shape(_y)[axis])]

    def jvp(node, args_, args, axis):
        return numpy.stack(args_, axis)

@operator
class zero_jac:
    ain = 'args'
    aout = 'y'

    def apl(node, args):
        return dict(y=3, nargs=len(args))

    def vjp(node, nargs):
        return ZeroGradient

    def jvp(node, nargs):
        return ZeroGradient



def test_operator_list_in():
    from numpy.testing import assert_array_equal

    with Builder() as m:
        a = m.input('a')
        t = stack(args=[a, a, a], axis=1)
        m.output(c=t)

    init = dict(a=[1, 2])

    c, tape = m.compute(init=init, vout='c', return_tape=True)
    assert_array_equal(c, [[1, 1, 1], [2, 2, 2]])

    vjp = tape.get_vjp()
    init = dict(_c=[[1, 1, 1], [1, 1, 1]])
    _a = vjp.compute(init=init, vout='_a', monitor=print)

    assert_array_equal(_a, [3, 3])

    jvp = tape.get_jvp()
    init = dict(a_=[1, 1])
    c_ = jvp.compute(init=init, vout='c_', monitor=print)

    assert_array_equal(c_, [[1, 1, 1], [1, 1, 1]])

# This was based on VHBoehm and Maxelee's test case on stdlib.eval
# failure with a list input in MADLens
def test_operator_list_with_zero_vjp():
    with Builder() as m:
        value = m.input('value')
        r = zero_jac([value])
        m.output(my_array=r)

    init = dict(value=1)
    my_array, tape = m.compute(init=init, vout='my_array', return_tape=True)
    assert my_array == 3

    vjp = tape.get_vjp()
    _value = vjp.compute(init=dict(_my_array=5), vout='_value')
    assert _value == 0

    jvp = tape.get_jvp()
    my_array_= jvp.compute(init=dict(value_=5), vout='my_array_')
    assert my_array_ == 0

def test_operator_list_out():
    from numpy.testing import assert_array_equal
    from vmad.core.symbol import List, Symbol

    with Builder() as m:
        a = m.input('a')

        # it is very awkward to prepare a list output
        # I doubt this will be of any usefulness
        b1 = Symbol('b1')
        b2 = Symbol('b2')
        l = List([b1, b2])

        t = split(x=a, axis=0, args=l)
        assert isinstance(t, List)
        assert next(iter(t)) is b1

        m.output(c=l)

    init = dict(a=[[1, 1], [2, 2]])

    c, tape = m.compute(init=init, vout='c', return_tape=True, monitor=print)
    assert_array_equal(c, [[1, 1], [2, 2]])

    vjp = tape.get_vjp()
    init = dict(_c=[[1, 1], [1, 1]])
    _a = vjp.compute(init=init, vout='_a', monitor=print)

    assert_array_equal(_a, [[1, 1], [1, 1]])

    jvp = tape.get_jvp()
    init = dict(a_=[[1, 1], [1, 1]])
    c_ = jvp.compute(init=init, vout='c_', monitor=print)

    assert_array_equal(c_, [[1, 1], [1, 1]])


def test_operator_multi_out():
    @operator
    class op:
        ain = 'x'
        # for python 2.x need to use this syntax
        # to preserve orders
        aout = 'y1', 'y2'

        def apl(node, x):
            return dict(y1=x, y2=2 * x)
        def vjp(node, _y1, _y2):
            return dict(_x = _y1 + 2 * _y2)
        def jvp(node, x_):
            return dict(y1_=x_, y2_=2 * x_)

    with Builder() as m:
        a = m.input('a')
        t1, t2 = op(x=a)
        m.output(c=t1, d=t2)

    init = dict(a=3)

    (c, d), tape = m.compute(init=init, vout=('c', 'd'), return_tape=True)
    assert c == 3
    assert d == 6

    vjp = tape.get_vjp()
    init = dict(_c=1, _d=1)
    _a = vjp.compute(init=init, vout='_a', monitor=print)
    assert _a == 3

    jvp = tape.get_jvp()
    init = dict(a_=1)
    c_, d_ = jvp.compute(init=init, vout=('c_', 'd_'), monitor=print)
    assert c_ == 1
    assert d_ == 2

def test_operator_default_jvp():
    @operator
    class op:
        ain = 'x'
        aout = 'y1'

        def apl(node, x):
            return dict(y1=x * 2)
        def vjp(node, _y1):
            return dict(_x = _y1 * 2)

    with Builder() as m:
        a = m.input('a')
        t1 = op(x=a)
        m.output(c=t1)

    init = dict(a=3)

    c, tape = m.compute(init=init, vout='c', return_tape=True)
    assert c == 6

    vjp = tape.get_vjp()
    init = dict(_c=1)
    _a = vjp.compute(init=init, vout='_a', monitor=print)
    assert _a == 2

    jvp = tape.get_jvp()
    init = dict(a_=1)
    c_ = jvp.compute(init=init, vout=('c_'), monitor=print)
    assert c_ == 2


def test_operator_multi_out_unused():
    @operator
    class op:
        ain = 'x'
        # for python 2.x need to use this syntax
        # to preserve orders
        aout = 'y1', 'y2'

        def apl(node, x):
            return dict(y1=x, y2=2 * x)
        def vjp(node, _y1, _y2):
            return dict(_x = _y1 + 2 * _y2)
        def jvp(node, x_):
            return dict(y1_=x_, y2_=2 * x_)

    with Builder() as m:
        a = m.input('a')
        t1, t2 = op(x=a)
        m.output(c=t1)

    init = dict(a=3)

    c, tape = m.compute(init=init, vout='c', return_tape=True)
    assert c == 3

    vjp = tape.get_vjp()
    init = dict(_c=1)
    _a = vjp.compute(init=init, vout='_a', monitor=print)
    assert _a == 1

    jvp = tape.get_jvp()
    init = dict(a_=1)
    c_ = jvp.compute(init=init, vout=('c_'), monitor=print)
    assert c_ == 1

def test_operator_record():
    # assert used extra args are recored on the tape
    @operator
    class myrecord:
        ain = 'x'
        aout = 'y'

        def apl(node, x, p):
            return x * p

        def rcd(node, x, p, y):
            return dict(x=x, u=p)

        def vjp(node, x, _y, u):
            return _y * u

        def jvp(node, x, x_, u):
            return x_ * u

    with Builder() as m:
        a = m.input('a')
        b = myrecord(x=a, p=2.0)
        m.output(b=b)

    init = dict(a = 1.0)
    b, tape = m.compute(init=init, vout='b', monitor=print, return_tape=True)

    assert b == 2.0
    assert 'p' not in tape[0].impl_kwargs
    assert 'u' in tape[0].impl_kwargs

def test_operator_record_extra():
    # assert used extra args are recored on the tape
    @operator
    class myrecord:
        ain = 'x'
        aout = 'y'

        def apl(node, x, p):
            return dict(y=x * p, extra=p)

        def rcd(node, x, p, y, extra):
            return dict(x=x, u=p, extra=extra)

        def vjp(node, x, _y, u):
            return _y * u

        def jvp(node, x, x_, u):
            return x_ * u

    with Builder() as m:
        a = m.input('a')
        b = myrecord(x=a, p=2.0)
        m.output(b=b)

    init = dict(a = 1.0)
    b, tape = m.compute(init=init, vout='b', monitor=print, return_tape=True)

    assert b == 2.0
    assert 'p' not in tape[0].impl_kwargs
    assert 'u' in tape[0].impl_kwargs

