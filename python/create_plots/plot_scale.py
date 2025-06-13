import sys
sys.path.append('/mount/vol1/scratch/work/stremmer/software/lib/')
import numpy as np
import canvas as can
import matplotlib.pyplot as plt


def create_plot(ih,iprint=False,fend="jpg"):
    order="nlo"
    iadd=""
    iadd2="_fix2_smear"
    #iadd2=""
    scales=["et4","ht4","mt"]
    label=["$\\mu_0=E_T/4$","$\\mu_0=H_T/4$","$\\mu_0=m_t$"]
    label=["{0}($E_T/4$)".format(order.upper()),"{0}($H_T/4$)".format(order.upper()),"{0}($m_t$)".format(order.upper())]
    colors=['tab:blue','tab:orange','tab:green']
    lstyle=["solid","solid","solid"]
    ngrid=7
    nscales=len(scales)


    pdf="NNPDF31_nlo_as_0118"
    hist_setup="../hist_setup.txt"
    plot=can.canvas(hist_setup,ih,pdf_unc=True,iopt=1)


    path="../../samples/nlo{0}/{1}/histo_scale/histo_{2}{3}/".format(iadd,pdf,order,iadd2)
    output_path="../../plots/{0}{1}_scale/".format(order,iadd2)
    file_out="{0}{3}_{1}.{2}".format(order,plot.obs,fend,iadd2)



    files=[]
    scalesf=[]

    for i in range(0,nscales):
        scale=scales[i]

        filesT=[]
        scalesT=[]
        for j in range(0,ngrid):
            filesT.append("{0}hist_{1}.txt".format(path,plot.obs))
            scalesT.append("{0}({1})".format(scale,str(j+1)))
        files.append(filesT)
        scalesf.append(scalesT)
    
    print(ih,plot.obs)



    for i in range(0,nscales):
        plot.add_hist(files[i],label[i],colors[i],lstyle[i],iscale=scalesf[i])


    if ih==0:
       for i in range(0,nscales):
          print("{0} = {1} +- {2}".format(label[i],plot.hist[i].cross[0],plot.hist[i].cerr[0]))


    order_main=[0,1,2]
    bands_main=[True,True,True]
    hatches=["False","False","False"]

    err_panel=True

    plot.main(order_main,bands_main)
    plot.plot_band(order_main,bands_main,ref=0,hatches=hatches,itag=err_panel,iprint=iprint)


    order_band2=[2,0,1]
    hatches2=["False","\\","//"]
    hatches2=["False","False","False"]

    plot.plot_band(order_band2,bands_main,ref=-2,ref2=order_band2,hatches=hatches2,ix=2,itag=err_panel,iprint=iprint)


    plot.legend_size=28
    plot.legend_borderaxespad=0.2
    plot.set_params(["Ratio","Scale unc."],single=True,sym=False)

    box1_opt={ "loc": 'upper right', "rescal": 0.0 }
    #if (ih==42 or ih==46):
    #   box1_opt["rescal"]=0.6

    #plot.add_box("NNPDF3.1 $\\,\\,\\,\\,\\, {{\\rm {0}\,\,QCD}}$".format(order.upper()),ncol=2,opt=box1_opt)
    plot.add_box("NNPDF3.1",ncol=1,opt=box1_opt)




    plot.save_plot(output_path,file_out)
    plt.close()
    


for i in range(0,50):
    create_plot(i)





