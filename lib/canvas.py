import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox
import matplotlib.transforms
import numpy as np
import data_lib as dat
import os
import sys

def get_limit(bin_min,bin_max,off=0.05,iopt=5):
    mid=1.0
    step=0.05
    
    
    while(2.0*step+mid<bin_max):
        step+=off

    if iopt==5:
       arr_y=np.array([1.0-2.0*step,1.0-step,1.0,1.0+step,1.0+2.0*step])
    elif iopt==3:
       arr_y=np.array([1.0-step,1.0,1.0+step])
    else:
       print("iopt({0}) in get_limit not found".format(iopt))
       sys.exit(0)

    ymin=1.0-2.0*step
    ymax=1.0+2.0*step
        
    return arr_y,ymin,ymax


class histogram():
    def __init__(self,bn,files,scale,label,color,lstyle,alpha,lw,norm,scal,exp,iscale="none"):
        self.bn=bn
        self.ngrid=len(files)
        self.cross=np.zeros(self.ngrid)
        self.cerr=np.zeros(self.ngrid)
        self.hc=np.zeros((self.ngrid,self.bn))
        self.hcerr=np.zeros((self.ngrid,self.bn))
        
        
        self.hlabel=label
        self.color=color
        self.lstyle=lstyle
        self.alpha=alpha
        self.lw=lw
        self.exp=exp

        if iscale=="none":
            iscale=["none"]*self.ngrid
                
        for i in range(0,self.ngrid):
            self.cross[i],self.cerr[i],self.hc[i],self.hcerr[i]=dat.get_histo(files[i],scale,iscale=iscale[i])
            if norm:
                self.hc[i]=self.hc[i]/self.cross[i]
                self.hcerr[i]=self.hcerr[i]/self.cross[i]
    
            
        if self.ngrid>1:
            self.cross_plus=np.max(self.cross)
            self.cross_minus=np.min(self.cross)

            self.hc_plus=np.zeros(self.bn+1)
            self.hc_minus=np.zeros(self.bn+1)
            
            
            for i in range(0,self.bn):
                arr=np.zeros(self.ngrid)
            
                for j in range(0,self.ngrid):
                    arr[j]=self.hc[j,i]
                    
                self.hc_plus[i]=np.max(arr)
                self.hc_minus[i]=np.min(arr)
            
        self.cross=scal*self.cross
        self.cerr=scal*self.cerr
        self.hc=scal*self.hc
        self.hcerr=scal*self.hcerr



