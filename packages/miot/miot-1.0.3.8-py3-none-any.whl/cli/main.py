#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

__version__ = '1.0.3.8'

def main():
    if "--version" in sys.argv[1:]:
        print(__version__)
        exit(0)

    print( "Welcome to the jungle" )

if __name__ == "__main__":
    main()
    
