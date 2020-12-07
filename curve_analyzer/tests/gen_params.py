#!/usr/bin/env sage

from pathlib import Path
import json

from curve_analyzer.definitions import TEST_PATH

def main():
    with open(Path(TEST_PATH, 'default.params'), "r") as f:
        params = json.load(f)
    for test in params:
        name, to_write = test, params[test]
        Path(TEST_PATH, name).mkdir(parents=True, exist_ok=True)
        full_name = Path(TEST_PATH, name, name + ".params")
        if full_name.is_file():
            with open(full_name, 'r') as f:
                current = f.read()
            if not current == to_write:
                with open(full_name, 'w') as f:
                    json.dump(to_write,f)
                print("Params file updated for", name)
        else:
            with open(full_name, 'w') as f:
                json.dump(to_write,f)
            print("Params file created for", name)

if __name__ == '__main__':
   main()
