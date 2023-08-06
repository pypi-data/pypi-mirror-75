import json
import sys

import yaml
import yaml_walker
from yaml_walker.api import Ypath, YDict


def query(pattern, data):
    return Ypath(pattern)(data)


def parse(yaml_path):
    with open(yaml_path) as fr:
        data = yaml.load(fr, yaml.FullLoader)
        return YDict(data)


def run_cli(argv):
    pattern = argv[0]
    yaml_path = argv[1]
    with open(yaml_path) as fr:
        data = yaml.load(fr, yaml.FullLoader)
        return query(pattern, data)


if __name__ == '__main__':
    if sys.argv[1] in ['-v', '--version']:
        print(f"yaml_walker: {yaml_walker.__version__}")
        sys.exit(-1)
    result = run_cli(sys.argv[1:])
    print(json.dumps(result, sort_keys=True, indent=4))
