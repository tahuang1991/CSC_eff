#!/usr/bin/python
#Author: Jinzhong Zhang(zhangjin@cern.ch), Northeastern University, Boston, U.S.A
#################################################################################
#Advanced Usage:
#python Step2_PlotAll.py arg1 arg2
#   arg1 is directory of the files given by the TagandProbe cmssw package. The file names have to match what is defined in Config.py;
#   arg2 "lct_effV"+arg2 and "seg_effV"+arg2 are the directory name in the TagandProbe result file;
#   arg2 can be specified as "bkg" or "sig" for background and signal modeling
#Example1(plot default efficiencies): python Step2_PlotAll.py
#Example2(systematic -- bkg modeling): python Step2_PlotAll.py /uscms/home/zhangjin/nobackup/ bkg
#Example3(systematic -- sig modeling): python Step2_PlotAll.py /uscms/home/zhangjin/nobackup/ sig
#Example4(systematic -- MCTruth     ): python Step2_PlotAll.py /uscms/home/zhangjin/nobackup/ mc
#Example2-4 are used for systematic calculation.
##################################################################################

from  ROOT import *
import ROOT
from  numpy import *
import numpy
from Config import *
gROOT.SetStyle("Plain")
gStyle.SetPaintTextFormat("4.1f")
gStyle.SetOptStat(0)

gStyle.SetFrameBorderMode(0)
gStyle.SetCanvasBorderMode(0)
gStyle.SetPadBorderMode(0)
gStyle.SetPadColor(0)
gStyle.SetCanvasColor(0)
gStyle.SetTitleColor(1)
gStyle.SetStatColor(0)
gStyle.SetFrameFillColor(0)
gStyle.SetFrameLineWidth(0)
gStyle.SetCanvasBorderMode(0) 
gStyle.SetCanvasBorderSize(0)
gStyle.SetFrameBorderMode(0)
#gStyle.SetPaveBorderMode(0)

gStyle.SetMarkerStyle(8) 
#gStyle.SetMarkerColor(0) 
#gStyle.SetHistLineWidth(1.85) 
gStyle.SetLineStyleString(2,"[12 12]")  
gStyle.SetOptTitle(1) 
gStyle.SetOptStat(1) 
gStyle.SetOptFit(1) 
#gStyle.SetOptTitle(0) 
gStyle.SetOptStat(0) 


