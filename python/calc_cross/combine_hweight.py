import sys
sys.path.append('/mount/vol1/scratch/work/stremmer/software/lib/')
sys.path.append('../')
from proc_info import*
import hweight_input as hweight
import numpy as np
import math
import re


proc="tta"
order="nlo"
iorder=-1
#ifrag=0
iphot=""
iphot="fix2_smear"
#iphot="frix_smear"
#iphot="hyb_smear"
fragfunc=0 #fragfunc=0 -> ALEPH LO, fragfunc=0 -> BFG II



ngamma=1

iadd=""
#iadd="_lhe"
#iadd="_NNPDF31_lo_as_0130"



if order=="lo":
   outfile="cross_lo"
else:
   outfile="cross_nlo"


#if ifrag==1 and order=="nlo":
#   outfile="{0}_fix".format(outfile)
#elif ifrag==1 and order=="lo":
#   print("ERROR: deactivate fixed cone isolation!")
#   sys.exit(0)

if order=="nlo" and iphot!="":
   outfile="{0}_{1}".format(outfile,iphot)

   if fragfunc==1:
      outfile="{0}_bfg".format(outfile)


if iorder!=-1:
   outfile="{0}_as{1}".format(outfile,iorder)



scales=["et4","ht4","mt"]


path="../../cross/nlo{0}/".format(iadd)



modes=get_all_procs(order)

#if ifrag==1 and order=="nlo":
#   modesT=modes
#   modes=[]
#   for i in range(0,len(modesT)):
#      if modesT[i].find("RS")==0:
#         modes.append("{0}_fix".format(modesT[i]))
#      else:
#         modes.append(modesT[i])
#   modes.append("Frag_I_fix")
#   modes.append("Frag_aleph_fix")

if order=="nlo" and iphot!="":
   modesT=modes
   modes=[]
   for i in range(0,len(modesT)):
      if modesT[i].find("RS")==0:
         modes.append("{0}_{1}".format(modesT[i],iphot))
      else:
         modes.append(modesT[i])
   if iphot.find("fix")!=-1:
      modes.append("Frag_I_{0}".format(iphot.replace("_smear","")))
      if fragfunc==0:
         modes.append("Frag_aleph_{0}".format(iphot.replace("_smear","")))
      elif fragfunc==1:
         modes.append("Frag_bfg_{0}".format(iphot.replace("_smear","")))
      else:
         print("fragfunc ({0}) not found".format(str(fragfunc)))
         sys.exit(0)




corrfac=[1.0]*len(modes)



if order=="nlo":
   iord=[]
   iordT=iorder
   for i in range(0,len(modes)):
      if modes[i].find("Virt")==0:
         iord.append(-1)
         if iorder>=0:
            modes[i]="{0}_as{1}".format(modes[i],str(iorder))
      else:
         iord.append(iordT)
else:
   iord=[iorder]*len(modes)





ishow=True
ngrid=7
icollect=True


ipdf=0
if ipdf>0:
    if ipdf==1:
        pdf="NNPDF31_nlo_as_0118"
        ngrid=108
    elif ipdf==2:
        pdf="CT18NLO"
        ngrid=66
    elif ipdf==3:
        pdf="MSHT20nlo_as118"
        ngrid=72

    path="../../cross/nlo_pdf/"
    #path="../../cross/nlo_pdf_msht/"
    icollect=False
    scales=["et4_1"]
    for i in range(0,len(scales)):
        scales[i]="{0}_{1}".format(pdf,scales[i])




cross,err=hweight.combine_cross(path,modes,order,scales,ngrid,iord=iord,outfile=outfile,rescal=corrfac,icollect=icollect)


