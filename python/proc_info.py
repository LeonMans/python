import sys
import os
import numpy as np
import re
sys.path.append('/mount/vol1/scratch/work/stremmer/software/lib/')


def get_all_procs(order):
   if order=="lo":
      mode=["LO"]
   elif order=="nlo":
      mode=["I1_pjc_final","Frag_final_smear","Frag_fragfunc_final_smear","I1_final","KP1_final","RS1_1_tot_final_smear","Virt1_final"]
      mode=["I1_pjc_final_qcut","Frag_final_qcut_smear","Frag_fragfunc_final_qcut_smear","I1_final_qcut","KP1_final_qcut","RS1_1_tot_final_qcut_smear","Virt1_final_qcut"]
   else:
      print("order ({0}) not found".format(order))
      sys.exit(0)

   return mode




def get_process(mode,ngamma):
   if mode=="LO" or mode=="I" or mode=="KP" or mode=="Virt":
      process=["gg","uux","uxu","ddx","dxd","bbx","bxb","bb","bxbx"]
   elif mode.find("RS")==0:
      process=["uux_udxg"]
   elif mode.find("Frag")==0:
      process=["gu","ug","gux","uxg","gd","dg","gdx","dxg","gb","bg","gbx","bxg"]
   else:
      print("mode ({0}) not found".format(mode))
      sys.exit(0)

   corrfac=[1.0]*len(process)


   alpha_old=0.75590479227951E-02
   alpha_new=1.0/137.035999084

   for i in range(0,len(corrfac)):
      corrfac[i]=((alpha_new/alpha_old)**ngamma)*corrfac[i]

   return process,corrfac
