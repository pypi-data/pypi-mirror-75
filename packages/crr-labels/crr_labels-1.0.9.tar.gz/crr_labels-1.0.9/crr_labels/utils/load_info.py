import json
import os
from typing import Dict


def load_info(filename: str) -> Dict:
    path = "{pwd}/../{filename}.json".format(
        pwd=os.path.dirname(os.path.realpath(__file__)),
        filename=filename
    )
    with open(path, "r") as f:
        return json.load(f)