if ishow:
    print("Write Latex results (fb):")
    crossT=np.copy(cross)
    errT=np.copy(err)
    cross=cross*1e3
    err=err*1e3
    for i in range(0,len(scales)):
        print(scales[i])        

        if err[i,0]>1.0:
            print("ERROR")
            sys.exit(0)
        else:
            exp=0
            terr=err[i,0]
            while(terr<1.0):
                terr*=10.0
                exp-=1

        factor=10**(-(exp-1))
        err_latex=int(math.ceil(err[i,0]*factor))
        cross_latex=round(cross[i,0],-(exp-2))

        print("{0} +- {1}".format(cross[i,0],err[i,0]))
        print("{0}({1})".format(str(cross_latex),str(err_latex)))


        factor=10**(-(exp))
        err_latex=int(math.ceil(err[i,0]*factor))
        cross_latex=round(cross[i,0],-(exp))

        print("{0} +- {1}".format(cross[i,0],err[i,0]))
        print("{0}({1})".format(str(cross_latex),str(err_latex)))

        #scale_up=(np.max(cross[i])-cross[i,0])/cross[i,0]*100.0
        #scale_down=(np.min(cross[i])-cross[i,0])/cross[i,0]*100.0

        ngrid_scale=7
        scale_up=(np.max(cross[i,0:ngrid_scale:1])-cross[i,0])/cross[i,0]*100.0
        scale_down=(np.min(cross[i,0:ngrid_scale:1])-cross[i,0])/cross[i,0]*100.0

        print("$ {0}({1})^{{+{2}\%}}_{{{3}\%}} $".format('{:.{prec}f}'.format(cross_latex,prec=-exp),str(err_latex),round(scale_up,1),round(scale_down,1)))
        #print(cross[i,0]*scale_up/100,cross[i,0]*scale_down/100)

    cross=np.copy(crossT)
    err=np.copy(errT)


if ipdf==1:
    npdf=100.0
    if ngrid==102:
        ioff=2
    elif ngrid==108:
        ioff=8
    else:
        print("ERROR")
        sys.exit(0)

    for i in range(0,len(scales)):
        mean=0.0
        mean2=0.0
        for j in range(ioff,ngrid):
            mean+=cross[i,j]
            mean2+=cross[i,j]**2
        mean=mean/npdf
        mean2=mean2/npdf
        pdf_err=np.sqrt((npdf/(npdf-1.0))*(mean2-mean**2))
        cross0=cross[i,0]
        err0=err[i,0]
        pdf_unc=pdf_err/cross0*100
        #print(scales[i],pdf_err/cross[i,0]*100,cross[i,0],pdf_err)

        print("{0} = {1} +- {2}".format(scales[i],cross0*1e3,err0*1e3))
        print("pdf_unc = {0} ({1} %)".format(pdf_unc*cross0/100.0*1e3,pdf_unc))
elif ipdf==2 or ipdf==3:
    if ipdf==2:
        npdf=58
        factor=1.645
    elif ipdf==3:
        npdf=64
        factor=1.0
    ioff=8

    for j in range(0,len(scales)):
        cross0=cross[j,0]
        err0=err[j,0]

        cross_up=0.0
        cross_down=0.0
        for i in range(0,npdf//2):
            cross_up+=np.max(np.array([cross[j,ioff+2*i]-cross0,cross[j,ioff+2*i+1]-cross0,0.0]))**2
            cross_down+=np.max(np.array([cross0-cross[j,ioff+2*i],cross0-cross[j,ioff+2*i+1],0.0]))**2

        cross_up=cross0+np.sqrt(cross_up)/factor
        cross_down=cross0-np.sqrt(cross_down)/factor

        pdf_up=(cross_up-cross0)/cross0*100
        pdf_down=(cross_down-cross0)/cross0*100

        print("{0} = {1} +- {2}".format(scales[j],cross0*1e3,err0*1e3))
        print("pdf_up = {0} ({1} %)\npdf_down = {2} ({3} %)".format(pdf_up*cross0/100.0*1e3,pdf_up,pdf_down*cross0/100.0*1e3,pdf_down))