class canvas():
    def __init__(self,hist_setup,ih,pdf_unc=False,size=30,norm=False,iopt=0):
        font = {'family' : 'DejaVu Sans',  #DejaVu Sans  #print(matplotlib.font_manager.findfont('DejaVu Sans')) #https://stackoverflow.com/questions/42097053/matplotlib-cannot-find-basic-fonts
                'weight' : 'normal',
                'size'   : size}
        plt.rc('font', **font)
        #matplotlib.font_manager._rebuild()
        #print(matplotlib.font_manager.findfont('DejaVu Sans'))
        #sys.exit(0)
        #plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
        #plt.rc('font',**{'family':'serif','serif':['Palatino']})
        plt.rc('text', usetex=True)
        #plt.rcParams.update({"text.usetex": True,"font.family": "Helvetica"})
        #plt.rcParams["font.size"] = size
        #plt.rcParams["font.family"] = "serif"
        #plt.rcParams['mathtext.fontset'] = 'custom'
        #plt.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
        #plt.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
        #plt.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'

        #plt.rcParams["mathtext.default"] = "regular"
        #plt.rcParams["mathtext.fontset"] = "dejavuserif" #dejavuserif

        # trigger core fonts for PS backend
        #plt.rcParams["pdf.use14corefonts"] = True
        #plt.rcParams["ps.useafm"] = True
        plt.rcParams['pdf.fonttype'] = 42
        plt.rcParams['ps.fonttype'] = 42

        plt.rcParams["axes.axisbelow"] = False

        #plt.rcParams["hatch.linewidth"] = 1.5

        
        #init local variables
        self.scale=1e3              #multiply by scale
        self.norm=norm              #normalised distributions
        
        self.read_init(hist_setup,ih)        

        self.ind=-1                 #initialization of ind which is index for histogram with which everything is compared
        self.pdf_unc=pdf_unc
        self.size_font=size
        self.grid_size=0.5
        
        self.nh=0
        self.hist=[]

        self.get_limit_iopt=5
    
        #init plot
        if pdf_unc==False:
            self.f, self.axes = plt.subplots(2,1, gridspec_kw={'height_ratios': [5, 2]},figsize=(12,11))
            plt.subplots_adjust(hspace=0.065,wspace = 0.08,left=0.165, right=0.95, top=0.965, bottom=0.11)
            self.xtmin=np.zeros(1)
            self.xtmax=np.zeros(1)
            self.firstcall=[True]
            self.modus=["none"]
            self.nplots=2
        elif pdf_unc==True:
            if iopt==0:
               self.f, self.axes = plt.subplots(3,1, gridspec_kw={'height_ratios': [5, 2,2]},figsize=(12,13))
               plt.subplots_adjust(hspace=0.1,wspace = 0.08,left=0.165, right=0.95, top=0.97, bottom=0.092)  #0.085
               self.nplots=3
            elif iopt==1:
               self.f, self.axes = plt.subplots(3,1, gridspec_kw={'height_ratios': [4, 2,2]},figsize=(12,13))
               plt.subplots_adjust(hspace=0.1,wspace = 0.08,left=0.15, right=0.95, top=0.97, bottom=0.092)  #0.085
               self.nplots=3
            elif iopt==2:
               self.f, self.axes = plt.subplots(4,1, gridspec_kw={'height_ratios': [3.5,2,2,2]},figsize=(12,13))
               plt.subplots_adjust(hspace=0.02,wspace = 0.08,left=0.15, right=0.95, top=0.97, bottom=0.092)  #0.085
               self.nplots=4
               self.get_limit_iopt=3



            self.ax3=self.axes[2]
            self.xtmin=np.zeros(self.nplots-1)
            self.xtmax=np.zeros(self.nplots-1)
            self.firstcall=[True]*(self.nplots-1)
            self.modus=["none"]*(self.nplots-1)
        elif pdf_unc==-1:
            self.f, temp_axes = plt.subplots(1,1, gridspec_kw={'height_ratios': [5]},figsize=(12,11))
            self.axes=[]
            self.axes.append(temp_axes)
            plt.subplots_adjust(hspace=0.065,wspace = 0.08,left=0.165, right=0.95, top=0.965, bottom=0.11)
            self.xtmin=np.zeros(1)
            self.xtmax=np.zeros(1)
            self.firstcall=[True]
            self.modus=["none"]
            self.nplots=1
        elif pdf_unc==-2:
            self.f, temp_axes = plt.subplots(1,1,figsize=(8,6))
            self.axes=[]
            self.axes.append(temp_axes)
            plt.subplots_adjust(left=0.165, right=0.95, top=0.965, bottom=0.16)
            self.xtmin=np.zeros(1)
            self.xtmax=np.zeros(1)
            self.firstcall=[True]
            self.modus=["none"]
            self.nplots=1
        elif pdf_unc==-3:
            self.f, temp_axes = plt.subplots(1,1,figsize=(12,8))
            self.axes=[]
            self.axes.append(temp_axes)
            plt.subplots_adjust(left=0.165, right=0.95, top=0.965, bottom=0.16)
            self.xtmin=np.zeros(1)
            self.xtmax=np.zeros(1)
            self.firstcall=[True]
            self.modus=["none"]
            self.nplots=1

        
        self.ax=self.axes[0]
        
        self.xmin=self.bins[0]
        self.xmax=self.bins[-1]


        #parameters for experimental data
        self.exp_lw=2.5
        self.exp_markersize=15
        self.ms_scale=16
        self.lobj_lw=2.3


        #params for legend
        self.legend_size=30
        self.legend_borderaxespad=0.5
        self.legend_handletextpad=0.2
        
        
        

    def read_init(self,hist_setup,ih):
        f=open(hist_setup,'r')
    
        data=dat.readline(f)
    
        nh_max=int(data[2])
        dat.readlines(f,1)
        
        for i in range(0,nh_max):
            data=dat.readline(f)
            
            if i==ih:
                self.obs=data[1]
                self.bn=int(data[2])
                self.start=float(data[3])
                self.end=float(data[3+self.bn])
                self.bins=np.zeros(self.bn+1)
                self.mid=np.zeros(self.bn)
                for j in range(0,self.bn+1):
                    self.bins[j]=float(data[3+j])
                    if j>0:
                        self.mid[j-1]=(self.bins[j]+self.bins[j-1])/2.0
                
                ilog=4+self.bn
                if len(data)<=ilog:
                    self.log=False
                else:
                    if data[ilog]=="T":
                        self.log=True
                    else:
                        self.log=False
                ixx=5+self.bn
                iyy=6+self.bn
                if len(data)<=iyy:
                    self.xlabel="x-label"
                    self.ylabel="y-label"
                else:
                    if self.norm:
                        self.ylabel="$\\frac{{1}}{{\\sigma}}\\cdot$"+data[ixx].replace("&"," ")
                        if self.ylabel.find("GeV")!=-1:
                            self.ylabel=self.ylabel.replace("fb","1")
                        else:
                            self.ylabel=self.ylabel.replace("  [fb]","")
                    else:
                        self.ylabel=data[ixx].replace("&"," ")
                    self.xlabel=data[iyy].replace("&"," ")
                return
            else:
                continue
        f.close()
    
        



    def add_hist(self,files,label,color,lstyle="solid",alpha=1.0,lw=2.0,scal=1.0,exp=False,iscale="none"):
        #init histogram
        self.nh=self.nh+1
        self.hist.append(histogram(self.bn,files,self.scale,label,color,lstyle,alpha,lw,self.norm,scal,exp,iscale))

    def resize(self,bn_start,bn_new):
        for i in range(0,self.nh):

            hc_temp=np.zeros((self.hist[i].ngrid,bn_new))
            hcerr_temp=np.zeros((self.hist[i].ngrid,bn_new))

            for j in range(0,bn_new):
                for k in range(0,self.hist[i].ngrid):
                    hc_temp[k,j]=self.hist[i].hc[k,bn_start+j]
                    hcerr_temp[k,j]=self.hist[i].hcerr[k,bn_start+j]

            self.hist[i].bn=bn_new
            self.hist[i].hc=np.copy(hc_temp)
            self.hist[i].hcerr=np.copy(hcerr_temp)


            if self.hist[i].ngrid>1:
                hc_temp=np.zeros(bn_new+1)
                for j in range(0,bn_new):
                    hc_temp[j]=self.hist[i].hc_plus[bn_start+j]

                self.hist[i].hc_plus=np.copy(hc_temp)

                hc_temp=np.zeros(bn_new+1)
                for j in range(0,bn_new):
                    hc_temp[j]=self.hist[i].hc_minus[bn_start+j]

                self.hist[i].hc_minus=np.copy(hc_temp)


        bins_new=np.zeros(bn_new+1)
        mid_new=np.zeros(bn_new)
        for i in range(0,bn_new):
            bins_new[i]=self.bins[bn_start+i]
            mid_new[i]=self.mid[bn_start+i]

        bins_new[bn_new]=self.bins[bn_start+bn_new]


        self.bn=bn_new
        self.bins=np.copy(bins_new)
        self.mid=np.copy(mid_new)

        self.start=self.bins[0]
        self.end=self.bins[-1]
        self.xmin=self.bins[0]
        self.xmax=self.bins[-1]


    def rescal(self,factor,ihist=-1):
        for i in range(0,self.nh):
            if ihist!=-1 and (ihist!=i):
                continue

            self.hist[i].cross=self.hist[i].cross*factor
            self.hist[i].cerr=self.hist[i].cerr*factor
            self.hist[i].hc=self.hist[i].hc*factor
            self.hist[i].hcerr=self.hist[i].hcerr*factor

            if self.hist[i].ngrid>1:
                self.hist[i].cross_plus=self.hist[i].cross_plus*factor
                self.hist[i].cross_minus=self.hist[i].cross_minus*factor
                self.hist[i].hc_plus=self.hist[i].hc_plus*factor
                self.hist[i].hc_minus=self.hist[i].hc_minus*factor




        
    def main(self,order,bands,hatches=False,alpha_param=False):
        ax_alpha=0.3
        ax_alpha2=1.0
        if alpha_param!=False:
            ax_alpha=alpha_param[0]
            ax_alpha2=alpha_param[1]

        temp=10.0
        iexp=0

        if hatches==False:
            hatches=["False"]*len(order)
        
        for i in range(0,len(order)):
            ih=order[i]
            if bands[i]:
                #print(len(self.bins),len(self.hist[ih].hc_plus),len(self.hist[ih].hc_minus))
                if hatches[i]=="False":
                    self.ax.fill_between(self.bins,self.hist[ih].hc_plus,self.hist[ih].hc_minus,step='post',alpha=ax_alpha,color=self.hist[ih].color,zorder=1.0+(i+1.0)/temp)
                else:
                    self.ax.fill_between(self.bins,self.hist[ih].hc_plus,self.hist[ih].hc_minus,step='post',alpha=ax_alpha2,facecolor="none",edgecolor=self.hist[ih].color,zorder=1.0+(i+1.0)/temp,hatch=hatches[i])

            if self.hist[ih].exp:
                self.ax.errorbar(self.mid+iexp,self.hist[ih].hc[0],yerr=self.hist[ih].hcerr[0],fmt='.',label=self.hist[ih].hlabel,alpha=self.hist[ih].alpha,color=self.hist[ih].color,markersize=1.0,zorder=1.0+(self.nh+2.0*i+1.0)/temp)
                self.ax.errorbar(self.mid+iexp,self.hist[ih].hc[0],yerr=self.hist[ih].hcerr[0],fmt='.',alpha=self.hist[ih].alpha,color=self.hist[ih].color,markersize=self.exp_markersize,zorder=1.0+(self.nh+2.0*i+1.0)/temp,linewidth=self.exp_lw)
                iexp=iexp+(self.xmax-self.xmin)/13*self.exp_markersize/self.f.dpi
            else:
                if self.hist[ih].hlabel!="skip":
                    self.ax.errorbar(self.mid,self.hist[ih].hc[0],yerr=self.hist[ih].hcerr[0],fmt='.',label=self.hist[ih].hlabel,alpha=self.hist[ih].alpha,color=self.hist[ih].color,markersize=1.0,zorder=1.0+(self.nh+2.0*i+1.0)/temp)
                else:
                    self.ax.errorbar(self.mid,self.hist[ih].hc[0],yerr=self.hist[ih].hcerr[0],fmt='.',alpha=self.hist[ih].alpha,color=self.hist[ih].color,markersize=1.0,zorder=1.0+(self.nh+2.0*i+1.0)/temp)

            if self.hist[ih].exp==False:
                self.ax.hist(self.mid,weights=self.hist[ih].hc[0],bins=self.bins,histtype="step",color=self.hist[ih].color,linewidth=self.hist[ih].lw,alpha=self.hist[ih].alpha,linestyle=self.hist[ih].lstyle,zorder=1.0+(self.nh+2.0*i+2.0)/temp)


    def plot_band(self,order,bands,ref=0,ref2=0,ix=1,itag=False,norm=False,iprint=False,hatches=False,alpha_param=False,zval=1.0):
        ax_alpha=0.3
        alpha_band=0.3
        alpha_band2=1.0

        if alpha_param!=False:
            alpha_band=alpha_param[0]
            alpha_band2=alpha_param[1]

        fac=10.0
        iexp=0

        if iprint:
            print("panel = {0}".format(ix))
        
        self.modus[ix-1]="band"

        if hatches==False:
            hatches=["False"]*len(order)
        
        for i in range(0,len(order)):
            ih=order[i]
            
            k=np.zeros(self.bn)
            kerr=np.zeros(self.bn)
            
            #if bands[i]:
            band_up=np.zeros(self.bn+1)
            band_down=np.zeros(self.bn+1)
            
            if ref==-1:
                iref=i
            elif ref==-2:
                iref=ref2[i]
            else:
                iref=ref
                
            for j in range(0,self.bn):
                if self.hist[ih].hc[0,j]==0.0 and self.hist[iref].hc[0,j]==0.0:
                    if self.pdf_unc==-1:
                        k[j]=0.0
                        kerr[j]=0.0
                    
                        if bands[i]:
                            band_up[j]=0.0
                            band_down[j]=0.0  
                    else:
                        k[j]=zval
                        kerr[j]=0.0
                    
                        if bands[i]:
                            band_up[j]=zval
                            band_down[j]=zval 
                    continue
                    
                if self.hist[iref].hc[0,j]==0.0:
                    if self.pdf_unc==-1:
                        k[j]=0.0
                        kerr[j]=0.0
                    
                        if bands[i]:
                            band_up[j]=0.0
                            band_down[j]=0.0  
                    else:
                        k[j]=zval
                        kerr[j]=0.0
                    
                        if bands[i]:
                            band_up[j]=zval
                            band_down[j]=zval
                else:
                    if norm:
                       k[j]=(self.hist[ih].hc[0,j]/self.hist[ih].cross[0])/(self.hist[iref].hc[0,j]/self.hist[iref].cross[0])
                    else:
                       k[j]=self.hist[ih].hc[0,j]/self.hist[iref].hc[0,j]

                    if ref!=-2:
                        if norm:
                           kerr[j]=(self.hist[ih].hcerr[0,j]/self.hist[ih].cross[0])/(self.hist[iref].hc[0,j]/self.hist[iref].cross[0])
                        else:
                           kerr[j]=self.hist[ih].hcerr[0,j]/self.hist[iref].hc[0,j]
                    else: # normalised distributions
                        if norm:
                           kerr[j]=np.sqrt(((self.hist[ih].hcerr[0,j]/self.hist[ih].cross[0])/(self.hist[iref].hc[0,j]/self.hist[iref].cross[0]))**2+((self.hist[ih].hc[0,j]/self.hist[ih].cross[0])*self.hist[iref].hcerr[0,j]/(self.hist[iref].hc[0,j]**2/self.hist[iref].cross[0]))**2)
                           #print("Norm is supported for ref=-2")
                           #sys.exit(0)
                        else:
                           kerr[j]=np.sqrt((self.hist[ih].hcerr[0,j]/self.hist[iref].hc[0,j])**2+(self.hist[ih].hc[0,j]*self.hist[iref].hcerr[0,j]/self.hist[iref].hc[0,j]**2)**2)
                           #print("--test--")
                           #kerr[j]=self.hist[ih].hcerr[0,j]/self.hist[iref].hc[0,j]
                    
                    if bands[i]:
                        if norm:
                           band_up[j]=(self.hist[ih].hc_plus[j]/self.hist[ih].cross[0])/(self.hist[iref].hc[0,j]/self.hist[iref].cross[0])
                           band_down[j]=(self.hist[ih].hc_minus[j]/self.hist[ih].cross[0])/(self.hist[iref].hc[0,j]/self.hist[iref].cross[0])
                        else:
                           band_up[j]=self.hist[ih].hc_plus[j]/self.hist[iref].hc[0,j]
                           band_down[j]=self.hist[ih].hc_minus[j]/self.hist[iref].hc[0,j]
                    

            if bands[i]:
                if hatches[i]=="False":
                    self.axes[ix].fill_between(self.bins,band_up,band_down,step='post',alpha=alpha_band,color=self.hist[ih].color,zorder=1.0+(i+1.0)/fac)
                else:
                    self.axes[ix].fill_between(self.bins,band_up,band_down,step='post',alpha=alpha_band2,facecolor="none",edgecolor=self.hist[ih].color,zorder=1.0+(i+1.0)/fac,hatch=hatches[i])

            #if itag or self.hist[ih].exp:
            if True:
                if not itag:
                    kerr=0.0
                #print(i,kerr)

                if self.hist[ih].exp:
                    self.axes[ix].errorbar(self.mid+iexp,k,yerr=kerr,fmt='.',alpha=self.hist[ih].alpha,color=self.hist[ih].color,markersize=self.exp_markersize,zorder=1.0+(self.nh+2.0*i+1.0)/fac,linewidth=self.exp_lw)
                    iexp=iexp+(self.xmax-self.xmin)/13*self.exp_markersize/self.f.dpi
                else:
                    #if self.nplots>1 or self.hist[ih].hlabel=="skip":
                    if self.hist[ih].hlabel=="skip":
                        self.axes[ix].errorbar(self.mid,k,yerr=kerr,fmt='.',alpha=self.hist[ih].alpha,color=self.hist[ih].color,markersize=1.0,zorder=1.0+(self.nh+2.0*i+1.0)/fac)
                    else:
                        self.axes[ix].errorbar(self.mid,k,yerr=kerr,fmt='.',alpha=self.hist[ih].alpha,color=self.hist[ih].color,label=self.hist[ih].hlabel,markersize=1.0,zorder=1.0+(self.nh+2.0*i+1.0)/fac)
            elif self.nplots==1 and self.hist[ih].hlabel!="skip":
                self.axes[ix].errorbar(self.mid,k,yerr=0.0,fmt='.',alpha=self.hist[ih].alpha,color=self.hist[ih].color,label=self.hist[ih].hlabel,markersize=1.0,zorder=1.0+(self.nh+2.0*i+1.0)/fac)            


            if self.hist[ih].exp==False:
                self.axes[ix].hist(self.mid,weights=k,bins=self.bins,histtype="step",color=self.hist[ih].color,linewidth=self.hist[ih].lw,alpha=self.hist[ih].alpha,linestyle=self.hist[ih].lstyle,zorder=1.0+(self.nh+2.0*i+2.0)/fac)               
            
            if bands[i]:
                temp_max=np.max(band_up[:-1])
                temp_min=np.min(band_down[:-1])
                
            else:
                temp_max=np.max(k)
                temp_min=np.min(k)
            
            if self.firstcall[ix-1]:
                self.firstcall[ix-1]=False
                self.xtmax[ix-1]=temp_max
                self.xtmin[ix-1]=temp_min
            else:
                self.xtmax[ix-1]=np.max([temp_max,self.xtmax[ix-1]])
                self.xtmin[ix-1]=np.min([temp_min,self.xtmin[ix-1]])

            if iprint:
                print(ih,self.hist[ih].hlabel)


                if self.hist[ih].ngrid>1:
                    for j in range(0,self.bn):
                        if self.hist[ih].hc[0,j]==0.0 or self.hist[iref].hc[0,j]==0.0:
                            band_up[j]=0.0
                            band_down[j]=0.0
                            continue
                        if norm:
                            band_up[j]=(self.hist[ih].hc_plus[j]/self.hist[ih].cross[0])/(self.hist[iref].hc[0,j]/self.hist[iref].cross[0])
                            band_down[j]=(self.hist[ih].hc_minus[j]/self.hist[ih].cross[0])/(self.hist[iref].hc[0,j]/self.hist[iref].cross[0])
                        else:
                            band_up[j]=self.hist[ih].hc_plus[j]/self.hist[iref].hc[0,j]
                            band_down[j]=self.hist[ih].hc_minus[j]/self.hist[iref].hc[0,j]



                for ij in range(0,len(k)):
                    if ref==-2 and norm:
                        print(ij,self.mid[ij],k[ij])
                    elif self.hist[ih].ngrid>1 and norm==False:
                        print(ij,self.mid[ij],k[ij],np.max([band_up[ij]/k[ij]-1,1-band_down[ij]/k[ij]]))
                    elif self.hist[ih].ngrid>1 and norm==True:
                        print(ij,self.mid[ij],k[ij],np.max([band_up[ij]/k[ij]-1,1-band_down[ij]/k[ij]]))
                    else:
                        print(ij,self.mid[ij],k[ij])

                
          
        if self.xtmin[ix-1]<0.0:
            self.xtmin[ix-1]=0.0
            
        

        

    def plot_sigma(self,order,ref,ix=1):        
        xx=np.linspace(self.xmin,self.xmax,10)

        self.modus[ix-1]="sigma"
        self.axes[ix].grid(True,linewidth=self.grid_size)
        
        if len(order)==2:
            self.axes[ix].plot(xx,np.array([0]*10),color="black",linewidth=0.4,alpha=0.5,zorder=1)
        else:
            self.axes[ix].plot(xx,np.array([0]*10),color=self.hist[ref].color,linewidth=0.4,alpha=0.5,zorder=1)
        
        for i in range(0,len(order)):
            ih=order[i]
            
            if ih==ref: 
                continue
            
            sigma=np.empty(self.bn)
            dev=np.zeros(self.bn)
            sigma.fill(1.0)
            
            for j in range(0,self.bn):
                yerr=np.sqrt(self.hist[ih].hcerr[0,j]**2+self.hist[ref].hcerr[0,j]**2)
                if yerr==0.0:
                    yerr=1.0
                    sigma[j]=0.0
                    
                dev[j]=(self.hist[ref].hc[0,j]-self.hist[ih].hc[0,j])/yerr
        
            
            if len(order)==2:
                self.axes[ix].errorbar(self.mid,dev,yerr=sigma,fmt='.',color='tab:blue',linewidth=self.hist[ih].lw,alpha=self.hist[ih].alpha,markersize=14.0,zorder=2+i)
            else:
                self.axes[ix].errorbar(self.mid,dev,yerr=sigma,fmt='.',color=self.hist[ih].color,linewidth=self.hist[ih].lw,alpha=self.hist[ih].alpha,markersize=14.0,zorder=2+i)
                        
            
            if self.firstcall[ix-1]:
                self.xtmax[ix-1]=np.max(dev)
                self.xtmin[ix-1]=np.min(dev)
            else:
                self.firstcall[ix-1]=False
                temp_max=np.max(dev)
                temp_min=np.min(dev)
                self.xtmax[ix-1]=np.max([temp_max,self.xtmax[ix-1]])
                self.xtmin[ix-1]=np.min([temp_min,self.xtmin[ix-1]])


    def add_horizontal_line(self,ix=1,ypos=0,color="black",linewidth=0.4,alpha=0.5):
       xx=np.linspace(self.xmin,self.xmax,10)

       self.axes[ix].plot(xx,np.array([ypos]*10),color=color,linewidth=linewidth,alpha=alpha,zorder=1)
            

    def set_params(self,ylab,single=False,sym=False,ysize=-1,ysize2=-1):
    #single (only relevant when pdf_unc=True): False -> both ratio plots have same limits, True -> ratio plots have different limits
        alp=0.6  #0.35
        label_pad=15

        if ysize==-1:
            ysize=self.size_font
        if ysize2==-1:
            ysize2=self.size_font
        
        for i in range(0,self.nplots):
            self.axes[i].set_xlim(self.xmin,self.xmax)
            self.axes[i].grid(True,linewidth=self.grid_size,alpha=alp)
            self.axes[i].set_axisbelow(True)
            
            if i==0:
                if self.nplots>1:
                    self.axes[0].set_xticklabels([])     
                self.axes[0].tick_params(axis='both',which='both',direction='in')        
                self.axes[0].set_ylabel(self.ylabel,fontsize=ysize)
                if self.pdf_unc!=-2:
                    self.axes[0].yaxis.set_label_coords(-0.1,0.5)
                else:
                    self.axes[0].yaxis.set_label_coords(-0.12,0.5)
            if i>0 and i<self.nplots-1:
                self.axes[i].set_xticklabels([])
                self.axes[i].tick_params(axis='y',direction='in')
                self.axes[i].tick_params(axis='x',direction='in')
            elif i==self.nplots-1:
                self.axes[i].tick_params(axis='y',direction='in')
                self.axes[i].tick_params(axis='x',direction='inout')
                self.axes[i].set_xlabel(self.xlabel,fontsize=self.size_font)
                if self.pdf_unc==False:
                    self.axes[i].xaxis.set_label_coords(0.5,-0.25)
                elif self.pdf_unc==True:
                    self.axes[i].xaxis.set_label_coords(0.5,-0.28)
                elif self.pdf_unc==-1:
                    self.axes[i].xaxis.set_label_coords(0.5,-0.07)
                elif self.pdf_unc==-2:
                    self.axes[i].xaxis.set_label_coords(0.5,-0.12)
                elif self.pdf_unc==-3:
                    self.axes[i].xaxis.set_label_coords(0.5,-0.10)
        
        #self.ax.legend(markerscale=2.5)      

        for i in range(0,self.nplots):
            if (i==0 and self.nplots>1) or self.pdf_unc<-1:
                continue
            if self.modus[i-1]=="skip":
                continue
            elif self.modus[i-1]=="band":
                self.set_lim(i,single,sym)
            elif self.modus[i-1]=="sigma":
                self.set_lim_sigma(i,single)
            else:
                print("mode not found")
            #print(self.axes[0].get_tightbbox(self.f.canvas.get_renderer()))
            #print(self.axes[1].get_tightbbox(self.f.canvas.get_renderer()))
            #renderer=self.f.canvas.get_renderer()
            #pos_old,t1,t2,t3=self.axes[1].get_tightbbox(renderer).bounds
            #pos_top,t1,t2,t3=self.axes[0].get_tightbbox(renderer).bounds
            #dpi=self.f.canvas.get_renderer().points_to_pixels(1.)
            if self.nplots>1:
                self.axes[i].set_ylabel(ylab[i-1],fontsize=ysize2)
                self.axes[i].yaxis.set_label_coords(-0.1,0.5)

        if self.log and (self.nplots>1 or self.pdf_unc<-1):
            self.ax.set_yscale('log')
        
        if self.start==0.0 and self.end==np.pi:
            for i in range(0,self.nplots):
                self.axes[i].set_xticks([0,np.pi/4,np.pi/2,3*np.pi/4,np.pi])
                if i==self.nplots-1:
                    self.axes[i].set_xticklabels(["0","$\\pi/4$","$\\pi/2$","$3\\pi/4$","$\\pi$"])

        #move ticks
        dx = 0.0
        dy = 0.1

 
        offset = matplotlib.transforms.ScaledTranslation(dx, dy, self.f.dpi_scale_trans)
        for label in self.ax.yaxis.get_majorticklabels():
            label.set_transform(label.get_transform() + offset)
            
        dx = 0.0
        dy = -0.05
        offset = matplotlib.transforms.ScaledTranslation(dx, dy, self.f.dpi_scale_trans)
        
        for i in range(1,self.nplots):
            for label in self.axes[i].xaxis.get_majorticklabels():
                label.set_transform(label.get_transform()+offset)
        
        
    def set_lim(self,ih,single,sym):
        #leg=self.ax.legend(markerscale=self.ms_scale)
        leg=self.ax.legend(markerscale=self.ms_scale,borderaxespad=self.legend_borderaxespad,prop={'size': self.legend_size},handletextpad=self.legend_handletextpad)
        for legobj in leg.legendHandles:
            legobj.set_linewidth(self.lobj_lw)


        #leg=self.axes[2].legend(markerscale=self.ms_scale,borderaxespad=self.legend_borderaxespad,prop={'size': self.legend_size})
        #for legobj in leg.legendHandles:
        #    legobj.set_linewidth(self.lobj_lw)

            
            
        if single:
            maxx=self.xtmax[ih-1]
            minn=self.xtmin[ih-1]
        else:
            maxx=np.max(self.xtmax)
            minn=np.min(self.xtmin)


        bin_max=1.0
        bin_min=1.0
        step=0.05
        ylim_up=1.05
        ylim_down=0.95
        if maxx > 10:
           maxx=10
        while bin_min>minn or bin_max<maxx:
            bin_max+=step
            bin_min-=step

        if bin_min<0.0:
            bin_min=0.0

        if bin_max==1.0:
            bin_max=ylim_up
            bin_min=ylim_down
        else:
            ylim_up=bin_max
            ylim_down=bin_min
        
        arr_y,ylim1,ylim2=get_limit(bin_min,bin_max,iopt=self.get_limit_iopt)

        if ylim1>0.0:
            self.axes[ih].set_ylim(ylim1,ylim2)
            self.axes[ih].set_yticks(arr_y)

