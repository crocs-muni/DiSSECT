import os, json



from pathlib import Path

with open("params","r") as f:
	params = f.read()
params = params.split("&test ")[1:]
written = ""
#print(test_dirs)
for test in params:
	
	name,to_write = test.split(":",1)
	Path("curve_analyzer/tests/"+name).mkdir(parents=True, exist_ok=True)	
	to_write = to_write.strip()
	full_name = "./curve_analyzer/tests/"+name+"/"+name+".params"
	with open(full_name, 'w') as f:
		f.write(to_write)
	written +=name + ", "
	#print(test)
print("Params files created for "+written[:-2])