gStyle.SetPadBorderSize(0)
gStyle.SetCanvasBorderSize(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetFrameBorderSize(0)
gStyle.SetStatBorderSize(0)
gStyle.SetTitleBorderSize(0)



#TagProbeFitResult="2015C_newAlign_withHLTIsoTkMu_matchOtherStationsORME13/TnP_"+dir_+"_"#Those files are the TagProbeFitTreeAnalyzer outputs.
TagProbeFitResult="TnP_"+dir_+"_"
#Group="Chambers"

if "Chambers" in Group:
  chambers=[]
  for ec_ in (True,False):
    for st_ in (1,2,3,4):
      for rg_ in range(1,5) if st_==1 else range(1,3):
        if st_!=1 and rg_==1: #ME21,31,41 have 18 chambers
          chambers_=range(1,19)
        elif st_==4 and rg_==2: #ME42 has 5 chambers on the plus side
          chambers_=range(1,37)
#          chambers_=(9,10,11,12,13) if ec_ else ()
        else: #ME11,12,13,22,32 have 36 chambers
          chambers_=range(1,37)
        for ch_ in chambers_:
          chambers.append( "ME%s%d_%d_%d"%( '+' if (ec_) else '-', st_, rg_, ch_ ) )
  n_chambers=len(chambers)


from array import array as arr
#Red = arr('d',[0.00, 0.00, 0.00, 1.00, 1.00])
#Green = arr('d',[0.00, 0.10, 1.00, 1.00, 0.00])
#Blue = arr('d',[1.00, 0.90, 0.00, 0.00, 0.00])
#Length = arr('d',[0.00, 0.40, 0.60, 0.80, 1.00])
#TColor.CreateGradientColorTable(5,Length,Red,Green,Blue,500)

#Red = arr('d',[.00, 1.00, 1.00])
#Green = arr('d',[1.00, 1.00, 0.00])
#Blue = arr('d',[0.00, 0.00, 0.00])
#Length = arr('d',[0.00, 0.5, 1.00])
#TColor.CreateGradientColorTable(3,Length,Red,Green,Blue,500)
#Red = arr('d',[1.00, 1.00, 1.00, .00])
#Green = arr('d',[0., 0.00, 1.00, 1.00])
#Blue = arr('d',[1.00, 0.00, 0.00, 0.00])
#Length = arr('d',[0.00, 0.1, 0.55, 1.00])
#TColor.CreateGradientColorTable(4,Length,Red,Green,Blue,500)
Red = arr('d',[0.,1.00, 1.00, 1.00, .00])
Green = arr('d',[0.,0., 0.00, 1.00, 1.00])
Blue = arr('d',[1.0,1.00, 0.00, 0.00, 0.00])
Length = arr('d',[0.00, 0.4, 0.6, 0.8, 1.00])
TColor.CreateGradientColorTable(5,Length,Red,Green,Blue,500)

gStyle.SetNumberContours(500)

def unshitify(pave):
    pave.SetFillStyle(0)
    pave.SetBorderSize(0)

cms_label = ROOT.TPaveText(0.06, 0.84, 0.9, 1.0, "NDC")
unshitify(cms_label)
cms_label.SetTextSize(0.03)
cms_label.SetTextAlign(12)
cms_label.AddText("CMS Preliminary                                                  #sqrt{s}=13 TeV,  2017B")


# by Nick:
#Float_t rgb[300] = {0}
rgb=zeros(300, dtype=float)
#pEff=zeros(100, dtype=int)
pEff = numpy.ndarray( [100],dtype=numpy.float32)
paletteSize = 100
nContours   = 100

for i in range(paletteSize):
    rgb[3 * i + 0] = 0.0
    rgb[3 * i + 1] = 0.8
    rgb[3 * i + 2] = 0.0
    if i <= 97:
        rgb[3 * i + 0] = 0.5
        rgb[3 * i + 1] = 1.0
        rgb[3 * i + 2] = 0.0
    if i <= 96:
        rgb[3 * i + 0] = 1.0
        rgb[3 * i + 1] = 1.0
        rgb[3 * i + 2] = 0.0
    if i <= 94:
        rgb[3 * i + 0] = 1.0
        rgb[3 * i + 1] = 0.5
        rgb[3 * i + 2] = 0.0
    if i <= 89:
        rgb[3 * i + 0] = 1.0
        rgb[3 * i + 1] = 0.0
        rgb[3 * i + 2] = 0.0
    pEff[i] = ROOT.TColor.GetColor(rgb[3 * i + 0], rgb[3 * i + 1], rgb[3 * i + 2])
#    print 'i= ',i,' pEff= ', pEff[i]
    
    
#gStyle.SetPalette(paletteSize, pEff)
#gStyle.SetNumberContours(paletteSize)

#print 'pallete: ', paletteSize, ' \n', pEff

#gStyle.SetNumberContours(nContours)
#gStyle.SetOptStat(0)
#gStyle.SetPalette(paletteSize, pEff)


import sys,os,re
if (sys.argv[0] == "python"): args=sys.argv[2:]
else: args=sys.argv[1:]

#Prefix="/scratch/senka/CSCeff_condor_RunC_matching/"
Prefix="/afs/hep.wisc.edu/cms/senka/CMSSW_7_4_7/src/CSCEfficiency/CSCEfficiency/NtupleAnzScripts/"
Postfix=""
print "TagAndProbeFitResult: ",TagProbeFitResult
#TagProbeFitResult=TagProbeFitResult.split("/")[-1]
ResultPlotsFileName=ResultPlotsFileName.split("/")[-1]
print " ->TagAndProbeFitResult: ",TagProbeFitResult

if len(args)>0:
    Prefix=args[0]
    if Prefix[-1] != "/":
        Prefix+="/"
    if len(args)>1:
        if args[1] == "bkg":
            Postfix="_BkgModeling"
        elif args[1] == "sig":
            Postfix="_SigModeling"
        elif args[1] == "mc":
            Postfix="_MCTruth"
        else:
            Postfix=args[1]
    ResultPlotsFileName=Prefix+ResultPlotsFileName.replace(".root",Postfix+".root")

file_out=TFile.Open(ResultPlotsFileName,'RECREATE')

etascheme="abseta"
#etascheme="tracks_eta"
phischeme="shiftedphi"
#phischeme="tracks_phi"
if "pt" in Group:
    binning="pt"
    plotname="tracks_pt_PLOT"
elif "eta" in Group:
    binning="eta"
    plotname=etascheme+"_PLOT"
elif "phi" in Group:
    binning="phi"
    plotname=phischeme+"_PLOT"
elif "PV" in Group:
    binning="PV"
    plotname="numberOfPrimaryVertices_PLOT"
else:
    plotname=phischeme+"_bin0__"+etascheme+"_bin0__tracks_pt_bin0__VoigtianPlusExpo"

if Postfix=="_MCTruth":
    plotname+="_&_mcTrue_true"

def GetEff(f_in,path="lct_effV",effcat="fit_eff"):
    print "LCT eff reading file: ",f_in
    try:
        eff=f_in.Get("Probes/"+path+"/"+effcat).get().find("efficiency")
        return [eff.getVal(),abs(eff.getErrorLo()),eff.getErrorHi()]
    except:
        print "\033[97mOther problems, skip",f_in.GetName(),"\033[0m"
        return [0.]*3

def GetBinnedEffPlot(f_in,path="lct_effV",effcat="fit_eff",st_=0,name_=plotname):
    print "binned LCT eff reading file: ",f_in
    canvas_=f_in.Get("Probes/"+path+"/"+effcat+"_plots/"+name_)
    if not canvas_:
        print "\033[91m Warning: Probes/"+path+"/"+effcat+"_plots/"+name_," does not exist in",f_in.GetName(),"\033[0m"
        return NULL
    dummyplot_=canvas_.GetListOfPrimitives().At(0)
    plot_=canvas_.FindObject("hxy_"+effcat).Clone();
    #we are going to fix the bugs in tagandprobe package in the following code
    #1 - recreate the arrays
    nbins=plot_.GetN()
    xval=zeros(nbins, dtype=float)
    xerr=zeros(nbins, dtype=float)
    yerrhi=zeros(nbins, dtype=float)
    yerrlo=zeros(nbins, dtype=float)
    #2 - the y values are correct
    Y=plot_.GetY()
    #3 - find the corresponding first bin in the predefined bins for the plot_ first bin0
    exec( "bins=%sbin%s"%(binning,str(st_) if binning=="eta" else "") )
    X=plot_.GetX()
    for abin in bins:
        if X[0]<abin:
            firstbin=bins.index(abin)-1
            break
    #4 - fill the yerror bars from the correct input (only for fit efficiency)
    if effcat=="fit_eff":
        list_=f_in.Get("Probes/"+path).GetListOfKeys()
        ikey=list_.First()
        while (ikey!=list_.After(list_.Last())):
            dirname_=ikey.GetName()
#            binnumber=re.match(".*"+binning+"_bin(\d*)_.*",dirname_)
            if "PV" in Group:
              binnumber=re.match(".*"+"numberOfPrimaryVertices"+"_bin(\d*)_.*",dirname_)
            else:
              binnumber=re.match(".*"+binning+"_bin(\d*)_.*",dirname_)

            if binnumber:
                ibin=int(binnumber.group(1))-firstbin
                if ibin<nbins and ibin>=0:
                    result_=f_in.Get("Probes/"+path+"/"+dirname_+"/fitresults")
                    if result_:
                        value_=result_.floatParsFinal().find("efficiency")
                        yerrlo[ibin]=abs(value_.getErrorLo())
                        yerrhi[ibin]=value_.getErrorHi()
                        """
                        if Y[ibin]!=value_.getVal(): #show differences (should less than 1E-6)
                            print Y[ibin],
                            value_.Print()
                        """
                        if Y[ibin]<0.999 and yerrhi[ibin]<1E-7:
                            yerrhi[ibin]=yerrlo[ibin] #sometime the result misses the high error, we make an approximation: ErrorHi=ErrorLo in this case
                        if Y[ibin]+yerrhi[ibin]>1.:
                            yerrhi[ibin]=1.-Y[ibin] # it happens sometime when ErrorHi=ErrorLo
            ikey = list_.After(ikey);
    #5 - fill the correct x values from the binning 
    for ibin in range(nbins):
        xval[ibin]=(bins[ibin+firstbin]+bins[ibin+firstbin+1])/2.
        xerr[ibin]=abs(bins[ibin+firstbin+1]-bins[ibin+firstbin])/2.
    #6 - remake the TGraph
    plotname_=f_in.GetName().replace(Prefix+TagProbeFitResult,"")[:-5]+path
    outputplot=TGraphAsymmErrors(nbins, xval, Y, xerr, xerr, yerrlo, yerrhi)
    outputplot.SetName(plotname_)
    outputplot.SetTitle(outputplot.GetName())
    outputplot.GetXaxis().SetTitle(dummyplot_.GetXaxis().GetTitle())
    outputplot.GetYaxis().SetTitle(dummyplot_.GetYaxis().GetTitle())
    outputplot.GetYaxis().SetTitleOffset(1.2)
    #outputplot.SetMarkerStyle(8)
    #outputplot.SetMarkerSize(.5)
    """
    outputplot.SetMinimum(0.9)
    outputplot.SetMaximum(1.0)
    EffCanvas=TCanvas(plotname_,plotname_,500,500)
    EffCanvas.cd()
    if binning=="pt":
        outputplot.GetXaxis().SetLimits(10., 100.);
    #gPad.SetLogx()
    outputplot.Draw("AP")
    raw_input("pause")
    """
    return outputplot

if "Stations" in Group:
    Effs=[]
    for idx in range(1,n_stations+1):
        filename_=Prefix+TagProbeFitResult+stations[idx][1]+".root"
        if not os.path.isfile(filename_):
            print filename_+" is not found, skip.. "
            Effs.append([0.]*6)
            continue
        f_in=TFile(filename_,"READ");
        categoryname="cnt_eff" if Postfix=="_MCTruth" else "fit_eff"
        if "pt" in Group or "eta" in Group or "phi" in Group or "PV" in Group:
            LCTEff=GetBinnedEffPlot(f_in, "lct_effV"+Postfix,categoryname,stations[idx][3])
            SEGEff=GetBinnedEffPlot(f_in, "seg_effV"+Postfix,categoryname,stations[idx][3])
            file_out.cd()
            if LCTEff:
                LCTEff.Write()
            if SEGEff:
                SEGEff.Write()
        else:
            Effs.append( GetEff(f_in, "lct_effV"+Postfix,categoryname)+GetEff(f_in,"seg_effV"+Postfix,categoryname) )
            f_in.Close()
    if not ("pt" in Group or "PV" in Group or "eta" in Group or "phi" in Group):
        Effs=array(Effs).transpose()*100.
        xval=array(range(1,n_stations+1))*1.0
        xerr=zeros(n_stations, dtype=float)
        SEGEff=TGraphAsymmErrors(n_stations, xval, array(Effs[0]), xerr, xerr, array(Effs[1]), array(Effs[2]))
        LCTEff=TGraphAsymmErrors(n_stations, xval, array(Effs[3]), xerr, xerr, array(Effs[4]), array(Effs[5]))
        SegCanvas=TCanvas("segment efficiency","segment efficiency",500,500)
        SegCanvas.cd()
	gStyle.SetPaintTextFormat("4.1f")	
        SEGEff.SetMaximum(100)
        SEGEff.SetMinimum(90)
        LCTEff.SetMaximum(100)
        LCTEff.SetMinimum(90)
        SEGEff.SetMarkerStyle(8)
        SEGEff.SetMarkerSize(.5)
        SEGEff.Draw("AP")
        cms_label.Draw()

        LCTCanvas=TCanvas("lct efficiency","lct efficiency",500,500)
        LCTCanvas.cd()
        LCTEff.SetMarkerStyle(8)
        LCTEff.SetMarkerSize(.5)
        LCTEff.Draw("AP")
        cms_label.Draw()
        for st in range(1,n_stations+1):
           binnum=SEGEff.GetXaxis().FindBin(st)
           SEGEff.GetXaxis().SetBinLabel( binnum,stations[st][1] )
           LCTEff.GetXaxis().SetBinLabel( binnum,stations[st][1] )
        SEGEff.GetXaxis().SetTitle("Ring")
        SEGEff.GetYaxis().SetTitle("Chamber within ring")

        file_out.cd()
        if LCTEff:
           LCTEff.Write("LCTEff")
        if SEGEff:
           SEGEff.Write("SEGEff")
elif "Chambers" in Group:
    SEGEff=TH2F("SEGEff","CSC Segment Reconstruction Efficiency (%)",36,1,37,20,-9,9)
    SEGEff.SetMarkerSize(0.7)
    gStyle.SetPaintTextFormat("4.1f")
    SEGEff.SetContour(500)
    SEGEff_upErr=TH2F("SEGEff_upErr","segment efficiency uperror",36,1,37,20,-8.7,9.3)
    SEGEff_upErr.SetMarkerSize(0.45)
    SEGEff_downErr=TH2F("SEGEff_downErr","segment efficiency loerror",36,1,37,20,-9.3,8.7)
    SEGEff_downErr.SetMarkerSize(0.45)
    SEGEff.GetYaxis().SetTickLength(0)
    Chambers_  = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36"]
    Rings_ = ["ME-42","ME-41","ME-32","ME-31","ME-22","ME-21","ME-13","ME-12","ME-11B","ME-11A","ME+11A","ME+11B","ME+12","ME+13","ME+21","ME+22","ME+31","ME+32","ME+41","ME+42"]
    for ich in range(36):
        SEGEff.GetXaxis().SetBinLabel(ich+1,Chambers_[ich])
        SEGEff_upErr.GetXaxis().SetBinLabel(ich+1,Chambers_[ich])
        SEGEff.GetXaxis().SetBinLabel(ich+1,Chambers_[ich])
    for irg in range(20):
        SEGEff.GetYaxis().SetBinLabel(irg+1,Rings_[irg])
        SEGEff_upErr.GetYaxis().SetBinLabel(irg+1,Rings_[irg])
        SEGEff_downErr.GetYaxis().SetBinLabel(irg+1,Rings_[irg])
    LCTEff=SEGEff.Clone("LCTEff")
    LCTEff.SetTitle("CSC Trigger Primitive Efficiency (%)")
    LCTEff_upErr=SEGEff_upErr.Clone("LCTEff_upErr")
    LCTEff_downErr=SEGEff_downErr.Clone("LCTEff_downErr")
    LCTEff.GetYaxis().SetTickLength(0)
    RingToYMap={(1,4):0,(1,1):1,(1,2):2,(1,3):3,(2,1):4,(2,2):5,(3,1):6,(3,2):7,(4,1):8,(4,2):9}
  #split tree to chamber
    for idx in range(n_chambers):
        ec=chambers[idx][2] == '+'
        st=int(chambers[idx][3])
        rg=int(chambers[idx][5])
        ch=int(chambers[idx][7:])
        filename_="%s%s%s.root" % (Prefix,TagProbeFitResult,chambers[idx])
        if not os.path.isfile(filename_):
            print filename_+" is not found, skip.. "
            Effs.append([0.]*6)
            continue
        f_in=TFile(filename_,"READ");
        print "chamber LCT eff reading file: ",f_in
        if Postfix=="_MCTruth":
            Effs=GetEff(f_in, "lct_effV"+Postfix,"cnt_eff")+GetEff(f_in,"seg_effV"+Postfix,"cnt_eff")
        else:
	    print "reading file: ", f_in, " reading efficiency: ", "seg_effV"+Postfix,"fit_eff"
            Effs=GetEff(f_in, "lct_effV"+Postfix,"fit_eff")+GetEff(f_in,"seg_effV"+Postfix,"fit_eff" )
        f_in.Close()
        iBin_y=RingToYMap[(st,rg)]
        iBin_y=11+iBin_y if ec else 10-iBin_y
        eff=Effs[0]*100.
	if Effs[0]<0.00001:
	    Effs[0]=0.00001
        if Effs[3]<0.00001:
            Effs[3]=0.00001
        LCTEff.GetYaxis().SetTitle("Ring")
        LCTEff.GetXaxis().SetTitle("Chamber within ring")
        LCTEff.GetYaxis().SetTitleOffset(1.35)
	LCTEff.SetBinContent(ch,iBin_y,Effs[0]*100.);
        if (eff>0):
            LCTEff_downErr.SetBinContent(ch,iBin_y,Effs[1]*100.);
            LCTEff_upErr.SetBinContent(ch,iBin_y,Effs[2]*100.);
        eff=Effs[3]*100.
        if Effs[3]<0.00001:
            Effs[3]=0.00001
	SEGEff.SetBinContent(ch,iBin_y,Effs[3]*100.);
        if (eff>0):             
            SEGEff_downErr.SetBinContent(ch,iBin_y,Effs[4]*100.);
            SEGEff_upErr.SetBinContent(ch,iBin_y,Effs[5]*100.);
    gStyle.SetPaintTextFormat("4.1f")
    SegCanvas=TCanvas("segment efficiency","segment efficiency",1500,1000)
    SegCanvas.cd()
    
    SEGEff.GetYaxis().SetTitle("Ring")
    SEGEff.GetXaxis().SetTitle("Chamber within ring")
    SEGEff.GetYaxis().SetTitleOffset(1.35)
#    SEGEff.SetTitle("")

    SEGEff.Draw("COLZ,TEXT")
    SEGEff_upErr.Draw("TEXT,SAME")
    SEGEff_downErr.Draw("TEXT,SAME")
    SEGEff.SetMaximum(100)
    SEGEff.SetMinimum(0)
    cms_label.Draw()

    LCTCanvas=TCanvas("lct efficiency","lct efficiency",1500,1000)
    LCTCanvas.cd()
    LCTEff.Draw("COLZ,TEXT")
    LCTEff_upErr.Draw("TEXT,SAME")
    LCTEff_downErr.Draw("TEXT,SAME")
    LCTEff.SetMaximum(100)
    LCTEff.SetMinimum(0)
    cms_label.Draw()

    file_out.cd()
    SegCanvas.Write()
    SegCanvas.SaveAs("SegCanvas_2D.pdf")
    SegCanvas.SaveAs("SegCanvas_2D.root")
    SegCanvas.SaveAs("SegCanvas_2D.C")
    LCTCanvas.Write()
    LCTCanvas.SaveAs("LCTCanvas_2D.pdf")
    LCTCanvas.SaveAs("LCTCanvas_2D.root")
    LCTCanvas.SaveAs("LCTCanvas_2D.C")
    SEGEff.Write()
    SEGEff_upErr.Write()
    SEGEff_downErr.Write()
    LCTEff.Write()
    LCTEff_upErr.Write()
    LCTEff_downErr.Write()
elif "pt" in Group or "PV" in Group or "eta" in Group or "phi" in Group:
    filename_=Prefix+TagProbeFitResult+"AllStations.root"
    print "pt/eta/phi eff reading file: ",f_in
    if not os.path.isfile(filename_):
        print filename_+" is not found, skip.. "
    else:
        f_in=TFile(filename_,"READ");
        categoryname="cnt_eff" if Postfix=="_MCTruth" else "fit_eff"
        LCTEff=GetBinnedEffPlot(f_in, "lct_effV"+Postfix,categoryname)
        SEGEff=GetBinnedEffPlot(f_in, "seg_effV"+Postfix,categoryname)
        f_in.Close()
        file_out.cd()
        if LCTEff:
           LCTEff.Write("LCTEff")
        if SEGEff:
           SEGEff.Write("SEGEff")
#raw_input("Plots are saved in "+ResultPlotsFileName+". Press ENTER to exit")
print "Plots are saved in",ResultPlotsFileName+"."
file_out.Close()
