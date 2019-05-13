from liblet import *

#CNF
def start_replacing(G):
    if len([p for p in G.P if G.S in p.rhs])!=0:
        new_s=G.S+"\'"
        return Grammar(set(G.N) | {new_s},G.T, set (G.P) | set([Production(new_s,(G.S,))]),new_s)
    return G

#NON_SOLITARY TERMINAL

def transform_nonsolitary(G):
    prods = set()
    for A, α in G.P:
        if len(α) > 1 and set(α) & G.T:
            rhs = []
            for x in α:
                if x in G.T:
                    N = 'N{}'.format(x)
                    prods.add(Production(N, (x, )))
                    rhs.append(N)
                else:
                    rhs.append(x)
            prods.add(Production(A, rhs))
        else:            
            prods.add(Production(A, α))
    return Grammar(G.N | {A for A, α in prods}, G.T, prods, G.S)

#MAKE RULES BINARY

def make_binary(G):
    prods = set()
    for A, α in G.P:
        if len(α) > 2:
            Ai = '{}{}'.format(A, 1)
            prods.add(Production(Ai, α[:2]))
            for i, Xi in enumerate(α[2:-1], 2):
                prods.add(Production('{}{}'.format(A, i), (Ai, Xi)))
                Ai = '{}{}'.format(A, i)
            prods.add(Production(A, (Ai, α[-1])))
        else:
            prods.add(Production(A, α))
    return Grammar(G.N | {A for A, α in prods}, G.T, prods, G.S)

#ELIMINATING ε-RULES

@closure
def replace_in_rhs(G, A):
    Ap = A + '’'
    prods = set()
    for B, β in G.P:
        if A in β:
            pos = β.index(A)
            rhs = β[:pos] + β[pos + 1:]
            if len(rhs) == 0: rhs = ('ε', )
            prods.add(Production(B, rhs))
            prods.add(Production(B, β[:pos] + (Ap, ) + β[pos + 1:]))
        else:
            prods.add(Production(B, β))    
    return Grammar(G.N | {Ap}, G.T, prods, G.S)

@closure
def inline_ε_rules(G_seen):
    G, seen = G_seen
    for A in G.N - seen:
        if ('ε', ) in G.alternatives(A):
            return replace_in_rhs(G, A), seen | {A}
    return G, seen

def eliminate_ε_rules(G):
    Gp, _ = inline_ε_rules((G, set()))
    prods = set(Gp.P)
    for Ap in Gp.N - G.N:
        A = Ap[:-1]
        for α in set(Gp.alternatives(A)) - {('ε', )}:
            prods.add(Production(Ap, α))
    return Grammar(Gp.N, Gp.T, prods, Gp.S)
#ELIMINATING UNIT RULES
@closure
def eliminate_unit_rules(G_seen):
    G, seen = G_seen
    for P in set(filter(Production.such_that(rhs_len = 1), G.P)) - seen:
        A, (B, ) = P
        if B in G.N:            
            prods = (set(G.P) | {Production(A, α) for α in G.alternatives(B)}) - {P}
            return Grammar(G.N, G.T, prods, G.S), seen | {P}
    return G, seen


#----EASTER HOMEWORK EXERCISE 3-------------------------------------------------------------------------------------------
#given a list with the progressive order of the function to call
def normalize_a_grammar(G,l):

    fun_list=[start_replacing,
            transform_nonsolitary,
            make_binary,
            eliminate_ε_rules,
            eliminate_unit_rules]
    for i in l:
        if fun_list[i].__name__=="eliminate_unit_rules":G,_=fun_list[i]((G,set()))
        else:G=fun_list[i](G)
    return G

#--------------------------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    s="""
    Numbers -> Integer | Real
    Integer -> Digit | Integer Digit
    Real -> Integer Fraction Scale
    Fraction -> . Integer
    Scale -> e Sign Integer | Empty
    Digit -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    Sign -> + | -
    Empty -> ε
    """
    transformed=[]
    G=Grammar.from_string(s)
    #wikipedia order
    transformed.append(normalize_a_grammar(G,range(5)))
    transformed.append(normalize_a_grammar(G,[3,0,4,1,2]))
    #book order
    transformed.append(normalize_a_grammar(G,[2,0,4,1,3]))
    for g1 in transformed: print(g1,"\nCardinalità insieme non-terminali: {}\nCradinalità insieme delle produzioni: {}".format(len(g1.N),len(g1.P)),"\n","-"*20)
    

