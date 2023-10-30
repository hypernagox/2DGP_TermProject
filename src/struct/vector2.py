class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vec2(self.x * scalar, self.y * scalar)
        else:
            return NotImplemented

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vec2(self.x / scalar, self.y / scalar)
        else:
            return NotImplemented

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        magnitude = self.length()
        if magnitude > 0:
            self.x /= magnitude
            self.y /= magnitude

    def normalized(self):
        magnitude = self.length()
        if magnitude > 0:
            return Vec2(self.x / magnitude, self.y / magnitude)
        return Vec2()

    def is_zero(self, tolerance=1e-10):
        return abs(self.x) < tolerance and abs(self.y) < tolerance


def dot(a, b):
    if isinstance(a, Vec2) and isinstance(b, Vec2):
        return a.x * b.x + a.y * b.y
    else:
        raise ValueError("Arguments must be instances of Vec2.")