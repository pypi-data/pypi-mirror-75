import re
import datetime
from pathlib import Path


class Tile:
    def __init__(self, path):
        path = Path(path)

        pattern = (
            r"^S2[AB]_MSIL2A_"
            r"(?P<start>\d{8}T(\d{6}))_"
            r"N(\d{4})_"
            r"(?P<orbit>R(\d{3}))_"
            r"(?P<name>[A-Z0-9]{6})_"
            r"(?P<stop>\d{8}T(\d{6}))"
            r"\.SAFE$"
        )

        match = re.match(pattern, path.name, re.IGNORECASE)

        if not match:
            raise RuntimeError("unable to parse tile name")

        self.props = match.groupdict()

    @property
    def name(self):
        return self.props["name"]

    @property
    def orbit(self):
        return self.props["orbit"]

    @property
    def start(self):
        return datetime.datetime.strptime(self.props["start"], "%Y%m%dT%H%M%S")

    @property
    def stop(self):
        return datetime.datetime.strptime(self.props["stop"], "%Y%m%dT%H%M%S")
