import sys
import os
sys.path.append('/mount/vol2/data/Mans/lib')
sys.path.append('../')
from proc_info import*
import hweight_input as hweight
import re
import numpy as np




order="nlo"
debug=False
proc="tta"

ngamma=1


iadd=""
path="/mount/vol2/data/stremmer/event_files/tt_semi/nlo_qcut/"
out_path="../../samples/nlo{0}/".format(iadd)



if order=="lo":
    iorders=[2]
    mode=get_all_procs(order)
elif order=="nlo":
    iorders=[]
    tmodes=get_all_procs(order)
    mode=[]
    for i in range(0,len(tmodes)):
       if tmodes[i].find("Virt")==0:
           continue
       mode.append(tmodes[i])
    mode.append("RS")
    mode.append("Frag_I_fix")
    mode.append("Frag_aleph_fix")
    mode.append("RS_fix2")
    mode.append("Frag_I_fix2")
    mode.append("Frag_aleph_fix2")
    mode.append("RS_hyb")

    #mode=["RS_fix2","RS_hyb"]
    #mode=["RS_fix2_smear"]
    #mode=["RS_frix"]
    #mode=["RS_fix2_smear","RS_hyb_smear","RS_frix_smear"]
    #mode=["RS_frix_smear"]
    #mode=["RS_fix2_smear","RS_hyb_smear","RS_frix_smear"]
elif debug!=True:
    sys.exit(0)



pdf="NNPDF31_nlo_as_0118_luxqed"

if debug:
   pdf="NNPDF31_nlo_as_0118_luxqed"
   tmode="RS_frix_smear"
   tprocess=["gg"]
   #tprocess=["uux","uxu"]
   #tprocess=["gu","ug"]
   tag_app="_debug"



   processT,corrfacT=get_process(tmode,ngamma)

   tcorrfac=[]
   for i in range(0,len(tprocess)):
      ifound=False
      for j in range(0,len(processT)):
         if tprocess[i]==processT[j]:
            ifound=True
            tcorrfac.append(corrfacT[j])
      if ifound==False:
         print("process not found")
         sys.exit(0)


   #hweight.calc_hist(order,tmode,tprocess,pdf,path,out_path,sub="{0}".format(tag_app),rescal=tcorrfac) 
   hweight.calc_hist_ord(order,tmode,tprocess,pdf,path,out_path,sub="{0}".format(tag_app),iord=iorders,rescal=tcorrfac)

else:
   iskip=[]
   for i in range(0,len(mode)):
      tpath="{0}{1}/".format(path,mode[i])
      if(os.path.exists(tpath) == False):
          #print("Skip {0}".format(mode[i]))
          iskip.append(mode[i])
          continue

      tmode=mode[i]
      process_temp,corrfac_temp=get_process(mode[i],ngamma)
      print(tmode,process_temp)

      icheck=False
      for j in range(0,len(process_temp)):
          if len(os.listdir("{0}{1}/hist/".format(tpath,process_temp[j])))==0:
              icheck=True
              break
      if icheck:
          iskip.append(mode[i])
          continue



      tprocess=process_temp
      tcorrfac=corrfac_temp
      hweight.calc_hist_ord(order,tmode,tprocess,pdf,path,out_path,iord=iorders,rescal=tcorrfac)
      print("\n\n")

   print("{0} modes are skipped:".format(len(iskip)))
   for i in range(0,len(iskip)):
       print("{0}: {1}".format(i,iskip[i]))


