from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
#section general
config.General.requestName = 'LCTeffAan_Run2018A_ZMu_306926_20180724'
config.General.workArea = 'LCTeffAna_crab_Run2018A_ZMu'#working dir 
config.General.transferOutputs = True
config.General.transferLogs = True

#section JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'test.py'
config.JobType.maxMemoryMB = 2000
config.JobType.maxJobRuntimeMin = 1440 # 1440min = 24hours
config.JobType.numCores = 1
config.JobType.allowUndistributedCMSSW = True
#config.JobType.generator
#config.JobType.pyCfgParams
#config.JobType.inputFiles


#section Data
#config.Data.inputDataset = '/SLHC23_patch1_2023Muon_gen_sim_Pt2_50_1M/tahuang-SLHC25_patch1_2023Muon_1M_L1_PU0_Pt2_50_updategemeta-1bf93df4dfbb43dc918bd6e47dedbf79/USER'
#config.Data.inputDataset = '/SingleMuon/Run2016G-v1/RAW'
#config.Data.inputDataset = '/SingleMuon/Run2016H-v1/RAW'
#config.Data.inputDataset = '/SingleMuon/Run2017H-v1/RAW'
config.Data.inputDataset = '/SingleMuon/Run2018A-ZMu-PromptReco-v1/RAW-RECO'
#config.Data.splitting = 'FileBased'
#config.Data.splitting = 'LumiBased'
config.Data.splitting = 'Automatic'
config.Data.inputDBS = 'global'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/tahuang/'
config.Data.publication = True
#import FWCore.PythonUtilities.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = 'goodList.json').getVLuminosityBlockRange()
config.Data.runRange = '315257-315270'#'278820-278820' # '193093-194075'
config.Data.outputDatasetTag = config.General.requestName
config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.ignoreGlobalBlacklist = True
#config.Site.whitelist = ["T0_CH_CERN_MSS"]
