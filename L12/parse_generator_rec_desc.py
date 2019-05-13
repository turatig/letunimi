from liblet import Grammar,Production
import sys
#USAGE: python3 parser_generator_rec_desc.py parser_program_name
#valid for the grammar defined in main
#Genera un parser che soddisfa i requisiti di HOMEWORK 1 e 4
def make_parse_source(G):
    code_ifs = []
    code_defs = []
    code_defs.append("#Code generated with parse_generator_rec_desc.py")
    code_defs.append('import sys')
    code_defs.append('def match(t,rest):')
    code_defs.append('\tif t==rest[0]: return True,rest[1:],[t]')
    code_defs.append('\telse:return False,rest,[]')
    for A in G.N:
        code_ifs.append("def parse_{}(rest):".format(A))
        for n, α in enumerate(G.alternatives(A)):
            code_defs.append("def alt_{}_{}(rest):\n\talt_rest=rest\n\tchildren=['{}']".format(A,n,A))
            for X in α:
                if X in G.T: 
                    code_defs.append("\tsucc,alt_rest,c = match('{}',alt_rest)".format(X))
                    code_defs.append("\tif not succ:return False,rest,[]")
                    code_defs.append("\tchildren.append(c)")
                else:
                    code_defs.append("\tsucc,alt_rest,c= parse_{}(alt_rest)".format(X))
                    code_defs.append("\tif not succ:return False,rest,[]")
                    code_defs.append("\tchildren.append(c)")
            code_defs.append("\treturn True,alt_rest,children")
            code_ifs.append("\tsucc_alt,rest,c= alt_{}_{}(rest)".format(A, n))
            code_ifs.append("\tif succ_alt: return True,rest,c".format(A, n))
        code_ifs.append("\treturn False,rest,[]")
    code_ifs.append('if __name__==\'__main__\':')
    code_ifs.append('\trest=sys.argv[1]+\'#\'')
    code_ifs.append('\tbelong_to,_,parse_tree=parse_{}(rest)'.format(G.S))
    code_ifs.append("\tif belong_to:print(parse_tree)\n\telse:print('Invalid Expression')")
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
