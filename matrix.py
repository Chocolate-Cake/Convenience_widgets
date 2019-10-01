vector = ["x1", "x2", "x3"]

A = [["A11", "A21", "A31"],
	["A12", "A22", "A32"],
	["A13", "A23", "A33"]]

B = ["", "", ""]

scalar = ""

for x in range(3):
	for y in range(3):
		B[x] += (vector[x] + '*' + A[y][x] + "+")

for x in range(3):
	B[x] = B[x][:len(B[x])-1]

#print(B)

for x in range(3):
	scalar += vector[x] + "(" + B[x] + ")+"

scalar = scalar[:len(scalar)-1]
print(scalar)

test = ""

for x in range(1, 4):
	for y in range(1,4):
		test += "x" + str(x) + "^2*A" + str(x) + str(y) + "+"
test = test[:len(test)-1]
print()
print(test)