from liblet import *
from cnf_transforming import *
from cleaning_cf import *
    
#CYK ALGORITHM
#return the recognition table in lol from dict R
def print_tab(R):  
    def from_dict_to_tab(R):
        max_length_key=[t2 for t1,t2 in R.keys() if len([t4 for t3,t4 in R.keys() if t4>t2])==0][0]
        l=[[(key,value) for key,value in R.items() if key[1]==x] for x in range(max_length_key,-1,-1)]
        for i in l:
            i.sort(key=lambda t:t[0][0])
            for j in range(len(i)):
                if i[j][1]==set():i[j]="_"
                else: i[j]=i[j][1]
        return l  
    for i in from_dict_to_tab(R):
            for j in i:
                for k in j:
                    print(k,end=" ")
                print("|",end=" ")
            print()

def cyk(G,s):
    def fill(R,i,l):
        res=set()
        if l==1:
            for A,(a,*rest) in G.P:
                if a==s[i]: res.add(A)
        else:
            for k in range(1,l):
                for A,a in G.P:
                    #a[0] because a is a tuple and we want the first string corresponding to a single right-hand-side
                    if len(a)!=2:continue
                    B,C=a
                    #if in CNF, this statement try to reduce every B,C already added to the table,
                    #observing that if we are searching for all the non-terminals which derive
                    #substr of s starting from i and of length l, we have to found those who match the requirement to have
                    #a right-hand of which the elements are in the table at position [i,k] (the first non-terminal derives substr at position i
                    # of length k) and at position [i+k,l-k] for a k in (1,l-1) included 
                    if B in R[(i,k)] and C in R[(i+k,l-k)]:res.add(A)
        return res
    R={}
    #online fill
    for i in range(len(s)):
        for j in range(i+1):
            R[(i-j,j+1)]=fill(R,i-j,j+1)
    if G.S in R[(0,len(s))]: return R,True
    else: return R,False

def get_parse_tree(G,R,INPUT):
    def get_nodes(X,i,j):
        if j==1: return [X,[INPUT[i]]]
        else:
            for k in range(1,j):
                for X,(B,C) in filter(Production.such_that(lhs=X,rhs_len=2),G.P):
                    if B in R[(i,k)] and C in R[(i+k,j-k)]:return [X,get_nodes(B,i,k),get_nodes(C,i+k,j-k)]
    return get_nodes(G.S,0,len(INPUT))



#----EASTER HOMEWORK EXERCISE 2-------------------------------------------------------------------------------------------
#with grammar in CNF G=Grammar in CNF , R=Rcognition table, INPUT
def get_parse_forest(G,R,INPUT):
    def get_nodes(X,i,j):
        if j==1: return [[X,[INPUT[i]]]]
        else:
            parse_forest=[]
            for k in range(1,j):
                for X,(B,C) in filter(Production.such_that(lhs=X,rhs_len=2),G.P):
                    if B in R[(i,k)] and C in R[(i+k,j-k)]:
                        for h in get_nodes(B,i,k):
                            for z in get_nodes(C,i+k,j-k):
                                parse_forest.append([X,h,z])
            return parse_forest

    return get_nodes(G.S,0,len(INPUT))
#--------------------------------------------------------------------------------------------------------------------------

