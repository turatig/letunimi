import sys
#Code generated with generate_all_globals.py
rest=''
pos=0
deriv=[]
def match(t):
	global rest,pos
	if t==rest[pos]:
		pos+=1
		return True
	else:return False
def alt_Et_0(rule):
	global pos,deriv
	p=pos
	ind=len(deriv)
	deriv.append(rule)
	succ = match('-')
	if not succ:
		pos=p
		deriv=deriv[:ind]
		return False
	succ= parse_T()
	if not succ:
		pos=p
		return False
	return True
def alt_Et_1(rule):
	global pos,deriv
	p=pos
	ind=len(deriv)
	deriv.append(rule)
	succ = match('+')
	if not succ:
		pos=p
		deriv=deriv[:ind]
		return False
	succ= parse_T()
	if not succ:
		pos=p
		return False
	return True
def alt_Ets_0(rule):
	global pos,deriv
	p=pos
	ind=len(deriv)
	deriv.append(rule)
	succ= parse_Et()
	if not succ:
		pos=p
		return False
	succ = match('#')
	if not succ:
		pos=p
		deriv=deriv[:ind]
		return False
	return True
def alt_Ets_1(rule):
	global pos,deriv
	p=pos
	ind=len(deriv)
	deriv.append(rule)
	succ= parse_Et()
	if not succ:
		pos=p
		return False
	succ= parse_Ets()
	if not succ:
		pos=p
		return False
	return True
def alt_E_0(rule):
	global pos,deriv
	p=pos
	ind=len(deriv)
	deriv.append(rule)
	succ= parse_Eh()
	if not succ:
		pos=p
		return False
	succ= parse_Ets()
	if not succ:
		pos=p
		return False
	return True
def alt_E_1(rule):
	global pos,deriv
	p=pos
	ind=len(deriv)
	deriv.append(rule)
	succ= parse_Eh()
	if not succ:
		pos=p
		return False
	succ = match('#')
	if not succ:
		pos=p
		deriv=deriv[:ind]
		return False
	return True
def alt_Eh_0(rule):
	global pos,deriv
	p=pos
	ind=len(deriv)
	deriv.append(rule)
	succ= parse_T()
	if not succ:
		pos=p
		return False
	return True
def alt_T_0(rule):
	global pos,deriv
	p=pos
	ind=len(deriv)
	deriv.append(rule)
	succ = match('t')
	if not succ:
		pos=p
		deriv=deriv[:ind]
		return False
	return True
def parse_Et():
	global deriv
	succ_alt= alt_Et_0(4)
	if succ_alt: return True
	succ_alt= alt_Et_1(7)
	if succ_alt: return True
	return False
def parse_Ets():
	global deriv
	succ_alt= alt_Ets_0(1)
	if succ_alt: return True
	succ_alt= alt_Ets_1(6)
	if succ_alt: return True
	return False
def parse_E():
	global deriv
	succ_alt= alt_E_0(0)
	if succ_alt: return True
	succ_alt= alt_E_1(5)
	if succ_alt: return True
	return False
def parse_Eh():
	global deriv
	succ_alt= alt_Eh_0(2)
	if succ_alt: return True
	return False
def parse_T():
	global deriv
	succ_alt= alt_T_0(3)
	if succ_alt: return True
	return False
if __name__=='__main__':
	rest=sys.argv[1]+'#'
	if parse_E():print(deriv)
	else:print('Invalid Expression')