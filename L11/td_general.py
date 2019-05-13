from liblet import *
def bf(G,INPUT,verb=False):
    q=Queue()
    q.enqueue((Derivation(G),Stack(['#',G.S]),INPUT+"#"))
    while q:
        rule_chain,st,rest=q.dequeue()
        cur_symbol=st.pop()
        if verb:print("Current symbol extracted from stack ",cur_symbol,"\nInput left: ",rest)
        if cur_symbol==rest[0]=="#":#EXPRESSION PARSED
            print("-"*50,"\n"*5)
            print("EXPRESSION PARSED",rule_chain)
            print("\n"*5,"-"*50)
            continue
        if cur_symbol in G.N:
            #PREDICT
            if verb:print("PREDICT UPDATE")
            for rule in [p for p in G.P if p.lhs==cur_symbol]:
                rc=rule_chain.leftmost(G.P.index(rule))
                n_st=st.copy()
                for r in rule.rhs[::-1]:
                    n_st.push(r)
                q.enqueue((rc,n_st,rest))
                if verb:print("\n"*2,"rule",rule,"\nstate description {}".format((rc,n_st,rest))," enqueued","\n"*2)
        else:
            #MATCH
            if cur_symbol==rest[0]:
                if verb:print(" "*30,"SUCCESSFULL MATCH : {} starts with {}".format(rest,cur_symbol),"\n"," "*30,"{} may parse input".format(rule_chain))
                q.enqueue((rule_chain,st,rest[1:]))
            elif verb:print(" "*30,"MATCH FAILED: keep calm and backtrack...")
if __name__=="__main__":          
    G = Grammar.from_string("""
    S -> A B | D C 
    A -> a | a A
    B -> b c | b B c 
    D -> a b | a D b 
    C -> c | c C | ε
    """)
    G
    word = 'aabc'
    n=input("Run in verbose mode?[y/n]: ")
    if n=="y":b=True
    else:b=False
    bf(G, word,b)
    n=input("Want beahaviour with ε_rules?[y/n]: ")
    if n=="y":
        G = Grammar.from_string("""
        S -> A B | D C 
        A -> a | a A | C A | ε
        B -> b c | b B c 
        D -> a b | a D b | C D 
        C -> c | c C | ε
        """)
        G
        word = 'aabc'
        n=input("Run in verbose mode?[y/n]: ")
        if n=="y":b=True
        else:b=False
        bf(G, word,b)