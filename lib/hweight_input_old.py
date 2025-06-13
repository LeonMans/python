import numpy as np
import data_lib as dat
import sys


def calc_cross(order,mode,process_all,path,out_path,scal=1000.0,rescal=False,iord=-1):
    nweight=0
    ngrid=0
    nscales=0
    scalenames=[]

    c_mode=[]
    cerr_mode=[]
    c_tot=[]
    cerr_tot=[]

    if iord==-1:
       norders=1
    else:
       norders=len(iord)

    if rescal==False:
       rescal=[]
       for i in range(0,len(mode)):
          rescal.append([1.0]*len(process_all[i]))

    for i in range(len(mode)):
        process=process_all[i]

        c_proc_tot=[]
        cerr_proc_tot=[]
    
        for j in range(len(process)):
            path_hist=path+"{0}/{1}/hist/".format(mode[i],process[j])    
            #print(path_hist)
            seeds,fnames=dat.get_all_seeds(path_hist,"histo")

            n_files=len(seeds)
        
            if n_files==0:
                print("FEHLER!!!!!!!!!!!!!!!")
        
        
            c_proc=[]
            cerr_proc=[]

        
            print("")
            print("{0}({1})".format(process[j],n_files))
        

            for k in range(1,n_files+1):
                file=path_hist+"{0}{1}.txt".format(fnames[0],seeds[k-1])
                f=open(file,'r')
                dat.readlines(f,1)
            
                skip=4
                if (k==1): #i==0 and j==0 and 
                    if (j==0):
                        if (i==0):
                            data=dat.readline(f)
                            ngrid=int(data[1])
                            data=dat.readline(f)
                            nscales=int(data[1])
                            nweight=ngrid*nscales
                            for ii in range(0,nscales):
                                scalenames.append(data[2+ii])
                            
                            c_mode=np.zeros((len(mode),nweight))
                            cerr_mode=np.zeros((len(mode),nweight))
                            c_tot=np.zeros(nweight)
                            cerr_tot=np.zeros(nweight)
                            skip=2
                            
                        c_proc_tot=np.zeros((len(process),nweight))
                        cerr_proc_tot=np.zeros((len(process),nweight))
                    
                    c_proc=np.zeros((n_files,nweight))
                    cerr_proc=np.zeros((n_files,nweight))
                #print("skip= ",skip)
                dat.readlines(f,skip)


                #if iord!=-1:
                #   eof=False
                #   while(True):
                #      line=f.readline()
                #      if line.find("alpha_s^{0}:".format(iord))!=-1:
                #         break
                #      if line=="":
                #         eof=True
                #         break
                #   if eof:
                #      continue


                
                for ii in range(0,nweight):
                    data=dat.readline(f)
                    c_proc[k-1,ii]=rescal[i][j]*scal*float(data[1])
                    cerr_proc[k-1,ii]=rescal[i][j]*scal*float(data[2])
                
                f.close()

            for ii in range(0,nweight):
                c_proc_tot[j,ii]=np.sum(c_proc[::,ii])/n_files
                cerr_proc_tot[j,ii]=np.sqrt(np.sum(cerr_proc[::,ii]**2))/n_files
            
            
            out="{0}{1}/".format(out_path,mode[i])
            print("")
            print("{0} is done".format(process[j]))       
            
            dat.create_dir(out) 
            res=open(out+"cross_{0}.txt".format(process[j]),'w')
            res.write("nscales= {0}\n".format(nscales))
            res.write("ngrid= {0}\n\n".format(ngrid))
        
            for ii in range(0,nscales):
                for jj in range(0,ngrid):
                    res.write("{0}({1})= {2} +- {3}\n".format(scalenames[ii],jj+1,c_proc_tot[j,ngrid*ii+jj],cerr_proc_tot[j,ngrid*ii+jj]))
                res.write("\n")
            res.write("\n")
        
            for ii in range(0,nscales):
                for jj in range(0,ngrid):
                    res.write("{0}({1}):\n".format(scalenames[ii],jj+1))
                    for kk in range(0,n_files):
                        res.write("{0}\t{1}\t{2}\n".format(c_proc[kk,ngrid*ii+jj],cerr_proc[kk,ngrid*ii+jj],seeds[kk]))
                    res.write("\n\n")
            res.close()
            
        for ii in range(0,nweight):
            c_mode[i,ii]=np.sum(c_proc_tot[::,ii])
            cerr_mode[i,ii]=np.sqrt(np.sum(cerr_proc_tot[::,ii]**2))


        out="{0}{1}/".format(out_path,mode[i])
        res=open(out+"cross.txt",'w')
        res.write("nscales= {0}\n".format(nscales))
        res.write("ngrid= {0}\n\n".format(ngrid))
    
        for ii in range(0,nscales):
            for jj in range(0,ngrid):
                res.write("{0}({1})= {2} +- {3}\n".format(scalenames[ii],jj+1,c_mode[i,ngrid*ii+jj],cerr_mode[i,ngrid*ii+jj]))
            res.write("\n")
        res.write("\n")
    
    for ii in range(0,nscales):
        for jj in range(0,ngrid):
            res.write("{0}({1}):\n".format(scalenames[ii],jj+1))
            for kk in range(0,len(process)):
                res.write("{0}\t{1}\t{2}\t{3}\n".format(process[kk],c_proc_tot[kk,ngrid*ii+jj],cerr_proc_tot[kk,ngrid*ii+jj],cerr_proc_tot[kk,ngrid*ii+jj]/c_proc_tot[kk,ngrid*ii+jj]*100))
            res.write("\n\n")
    res.close()
    

             

    for ii in range(0,nweight):
        c_tot[ii]=np.sum(c_mode[::,ii])
        cerr_tot[ii]=np.sqrt(np.sum(cerr_mode[::,ii]**2))

    scale_up=np.zeros(nscales)
    scale_down=np.zeros(nscales)
    
    cross_center=np.zeros(nscales)
    err_center=np.zeros(nscales)
    
    for ii in range(0,nscales):
        cross_temp=np.zeros(ngrid)
        cross_center[ii]=c_tot[ngrid*ii]
        err_center[ii]=cerr_tot[ngrid*ii]
        for jj in range(0,ngrid):
            cross_temp[jj]=c_tot[ngrid*ii+jj]-cross_center[ii]
        
        scale_up[ii]=np.max(cross_temp)/cross_center[ii]*100
        scale_down[ii]=np.min(cross_temp)/cross_center[ii]*100
        
    #print(scale_up)
    #print(scale_down)
        

    return

    res=open(out_path+"cross_{0}.txt".format(order),'w')
    res.write("nscales= {0}\n".format(nscales))
    res.write("ngrid= {0}\n\n".format(ngrid))

    for ii in range(0,nscales):
        res.write("{0}= {1} +- {2}\n".format(scalenames[ii],cross_center[ii],err_center[ii]))
        res.write("{0}: scale up   = {1}\n".format(scalenames[ii],scale_up[ii]))
        res.write("{0}: scale down = {1}\n\n".format(scalenames[ii],scale_down[ii]))
    res.write("\n")


    for ii in range(0,nscales):
        for jj in range(0,ngrid):
            res.write("{0}({1})= {2} +- {3}\n".format(scalenames[ii],jj+1,c_tot[ngrid*ii+jj],cerr_tot[ngrid*ii+jj],cerr_tot[ngrid*ii+jj]/c_tot[ngrid*ii+jj]*100))
        res.write("\n")
    res.write("\n")

    for ii in range(0,nscales):
        for jj in range(0,ngrid):
            res.write("{0}({1}):\n".format(scalenames[ii],jj+1))
            for kk in range(0,len(mode)):
                res.write("{0}\t{1}\t{2}\t{3}\n".format(mode[kk],c_mode[kk,ngrid*ii+jj],cerr_mode[kk,ngrid*ii+jj],cerr_mode[kk,ngrid*ii+jj]/c_mode[kk,ngrid*ii+jj]*100))
            res.write("\n\n")
    res.close()



