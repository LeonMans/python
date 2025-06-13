import numpy as np
import data_lib as dat



def calc_cross(mode,process,path,out_path="",scal=1000.0):
    #calculate cross section from a given path/mode from some processes from hist files from helac dipoles
    #scal is set to 1000.0 to obtain same unit as in lhe files
    
    nproc=len(process)

    c_tot=np.zeros(nproc)
    cerr_tot=np.zeros(nproc)

    for i in range(0,nproc): #nproc
        path_hist=path+"{0}/{1}/hist/".format(mode,process[i])        

        seeds,fnames=dat.get_all_seeds(path_hist,"hi_file")
        
        n_files=len(seeds)
        
        if n_files==0:
            print("FEHLER!!!!!!!!!!!!!!!")
        
        c_proc=np.zeros(n_files)
        cerr_proc=np.zeros(n_files)
        
        print()
        print(process[i],n_files)

        for j in range(1,n_files+1):
            #f=open(path_hist+objects[j-1],'r')
            file=path_hist+"{0}{1}".format(fnames[0],seeds[j-1])
            f=open(file,'r')
            dat.readlines(f,1)
            data=dat.readline(f)
            

            c_proc[j-1]=scal*float(data[0])
            cerr_proc[j-1]=scal*float(data[1])

            
            f.close()
 
        c_tot[i]=np.sum(c_proc)/n_files
        cerr_tot[i]=np.sqrt(np.sum(cerr_proc**2))/n_files   

            
        print()
        print("{0} is done".format(process[i]))
        print(c_tot[i])
        print(cerr_tot[i])
        print(cerr_tot[i]/c_tot[i]*100)        
            
        output_path=out_path+"{0}/{1}/".format(mode,process[i])
        dat.create_dir(output_path) 
        res=open(output_path+"cross.txt",'w')
        res.write("{0}\t{1}\n\n".format(c_tot[i],cerr_tot[i]))
        for j in range(0,n_files):
            res.write("{0}\t{1}\t{2}".format(c_proc[j],cerr_proc[j],seeds[j]))
            if j<n_files-1:
                res.write("\n")
        res.close()
            
    c=np.sum(c_tot)
    cerr=np.sqrt(np.sum(cerr_tot**2))
    

    print()
    print("{0} is done.".format(mode))
    print(c)
    print(cerr)
    print(cerr/c*100)
    
    output_path=out_path+"{0}/".format(mode)
    res=open(output_path+"cross.txt".format(mode),'w')
    res.write("{0}\t{1}\n\n".format(c,cerr))
    for j in range(0,nproc):
        res.write("{0}\t{1}\t{2}\t{3}".format(process[j],c_tot[j],cerr_tot[j],cerr_tot[j]/c_tot[j]*100))
        if j<nproc-1:
            res.write("\n") 
    res.close()
        
    return c,cerr



def create_hist_dip(mode,process,path,names,bn,start,end,out_path,sub="",scal=1000.0):
    #differential cross section from hist files
    #to obtain same unit as in lhe files
    nh=len(names)
    nproc=len(process)    
    
    q=np.zeros(nh+1,dtype=int)
    for i in range(1,nh+1):
        q[i]=q[i-1]+bn[i-1]
    bin_tot=q[-1]
    bin_size=(end-start)/bn

    hc_tot=np.zeros(bin_tot)
    hcerr_tot=np.zeros(bin_tot)        #end: total number of bins
    bins=np.zeros(bin_tot)
    c_tot=0.0
    cerr_tot=0.0

    for i in range(0,nproc):
        path_hist=path+"{0}/{1}/hist/".format(mode,process[i])
        
        seeds,fnames=dat.get_all_seeds(path_hist,"hi_file")
        
        n_files=len(seeds)
        
        if n_files==0:
            print("FEHLER!!!!!!!!!!!!!!!")

        c_proc=0.0
        cerr_proc=0.0
        hc_proc=np.zeros(bin_tot)
        hcerr_proc=np.zeros(bin_tot)
    

        print()
        print(process[i],n_files)
    
        for j in range(1,n_files+1):
            #f=open(path_hist+objects[j-1],'r')
            file=path_hist+"{0}{1}".format(fnames[0],seeds[j-1])
            f=open(file,'r')
            dat.readlines(f,1)
            data=dat.readline(f)
            
            c_proc+=float(data[0])
            cerr_proc+=float(data[1])**2


        
            for k in range(0,bin_tot):
                data=dat.readline(f)
                bins[k]=float(data[0])
                hc_proc[k]+=float(data[1])
                hcerr_proc[k]+=float(data[2])**2

                
            f.close()
    
        c_tot+=c_proc*(scal/n_files)
        cerr_tot+=cerr_proc*(scal/n_files)**2
        hc_tot+=hc_proc*(scal/n_files)
        hcerr_tot+=hcerr_proc*(scal/n_files)**2

    

    cross=c_tot
    cerr=np.sqrt(cerr_tot)
    hcerr_tot=np.sqrt(hcerr_tot)

    counter=0

    output_path="{0}{1}/{2}/".format(out_path,mode,sub)
    #print(output_path)
    #return
    dat.create_dir(output_path)
    for i in range(nh):
        out=open(output_path+"hist_{0}.txt".format(names[i]),'w')
        out.write("cross= {0} +- {1}\n".format(cross,cerr))
        out.write("{0} {1} {2}\n".format(bn[i],start[i],end[i]))
        for j in range(0,bn[i]):
            hc_tot[counter]/=bin_size[i]
            hcerr_tot[counter]/=bin_size[i]
            out.write("{0}  {1}  {2}\n".format(bins[counter],hc_tot[counter],hcerr_tot[counter]))
            counter=counter+1
        out.close()
        
    return cross,cerr,hc_tot,hcerr_tot


