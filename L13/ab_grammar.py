#Code generated with cont_parser_generator.py
import sys
from liblet import Grammar,Production,Derivation
def end_match(deriv,rest):
	if not rest:print(deriv)
def match(deriv,t,rest,cont):
	if rest and t==rest[0]:cont(deriv,rest[1:])
def B_alt0(deriv, rest,cont):
	match(deriv, 'b', rest, cont)
def A_alt0(deriv, rest,cont):
	match(deriv, 'a', rest, cont)
def S_alt0(deriv, rest,cont):
	parse_A(deriv,rest,cont)
def S_alt1(deriv, rest,cont):
	def t(deriv, rest):
		parse_B(deriv,rest,cont)
	match(deriv, 'a', rest, t)
def parse_B(deriv,rest,cont):
	B_alt0(deriv.leftmost(3), rest,cont)
def parse_A(deriv,rest,cont):
	A_alt0(deriv.leftmost(2), rest,cont)
def parse_S(deriv,rest,cont):
	S_alt0(deriv.leftmost(0), rest,cont)
	S_alt1(deriv.leftmost(1), rest,cont)
if __name__=='__main__':
	s="""
	S -> A
	S -> a B
	A -> a
	B -> b
	"""
	rest=sys.argv[1]
	parse_S(Derivation(Grammar.from_string(s)),rest,end_match)