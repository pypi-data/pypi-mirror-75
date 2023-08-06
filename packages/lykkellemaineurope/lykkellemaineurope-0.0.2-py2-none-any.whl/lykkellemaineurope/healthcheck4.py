# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 20:47:59 2019
daily checklist that runs a health check on the load details
@author: debaj
"""
from os.path import expanduser
from lykkelledatahandler.exceptioneod4 import exception

home = expanduser("~")

class exceptionlog:
    def __init__(self):
        print("-------------------------stockexceptionlog-------------------------------")
        exception.stockexception()
        print("-------------------------End-------------------------------")
        print("\n")
        print("-------------------------Benchmarkexceptionlog-------------------------------")
        exception.benchmarkexception()
        print("-------------------------End-------------------------------")
#        print("-------------------------Bondexceptionlog-------------------------------")
#        exception.bondexception()
#        print("-------------------------End-------------------------------")

#exceptionlog()



