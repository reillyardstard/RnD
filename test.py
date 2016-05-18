# -*- coding: utf-8 -*-
"""
Created on Tue May 10 22:38:41 2016

@author: jasonsmith
"""
import time

def f1():
    for a in range(1, 1000) :
        for b in range(1, 1000) :
            for c in range(1, 1000) :
                if a + b + c == 1000 :
                    if (a*a) + (b*b) == (c*c):
                        print 'f1()',a,b,c
                        return          

def f2():  
    for a in range(1, 1000) :
        for b in range(a, 1000) :
            for c in range(b, 1000) :
                if a + b + c == 1000 :
                    if (a*a) + (b*b) == (c*c):
                        print 'f2()',a,b,c
                        return 

s1=time.clock()
#f1()  # 13.5
s2=time.clock()
print(s2-s1)                

s1=time.clock()
#f2()  # 5.6
s2=time.clock()
print(s2-s1)                

