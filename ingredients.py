str1 = input()
str2 = input()

def make_list(st):
	st = st.replace('\n', '')
	st = st.split(',')
	ls = []
	for x in st:
		ls.append(x.strip().lower())
	return ls

def print_list(l):
	for x in l:
		print('\t' + x)

ls1 = make_list(str1)
ls2 = make_list(str2)

unique1 = []

for x in ls1:
	if x not in ls2:
		unique1.append(x)

unique2 = []

for x in ls2:
	if x not in ls1:
		unique2.append(x)

unique1.sort()
unique2.sort()

print()
print("1 ------------------------- ")
print_list(unique1)
print()
print()
print("2 -------------------------")
print_list(unique2)