#----EASTER HOMEWORK EXERCISE 1-------------------------------------------------------------------------------------------
#with the original grammar G=Original_Grammar in CNF , R=Rcognition table, INPUT
def get_orig_parse_forest(G,R,INPUT):
    #adding sets for ε_rules to the recognition table
    nullable={P for P,rhs in G.P if 'ε' in rhs}
    if len(nullable)!=0:
        for i in range(len(INPUT)+1):
            R[(i,0)]=nullable

    #checks the rule applicability and returns positions in the recognition table for all the symbols in the right hand side
    def check_rhs(rhs,i,l):
        if not rhs:
            return (l==0 and [[("#","#")]])
        if rhs[0] in G.T:
            if i<len(INPUT) and INPUT[i]!=rhs[0]:return False
            positions=[]
            #check if the rest of right hand-side match the string 
            part_res=check_rhs(rhs[1:],i+1,l-1)
            #if the rest of the rhs matches
            if part_res:
                #combine the results
                for t in part_res:
                    positions.append([(i,"In input")]+t)
            return len(positions)!=0 and positions
        #if the current symbol is a non-terminal
        else:
            positions=[]
            start=1
            #if the non-terminal is lhs of an ε_rule,try length 0 too
            if rhs[0] in nullable:
                start=0
            for k in range(start,l+1):
                #if there's a match
                if rhs[0] in R[(i,k)]:
                    part_res=check_rhs(rhs[1:],i+k,l-k)
                    #if the rest of the rhs matches
                    if part_res:
                        #combine the results
                        for t in part_res:
                            positions.append([(i,k)]+t)            
            return len(positions)!=0 and positions



    def get_nodes(X,i=0,j=0):
        if X in G.T: return [[X]]
        if j==0: return [[X,['ε']]]
        else:
            parse_forest=[]
            #for every production check applicability
            for A,rhs in filter(Production.such_that(lhs=X),G.P):
                    checked=check_rhs(rhs,i,j)
                    #if the rule is applicable
                    if(checked):
                        #for every positions for which the rule produces input from i to j
                        for t in checked:
                            part_forest=[[X]]
                            for p in range(len(rhs)):
                                acc=[]
                                for r in get_nodes(rhs[p],*t[p]):
                                    for c in part_forest:
                                        acc.append(c+[r])
                                part_forest=[n for n in acc]
                            for complete_tree in part_forest:
                                parse_forest.append(complete_tree)
            return parse_forest
    #if the original grammar is ε_rules free
    if len(nullable)==0:
        return get_nodes(G.S,0,len(INPUT))
    #else we have to match 
    else:
        return get_nodes(G.S,0,len(INPUT))
#--------------------------------------------------------------------------------------------------------------------------


def get_leftmost_prods(G, R, INPUT):
    @show_calls(True)
    def prods(X, i, l):
        if l == 1:
            return [G.P.index(Production(X, (INPUT[i],)))]
        for A,(B,C) in filter(Production.such_that(lhs = X, rhs_len = 2), G.P):
            for k in range(1, l):
                if B in R[(i, k)] and C in R[(i + k, l - k)]:
                    return [G.P.index(Production(A, (B,C)))] + prods(B, i, k) + prods(C, i + k, l - k)
    return prods(G.S, 0, len(INPUT))

def get_rightmost_prods(G, R, INPUT):
    @show_calls(True)
    def prods(X, i, l):
        if l == 1:
            return [G.P.index(Production(X, (INPUT[i],)))]
        for A, (B,C) in filter(Production.such_that(lhs = X, rhs_len = 2), G.P):
            for k in range(1, l):
                if B in R[(i, k)] and C in R[(i + k, l - k)]:
                    return  [G.P.index(Production(A,(B,C)))]+prods(C, i + k, l - k)+prods(B, i, k)
    return prods(G.S, 0, len(INPUT))


if __name__=="__main__":
    t="""
    Numbers -> Integer | Real
    Integer -> Digit | Integer Digit
    Real -> Integer Fraction Scale
    Fraction -> . Integer
    Scale -> e Sign Integer | Empty
    Digit -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    Sign -> + | -
    Empty -> ε
    """
    s="""
    A -> A + A | A + A B
    A -> A - A
    A -> A * A
    A -> a
    B -> ε
    """

    #testing with inherently ambigous grammar s
    G=normalize_a_grammar(Grammar.from_string(s),range(5))
    INPUTs="a+a-a"
    tab,belonging=cyk(G,INPUTs)
    if belonging:
        print("Recognition table for input {}".format(INPUTs))
        print_tab(tab)
        forest1=get_parse_forest(G,tab,INPUTs)
        print("Parse for forest for cnf grammar")
        for i in forest1:
            print(i)
        forest2=get_orig_parse_forest(Grammar.from_string(s),tab,INPUTs)
        print("Parse for forest for the original grammar")
        for i in forest2:
            print(i)
    else:print("La parola non appartiene al linguaggio generato da G")

    #testing with book grammar t
    #normalize the grammar applying functions in the wikipedia order (cnf_transforming.py for normalize a grammar function)
    G=normalize_a_grammar(Grammar.from_string(t),range(5))
    #G=clean(G)
    INPUTt='32.5e+1'
    tab,belonging=cyk(G,INPUTt)
    if belonging:
        print("Recognition table for input {}".format(INPUTt))
        print_tab(tab)
        forest1=get_parse_forest(G,tab,INPUTt)
        print("Parse for forest for cnf grammar")
        for i in forest1:
            print(i)
        forest2=get_orig_parse_forest(Grammar.from_string(t),tab,INPUTt)
        print("Parse for forest for the original grammar")
        for i in forest2:
            print(i)
    else:print("La parola non appartiene al linguaggio generato da G")