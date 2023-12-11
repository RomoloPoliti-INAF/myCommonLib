from dataclasses import dataclass
from rich.console import Console


@dataclass
class SoftMode:
    verbose: int
    debug: bool
    console:Console=Console()

    def check(self, level: int = 0) -> bool:
        if self.verbose >= level:
            return True
        else:
            return False

softMode = SoftMode(0,False)