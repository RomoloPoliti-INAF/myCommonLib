


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


class Vers:
    def __init__(self, ver: tuple):
        self.major = ver[0]
        self.minor = ver[1]
        self.bug = ver[2]
        self.type = ver[3]
        self.build = ver[4]

    def full(self):
        if self.type.lower() == 'f':
            nVer = f"{self.major}.{self.minor}.{self.bug}"
        else:
            nVer = f"{self.major}.{self.minor}.{
                self.bug}.{code[self.type]}.{self.build}"
        return nVer

    def short(self):
        return f"{self.major}.{self.minor}"


# version = Vers(VERSION)
