from liblet import *
#PRETTY USELESS BOILER PLATE:
#just wanted a top() method for the stack obj
class EmptyStack(Exception):
    def __init__(self,m):
        self.__m__=m
    def __str__(self):
        return self.__m__

class stack():
    def __init__(self,l=[]):
        self.__l__=[i for i in l]
        self.__lungh__=len(l)
    def __len__(self):
        return self.__lungh__
    def __str__(self):
        return str(self.__l__)
    def __iter__(self):
        self.__inc__=0
        return self
    def __next__(self):
        self.__inc__+=1
        if self.__inc__>self.__lungh__:raise StopIteration
        return self.__l__[self.__inc__-1]
    def push(self,e):
        self.__l__.append(e)
        self.__lungh__+=1
    def pop(self):
        try:
            r=self.__l__[self.__lungh__-1]
        except IndexError as e:
            raise EmptyStack("The stack is empty")
        self.__l__=self.__l__[:self.__lungh__-1]
        self.__lungh__-=1
        return r
    def top(self):
        try:
            r=self.__l__[self.__lungh__-1]
        except IndexError as e:
            raise EmptyStack("The stack is empty")
        return r
    def copy(self):
        return stack([el for el in self.__l__])
        
#USEFULL CODE
def logn(f):
    def scope(*args):
        print("Call function ",f.__name__.upper(),"\nwith args: ",end='(')
        for i in args:
            print(i,end=", ")
        print(")","\n")
        return f(*args)
    return scope

#@logn
def shift(st,rest):
    copy=st.copy()
    copy.push([rest[0]])
    return copy,rest[1:]
#@logn
def reduce(p,st,rest):
    copy=st.copy()
    children=[copy.pop() for t in p.rhs][::-1]
    copy.push([p.lhs]+children)
    return copy,rest

#HOMEWORK 1:
#general bottom up bf reimplemented with option for printing steps
def breadth_first(G,INPUT,verb=False):
    def end_parse(st,rest):
        if not rest and len(st)==1 and st.top()[0]==G.S:
            print("Parse tree")
            print(st.top())
            return True
        return False

    q=Queue()
    q.enqueue((stack(),INPUT))
    while q:
        sta,rst=q.dequeue()
        if verb: print("Current stack:",[i[0] for i in sta],"\ninput left: ",rst)
        if not end_parse(sta,rst):
            copy=sta.copy()
            el=[copy.pop()[0] for i in range(len(sta))][::-1]
            tops={tuple([i for i in el[len(el)-j:len(el)]]) for j in range(1,len(el)+1)}
            if verb:print("possibly matching rhss: ",tops)
            if rst:
                    s,r=shift(sta,rst)
                    q.enqueue((s,r))
            for p in [p for p in G.P if p.rhs in tops]:
                    s,r=reduce(p,sta,rst)
                    q.enqueue((s,r))
#HOMEWORK 2:
#df bottom-up reimplemented in purely recursive style. Doesn't append tree but just symbol

def depth_first(G,INPUT):
    def reduce(p,st,tree):
        sc=st.copy()
        [sc.pop() for i in p.rhs]
        t=[G.P.index(p)]+[i for i in tree]
        sc.push(p.lhs)
        return sc,t
    def shift(st,rest):
        sc=st.copy()
        sc.push(rest[0])
        return sc,rest[1:]
    def end_parse(st,rest,tree):
        if len(st)==1 and st.top()==G.S and not rest:
            print("Parse tree")
            d=Derivation(G)
            for i in tree:d=d.leftmost(i)
            print(d)
            return True
        return False
    def df(st,rest,tree):
        if not end_parse(st,rest,tree):
            sc=st.copy()
            el=[sc.pop() for i in st][::-1]
            tops={tuple([i for i in el[len(el)-j:len(el)]]) for j in range(len(st)+1)}
            if rest:
                sc,rst=shift(st,rest)
                df(sc,rst,tree)
            for rule in [p for p in G.P if p.rhs in tops]:
                sc,t=reduce(rule,st,tree)
                df(sc,rest,t)
    df(stack(),INPUT,[])
    
if __name__=="__main__":
    n=input("Do you want to run in verbose?[y/n]: ")
    g = Grammar.from_string('S -> a S b | S a b | a a a')
    if n=="y":b=True
    else:b=False
    breadth_first(g,"aaaab",b)
    print("Depth first")
    depth_first(g,"aaaab")




        
