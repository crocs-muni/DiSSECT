#!/usr/bin/env sage

from pathlib import Path
import json

from curve_analyzer.definitions import TEST_PATH

def read_default(path):
    with open(Path(path),"r") as f:
        return json.load(f)

def write_file(name, path,to_write, message):
    with open(path, 'w') as f:
        json.dump(to_write, f)
    print(message, name)


def main():
    params = read_default(Path(TEST_PATH, 'default.params'))
    for test in params:
        name, to_write = test, params[test]
        Path(TEST_PATH, name).mkdir(parents=True, exist_ok=True)
        full_name = Path(TEST_PATH, name, name + ".params")
        if full_name.is_file():
            with open(full_name, 'r') as f:
                current = f.read()
            if not current == to_write:
                write_file(name,full_name,to_write,"Params file updated for")
        else:
            write_file(name,full_name,to_write,"Params file created for")

if __name__ == '__main__':
   main()
