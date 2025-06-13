import sys
sys.path.append('/mount/vol1/scratch/work/stremmer/software/lib/')
import numpy as np
import canvas as can
import matplotlib.pyplot as plt


def create_plot(ih,iprint=False,fend="jpg"):
    order="lo"


    #scale="et4"
    #iscale="E_T/4"
    scale="ht4"
    iscale="H_T/4"



    proc="tta"

    iorder=-1
    iadd_ord=""
    if iorder!=-1:
       iadd_ord="_as{0}".format(str(iorder))


    mode="LO"


    iadd=""

    tpath="scale_unc"
    if mode.find("histo")==0:
       tpath="histo_scale"


    output_path="../../plots/test_{0}_{1}{2}/".format(mode,scale,iadd_ord)

    pdf="NNPDF31_nlo_as_0118"
    path="../../samples/nlo{0}/{1}/{2}/{3}/".format(iadd,pdf,tpath,mode)
    path_lhe="../../samples/nlo_lhe{0}/{1}/{2}/{3}/".format(iadd,pdf,tpath,mode)

    
    hist_setup="../hist_setup.txt"


    plot=can.canvas(hist_setup,ih,pdf_unc=False)
    
    nscales=7


    file1=[]
    file2=[]
    file3=[]
    file4=[]
    scales=[]


    for i in range(0,nscales):
        file1.append("{0}hist_{1}.txt".format(path,plot.obs))
        file2.append("{0}hist_{1}.txt".format(path_lhe,plot.obs))
        scales.append("{0}{1}({2})".format(scale,iadd_ord,str(i+1)))





 

    file_out="{0}_reg_{1}.{2}".format(order,plot.obs,fend)
    
    print(ih,plot.obs)


    plot.add_hist(file1,"HELAC",'tab:blue',"solid",iscale=scales)
    plot.add_hist(file2,"LHEF",'tab:orange',"solid",iscale=scales)





    plot.xlabel=plot.xlabel.replace("e^+","\\ell^+")
    plot.ylabel=plot.ylabel.replace("e^+","\\ell^+")
    plot.xlabel=plot.xlabel.replace("\\mu^-","\\ell^-")
    plot.ylabel=plot.ylabel.replace("\\mu^-","\\ell^-")

    order_main=[0,1]
    bands_main=[False,False]

    #plot.log=False
    
    plot.main(order_main,bands_main)




    plot.plot_sigma(order_main,0)
    plot.set_params(["sigma dev"])


    plot.legend_size=28
    plot.legend_borderaxespad=0.2
    plot.set_params(["Ratio"],sym=True)
    plot.add_box("NNPDF3.1 $\\,\\,\\,\\,\\,\\mu_0={0}$".format(iscale),ncol=2)



    plot.save_plot(output_path,file_out)
    
    if False:
        devia=1e-5
        for i in range(0,plot.bn):
            err1=plot.hist[0].hcerr[0,i]
            err2=plot.hist[1].hcerr[0,i]
            hc1=plot.hist[0].hc[0,i]
            hc2=plot.hist[1].hc[0,i]
            
            if err1==0.0 or hc1==0.0:
                continue
            
            if (np.abs(err1-err2)/np.min([err1,err2])>devia):
                print("ERROR: ",err1,err2,np.abs(err1-err2)/np.min([err1,err2]))
            if (np.abs(hc1-hc2)/np.min([hc1,hc2])>devia):
                print("ERROR: ",hc1,hc2,np.abs(hc1-hc2)/np.min([hc1,hc2]))
        

    plt.close()
    

for i in range(0,50):
    create_plot(i)




#arr=[8,13,15,7,46,47,42,43]
#
#for i in range(0,len(arr)):
#    create_plot(arr[i],True,"jpg")


