
import random
import itertools
import functools

def n_random_coords(n, *, dimensionality=2, max_distance=1, seed=None):
    """
    Generate n random coordinates with the given dimensionality, contained within the bounds (0,0,...) and (max_distance,max_distance,...)
    """
    coords = set()
    random.seed(seed)
    while len(coords) < n:
        coords.add(tuple(random.random()*max_distance for _ in range(dimensionality)))
    return coords

def zero_pad(coord: tuple[int], dimensions) -> tuple[int]:
    """
    Trim dimensionality of coordinate tuple or pad with zeroes s.t. len(coord)==dimensions
    """
    return tuple(itertools.chain(coord[:dimensions], [0]*max(0,dimensions - len(coord))))

def length_match(tuple_list: list[tuple[int]], length=None) -> list[tuple[int]]:
    """
    Trim dimensionality of coordinate tuples in list or pad with zeroes s.t. len(A)==len(B) for any arbitrary A,B in list
    If length==None then pads to match greatest dimensionality in list
    """
    if length is None:
        length = max(len(tup) for tup in tuple_list)
    return [zero_pad(tup, length) for tup in tuple_list]

def length_match_first_n_inputs(n=None):
    """
    Call length match across the first n non-named inputs
    If n=None then all non-named operands
    """
    def length_match_decorator(func):
        @functools.wraps(func)
        def length_match_decoration(*args, **kwargs):
            if n is None:
                return func(*length_match(args), **kwargs)
            else:
                return func(*length_match(args[:n]), *args[n:], **kwargs)
        return length_match_decoration
    return length_match_decorator

@length_match_first_n_inputs(2)
def distance_between(A: tuple[int], B: tuple[int], L=2):
    """
    Calculate the Lx distance between two coordinates A,B
    L=1 => Manhattan
    L=2 => Euclidean
    """
    return sum(abs(A[i]-B[i])**L for i in range(len(A))) ** (1/L)

@length_match_first_n_inputs()
def sum_coords(*tuple_list):
    """
    Calculate the sum of a list of coordinates
    """
    return tuple(sum(tup[index] for tup in tuple_list) for index in range(len(tuple_list[0])))

def scale_coord(coord: tuple[int], scalar):
    """
    Multiply a coordinate by a non-coordinate scalar
    """
    return tuple(coord[i]*scalar for i in range(len(coord)))

@length_match_first_n_inputs(3)
def cosine_of(A,B,C: tuple[int]):
    """
    For the triangle A,B,C calculate the cosine of the angle at A
    """
    a,b,c = distance_between(B,C), distance_between(A,C), distance_between(A,B)
    return (b**2 + c**2 - a**2) / (2*b*c)