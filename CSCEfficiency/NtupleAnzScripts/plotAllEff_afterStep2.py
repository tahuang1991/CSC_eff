from  ROOT import *
from  numpy import *
from array import *
import CMS_lumi, tdrstyle
import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TEfficiency, TLegend

from ROOT import SetOwnership
from Config import *

gROOT.SetStyle("Plain")
gStyle.SetPaintTextFormat("0.3g")
gStyle.SetOptStat(0)
tdrstyle.setTDRStyle()
gStyle.SetPadGridY(1)

Prefix="outputhisto_name"
import sys,os,re
if (sys.argv[0] == "python"): args=sys.argv[2:]
else: args=sys.argv[1:]
if len(args)>0:
    Prefix=args[0]
    Postfix=""
    if len(args)>1:
        if args[1] == "bkg":
            Postfix="_BkgModeling"
        elif args[1] == "sig":
            Postfix="_SigModeling"
        elif args[1] == "mc":
            Postfix="_MCTruth"
        else:
            Postfix=args[1]

def unshitify(pave):
    pave.SetFillStyle(0)
    pave.SetBorderSize(0)

cms_label = ROOT.TPaveText(0.15, 0.95, 0.9, 1.0, "NDC")
unshitify(cms_label)
cms_label.SetTextSize(0.03)
cms_label.SetTextAlign(12)
#cms_label.AddText("CMS Preliminary 2018                       #sqrt{s}=13 TeV");
cms_label.AddText("CMS Preliminary 2018                       cosmics");

dir=""

ResultPlotsFileName="resultplots_NtupleAnzScripts_output.root"
file_out=TFile.Open(ResultPlotsFileName,'RECREATE')

print "Group: ",Group
X_axis="probe"
if "phi" in Group:
    X_axis+=" #phi"    
if "eta" in Group:
    X_axis+=" #eta"    
if "pt" in Group:
    X_axis+=" p_{T}"    
if "PV" in Group:
    X_axis="NPU"    
print "X_axis= ",X_axis

for obj in (1,2):
    if (obj==1):
        Prefix+="_LCT"
    if (obj==2):
        Prefix=Prefix.replace("LCT","SEG")

    c1=TCanvas("c1","c1",600,600)
    c2=TCanvas("c2","c2",600,600)
    leg=TLegend(0.45, 0.25, 0.95, 0.36)
   
    leg.SetNColumns(2) 
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetShadowColor(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(132)
    leg.SetTextSize(0.04)

    leg_ME1=TLegend(0.45, 0.25, 0.95, 0.36)
   
    leg_ME1.SetNColumns(2) 
    leg_ME1.SetFillColor(0)
    leg_ME1.SetFillStyle(0)
    leg_ME1.SetShadowColor(0)
    leg_ME1.SetBorderSize(0)
    leg_ME1.SetTextFont(132)
    leg_ME1.SetTextSize(0.04)
    color=0
    
    input_file_name=dir+"resultplots_NtupleAnzScripts.root"
    print " input file: ",input_file_name
    file_in = TFile.Open(input_file_name,"read")
    for st_ in ("4","3","2","1"):
        color+=1
        if (color==3 or color==5):
           color+=1
        variable=""
        print "st: %s, obj: %s"%(st_,obj)
	try:
            if (obj==1):
                histo=file_in.Get("ME%slct_effV"%st_)
            if (obj==2):
                histo=file_in.Get("ME%sseg_effV"%st_)
            print " found %s"%st_
        except:
	    print "not found %s"%st_
            continue

        print " plotting %s"%st_
        if (obj==1):
            histo=file_in.Get("ME%slct_effV"%st_)
            print "ME%slct_effV"%st_
        if (obj==2):
            histo=file_in.Get("ME%sseg_effV"%st_)
            print "ME%sseg_effV"%st_
        c1.cd()
        histo.SetLineColor(color)
        histo.SetMarkerSize(0.5)
        histo.SetMarkerColor(color)
        leg.AddEntry(histo,"ME%s"%st_,"lp")
        if (color==1):
            histo.SetTitle(";%s;efficiency"%variable);
            histo.SetMinimum(0.7) 
            histo.GetYaxis().SetRangeUser(0.7,1.05)
            histo.GetXaxis().SetTitle(X_axis)
            histo.GetYaxis().SetTitleOffset(1.6)
            histo.GetXaxis().SetTitleOffset(1.4)
            if (obj==1):
                histo.GetYaxis().SetTitle("CSC Trigger Primitive Efficiency")
            if (obj==2):
                histo.GetYaxis().SetTitle("CSC Segment Reconstruction Efficiency")
            print "   ========> st_= ",st_ ," color= ",color
            histo.Draw("ap")
        else:
            print "   ========> st_= ",st_ ," color= ",color
            histo.Draw("samep")
    c1.cd()
    leg.Draw()
    cms_label.Draw()
    file_out.cd()
    c1.SaveAs("%s.pdf"%(Prefix))
    c1.SaveAs("%s.root"%(Prefix))
    c1.SaveAs("%s.C"%(Prefix))
    print "save eff plot: %s.*"%Prefix
    color=0
    for st_ in ("12+13","11B","11A"): 
        color+=1
        if (color==3 or color==5):
           color+=1
        variable=""
        print "st: %s, obj: %s"%(st_,obj)

	try:
            if (obj==1):
                histo=file_in.Get("ME%slct_effV"%st_)
            if (obj==2):
                histo=file_in.Get("ME%sseg_effV"%st_)
            print " found %s"%st_
        except:
	    print "not found %s"%st_
            continue

        print " plotting %s"%st_
        if (obj==1):
            histo=file_in.Get("ME%slct_effV"%st_)
        if (obj==2):
            histo=file_in.Get("ME%sseg_effV"%st_)
        c2.cd()
        histo.SetLineColor(color)
        histo.SetMarkerSize(0.5)
        histo.SetMarkerColor(color)
        leg_ME1.AddEntry(histo,"ME%s"%st_,"lp")
        if (color==1):
            histo.SetTitle(";%s;efficiency"%variable);
            histo.SetMinimum(0.6) 
            histo.GetYaxis().SetRangeUser(0.6,1.05)
            histo.GetXaxis().SetTitle(X_axis)
            histo.GetYaxis().SetTitleOffset(1.6)
            histo.GetXaxis().SetTitleOffset(1.4)
            if (obj==1):
                histo.GetYaxis().SetTitle("CSC Trigger Primitive Efficiency")
            if (obj==2):
                histo.GetYaxis().SetTitle("CSC Segment Reconstruction Efficiency")
            histo.Draw("ap")
            print "   ========> st_= ",st_ ," color= ",color
        else:
            print "   ========> st_= ",st_ ," color= ",color
            histo.Draw("samep")
         
    c2.cd()
    leg_ME1.Draw()
    cms_label.Draw()
    file_out.cd()
    c2.Write("%s%s_ME1.root"%(Prefix,"_canvas"))
    c2.SaveAs("%s_ME1.pdf"%(Prefix))
    c2.SaveAs("%s_ME1.root"%(Prefix))
    c2.SaveAs("%s_ME1.C"%(Prefix))
    print "save eff plot st1: %s_ME1.*"%Prefix
