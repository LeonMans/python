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

    #iphot=["_fix2","_hyb","_frix"]
    iphot=["_fix2_smear","_hyb_smear","_frix_smear"]
    label=["Fixed cone","Hybrid iso","Smooth cone"]
    colors=['tab:blue','tab:green','tab:orange']
    lstyle=["solid","solid","solid"]
    order_main=[0,2,1]
    bands_main=[True,True,True]
    hatches=["False","False","False"]


    #iadd="2"
    #iphot=["_fix2_smear",""]
    #label=["Fixed cone","Smooth cone"]
    #colors=['tab:blue','tab:orange']
    #lstyle=["solid","solid"]
    #order_main=[0,1]
    #bands_main=[True,True]
    #hatches=["False","False"]



    #iphot=["_fix2_smear","_hyb"]
    #label=["Fixed cone","Hybrid iso"]
    #colors=['tab:orange','tab:green']
    #lstyle=["solid","solid"]
    #order_main=[0,1]
    #bands_main=[True,True]
    #hatches=["False","False"]

    ngrid=7

    nlen=len(iphot)


    pdf="NNPDF31_nlo_as_0118"
    hist_setup="../hist_setup.txt"
    plot=can.canvas(hist_setup,ih,pdf_unc=False)


    output_path="../../plots/comp_fix{0}/".format(iadd)
    file_out="phot_iso_{0}.{1}".format(plot.obs,fend)




    files=[]
    scalesf=[]

    for i in range(0,nlen):
        path_nlo="../../samples/nlo{0}/{1}/histo_scale/histo_nlo{2}/".format("",pdf,iphot[i])
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


    plot.plot_band(order_main,bands_main,ref=0,itag=err_panel,iprint=iprint)

    plot.xlabel=plot.xlabel.replace("\gamma_1","\gamma")
    plot.ylabel=plot.ylabel.replace("\gamma_1","\gamma")
    #print(plot.xlabel,plot.ylabel)


    plot.legend_size=26
    plot.legend_borderaxespad=0.2
    plot.set_params(["Ratio"],single=True,sym=False)

    box1_opt={ "loc": 'upper right', "rescal": 0.0 }
    if (ih==35):
       box1_opt["rescal"]=0.70
    elif (ih==36):
       box1_opt["rescal"]=0.10

    #plot.add_box("NNPDF3.1 $\\,\\,\\,\\,\\, {{\\rm {0}\,\,QCD}}$".format(order.upper()),ncol=2,opt=box1_opt)
    plot.add_box("NNPDF3.1\n$\\mu_0={0}$".format(iscale),ncol=1,opt=box1_opt)




    plot.save_plot(output_path,file_out)
    plt.close()
    


#for i in range(0,50):
#    create_plot(i)




#arr=[0,2,9,35,44,46]


arr=[2,36,44,46]

for i in arr:
   create_plot(i,True,"pdf")

