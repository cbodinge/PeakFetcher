from pathlib import Path
import extractor


class Injection:
    """
    Data Object that organizes the relevant information from a .d file.
    path is a pathlib.Path object that points to the .d Agilent file.
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        self.transitions = extractor.main(path)