def combine_cross(path,modes,order,scales,ngrid,outfile="none",rescal=False,icollect=True,files=False):
    #out_path=path

    if rescal==False:
       rescal=[1.0]*len(modes)

    ifile=True
    if files==False:
       ifile=False
    else:
       if len(files)!=len(modes):
           print("ERROR len(files)!=len(modes)")
           sys.exit(0)

    nscales=len(scales)
    nmodes=len(modes)

    cross_mode=np.zeros((nmodes,nscales,ngrid))
    err_mode=np.zeros((nmodes,nscales,ngrid))

    for i in range(0,nmodes):
        cross=np.zeros((nscales,ngrid))
        err=np.zeros((nscales,ngrid))
        for j in range(0,nscales):
            if ifile:
                cross[j],err[j]=collect_cross(files[i],scales[j],ngrid)
            else:
                cross[j],err[j]=collect_cross("{0}/{1}/cross.txt".format(path,modes[i]),scales[j],ngrid)
        cross_mode[i]=cross*rescal[i]
        err_mode[i]=err*rescal[i]


    cross_tot=np.zeros((nscales,ngrid))
    err_tot=np.zeros((nscales,ngrid))

    for i in range(0,nmodes):
        cross_tot+=cross_mode[i]
        err_tot+=err_mode[i]**2

    err_tot=np.sqrt(err_tot)


    scale_up=np.zeros(nscales)
    scale_down=np.zeros(nscales)
    
    cross_center=np.zeros(nscales)
    err_center=np.zeros(nscales)


    for i in range(0,nscales):
        cross_temp=np.zeros(ngrid)
        cross_center[i]=cross_tot[i,0]
        err_center[i]=err_tot[i,0]
        for j in range(0,ngrid):
            cross_temp[j]=cross_tot[i,j]-cross_center[i]

        #print(cross_center[i])
        scale_up[i]=np.max(cross_temp)/cross_center[i]*100
        scale_down[i]=np.min(cross_temp)/cross_center[i]*100
    


    if outfile=="none":
        res=open(path+"cross_{0}.txt".format(order),'w')
    else:
        res=open(path+outfile+".txt",'w')
    res.write("nscales= {0}\n".format(nscales))
    res.write("ngrid= {0}\n\n".format(ngrid))

    for ii in range(0,nscales):
        res.write("{0}= {1} +- {2}\n".format(scales[ii],cross_center[ii],err_center[ii]))
        res.write("{0}: scale up   = {1}\n".format(scales[ii],scale_up[ii]))
        res.write("{0}: scale down = {1}\n\n".format(scales[ii],scale_down[ii]))
    res.write("\n")


    for ii in range(0,nscales):
        for jj in range(0,ngrid):
            res.write("{0}({1})= {2} +- {3}\n".format(scales[ii],jj+1,cross_tot[ii,jj],err_tot[ii,jj],err_tot[ii,jj]/cross_tot[ii,jj]*100))
        res.write("\n")
    res.write("\n")


    if icollect:
        for ii in range(0,nscales):
            for jj in range(0,ngrid):
                res.write("{0}({1}):\n".format(scales[ii],jj+1))
                res.write("{0}\t{1}\t{2}\t{3}\n".format("total",cross_tot[ii,jj],err_tot[ii,jj],err_tot[ii,jj]/cross_tot[ii,jj]*100))
                for kk in range(0,nmodes):
                    res.write("{0}\t{1}\t{2}\t{3}\n".format(modes[kk],cross_mode[kk,ii,jj],err_mode[kk,ii,jj],err_mode[kk,ii,jj]/cross_mode[kk,ii,jj]*100))
                res.write("\n\n")


    res.close()

    return cross_tot,err_tot

