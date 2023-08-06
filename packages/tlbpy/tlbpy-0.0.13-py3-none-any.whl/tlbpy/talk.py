#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Talk']

class Talk:
    def __init__(self, talkative, compteur = 1):
        self.talkative = talkative
        self.i = 0
        self.max_compteur = compteur

    def __call__(self, say, *args, **kwargs):
        if self.talkative and (self.i % self.max_compteur == 0):
            try:
                print(say.format(*args, **kwargs))
            except:
                print("echec de l'affichage")
        self.i = (self.i + 1)%1000