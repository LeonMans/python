import sys
sys.path.append('/mount/vol1/scratch/work/stremmer/software/lib/')
import numpy as np
import canvas as can
import matplotlib.pyplot as plt


def create_plot(ih,iprint=False,fend="jpg"):
    order="nlo"
    iadd=""
    scales=["et4"]
    iscale="E_T/4"
    iphot=["_fix2","_hyb",""]
    label=["Fixed cone","Hybrid iso","Smooth cone"]
    colors=['tab:orange','tab:green','tab:blue']
    lstyle=["solid","solid","solid"]
    order_main=[0,1,2]
    bands_main=[True,True,True]
    hatches=["False","False","False"]


    iphot=["_fix2","_hyb"]
    label=["Fixed cone","Hybrid iso"]
    colors=['tab:orange','tab:green']
    lstyle=["solid","solid"]
    order_main=[0,1]
    bands_main=[True,True]
    hatches=["False","False"]

    ngrid=7

    nlen=len(iphot)


    pdf="NNPDF31_nlo_as_0118"
    hist_setup="../hist_setup.txt"
    plot=can.canvas(hist_setup,ih,pdf_unc=False)


    output_path="../../plots/comp_fix_test/"
    file_out="comp_{0}.{1}".format(plot.obs,fend)




    files=[]
    scalesf=[]

    for i in range(0,nlen):
        path_nlo="../../samples/nlo{0}/{1}/histo_scale/histo_nlo{2}/".format(iadd,pdf,iphot[i])
        scale=scales[0]

        filesT_nlo=[]
        scalesT=[]
        for j in range(0,ngrid):
            filesT_nlo.append("{0}hist_{1}.txt".format(path_nlo,plot.obs))
            scalesT.append("{0}({1})".format(scale,str(j+1)))
        files.append(filesT_nlo)
        scalesf.append(scalesT)
    
    print(ih,plot.obs)



    for i in range(0,nlen):
        plot.add_hist(files[i],label[i],colors[i],lstyle[i],iscale=scalesf[i])


    if ih==0:
       for i in range(0,nlen):
          print("{0} = {1} +- {2}".format(label[i],plot.hist[i].cross[0],plot.hist[i].cerr[0]))




    err_panel=True

    plot.main(order_main,bands_main,hatches=hatches)


    #plot.plot_band(order_main,bands_main,ref=0,itag=err_panel,iprint=iprint)
    plot.plot_sigma(order_main,0)


    #order_band2=[3,0,1,2]
    #order_band2_ref=[3,3,4,5]
    #hatches2=["//","False","False","False"]
    #bands2=[True,True,True,True]

    #plot.plot_band(order_band2,bands2,ref=-2,ref2=order_band2_ref,ix=2,hatches=hatches2,itag=err_panel,iprint=iprint)


    plot.legend_size=28
    plot.legend_borderaxespad=0.2
    plot.set_params(["sigma dev"],single=True,sym=False)

    #box1_opt={ "loc": 'upper right', "rescal": 0.0 }
    #if (ih==42 or ih==46):
    #   box1_opt["rescal"]=0.6

    #plot.add_box("NNPDF3.1 $\\,\\,\\,\\,\\, {{\\rm {0}\,\,QCD}}$".format(order.upper()),ncol=2,opt=box1_opt)
    plot.add_box("NNPDF3.1\n$\\mu_0={0}$".format(iscale),ncol=1) #,opt=box1_opt)




    plot.save_plot(output_path,file_out)
    plt.close()
    


for i in range(0,50):
    create_plot(i)