def collect_cross(file,scale,ngrid):
    cross=np.zeros(ngrid)
    err=np.zeros(ngrid)

    f=open(file,'r')

    dat.readlines(f,1)
    data=dat.readline(f)

    ngrid_file=int(data[1])

    #if ngrid_file<ngrid:
    #    print("{0} not found".format(file))
    #    return cross,err
    

    for i in range(0,ngrid):
        while(True):
            line=f.readline()
            if (line.find("{0}({1})=".format(scale,i+1))!=-1):
                break
            if line=="":
                print("End of file: scale {0}({1}) not found".format(scale,i+1))
                sys.exit(0)

        data=dat.readline_line(line)
        cross[i]=float(data[1])
        err[i]=float(data[3])

    f.close()
    return cross,err


def calc_hist(order,mode,process_all,pdf,path,out_path,scal=1000.0,sub="",rescal=False):
    
    names=[]
    bn=[]
    start=[]
    end=[]
    bins=[]
    edges=[]


    nweight=0
    ngrid=0
    nscales=0
    nh=0
    scalenames=[]

    c_proc=[]
    c_mode=[]
    c_tot=[]
    cerr_proc=[]
    cerr_mode=[]
    cerr_tot=[]

    hc_proc=[]
    hc_mode=[]
    hc_tot=[]

    hcerr_proc=[]
    hcerr_mode=[]
    hcerr_tot=[]

    mid=[]
    bin_size=[]

    if rescal==False:
       rescal=[]
       for i in range(0,len(mode)):
          rescal.append([1.0]*len(process_all[i]))

    for i in range(len(mode)):
        process=process_all[i]
    
        print(mode[i])
        for j in range(len(process)):
            path_hist=path+"{0}/{1}/hist/".format(mode[i],process[j])        
            seeds,fnames=dat.get_all_seeds(path_hist,"histo")

            n_files=len(seeds)
        
            if n_files==0:
                print("FEHLER!!!!!!!!!!!!!!!")
            
            for k in range(1,n_files+1):
                file=path_hist+"{0}{1}.txt".format(fnames[0],seeds[k-1])
                f=open(file,'r')
                dat.readlines(f,1)
            
                print("{0}: {1}/{2}".format(process[j],k,n_files))
            
            
                skip=4
                if (k==1): #i==0 and j==0 and 
                    if (j==0):
                        if (i==0):
                            data=dat.readline(f)
                            ngrid=int(data[1])
                            data=dat.readline(f)
                            nscales=int(data[1])
                            nweight=ngrid*nscales
                            for ii in range(0,nscales):
                                scalenames.append(data[2+ii])
                            

                            c_tot=np.zeros(nweight)
                            cerr_tot=np.zeros(nweight)
                        
                            data=dat.readline(f)
                            nh=int(data[1])
                            skip=1
                        #else:
                        #    dat.readlines(f,3)
            
                        c_mode=np.zeros(nweight)
                        cerr_mode=np.zeros(nweight)
                    
                    c_proc=np.zeros(nweight)
                    cerr_proc=np.zeros(nweight)
                dat.readlines(f,skip)            
            
            
                for ii in range(0,nweight):
                    data=dat.readline(f)
                    c_proc[ii]+=float(data[1])
                    cerr_proc[ii]+=float(data[2])**2
                
                
                skip=nh+1
                if (i==0 and j==0 and k==1):
                    dat.readlines(f,1)
                    for ii in range(0,nh):
                        data=dat.readline(f)
                        names.append(data[0])
                        bn.append(int(data[1]))
                        
                        
                        if data[2]=="F":
                            tag_edges=False
                        elif data[2]=="T":
                            tag_edges=True
                        else:
                            print("ERROR: ih={0}".format(ii))
                        edges.append(tag_edges)
                            
                            
                        if tag_edges==False:
                            start.append(float(data[3]))
                            end.append(float(data[4]))
                        
                            bins_temp,mid_temp,size_temp=dat.get_bins(start[-1],end[-1],bn[-1])
                            mid.append(mid_temp)
                            bin_size.append(size_temp)
                        else:
                            bins_temp=[]
                            mid_temp=[]
                            for kk in range(0,bn[ii]+1):
                                bins_temp.append(float(data[kk+3]))
                                if kk>0:
                                    mid_temp.append((bins_temp[kk]+bins_temp[kk-1])/2.0)
                            start.append(bins_temp[0])
                            end.append(bins_temp[-1])
                            bin_size.append(0.0)
                            mid.append(mid_temp)
                                
                        bins.append(bins_temp)
                    
                        hc_proc.append(np.zeros((bn[-1],nweight)))
                        hc_mode.append(np.zeros((bn[-1],nweight)))
                        hc_tot.append(np.zeros((bn[-1],nweight)))
                    
                        hcerr_proc.append(np.zeros((bn[-1],nweight)))
                        hcerr_mode.append(np.zeros((bn[-1],nweight)))
                        hcerr_tot.append(np.zeros((bn[-1],nweight)))
                    
                    
                        skip=0
                    
                dat.readlines(f,skip)


                if (k==1):
                    for ii in range(0,nh):
                        hc_proc[ii][::,::]=0.0
                        hcerr_proc[ii][::,::]=0.0
                if (j==0):
                    for ii in range(0,nh):
                        hc_mode[ii][::,::]=0.0
                        hcerr_mode[ii][::,::]=0.0

                for ii in range(0,nh):
                    dat.readlines(f,2)
                    for jj in range(0,bn[ii]):
                        data=dat.readline(f)
                
                        for kk in range(0,nweight):
                            hc_proc[ii][jj,kk]+=float(data[1+kk])
                            hcerr_proc[ii][jj,kk]+=float(data[1+nweight+kk])**2

                f.close()
                
                #print(seeds[k-1],hcerr_proc[31][11,0])
            
            c_mode+=rescal[i][j]*scal*c_proc/n_files
            cerr_mode+=cerr_proc*(rescal[i][j]*scal/n_files)**2
        
        
            for ii in range(0,nh):
                hc_mode[ii]+=rescal[i][j]*scal*hc_proc[ii]/n_files
                hcerr_mode[ii]+=hcerr_proc[ii]*(rescal[i][j]*scal/n_files)**2


        c_tot+=c_mode
        cerr_tot+=cerr_mode 
    
    
        for ii in range(0,nh):
            hc_tot[ii]+=hc_mode[ii]
            hcerr_tot[ii]+=hcerr_mode[ii]
        

        for ii in range(0,nscales):
            for jj in range(0,ngrid):
                out="{0}{1}_{2}/scale_unc/{3}{5}/scale{4}".format(out_path,pdf,scalenames[ii],mode[i],jj,sub)
                dat.create_dir(out) 
                for kk in range(0,nh):
                    res=open("{0}/hist_{1}.txt".format(out,names[kk]),'w')
            
                    res.write("cross= {0} +- {1}\n".format(c_mode[ii*ngrid+jj],np.sqrt(cerr_mode[ii*ngrid+jj])))
                    res.write("{0} {1} {2}\n".format(bn[kk],start[kk],end[kk]))
                
                    for ll in range(0,bn[kk]):
                        if edges[kk]==False:
                            a=bin_size[kk]
                        else:
                            a=bins[kk][ll+1]-bins[kk][ll]
                        res.write("{0}  {1}  {2}\n".format(mid[kk][ll],hc_mode[kk][ll,ii*ngrid+jj]/a,np.sqrt(hcerr_mode[kk][ll,ii*ngrid+jj])/a))

                    res.close()
                
    print("finished")
    
    return


