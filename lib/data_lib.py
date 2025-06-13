import numpy as np
import os
import re
import sys

def readlines(f,q):
    for i in range(0,q):
        f.readline()

def readline(f):
    line=f.readline()
    line=line.replace("\n","")
    data=line.split(" ")
    data_new=[]
    for i in range(0,len(data)):
        if (data[i]!=""):
            data_new.append(data[i])
    return data_new

def readline_line(line):
    line=line.replace("\n","")
    data=line.split(" ")
    data_new=[]
    for i in range(0,len(data)):
        if (data[i]!=""):
            data_new.append(data[i])
    return data_new

def get_bins(start,end,bn,bnmax=0):
    if bnmax==0:
        bnmax=bn
    
    bin_size=(end-start)/bn
    bins=np.zeros(bnmax+1)
    mid=np.zeros(bnmax)
    bins[0]=start
    for i in range(0,bn):
        bins[i+1]=bin_size*(i+1)+start
        mid[i]=bin_size*(i+0.5)+start
    return bins,mid,bin_size



def get_histo(file,scale=1.0,bn_set=-1,iscale="none"):
    f=open(file,'r')

    if iscale!="none":
       while(True):
          line=f.readline()
          if line.find(iscale)!=-1:
             break
          elif line=="":
             print("ERROR: end of file:")
             print("file = {0}".format(file))
             print("iscale = {0}".format(iscale))
             sys.exit(0)


    data=readline(f)
    cross=float(data[1])
    err=float(data[3])
    
    data=readline(f)
    bn=int(data[0])
    start=float(data[1])
    end=float(data[2])
    
    if bn_set!=-1 and bn_set<bn:
        bn=bn_set
    
    
    hc=np.zeros(bn)
    hcerr=np.zeros(bn)
    bins=np.zeros(bn)
    
    for i in range(0,bn):
        data=readline(f)
        bins[i]=float(data[0])
        hc[i]=float(data[1])
        hcerr[i]=float(data[2])
        
    f.close()
        
    cross*=scale
    err*=scale
    hc*=scale
    hcerr*=scale
    
    #return cross,err,hc,hcerr,bn,start,end,bins
    return cross,err,hc,hcerr



def find_pos(text,sub): #find all pos of a substring in a string
    j=0
    pos=[]
    while True:
        i=text.find(sub)
        if i==-1:
            break
        else:
            pos.append(i+j)
            text=text[i+1::]
            j+=i+1
    
    pos=np.array(pos)
    return pos


def create_dir(path):
    if os.path.isdir(path) != True:
        os.makedirs(path)



def get_seed(file):
    return re.findall(r'\d+',file)[0]
    
def get_all_seeds(path,key=False):
    objects=os.listdir(path)
    
    n_files=len(objects)
    seeds=[]
    names=[]
    for i in range(0,n_files):
        file=objects[i]
        if key!=False:
            if file.find(key)==-1:
                continue
        
        dummy=re.findall(r'\d+',file)

        if dummy!=[]:
            new_seed=dummy[0]
        else:
            continue
        
        new=True
        for j in range(len(seeds)):
            if int(new_seed)==seeds[j]:
                new=False
                break
        if new:
            seeds.append(int(new_seed))
            
        new=True
        tname=objects[i].split(new_seed)
        for j in range(len(names)):
            if tname[0]==names[j]:
                new=False
                break
        if new:
            names.append(tname[0])
            
    names=sorted(names)
    seeds=sorted(seeds)
    return seeds,names

def get_seeds(mode,process,path,start,n,key,construct=False):
    if construct==False:
        return False
    
    seed=[]
    for i in range(0,len(start)):
        path_lhe=path+"{0}/{1}/lhe/".format(mode,process[i])
        seeds,names=get_all_seeds(path_lhe,key)
        if n[i]!=-1:
            seed.append(sorted(seeds[start[i]:start[i]+n[i]]))
        else:
            seed.append(sorted(seeds[start[i]:]))
            
    return seed


def translate_helac(prc):
   outp=""
   ipart=0
   part_arr=[]

   lold=""
   for i in range(0,len(prc)):
      lnew=prc[i]
      if lnew=="x":
         lold="{0}{1}".format(lold,lnew)
         if len(lold) > 2:
            print("ERROR in translate_helac: {0}".format(lold))
         part_arr.append(get_part_id(lold))
         outp="{0} {1}".format(outp,part_arr[ipart])
         ipart+=1
         lold=""
      else:
         if lold!="":
            part_arr.append(get_part_id(lold))
            outp="{0} {1}".format(outp,part_arr[ipart])
            ipart+=1
            lold=""
      if lnew=="g" or lnew=="a":
         part_arr.append(get_part_id(lnew))
         outp="{0} {1}".format(outp,part_arr[ipart])
         ipart+=1
         lold=""
      elif lnew!="x":
         lold=lnew
   if lold!="":
      lnew=lold
      part_arr.append(get_part_id(lnew))
      outp="{0} {1}".format(outp,part_arr[ipart])
      ipart+=1
      lold=""

   part_arr=np.array(part_arr,dtype=int)

   outp=outp[1:]
   return part_arr


def get_part_id(ps):
   sign=1
   if ps.find("x")!=-1:
      sign=-1

   if ps=="g":
      ids=35
   elif ps=="a":
      ids=31
   elif ps[0]=="u":
      ids=3
   elif ps[0]=="d":
      ids=4
   elif ps[0]=="c":
      ids=7
   elif ps[0]=="s":
      ids=8
   elif ps[0]=="b":
      ids=12
   else:
      print("ERROR in get_part_id: {0}".format(ps))
      sys.exit(0)

   return sign*ids

def get_part_str(ids):

   if ids==35:
      ps="g"
   elif ids==31:
      ps="a"
   elif np.abs(ids)==3:
      ps="u"
   elif np.abs(ids)==4:
      ps="d"
   elif np.abs(ids)==7:
      ps="c"
   elif np.abs(ids)==8:
      ps="s"
   elif np.abs(ids)==12:
      ps="b"
   else:
      print("ERROR in get_part_str: {0}".format(ps))
      sys.exit(0)

   if ids<0:
      ps="{0}x".format(ps)

   return ps