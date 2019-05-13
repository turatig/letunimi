from liblet import Grammar,Production
import sys
#USAGE: python3 global_parser_generator.py parser_program_name
#valid for the grammar defined in main
#using global variable only
#Genera un parser che soddisfa i requisiti di HOMEWORK 2 e 3
def make_parse_source(G):
    code_ifs = []
    code_defs = []
    code_defs.append("#Code generated with global_parser_generator.py")
    code_defs.append("import sys")
    code_defs.append("from liblet import Grammar,Production,Derivation")
    code_defs.append("rest=''\npos=0\nderiv=None")
    code_defs.append("def logn(f):\n\tdef scope(*args):\n\t\tprint('Call function :',f.__name__,' with args {}'.format(args))")
    code_defs.append("\t\treturn f(*args)\n\treturn scope")
    code_defs.append("\ndef end_match():\n\tglobal rest,pos,deriv\n\tif rest and pos==len(rest):print(deriv)")
    code_defs.append("\ndef match(t,cont):\n\tglobal rest,pos\n\tif rest and t==rest[pos]:\n\t\tpos+=1\n\t\tcont()")
    for A in G.N:
        code_ifs.append("def parse_{}(cont):".format(A))
        for a, α in enumerate(G.alternatives(A)):
            d = G.P.index(Production(A, α))
            code_defs.append('def {}_alt{}(cont):\n\tglobal pos,deriv\n\tp=pos\n\tcopy=deriv\n\tderiv=deriv.leftmost({})'.format(A,a,d))
            #definition of nested funcitons labeled "t"^t
            for t in range(1, len(α)):
                code_defs.append('{}def {}():'.format('\t' * t, 't' * (len(α) - t)))
            for t, X in enumerate(reversed(α)):
                if X in G.T:
                    code_defs.append("{}match('{}', {})".format('\t' * (len(α) - t), X, 't' * t if t else 'cont'))
                else:
                    code_defs.append("{}parse_{}({})".format('\t' * (len(α) - t), X, 't' * t if t else 'cont'))
            code_defs.append("\tpos=p\n\tderiv=copy")
            code_ifs.append('\t{}_alt{}(cont)'.format(A, a, d))
    code_ifs.append('if __name__==\'__main__\':')
    code_ifs.append("\ts=\"\"\"")
    for p in G.P:
        code_ifs.append("\t{}".format(p))
    code_ifs.append("\t\"\"\"")
    code_ifs.append('\trest=sys.argv[1]')
    code_ifs.append("\tderiv=Derivation(Grammar.from_string(s))")
    code_ifs.append('\tparse_{}(end_match)'.format(G.S))
    return '\n'.join(code_defs) + '\n' + '\n'.join(code_ifs)

if __name__=="__main__":

    s="""
    S -> A | a B
    A -> a
    B -> b
    """
    source=make_parse_source(Grammar.from_string(s))
    f=open("{}.py".format(sys.argv[1]),"w+")
    for line in source:
        f.write(line)
    f.close()