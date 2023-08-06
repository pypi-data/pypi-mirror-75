import math
from typing import Dict

class IVector:
    def __init__(self, coords: Dict = None):
        if coords is not None:
            self.coords = coords
        else:
            self.coords = {}

    @property
    def x(self):
        return self.coords.get('x', None)

    @property
    def y(self):
        return self.coords.get('y', None)

    @property
    def z(self):
        return self.coords.get('z', None)

    @property
    def length(self):
        return self.length()

    def unit(self):
        length = self.length()
        if length == 0:
            return None
        new_vector = IVector()
        for coord in self.coords:
            new_vector.coords[coord] = self.coords[coord]/length
        return new_vector

    def length(self):
        sum = 0
        for ii in self.coords:
            sum += self.coords[ii] ** 2

        return math.sqrt(sum)

    def distance_from(self, other):
        if isinstance(other, IVector):
            sum = 0.0
            for ii in self.coords.keys():
                delta = (float(self.coords[ii]) - float(other.coords[ii])) ** 2
                sum += delta
            return math.sqrt(sum)
        else:
            raise TypeError(f"type {other} cannot be distanced from {type(self)}")

    def __eq__(self, other) -> bool:
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            return False
        for ii in self.coords.keys():
            if not self._is_close(self.coords[ii], other.coords[ii]):
                return False

        return True

    def __str__(self, n_digits: int = 2):
        ret = "<"
        ii = 0
        for key in self.coords.keys():
            if ii > 0:
                ret += ", "
            ret += f"{round(float(self.coords[key]), n_digits)}"
            ii +=1

        ret +=">"
        return ret

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self),
                                                                                                   type(other))):
            raise TypeError(f"Object of type [{type(other)}] cannot be added to {type(self)}")

        ret = IVector()
        for ii in self.coords:
            ret.coords[ii] = self.coords[ii] + other.coords[ii]

        return ret

    def __sub__(self, other):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"Object of type [{type(other)}] cannot be subtracted from {type(self)}")

        ret = IVector()
        for ii in self.coords:
            ret.coords[ii] = self.coords[ii] - other.coords[ii]

        return ret

    def __mul__(self, other):
        if not (isinstance(other, float) or isinstance(other, int)):
            raise TypeError(f"Object of type [{type(other)}] cannot be multiplied to {type(self)}")

        new_vector = self.unit()
        for ii in new_vector.coords:
            new_vector.coords[ii] = new_vector.coords[ii] * self.length() * other

        return new_vector

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not (isinstance(other, float) or isinstance(other, int)):
            raise TypeError(f"Object of type [{type(other)}] cannot be divided from {type(self)}")

        new_vector = self.unit()
        for ii in new_vector.coords:
            new_vector.coords[ii] = new_vector.coords[ii] * (self.length() / other)

        return new_vector
        # return self.unit() * self.length() / other


    def _is_close(self, a:float, b:float, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def dot(self, other):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"type {other} cannot be dot multiplied by {type(self)}. Must match type...")
        sum = 0
        for ii in self.coords:
            sum += self.coords[ii] * other.coords[ii]
        return sum

    def project_onto(self, other):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"type {other} cannot be projected onto {type(self)}. Must match type...")

        dot = self.dot(other)
        return other.unit() * dot / other.length()

    def hadamard_product(self, other):
        if type(other) == float or type(other) == int:
            mult_vec = IVector()
            for coord in self.coords:
                mult_vec.coords[coord] = other
            other = mult_vec

        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"type {other} cannot be hadamard multiplied by {type(self)}. Must match type...")
        else:
            new_vector = IVector()
            for ii in self.coords:
                new_vector.coords[ii] = self.coords[ii] * other.coords[ii]
            return new_vector

    def hadamard_division(self, other, num_digits=None):
        if type(other) == float or type(other) == int:
            div_vec = IVector()
            for coord in self.coords:
                div_vec.coords[coord] = other
            other = div_vec

        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"type {type(other)} cannot be hadamard divided by {type(self)}. Must match type...\n"
                            f"{issubclass(type(other), type(self))}\n"
                            f"{issubclass(type(self), type(other))}")

        else:
            new_vector = IVector()
            for ii in self.coords:
                if num_digits is not None:
                    new_vector.coords[ii] = round(self.coords[ii] * 1.0 / other.coords[ii], num_digits)
                else:
                    new_vector.coords[ii] = self.coords[ii] * 1.0 / other.coords[ii]
            return new_vector

    def bounded_by(self, a, b) -> bool:
        if not isinstance(a, type(self)) and isinstance(b, type(self)):
            raise TypeError(f"a and b must match vector type: {type(self)}. {type(a)} and {type(b)} were given")

        for ii in self.coords.keys():
            min_val = min(a.coords[ii], b.coords[ii])
            max_val = max(a.coords[ii], b.coords[ii])

            if not min_val <= self.coords[ii] <= max_val:
                return False

        return True

    def interpolate(self, other, amount: float = 0.5, interpolate_type: str = "linear" ):
        if not (isinstance(other, type(self)) or issubclass(type(other), type(self)) or issubclass(type(self), type(other))):
            raise TypeError(f"Cannot interpolate between objects of type {type(self)} and {type(other)}")

        if interpolate_type == "linear":
            return (other - self) * amount + self
        else:
            raise NotImplementedError(f"Unimplemented interpolation type: {interpolate_type}")

class Vector2 (IVector):
    def __init__(self, x: float, y: float):
        IVector.__init__(self)
        self.coords['x'] = x
        self.coords['y'] = y

    def as_tuple(self):
        return (self.x, self.y)

if __name__ == "__main__":
    a = Vector2(1, 2)

    print (a * 4)