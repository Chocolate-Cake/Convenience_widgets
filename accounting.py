import sys, termios, tty, os, time, random
from os import system


tax = 0.4
ntax = 1 - tax

class answer:
	def __init__(self, c, s, n, a, l):
		self.c = float(c)
		self.s = float(s)
		self.n = float(n)
		self.a = float(a)
		self.l = float(l)

	def print(self, base):
		mult = 1
		if base < 0:
			mult = -1
		base = float(int(base))
		print("cash: " + str(self.c*base*mult))
		print("shareholder's equity: " + str(self.s*base*mult))
		print("net income: " + str(self.n*base*mult))
		print("assets: " + str(self.a*base*mult))
		print("liabilities: " + str(self.l*base*mult))

#positive only
rev = ["revenue", answer(ntax, ntax, ntax, ntax, ntax)]
xp_op = ["operating expenses", answer(-ntax, -ntax, -ntax, -ntax, -ntax)]
dep = ["depreciation", answer(tax, -ntax, -ntax, -ntax, -ntax)]
stock = ["stock based compensation", answer(tax, tax, -ntax, tax, tax)]
amort = ["amortization", answer(tax, -ntax, -ntax, -ntax, -ntax)]
int_in = ["interest income", answer(ntax, ntax, ntax, ntax, ntax)]
int_xp = ["interest expense", answer(-ntax, -ntax, -ntax, -ntax, -ntax)]
gw_impair = ["goodwill impairment", answer(tax, -ntax, -ntax, -ntax, -ntax)]
ppe_write_down = ["PPE write down", answer(tax, -ntax, -ntax, -ntax, -ntax)]
def_tax = ["deferred income taxes", answer(1, 0, 0, 1, 1)]
pref_div = ["preferred dividends", answer(-1, -1, 0, -1, -1)]
com_div = ["common dividends", answer(-1, -1, 0, -1, -1)]
fx = ["FX rate effects", answer(1, 1, 0, 1, 1)]

#has negative and positive
gl_sale_ppe = ["gain/loss on sale of PPE", answer(ntax, ntax, ntax, ntax, ntax), answer(ntax, ntax, ntax, ntax, ntax)]
gl_sale_inv = ["gain/loss on sale of inventory", answer(ntax, ntax, ntax, ntax, ntax), answer(ntax, ntax, ntax, ntax, ntax)]
ar = ["accounts receivable", answer(tax, -ntax, -ntax, -ntax, -ntax), answer(1, 0, 0, 0, 0)]
pre_xp = ["prepaid expenses", answer(-1, 0, 0, 0, 0), answer(tax, -ntax, -ntax, -ntax, -ntax)]
inv = ["inventory", answer(-1, 0, 0, 0, 0), answer(tax, -ntax, -ntax, -ntax, -ntax)]
acc_xp = ["accrued expenses", answer(tax, -ntax, -ntax, tax, tax), answer(-1, 0, 0, -1, -1)]
ap = ["accounts payable", answer(tax, -ntax, -ntax, tax, tax), answer(-1, 0, 0, -1, -1)]
def_rev = ["deferred revenue", answer(1, 0, 0, 1, 1), answer(-tax, ntax, ntax, -tax, -tax)]
sti = ["short term investments", answer(-1, 0, 0, 0, 0), answer(1, 0, 0, 0, 0)]
lti = ["long term investments", answer(-1, 0, 0, 0, 0), answer(1, 0, 0, 0, 0)]
ppe = ["PPE", answer(-1, 0, 0, 0, 0), answer(1, 0, 0, 0, 0)]
ltd = ["long term debt", answer(1, 0, 0, 1, 1), answer(-1, 0, 0, -1, -1)]
std = ["short term debt", answer(1, 0, 0, 1, 1), answer(-1, 0, 0, -1, -1)]
ps = ["preferred stock (is not equity)", answer(1, 0, 0, 1, 1), answer(-1, 0, 0, -1, -1)]
cs = ["common shares", answer(1, 1, 0, 1, 1), answer(-1, -1, 0, -1, -1)]

pos = {
	0: rev, 
	1: xp_op, 
	2: dep, 
	3: stock, 
	4: amort,
	5: int_in,
	6: int_xp,
	7: gw_impair,
	8: ppe_write_down,
	9: def_tax,
	10: pref_div,
	11: com_div,
	12: fx
}

both = {
	13: gl_sale_ppe,
	14: gl_sale_inv,
	15: ar,
	16: pre_xp,
	17: inv,
	18: acc_xp,
	19: ap,
	20: def_rev,
	21: sti,
	22: lti,
	23: ppe,
	24: ltd,
	25: std,
	26: ps,
	27: cs
}

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getQ():
	num_q = random.randint(1, 27)
	num_change = random.choice([-100, -10, 10, 100])
	to_ask = None
	to_post = None
	sign = ''

	if num_q < 13:
		temp = pos[num_q]
		to_ask = temp[0]
		to_post = temp[1]
		num_change = abs(num_change)
		sign = '+'
	else:
		temp = both[num_q]
		to_ask = temp[0]
		if num_change > 0:
			to_post = temp[1]
			sign = '+'
		else:
			to_post = temp[2]

	return to_ask, to_post, sign, num_change

def clear():
	try:
		_ = system('cls')
		_ = system('clear')
	except:
		pass

clear()
print("Instructions:")
print("Press space to generate new question")
print("Press anything other than space to quit")

while True:

	c = getch()
	if c == ' ':
		clear()
		a, p, s, n = getQ()
		print(a + " changes by " + s + str(n))
		print("Press space to show answer")
	else:
		break

	c = getch()
	if c == ' ':
		print(" ")
		p.print(n)
		print("Press space to generate new question")
	else:
		break





