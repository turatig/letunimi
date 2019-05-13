from liblet import Grammar,Production
import sys
#USAGE: python3 generate_all_globals.py parser_program_name
#valid for the grammar defined in main
#using global variable only
#Genera un parser che soddisfa i requisiti di HOMEWORK 2 e 3
def make_parse_source(G):
    code_ifs = []
    code_defs = []
    code_defs.append('import sys')
    code_defs.append("#Code generated with generate_all_globals.py")
    code_defs.append('rest=\'\'')
    code_defs.append('pos=0')
    code_defs.append('deriv=[]')
    code_defs.append('def match(t):')
    code_defs.append('\tglobal rest,pos')
    code_defs.append('\tif t==rest[pos]:\n\t\tpos+=1\n\t\treturn True')
    code_defs.append('\telse:return False')
    for A in G.N:
        code_ifs.append("def parse_{}():\n\tglobal deriv".format(A))
        for n, α in enumerate(G.alternatives(A)):
            code_defs.append("def alt_{}_{}(rule):\n\tglobal pos,deriv\n\tp=pos\n\tind=len(deriv)\n\tderiv.append(rule)".format(A, n))
            for X in α:
                if X in G.T: 
                    code_defs.append("\tsucc = match('{}')".format(X))
                    code_defs.append("\tif not succ:\n\t\tpos=p\n\t\tderiv=deriv[:ind]\n\t\treturn False")
                else:
                    code_defs.append("\tsucc= parse_{}()".format(X))
                    code_defs.append("\tif not succ:\n\t\tpos=p\n\t\treturn False")
            code_defs.append("\treturn True")
            code_ifs.append("\tsucc_alt= alt_{}_{}({})".format(A, n,G.P.index(Production(A,α))))
            code_ifs.append("\tif succ_alt: return True")
        code_ifs.append("\treturn False")
    code_ifs.append('if __name__==\'__main__\':')
    code_ifs.append('\trest=sys.argv[1]+\'#\'')
    code_ifs.append('\tif parse_{}():print(deriv)\n\telse:print(\'Invalid Expression\')'.format(G.S))
    return '\n'.join(code_defs) + '\n' + '\n'.join(code_ifs)

if __name__=="__main__":

    s="""
    E -> Eh Ets
    Ets -> Et #
    Eh -> T
    T -> t
    Et -> - T
    E -> Eh #
    Ets -> Et Ets
    Et -> + T
    """
    source=make_parse_source(Grammar.from_string(s))
    f=open("{}.py".format(sys.argv[1]),"w+")
    for line in source:
        f.write(line)
    f.close()
