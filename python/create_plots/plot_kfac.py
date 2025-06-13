import sys
sys.path.append('/mount/vol1/scratch/work/stremmer/software/lib/')
import numpy as np
import canvas as can
import matplotlib.pyplot as plt


def create_plot(ih,iprint=False,fend="jpg"):
    order="nlo"
    iadd=""
    scales=["et4","ht4","mt"]
    label=["$\\mu_0=E_T/4$","$\\mu_0=H_T/4$","$\\mu_0=m_t$"]
    #label=["NLO($E_T/4$)","NLO($H_T/4$)","NLO($m_t$)"]
    colors=['tab:blue','tab:orange','tab:green']
    lstyle=["solid","solid","solid"]
    ngrid=7
    nscales=len(scales)


    pdf="NNPDF31_nlo_as_0118"
    hist_setup="../hist_setup.txt"
    plot=can.canvas(hist_setup,ih,pdf_unc=True,iopt=1)


    path_lo="../../samples/nlo{0}/{1}/histo_scale/histo_{2}/".format(iadd,pdf,"lo")
    path_nlo="../../samples/nlo{0}/{1}/histo_scale/histo_{2}/".format(iadd,pdf,"nlo_fix2_smear")
    output_path="../../plots/kfac/"
    file_out="kfac_frag_{0}.{1}".format(plot.obs,fend)




    files_lo=[]
    files_nlo=[]
    scalesf=[]

    for i in range(0,nscales):
        scale=scales[i]

        filesT_lo=[]
        filesT_nlo=[]
        scalesT=[]
        for j in range(0,ngrid):
            filesT_lo.append("{0}hist_{1}.txt".format(path_lo,plot.obs))
            filesT_nlo.append("{0}hist_{1}.txt".format(path_nlo,plot.obs))
            scalesT.append("{0}({1})".format(scale,str(j+1)))
        files_lo.append(filesT_lo)
        files_nlo.append(filesT_nlo)
        scalesf.append(scalesT)
    
    print(ih,plot.obs)



    for i in range(0,nscales):
        plot.add_hist(files_nlo[i],label[i],colors[i],lstyle[i],iscale=scalesf[i])
    for i in range(0,nscales):
        plot.add_hist(files_lo[i],"skip",colors[i],lstyle[i],iscale=scalesf[i])


    if ih==0:
       for i in range(0,nscales):
          print("{0} = {1} +- {2}".format(label[i],plot.hist[i].cross[0],plot.hist[i].cerr[0]))


    order_main=[0,1,2]
    bands_main=[True,True,True]
    hatches=["False","False","False"]

    #order_main=[3,4,5,0,1,2]
    #bands_main=[True,True,True,True,True,True]
    #hatches=["//","//","//","False","False","False"]

    err_panel=True

    plot.main(order_main,bands_main,hatches=hatches)


    order_band2=[3,4,5,0,1,2]
    order_band2_ref=[3,4,5,3,4,5]
    hatches2=["/","/","/","False","False","False"]
    bands2=[True,True,True,True,True,True]

    plot.plot_band(order_band2,bands2,ref=-2,ref2=order_band2_ref,ix=1,alpha_param=[0.3,0.3],hatches=hatches2,itag=err_panel,iprint=iprint)

    order_band1=[0,1,2]
    bands1=[True,True,True]
    plot.plot_band(order_band1,bands1,ref=0,ix=2,itag=err_panel,iprint=iprint)

    plot.xlabel=plot.xlabel.replace("\gamma_1","\gamma")
    plot.ylabel=plot.ylabel.replace("\gamma_1","\gamma")
    #print(plot.xlabel,plot.ylabel)



    plot.legend_size=28
    plot.legend_borderaxespad=0.2
    plot.set_params(["${{\\rm NLO}}/{{\\rm LO}}$","Ratio"],single=True,sym=False)

    box1_opt={ "loc": 'upper right', "rescal": 0.0 }
    if (ih==35):
       box1_opt["rescal"]=0.8

    #plot.add_box("NNPDF3.1 $\\,\\,\\,\\,\\, {{\\rm {0}\,\,QCD}}$".format(order.upper()),ncol=2,opt=box1_opt)
    plot.add_box("NNPDF3.1",ncol=1,opt=box1_opt)




    plot.save_plot(output_path,file_out)
    plt.close()
    


#for i in range(0,50):
#    create_plot(i)



arr=[2,15,17,35,44]
#arr=[17]
for i in arr:
    create_plot(i,True,"pdf")



