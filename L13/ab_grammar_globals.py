#Code generated with global_parser_generator.py
import sys
from liblet import Grammar,Production,Derivation
rest=''
pos=0
deriv=None
def logn(f):
	def scope(*args):
		print('Call function :',f.__name__,' with args {}'.format(args))
		return f(*args)
	return scope

def end_match():
	global rest,pos,deriv
	if rest and pos==len(rest):print(deriv)

def match(t,cont):
	global rest,pos
	if rest and t==rest[pos]:
		pos+=1
		cont()
def S_alt0(cont):
	global pos,deriv
	p=pos
	copy=deriv
	deriv=deriv.leftmost(0)
	parse_A(cont)
	pos=p
	deriv=copy
def S_alt1(cont):
	global pos,deriv
	p=pos
	copy=deriv
	deriv=deriv.leftmost(1)
	def t():
		parse_B(cont)
	match('a', t)
	pos=p
	deriv=copy
def A_alt0(cont):
	global pos,deriv
	p=pos
	copy=deriv
	deriv=deriv.leftmost(2)
	match('a', cont)
	pos=p
	deriv=copy
def B_alt0(cont):
	global pos,deriv
	p=pos
	copy=deriv
	deriv=deriv.leftmost(3)
	match('b', cont)
	pos=p
	deriv=copy
def parse_S(cont):
	S_alt0(cont)
	S_alt1(cont)
def parse_A(cont):
	A_alt0(cont)
def parse_B(cont):
	B_alt0(cont)
if __name__=='__main__':
	s="""
	S -> A
	S -> a B
	A -> a
	B -> b
	"""
	rest=sys.argv[1]
	deriv=Derivation(Grammar.from_string(s))
	parse_S(end_match)