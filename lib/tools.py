import numpy as np
import os
import sys


def check(inp,arr,ind=0):
   for i in range(0,len(arr)):
      if ind==0 and inp.find(arr[i])==0:
         return True
      if ind==-1 and inp.find(arr[i])!=-1:
         return True
   return False

def ifactorial(num):
   if num<0:
      print("ERROR in ifactorial")
      sys.exit(0)
   if num==0 or num==1:
      return 1
   res=1
   for i in range(1,num):
      res*=(i+1)
   return res