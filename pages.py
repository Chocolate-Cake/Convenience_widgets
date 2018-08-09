import math

print("Input total number of pages to print:")
total_pages = int(input())

print("Input number of slides per page:")
per_page = int(input())

set_ignore = []

print("Input any slide numbers to not print (0 to finish):")
running = True
while running:
	temp = int(input())
	if temp == 0:
		running = False
	else:
		set_ignore.append(temp)

counter = 0
switch = True

set_one = []
set_two = []

for x in range(1, total_pages + 1):
	if x not in set_ignore:
		if switch:
			set_one.append(x)
		else:
			set_two.append(x)
		counter+= 1
		if counter == per_page:
			switch = not switch
			counter = 0

print(set_one)
print("Pages in set 1: " + str(math.ceil(len(set_one)/4)))
print(set_two)
print("Pages in set 2: " + str(math.ceil(len(set_two)/4)))

