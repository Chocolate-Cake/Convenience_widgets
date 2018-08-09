import math

def handle_payoffs(is_call, now, up, down):
	if is_call:
		u_payoff = max(0, up-now)
		d_payoff = max(0, down-now)
	else:
		u_payoff = max(0, now-up)
		d_payoff = max(0, now-down)
	return u_payoff, d_payoff

#r = riskfree rate, t = time units passed per level of tree
def rep_portfolio_iter(init, current_p, u, d, r, t, is_call, levels_after_this, this_str):

	#continue expanding tree
	if levels_after_this > 1:
		u_security_price = rep_portfolio_iter(init, current_p * (1 + u), u, d, r, t, is_call, levels_after_this - 1, this_str + 'u')
		d_security_price = rep_portfolio_iter(init, current_p * (1 + d), u, d, r, t, is_call, levels_after_this - 1, this_str + 'd')
	#next level is leaf of tree
	else:
		u_security_price, d_security_price = handle_payoffs(is_call, init, current_p * (1 + u), current_p * (1 + d))

	#stocks
	delta = (u_security_price - d_security_price)/(current_p * (1 + u) - current_p * (1 + d))
	#bonds
	bonds = pow(math.e, -r*t)*(u_security_price - delta*current_p*(1 + u))
	price = delta * current_p + bonds
	if this_str == "":
		this_str = "0"
	print(this_str + " = " + str(price))
	return price

def risk_neutral_iter(init, q_star, current_p, u, d, is_call, levels_after_this, this_str):
	
	if levels_after_this > 1:
		u_security_price = risk_neutral_iter(init, q_star, current_p * (1 + u), u, d, is_call, levels_after_this - 1, this_str + 'u')
		d_security_price = risk_neutral_iter(init, q_star, current_p * (1 + d), u, d, is_call, levels_after_this - 1, this_str + 'd')
	else:
		u_security_price, d_security_price = handle_payoffs(is_call, init, current_p * (1 + u), current_p * (1 + d))

	price = q_star*u_security_price + (1 - q_star)*d_security_price
	if this_str == "":
		this_str = "0"
	print(this_str + " = " + str(price))
	return price

#r = riskfree rate, h = time unites passed per level of tree
def risk_neutral(init, u, d, r, h, is_call, levels_after_this):
	
	q_star = (pow(math.e, r*h) - (1 + d))/(u - d)
	return risk_neutral_iter(init, q_star, init, u, d, is_call, levels_after_this, "")

result1 = rep_portfolio_iter(50, 50, 0.1, -0.1, 0, 1/3, True, 3, "")
print("----")
result2 = risk_neutral(50, 0.1, -0.1, 0, 1/3, True, 3)
