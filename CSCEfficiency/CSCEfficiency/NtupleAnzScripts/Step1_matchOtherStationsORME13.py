#!/usr/bin/python
#Author: Jinzhong Zhang(zhangjin@cern.ch), Northeastern University, Boston, U.S.A
#Usage: python Step1.py haddedrootfile.root (Classify the Ntuple file and do the tagandprobe fit)

from  ROOT import *
from  numpy import *
from Config import *

import sys,os,subprocess
if (sys.argv[0] == "python"): args=sys.argv[2:]
else: args=sys.argv[1:]

DenominatorRequire_ExtraStation="( ( (CSCDxyTTSeg#1<5. || CSCDxyTTSeg#1<5*CSCDxyErrTTSeg#1) && CSCDxyTTSeg#1>0.) || ((CSCDxyTTSeg#2<5. || CSCDxyTTSeg#2<5*CSCDxyErrTTSeg#2) && CSCDxyTTSeg#2>0.) || ((CSCDxyTTSeg#3<5. || CSCDxyTTSeg#3<5*CSCDxyErrTTSeg#3) && CSCDxyTTSeg#3>0.) ) "
DenominatorRequire_ExtraStation1="( ( (CSCDxyTTSeg#1<5. || CSCDxyTTSeg#1<5*CSCDxyErrTTSeg#1) && CSCDxyTTSeg#1>0.) || ((CSCDxyTTSeg#2<5. || CSCDxyTTSeg#2<5*CSCDxyErrTTSeg#2) && CSCDxyTTSeg#2>0.) || ((CSCDxyTTSeg#3<5. || CSCDxyTTSeg#3<5*CSCDxyErrTTSeg#3) && CSCDxyTTSeg#3>0.) || CSCRg1==3 ) "#for segment efficiency, without closest to LCT requirement


if len(args)<1:
  print "Usage: python Step1.py haddedrootfile.root (Classify the Ntuple file and do the tagandprobe fit)"
  sys.exit()

def CalculateOverallScaleNum(tree_):
  overall=0.
  for n in range(tree_.GetEntries()):
    tree_.GetEntry(n)
    overall+=tree_.mcweight*puweight[int(tree_.numberOfPUVerticesMixingTruth)]
  return tree_.GetEntries()/overall

file_in = TFile.Open(args[0],"read")
file_dummy = TFile.Open(TemporaryOutputFile,"RECREATE")
print 'apply cut dummy: ',MuTrackPairCut
tree_in_dummy = file_in.Get(TreeName).CopyTree( MuTrackPairCut )
tree_in=tree_in_dummy.CloneTree(0)

if RunOnMC:
  puweight=Getpuweight(DataPileupRootFileName,pileup_mc)
  overallweight=CalculateOverallScaleNum(tree_in_dummy)
else:
  overallweight=1.

segSelect=[""]*4
lctSelect=[""]*4

#add branch abseta, shiftedphi, and weight
print "Now adding:\n abseta,\n weight",
abseta = zeros(1, dtype=float)
absetaBranch = tree_in.Branch('abseta',abseta, 'abseta/D')
shiftedphi = zeros(1, dtype=float)
shiftedphiBranch = tree_in.Branch('shiftedphi',shiftedphi, 'shiftedphi/D')
weight = zeros(1, dtype=float)
weightBranch = tree_in.Branch('weight',weight, 'weight/D')
if RunOnMC:
  #add branch mcTrue for MC
  print ",\n mcTrue:"
  MCTruth_=ConvertCLogicalExp(MCTruth).replace("MuTag"," tree_in_dummy.MuTag").replace(" track"," tree_in_dummy.track")
  print "\t MC truth criteria: \n",MCTruth_,","
  mcTrue = zeros(1, dtype=int)
  mcTrueBranch = tree_in.Branch('mcTrue',mcTrue, 'mcTrue/I')
else:
  print "(=1),"

