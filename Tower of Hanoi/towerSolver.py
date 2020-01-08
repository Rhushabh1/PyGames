# puck_count = 3
# a = list(range(puck_count))
# b = []
# c = []


def transfer_function(start, end, helper, pucks):
	if pucks == 1:
		return [[start, end]]

	a = transfer_function(start, helper, end, pucks-1)
	b = transfer_function(start, end, helper, 1)
	c = transfer_function(helper, end, start, pucks-1)
	a.extend(b)
	a.extend(c)
	return a


# transfer all pucks from start, helper to end 
def transfer_pucks(start, end, helper):
	pass
