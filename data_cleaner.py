import sys, os
import pandas as pd

def process_name(origin):
	if origin is not None:
		prefix = origin.split(".")[0]
		suffix = origin.split(".")[1]
		return origin, prefix, suffix
	else:
		return None, None, None

def crop_csv(origin, prefix, num):
	df = pd.read_csv(origin)
	selected = df.iloc[:num,]
	selected.to_csv(prefix + "_crop_csv.csv")

def dta_to_csv(origin, prefix, num):
	df = pd.read_stata(origin)
	selected = df.iloc[:num,]
	selected.to_csv(prefix + "_dta_to_csv.csv")

def process_source_files(dirname, targetdir, num):
	path = os.getcwd() + "/"
	onlyfiles = [f for f in os.listdir(path + dirname) if os.path.isfile(os.path.join(path + dirname, f))]
	
	for f in onlyfiles:
		origin, prefix, suffix = process_name(f)
		source = path + "/" + dirname + "/" + origin
		target = path + "/" + targetdir + "/" + prefix
		if origin is not None and suffix == "csv":
			crop_csv(source, target, num)
		elif origin is not None and suffix == "dta":
			dta_to_csv(source, target, num)

def handle_folder():
	if len(sys.argv) < 3:
		print("missing arguments")
	else:
		num = 100
		if len(sys.argv) > 3:
			num = int(sys.argv[3])
		origin = sys.argv[1]
		target = sys.argv[2]
		process_source_files(origin, target, num)

if __name__ == "__main__":
	handle_folder()
	print("DONE")