def get_histograms(order,mode,process_all,pdf,path,out_path,scal=1000.0):
    
    names=[]
    bn=[]
    start=[]
    end=[]
    bins=[]
    edges=[]


    nweight=0
    ngrid=0
    nscales=0
    nh=0
    scalenames=[]

    mid=[]
    
    
    process=process_all[0]
    
    path_hist=path+"{0}/{1}/hist/".format(mode[0],process[0])        
    seeds,fnames=dat.get_all_seeds(path_hist,"histo")

    n_files=len(seeds)
        
    if n_files==0:
        print("FEHLER!!!!!!!!!!!!!!!")
            

    file=path_hist+"{0}{1}.txt".format(fnames[0],seeds[0])
    f=open(file,'r')
    dat.readlines(f,1)
            

    data=dat.readline(f)
    ngrid=int(data[1])
    data=dat.readline(f)
    nscales=int(data[1])
    nweight=ngrid*nscales
    for ii in range(0,nscales):
        scalenames.append(data[2+ii])
                            


    data=dat.readline(f)
    nh=int(data[1])
    skip=1

    dat.readlines(f,skip)            
    
    dat.readlines(f,nweight)
    
                
    skip=nh+1

    dat.readlines(f,1)
    
    for ii in range(0,nh):
        data=dat.readline(f)
        names.append(data[0])
        bn.append(int(data[1]))
                        
                        
        if data[2]=="F":
            tag_edges=False
        elif data[2]=="T":
            tag_edges=True
        else:
            print("ERROR: ih={0}".format(ii))
        edges.append(tag_edges)
                            
                            
        if tag_edges==False:
            start.append(float(data[3]))
            end.append(float(data[4]))
                        
            bins_temp,mid_temp,size_temp=dat.get_bins(start[-1],end[-1],bn[-1])
        else:
            bins_temp=[]
            mid_temp=[]
            for kk in range(0,bn[ii]+1):
                bins_temp.append(float(data[kk+3]))
                if kk>0:
                    mid_temp.append((bins_temp[kk]+bins_temp[kk-1])/2.0)
                start.append(bins_temp[0])
                end.append(bins_temp[-1])
                               
        mid.append(mid_temp)
        bins.append(bins_temp)
    
    f=open("{0}hist_setup.txt".format(out_path),'w')
    f.write("nh = {0}\n\n".format(nh))
    
    for i in range(0,nh):
        f.write("{0}  {1}  {2}".format(i,names[i],bn[i]))
        
        for j in range(0,bn[i]+1):
            f.write("  {0:.16f}".format(bins[i][j]))
        
        f.write("\n")
    
    f.close()
         

def read_histograms(hist_setup):

    names=[]
    bn=[]
    bins=[]

    f=open(hist_setup,'r')
    nh=int(dat.readline(f)[2])
    dat.readlines(f,1)

    for i in range(0,nh):
        data=dat.readline(f)
        names.append(data[1])
        bn.append(int(data[2]))
        bins_temp=[]
        for j in range(0,bn[i]+1):
            bins_temp.append(float(data[3+j]))
        bins.append(bins_temp)

    f.close()
    return names,bn,bins
