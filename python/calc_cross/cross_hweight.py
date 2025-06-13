import sys
import os
sys.path.append('/mount/vol1/scratch/work/stremmer/software/lib/')
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
path="/mount/vol1/scratch/work/stremmer/event_files/tta_frag/nlo/"
out_path="../../cross/nlo{0}/".format(iadd)



iadd2=""
if order=="lo":
    iorders=[2]
    mode=get_all_procs(order)
elif order=="nlo":
    iorders=[3]
    tmodes=get_all_procs(order)
    mode=[]
    for i in range(0,len(tmodes)):
       if tmodes[i].find("Virt")==0:
           continue
       mode.append(tmodes[i])
    mode.append("RS_fix")
    mode.append("Frag_I_fix")
    mode.append("Frag_aleph_fix")
    mode.append("RS_fix2")
    mode.append("Frag_I_fix2")
    mode.append("Frag_aleph_fix2")
    mode.append("RS_hyb")


    #mode=["RS_frix_smear"]
    #mode=["I","KP"]
    #mode=["RS_frix_smear"]
    #mode=["RS_fix2_smear","RS_hyb_smear","RS_frix_smear"]
elif debug!=True:
    sys.exit(0)





if debug:
    tmode="Born11"
    tprocess=["gg"]
    alpha_scal=0.9304426637238681
    scaling=alpha_scal*1.0*(1.3535983e0/1.4806842e0)**2
    #scaling=1.0

    tcorrfac=[scaling]*len(tprocess[0])

    hweight.calc_cross(order,tmode,tprocess,path,out_path,rescal=tcorrfac)
else:
    iskip=[]
    for i in range(0,len(mode)):
        tmode=mode[i]+iadd2

        tpath="{0}{1}/".format(path,tmode)
        if(os.path.exists(tpath) == False):
            #print("Skip {0}".format(mode[i]))
            iskip.append(tmode)
            continue

        process_temp,corrfac_temp=get_process(mode[i],ngamma)

        print(tmode) #corrfac_temp


        #security check
        icheck=False
        for j in range(0,len(process_temp)):
            if len(os.listdir("{0}{1}/hist/".format(tpath,process_temp[j])))==0:
                icheck=True
                break
        if icheck:
            iskip.append(tmode)
            continue

        if False:
            process_temp2=process_temp
            process_temp=[]
            corrfac_temp2=corrfac_temp
            corrfac_temp=[]
            for j in range(0,len(process_temp2)):
                if process_temp2[j]!="gg":
                    process_temp.append(process_temp2[j])
                    corrfac_temp.append(corrfac_temp2[j])


        tprocess=process_temp
        tcorrfac=corrfac_temp
        hweight.calc_cross(order,tmode,tprocess,path,out_path,rescal=tcorrfac,iord=iorders)
        print("\n\n")

    print("{0} modes are skipped:".format(len(iskip)))
    for i in range(0,len(iskip)):
        print("{0}: {1}".format(i,iskip[i]))