#add branch LCT and SEG determinant
for st_ in (0,1,2,3,4):
  if st_:
    segSelect[st_-1] = ConvertCLogicalExp(ProbeSegment).replace("CSC","tree_in_dummy.CSC").replace("#",str(st_))
    lctSelect[st_-1] = ConvertCLogicalExp(ProbeLCT).replace("CSC","tree_in_dummy.CSC").replace("#",str(st_))
  if "Stations" not in Group and "Chambers" not in Group:
    if st_:
      continue
  elif st_==0:
    continue
  exec( "foundSEGSt%d = zeros(1, dtype=int)"%(st_) )
  exec( "foundLCTSt%d = zeros(1, dtype=int)"%(st_) )
  exec( "segBranch%d = tree_in.Branch('foundSEGSt%d',foundSEGSt%d, 'foundSEGSt%d/I' )"%(st_,st_,st_,st_) )
  exec( "lctBranch%d = tree_in.Branch('foundLCTSt%d',foundLCTSt%d, 'foundLCTSt%d/I' )"%(st_,st_,st_,st_) )
print " foundSEGSt1-4 (seg probe),\n foundLCTSt1-4 (lct probe)"
print "to the tree.\n\nPlease wait about half to more than one hours......\n"
print "segment selection criteria: \n",segSelect
print "local charged trigger selection criteria: \n",lctSelect

#loop over entries and fill
for n in range(tree_in_dummy.GetEntries()):
  tree_in_dummy.GetEntry(n)
  abseta[0] = abs(tree_in_dummy.tracks_eta)
  shiftedphi[0] = tree_in_dummy.tracks_phi if tree_in_dummy.tracks_phi<6.1959188464 else tree_in_dummy.tracks_phi-6.28318530718
  if RunOnMC:
    weight[0] = tree_in_dummy.mcweight*puweight[int(tree_in_dummy.numberOfPUVerticesMixingTruth)]*sampleweight
    exec ( "mcTrue[0] = 1 if %s else 0"%(MCTruth_) )
  else:
    weight[0] = 1.
  if "Stations" not in Group and "Chambers" not in Group:
    exec( "foundSEGSt0[0] = 1 if %s else 0"%(segSelect[0]+" or "+segSelect[1]+" or "+segSelect[2]+" or "+segSelect[3]) )
    exec( "foundLCTSt0[0] = 1 if %s else 0"%(lctSelect[0]+" or "+lctSelect[1]+" or "+lctSelect[2]+" or "+lctSelect[3]) )
  else:
    for st_ in (1,2,3,4):
      exec( "foundSEGSt%d[0] = 1 if %s else 0"%(st_,segSelect[st_-1]) )
      exec( "foundLCTSt%d[0] = 1 if %s else 0"%(st_,lctSelect[st_-1]) )
  tree_in.Fill()

