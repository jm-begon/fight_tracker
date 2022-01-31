class Boolable:
    def __bool__(self):
        return False


class DescriptiveTrue(Boolable):
    def __init__(self, description):
        self.description = description

    def __bool__(self):
        return True

    def __str__(self):
        return f"{self.description}"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.description)})"


class Intable:
    def __int__(self):
        return 0

    def __add__(self, other):
        return Addition(self, other)

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class DescriptiveInt(Intable):
    def __init__(self, value, description):
        self.value = value
        self.description = description

    def __int__(self):
        return self.value

    def __str__(self):
        return f"{self.value} ({self.description})"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.value)}, " \
               f"{repr(self.description)})"


class Addition(Intable):
    def __init__(self, *intables):
        self.intables = list(intables)

    def __int__(self):
        return sum(int(i) for i in self.intables)

    def __repr__(self):
        return f"{self.__class__.__name__}(*{repr(self.intables)})"

    def __str__(self):
        return " + ".join(str(x) for x in self.intables)


class Subtraction(Intable):
    def __init__(self, left_operand, right_operand):
        self.left = left_operand
        self.right = right_operand

    def __int__(self):
        return int(self.left) - int(self.right)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, " \
               f"{repr(self.right)})"

    def __str__(self):
        return f"{self.left} - {self.right}"