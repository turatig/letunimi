from liblet import *

def enclosing(f):

    def inference_rule(*args):
        #set dimension: monitors if at least one element were add
        closed=set(args[0])
        l=0
        while(l<len(closed)):
            l=len(closed)
            closed=f(closed,args[1])
        return closed

    return inference_rule


@enclosing
def productive(prod,G):
    #initialize the algorithm creating the set of productive symbols of the grammar including terminal (which are obviously productive)
    #consider all the productions
    for p in G.P:
        if set(p.rhs).issubset(prod):prod |={p.lhs}
    return prod

@enclosing
def reachable(prod,G):
    for p in G.P:
        if {p.lhs}.issubset(prod): prod |=set(p.rhs)
    return prod

def clean(G):
    #the matter here is that we have a tuple of productions so we can't remove from the tuple
    usefull=productive(set(G.T),G)
    G=Grammar(set(G.N) & usefull,G.T,(Production(p.lhs,p.rhs) for p in G.P if p.lhs in usefull and all(t in usefull for t in p.rhs)), G.S)
    usefull=reachable({G.S},G)
    G=Grammar(set(G.N) & usefull,G.T,(Production(p.lhs,p.rhs) for p in G.P if p.lhs in usefull and all(t in usefull for t in p.rhs)), G.S)
    return G



if __name__=="__main__":
    G = Grammar.from_string("""
    S -> A B | D E
    A -> a
    B -> b C
    C -> c
    D -> d F 
    E -> e 
    F -> f D
    """)
    G=clean(G)
    print(G)