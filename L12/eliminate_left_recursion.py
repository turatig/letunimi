from liblet import Grammar,Production
def eliminate_left_recursion(G):
    def new_rules(N):
        head,tail,tails=N+"h",N+"t",N+"ts"
        prods=set((Production(N,(head,tails)),Production(N,(head,)),Production(tails,(tail,tails)),Production(tails,(tail,))))
        for rhs in G.alternatives(N):
            if rhs[0]==N:prods.add(Production(tail,rhs[1:]))
            else:prods.add(Production(head,rhs))
        return prods,set([head,tail,tails])
    left_recursive_nt={P for P,rhs in G.P if P==rhs[0]}
    prods={P for P in G.P if P.lhs not in left_recursive_nt}
    nt=set(G.N)
    for N in left_recursive_nt:
        new_prods,new_nt=new_rules(N)
        prods|=new_prods
        nt|=new_nt

    return Grammar(nt,G.T,prods,G.S)

def match(t,rest):
    if t==rest[0]:return True,rest[1:]
    else:return False,rest

def recursive_descend(G,INPUT):

    def parse(N,deriv,rest):
        if rest[0]=='#':return True,'ε',deriv
        elif N=="T":
            s,r=match("t",rest)
            if s: return True,r,deriv.leftmost(G.P.index(Production(N,("t",))))
        elif N=="E":
            s,r=parse("Eh",deriv,rest)
            if s:
                pass

            
s="""
E -> E + T | E - T | T
T -> t
"""
G=Grammar.from_string(s)
G=eliminate_left_recursion(G)
for P in G.P:
    print(P)