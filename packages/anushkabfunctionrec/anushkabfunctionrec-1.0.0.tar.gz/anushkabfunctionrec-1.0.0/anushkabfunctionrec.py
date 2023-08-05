# -*- coding: utf-8 -*-
"""anushkabfunctionrec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pTOg__Yyi_OQHa8FJnq02ChgnpR3OETy
"""

#This function allows you to extract each element from the list.
#This is specifically used for nested lists.
def print_elist(a_list):
  for eachelement in a_list:
    #This checks whether your element is a list or not
    if isinstance(eachelement,list):
      #If it is a list,we will recurse the function and retrieve each element
      print_elist(eachelement)
    else:
      #If it is not a list, we will print the element.
      print(eachelement)