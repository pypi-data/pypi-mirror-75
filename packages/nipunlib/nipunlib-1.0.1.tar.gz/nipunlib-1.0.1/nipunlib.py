# -*- coding: utf-8 -*-
"""nipunlib.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12zGcell3oXOf-GwsxWthQDveZnchvu5_
"""

def reclist(a_list):
  for eachelement in a_list:
    if isinstance(eachelement, list):
      reclist(eachelement)
    else:
      print(eachelement)

