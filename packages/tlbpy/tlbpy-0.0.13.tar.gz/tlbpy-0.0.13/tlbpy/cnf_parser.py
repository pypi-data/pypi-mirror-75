#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['cnf_parser']

def cnf_parser(path):
    """
    CNF file parser
    """
    data = []
    nb_lit = 0
    nb_clause = 0
    with open(path) as f:
        i = 0
        for line in f.readlines():
            if not (line.startswith('c') or line.split() == [] or line.startswith('0')):
                if line.startswith('p'):
                    try:
                        _, _, nl, nc = line.split()
                        nb_lit = int(nl)
                        nb_clause = int(nc)
                    except:
                        raise Exception("(p) - parameter problem : " + str(line.split()))
                elif line.startswith('%'):
                    if data[-1][0] == 0:
                        raise Exception("Pas de bon nombre de clause dans le fichier : "+path)
                else:
                    try:
                        clause = [int(lit) for lit in line.split() if int(lit) != 0]
                        data.append(clause)
                        i+=1
                    except:
                        raise Exception("line["+str(i)+"] clause - parameter problem : "+str(line.split()))
    return data, nb_lit, nb_clause
