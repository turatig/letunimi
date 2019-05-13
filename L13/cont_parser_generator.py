from liblet import Grammar,Production
import sys
#USAGE: python3 cont_parser_generator.py parser_program_name
#valid for the grammar defined in main
#Genera un parser che soddisfa i requisiti di HOMEWORK 1
def make_parse_source(G):
    code_ifs = []
    code_defs = []
    code_defs.append("#Code generated with cont_parser_generator.py")
    code_defs.append("import sys")
    code_defs.append("from liblet import Grammar,Production,Derivation")
    code_defs.append("def end_match(deriv,rest):\n\tif not rest:print(deriv)")
    code_defs.append("def match(deriv,t,rest,cont):\n\tif rest and t==rest[0]:cont(deriv,rest[1:])")
    for A in G.N:
        code_ifs.append("def parse_{}(deriv,rest,cont):".format(A))
        for a, α in enumerate(G.alternatives(A)):
            
            code_defs.append('def {}_alt{}(deriv, rest,cont):'.format(A, a))
            for t in range(1, len(α)):
                code_defs.append('{}def {}(deriv, rest):'.format('\t' * t, 't' * (len(α) - t)))
            for t, X in enumerate(reversed(α)):
                if X in G.T:
                    code_defs.append("{}match(deriv, '{}', rest, {})".format('\t' * (len(α) - t), X, 't' * t if t else 'cont'))
                else:
                    code_defs.append("{}parse_{}(deriv,rest,{})".format('\t' * (len(α) - t), X, 't' * t if t else 'cont'))
            d = G.P.index(Production(A, α))
            code_ifs.append('\t{}_alt{}(deriv.leftmost({}), rest,cont)'.format(A, a, d))
    code_ifs.append('if __name__==\'__main__\':')
    code_ifs.append("\ts=\"\"\"")
    for p in G.P:
        code_ifs.append("\t{}".format(p))
    code_ifs.append("\t\"\"\"")
    code_ifs.append('\trest=sys.argv[1]')
    code_ifs.append('\tparse_{}(Derivation(Grammar.from_string(s)),rest,end_match)'.format(G.S))
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