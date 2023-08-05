from typing import List, Any
import sys
import json
import os
import requests


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def read_json(path: str):
    with open(path) as f:
        return json.load(f)


def write_json(path: str, obj: Any):
    with open(path, "w") as f:
        json.dump(obj, f)


def read_jsonlines(path: str):
    out = []
    with open(path) as f:
        for line in f:
            out.append(json.loads(line))
    return out


def write_jsonlines(path: str, elements: List[Any]):
    with open(path, "w") as f:
        for e in elements:
            f.write(json.dumps(e))
            f.write("\n")


def download(remote_path, local_path):
    eprint(f"Downloading {remote_path} to {local_path}")
    response = requests.get(remote_path, stream=True)
    with open(local_path, "w") as f:
        for data in response.iter_content():
            f.write(data)


class requires_file:
    def __init__(self, path):
        self._path = path

    def __call__(self, f):
        if os.path.exists(self._path):
            return f
        else:
            eprint(f"File missing, skipping function: {self._path}")

            def nop(*args, **kwargs):  # pylint: disable=unused-argument
                pass

            return nop
