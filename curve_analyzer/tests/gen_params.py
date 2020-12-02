#!/usr/bin/env sage

from pathlib import Path

from curve_analyzer.definitions import TEST_PATH

def main():
    with open(Path(TEST_PATH, 'params'), "r") as f:
        params = f.read()
    params = params.split("&test ")[1:]

    for test in params:
        name, to_write = test.split(":", 1)
        Path(TEST_PATH, name).mkdir(parents=True, exist_ok=True)
        to_write = to_write.strip()
        full_name = Path(TEST_PATH, name, name + ".params")
        if full_name.is_file():
            with open(full_name, 'r') as f:
                current = f.read()
            if not current == to_write:
                with open(full_name, 'w') as f:
                    f.write(to_write)
                print("Params file updated for", name)
        else:
            with open(full_name, 'w') as f:
                f.write(to_write)
            print("Params file created for", name)

if __name__ == '__main__':
   main()