#            arr_y_new=[arr_y[0],(arr_y[0]+arr_y[1])/2.0,arr_y[1],(arr_y[1]+arr_y[2])/2.0,arr_y[2],
#                      (arr_y[2]+arr_y[3])/2.0,arr_y[3],(arr_y[3]+arr_y[4])/2.0,arr_y[4]]
#
#            label_temp=[""]*len(arr_y_new)
#            label_temp=["","",str(arr_y[1]),"",str(arr_y[2]),"",str(arr_y[3]),"",""]
#
#            self.axes[ih].set_yticks(arr_y_new)
#            self.axes[ih].set_yticklabels(label_temp)

        else:
            #self.axes[ih].locator_params(axis='y',nbins=3)
            #self.axes[ih].yaxis.set_major_locator(plt.MaxNLocator(3))

            if single==False:
                ymin=0.0
                ymax=0.0
                for i in range(1,self.nplots):
                    if i==1:
                        ymin,ymax=self.axes[i].get_ylim()
                    else:
                        ymint,ymaxt=self.axes[i].get_ylim()
                        if (ymint<ymin):
                            ymin=ymint
                        if (ymaxt>ymax):
                            ymax=ymaxt

                if self.nplots>1:
                    self.axes[ih].set_ylim(ymin,ymax)


        #print(minn)
        if sym and (minn-1.0)>=0.0:
            ymint,ymaxt=self.axes[ih].get_ylim()
            self.axes[ih].set_ylim(1.0,ymaxt)


    def set_lim_sigma(self,ih,single):
        #self.axes[ih].set_yticks([-3,-2,-1,0,1,2,3])
        #self.axes[ih].set_yticklabels(["","-2","-1","0","1","2",""])
        #return

        #leg=self.ax.legend(markerscale=self.ms_scale)
        leg=self.ax.legend(markerscale=self.ms_scale,borderaxespad=self.legend_borderaxespad,prop={'size': self.legend_size},handletextpad=self.legend_handletextpad)
        for legobj in leg.legendHandles:
            legobj.set_linewidth(self.lobj_lw)


        max=self.xtmax[ih-1]
        min=self.xtmin[ih-1]

        maxx=np.max([np.abs(max),np.abs(min)])

        if maxx<2.0:
            self.axes[ih].set_ylim(-3,3)
            self.axes[ih].set_yticks([-2,-1,0,1,2])
        else:
            self.axes[ih].set_yticks([-3,-2,-1,0,1,2,3])
            self.axes[ih].set_yticklabels(["","-2","-1","0","1","2",""])
        

        return


    def add_box(self,text,ncol=1,ix=0,opt={}):
        #leg=self.ax.legend(markerscale=self.ms_scale,ncol=ncol,columnspacing=-0.1)

        ms_scaleT=self.ms_scale
        borderaxespadT=self.legend_borderaxespad
        legend_sizeT=self.legend_size
        columnspacingT=-0.1
        handletextpadT=self.legend_handletextpad
        locT='best'
        if "ms_scale" in opt:
           ms_scaleT=opt["ms_scale"]
        if "borderaxespad" in opt:
           borderaxespadT=opt["borderaxespad"]
        if "legend_size" in opt:
           legend_sizeT=opt["legend_size"]
        if "columnspacing" in opt:
           columnspacingT=opt["columnspacing"]
        if "loc" in opt:
           locT=opt["loc"]
        if "handletextpad" in opt:
           handletextpadT=opt["handletextpad"]

        if "rescal" in opt:
           ymint,ymaxt=self.axes[ix].get_ylim()
           self.axes[ix].set_ylim(ymint,ymaxt+opt["rescal"]*(ymaxt-ymint))

        leg=self.axes[ix].legend(markerscale=ms_scaleT,borderaxespad=borderaxespadT,prop={'size': legend_sizeT},ncol=ncol,columnspacing=columnspacingT,loc=locT,handletextpad=handletextpadT)
        for legobj in leg.legendHandles:
            legobj.set_linewidth(self.lobj_lw)
        if text=="skip":
           return
        txt=offsetbox.TextArea(text) 
        box = leg._legend_box 
        box.get_children().append(txt) 
        box.set_figure(box.figure) 
    
    
    def save_plot(self,path,file):
        if os.path.isdir(path) != True:
            os.makedirs(path)


        plt.savefig(path+file)
        
        
        
        
        
     
