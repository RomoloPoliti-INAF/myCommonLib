

# def shVersion():
#     code = {"a": "alpha", "b": "beta", "rc": "ReleaseCandidate", "f": "Final"}
#     nVer = f"{VERSION[0]}.{VERSION[1]}"
#     if VERSION[2] != 0:
#         nVer += f".{VERSION[2]}"
#     if VERSION[3].lower() != "f":
#         nVer += f".{code[VERSION[3].lower()]}"
#         if VERSION[4] != 0:
#             nVer += f".{VERSION[4]}"
#     return nVer


code = {"d": "dev", "a": "alpha", "b": "beta",
        "rc": "ReleaseCandidate", "f": "Final"}

numeric_map = {"d": 1, "a": 2, "b": 3, "rc": 4, "f": 5}


class Vers:
    def __init__(self, ver: tuple)->None:
        self.major, self.minor, *extra = ver
        self.bug = extra[0] if extra else None
        self.type = extra[1] if len(extra) > 1 else None
        if not type(self.type) is str:
            raise Exception(
                f"The fourth element of the version number must be a string")
        if not self.type in code.keys():
            raise ValueError(f"the fourth element of the version mus be one of {','.join(code.keys())}")
        self.build = extra[2] if len(extra) > 2 else None


    def full(self)->str:
        if self.type.lower() == 'f':
            nVer = f"{self.major}.{self.minor}.{self.bug}"
        else:
            nVer = f"{self.major}.{self.minor}.{self.bug}.{code[self.type]}.{self.build}"
        return nVer

    def short(self)->str:
        return f"{self.major}.{self.minor}"

    def __repr__(self) -> str:
        return f"Version {self.full()}"

    def __eq__(self, other)->bool:
        return all(getattr(self, item) == getattr(other, item) for item in self.__dict__ if not item.startswith('_'))
    
    def __gt__(self, other) -> bool:
        if self.major != other.major:
            return self.major > other.major
        elif self.minor != other.minor:
            return self.minor > other.minor
        elif self.bug != other.bug:
            return self.bug > other.bug
        elif numeric_map[self.type] != numeric_map[other.type]:
            return numeric_map[self.type] > numeric_map[other.type]
        else:
            return self.build > other.build
        
    def __ge__(self,other)->bool:
        if self > other or self == other:
            return True
        else:
            return False
        
    def __lt__(self,other)->bool:
        if self.major != other.major:
            return self.major < other.major
        elif self.minor != other.minor:
            return self.minor < other.minor
        elif self.bug != other.bug:
            return self.bug < other.bug
        elif numeric_map[self.type] != numeric_map[other.type]:
            return numeric_map[self.type] < numeric_map[other.type]
        else:
            return self.build < other.build

    def __le__(self, other) -> bool:
        if self < other or self == other:
            return True
        else:
            return False


# version = Vers(VERSION)