def Fit(filename_,st_):
  if os.path.isfile(filename_):
    print "  ---> run TnP: nohup cmsRun TagandProbe.py %s %d &"%(filename_,st_)
    cmd="nohup cmsRun TagandProbe.py %s %d &"%(filename_,st_)
    subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    os.system("sleep 1")
    status = subprocess.Popen(["ps -f|grep -v 'grep'|grep '%s'"%(cmd[6:-2])], shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read()
    if status:
      print "\033[92m",status,"\033[0m"
    else:
      print "\033[91mThe job for",filename_,"is NOT running. Memory or disk full?\033[0m"
  else:
    print "\033[91m",filename_," does not exist.\033[0m"
    
def SaveandFit(tree_,cut_,filename_,st_):
  print ' numerator cut: ',cut_
  outputfile=TFile.Open(filename_,'RECREATE')
  outputdir=outputfile.mkdir("Probes")
  outputdir.cd()
  print '   -> apply cut: ', cut_
  tree_out=tree_in.CopyTree(cut_)
  if tree_out.GetEntries() > 0:
    tree_out.AutoSave()
    print "Output to ", filename_
    outputfile.Close()
    Fit(filename_,st_)
  else:
    print "No muon is expected to pass",filename_+"."
    outputfile.Close()
    os.system( "rm "+filename_ )
    return

#Save to files according to the classification criteria
if "Stations" in Group:
  for st in range(1,n_stations+1):
    other_stations=[1,2,3,4]

#    if st<4:
    if st<6:
       other_stations.remove(1)
    else:
       other_stations.remove(st-4)

#       other_stations.remove(st-2)
    print "-----> remaining stations: ",other_stations
    print " station: ", st
#    if st==3:
    if st==4 or st==5:
   	print "   selection: ",stations[st][0]+"&&"+DenominatorRequire.replace("#",str(stations[st][3]))+"&&"+DenominatorRequire_ExtraStation1.replace("#1",str(other_stations[0])).replace("#2",str(other_stations[1])).replace("#3",str(other_stations[2]))
    else:
        print "   selection: ",stations[st][0]+"&&"+DenominatorRequire.replace("#",str(stations[st][3]))+"&&"+DenominatorRequire_ExtraStation.replace("#1",str(other_stations[0])).replace("#2",str(other_stations[1])).replace("#3",str(other_stations[2]))
#    if st==3:
    if st==4 or st==5:

	SaveandFit( tree_in,stations[st][0]+"&&"+DenominatorRequire.replace("#",str(stations[st][3]))+"&&"+DenominatorRequire_ExtraStation1.replace("#1",str(other_stations[0])).replace("#2",str(other_stations[1])).replace("#3",str(other_stations[2])),TemporaryOutputFile[:-5]+stations[st][1]+'.root',stations[st][3] )
    else:
        SaveandFit( tree_in,stations[st][0]+"&&"+DenominatorRequire.replace("#",str(stations[st][3]))+"&&"+DenominatorRequire_ExtraStation.replace("#1",str(other_stations[0])).replace("#2",str(other_stations[1])).replace("#3",str(other_stations[2])),TemporaryOutputFile[:-5]+stations[st][1]+'.root',stations[st][3] )

 
elif "Chambers" in Group:
  for idx in range(n_chambers):
    ec=chambers[idx][2] is '+'
    st=int(chambers[idx][3])
    rg=int(chambers[idx][5])
    ch=int(chambers[idx][7:])
    other_stations=[1,2,3,4]
    other_stations.remove(st)
    if st==1:
      print "      selection: ","%sCSCEndCapPlus && CSCRg%s==%s && CSCCh%s==%s &&"%("" if (ec) else '!',st,rg,st,ch)+DenominatorRequire.replace("#",str(st))+"&&"+DenominatorRequire_ExtraStation1.replace("#1",str(other_stations[0])).replace("#2",str(other_stations[1])).replace("#3",str(other_stations[2]))
      SaveandFit( tree_in,"%sCSCEndCapPlus && CSCRg%s==%s && CSCCh%s==%s &&"%("" if (ec) else '!',st,rg,st,ch)+DenominatorRequire.replace("#",str(st))+"&&"+DenominatorRequire_ExtraStation1.replace("#1",str(other_stations[0])).replace("#2",str(other_stations[1])).replace("#3",str(other_stations[2])),TemporaryOutputFile[:-5]+chambers[idx]+'.root',st )
    else:
      print "      selection: ","%sCSCEndCapPlus && CSCRg%s==%s && CSCCh%s==%s &&"%("" if (ec) else '!',st,rg,st,ch)+DenominatorRequire.replace("#",str(st))+"&&"+DenominatorRequire_ExtraStation.replace("#1",str(other_stations[0])).replace("#2",str(other_stations[1])).replace("#3",str(other_stations[2]))
      SaveandFit( tree_in,"%sCSCEndCapPlus && CSCRg%s==%s && CSCCh%s==%s &&"%("" if (ec) else '!',st,rg,st,ch)+DenominatorRequire.replace("#",str(st))+"&&"+DenominatorRequire_ExtraStation.replace("#1",str(other_stations[0])).replace("#2",str(other_stations[1])).replace("#3",str(other_stations[2])),TemporaryOutputFile[:-5]+chambers[idx]+'.root',st )

else:
  Denominator=""
  for st_ in (1,2,3,4):
    other_stations=[1,2,3,4]
    other_stations.remove(st_)
    Denominator+=DenominatorRequire.replace("#",str(st_))+"&&"+DenominatorRequire_ExtraStation.replace("#1",str(other_stations[0])).replace("#2",str(other_stations[1])).replace("#3",str(other_stations[2]))
    if st_<4:
      Denominator+="||"
  print "   secetion::::: "
  SaveandFit( tree_in,Denominator,TemporaryOutputFile[:-5]+"AllStations.root",0 )

#close files
file_dummy.Close()
file_in.Close()
#os.system( "rm "+TemporaryOutputFile )
