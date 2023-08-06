class MultiRangeError(Exception):
    """Generar exception"""


class NoRangeableObjectError(MultiRangeError):
    """Error when an argument cant be maped to an rangeable objects"""

    def __init__(self, arg):
        super().__init__(f'Type found {type(arg)}. Types expected: int > 0, tuple, list, set, range, MultiRange')
