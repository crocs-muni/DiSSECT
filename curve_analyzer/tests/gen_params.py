#!/usr/bin/env sage

import os, json
from pathlib import Path

with open("params", "r") as f:
	params = f.read()
params = params.split("&test ")[1:]

for test in params:
	name,to_write = test.split(":",1)
	Path("curve_analyzer/tests/" + name).mkdir(parents=True, exist_ok=True)	
	to_write = to_write.strip()
	full_name = os.path.join(".", name, name + ".params")
	if os.path.isfile(full_name):
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