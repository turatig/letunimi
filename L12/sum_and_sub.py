#Code generated with parse_generator_rec_desc.py
import sys
def match(t,rest):
	if t==rest[0]: return True,rest[1:],[t]
	else:return False,rest,[]
def alt_Ets_0(rest):
	alt_rest=rest
	children=['Ets']
	succ,alt_rest,c= parse_Et(alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	succ,alt_rest,c = match('#',alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	return True,alt_rest,children
def alt_Ets_1(rest):
	alt_rest=rest
	children=['Ets']
	succ,alt_rest,c= parse_Et(alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	succ,alt_rest,c= parse_Ets(alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	return True,alt_rest,children
def alt_Eh_0(rest):
	alt_rest=rest
	children=['Eh']
	succ,alt_rest,c= parse_T(alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	return True,alt_rest,children
def alt_Et_0(rest):
	alt_rest=rest
	children=['Et']
	succ,alt_rest,c = match('-',alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	succ,alt_rest,c= parse_T(alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	return True,alt_rest,children
def alt_Et_1(rest):
	alt_rest=rest
	children=['Et']
	succ,alt_rest,c = match('+',alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	succ,alt_rest,c= parse_T(alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	return True,alt_rest,children
def alt_T_0(rest):
	alt_rest=rest
	children=['T']
	succ,alt_rest,c = match('t',alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	return True,alt_rest,children
def alt_E_0(rest):
	alt_rest=rest
	children=['E']
	succ,alt_rest,c= parse_Eh(alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	succ,alt_rest,c= parse_Ets(alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	return True,alt_rest,children
def alt_E_1(rest):
	alt_rest=rest
	children=['E']
	succ,alt_rest,c= parse_Eh(alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	succ,alt_rest,c = match('#',alt_rest)
	if not succ:return False,rest,[]
	children.append(c)
	return True,alt_rest,children
def parse_Ets(rest):
	succ_alt,rest,c= alt_Ets_0(rest)
	if succ_alt: return True,rest,c
	succ_alt,rest,c= alt_Ets_1(rest)
	if succ_alt: return True,rest,c
	return False,rest,[]
def parse_Eh(rest):
	succ_alt,rest,c= alt_Eh_0(rest)
	if succ_alt: return True,rest,c
	return False,rest,[]
def parse_Et(rest):
	succ_alt,rest,c= alt_Et_0(rest)
	if succ_alt: return True,rest,c
	succ_alt,rest,c= alt_Et_1(rest)
	if succ_alt: return True,rest,c
	return False,rest,[]
def parse_T(rest):
	succ_alt,rest,c= alt_T_0(rest)
	if succ_alt: return True,rest,c
	return False,rest,[]
def parse_E(rest):
	succ_alt,rest,c= alt_E_0(rest)
	if succ_alt: return True,rest,c
	succ_alt,rest,c= alt_E_1(rest)
	if succ_alt: return True,rest,c
	return False,rest,[]
if __name__=='__main__':
	rest=sys.argv[1]+'#'
	belong_to,_,parse_tree=parse_E(rest)
	if belong_to:print(parse_tree)
	else:print('Invalid Expression')