# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: RECO -s RAW2DIGI,L1Reco,RECO,ALCA:TkAlMuonIsolated,EI,PAT,DQM:@allForPrompt --runUnscheduled --nThreads 4 --data --era Run2_2017 --scenario pp --conditions 92X_dataRun2_July6ReReco_PixelCommissioning_v2 --eventcontent RECO,AOD,MINIAOD,DQM --datatier RECO,AOD,MINIAOD,DQMIO --customise Configuration/DataProcessing/RecoTLR.customisePostEra_Run2_2017 --filein file:pippo.root -n 100 --python_filename=recoskim_Run2017B_SingleMuon.py --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO',eras.Run2_2017)
HLTProcessName='HLT'

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.AlCaRecoStreams_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.PAT_cff')
process.load('DQMOffline.Configuration.DQMOffline_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from RecoMuon.TrackingTools.MuonSegmentMatcher_cff import *
process.load("TrackingTools.TrackAssociator.DetIdAssociatorESProducer_cff")
from TrackingTools.TrackAssociator.default_cfi import *
from RecoMuon.MuonIsolationProducers.trackExtractorBlocks_cff import MIsoTrackExtractorBlock

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('file:pippo.root'),
    fileNames = cms.untracked.vstring($inputFileNames),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('RECO nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)


process.MuonSegmentMatcher = cms.PSet(
    MatchParameters = cms.PSet(
        CSCsegments = cms.InputTag("cscSegments"),
        DTradius = cms.double(0.01),
        DTsegments = cms.InputTag("dt4DSegments"),
        RPChits = cms.InputTag("rpcRecHits"),
        TightMatchCSC = cms.bool(True),
        TightMatchDT = cms.bool(False)
    )
)

# Output definition

process.RECOoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RECO'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('RECO_RAW2DIGI_L1Reco_RECO_ALCA_EI_PAT_DQM.root'),
    outputCommands = process.RECOEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

process.AODoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('AOD'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fileName = cms.untracked.string('RECO_RAW2DIGI_L1Reco_RECO_ALCA_EI_PAT_DQM_inAOD.root'),
    outputCommands = process.AODEventContent.outputCommands
)

process.MINIAODoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('MINIAOD'),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('RECO_RAW2DIGI_L1Reco_RECO_ALCA_EI_PAT_DQM_inMINIAOD.root'),
    outputCommands = process.MINIAODEventContent.outputCommands,
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('RECO_RAW2DIGI_L1Reco_RECO_ALCA_EI_PAT_DQM_inDQM.root'),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition
process.ALCARECOStreamTkAlMuonIsolated = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('pathALCARECOTkAlMuonIsolated')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('ALCARECO'),
        filterName = cms.untracked.string('TkAlMuonIsolated')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('TkAlMuonIsolated.root'),
    outputCommands = cms.untracked.vstring('drop *', 
        'keep *_ALCARECOTkAlMuonIsolated_*_*', 
        'keep L1AcceptBunchCrossings_*_*_*', 
        'keep L1GlobalTriggerReadoutRecord_gtDigis_*_*', 
        'keep *_TriggerResults_*_*', 
        'keep DcsStatuss_scalersRawToDigi_*_*', 
        'keep *_offlinePrimaryVertices_*_*')
)

# Other statements
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOTkAlMuonIsolated_noDrop.outputCommands)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_July6ReReco_PixelCommissioning_v2', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.eventinterpretaion_step = cms.Path(process.EIsequence)
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_HcalStripHaloFilter = cms.Path(process.HcalStripHaloFilter)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_globalSuperTightHalo2016Filter = cms.Path(process.globalSuperTightHalo2016Filter)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_chargedHadronTrackResolutionFilter = cms.Path(process.chargedHadronTrackResolutionFilter)
process.Flag_globalTightHalo2016Filter = cms.Path(process.globalTightHalo2016Filter)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_BadChargedCandidateSummer16Filter = cms.Path(process.BadChargedCandidateSummer16Filter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_BadPFMuonFilter = cms.Path(process.BadPFMuonFilter)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_BadChargedCandidateFilter = cms.Path(process.BadChargedCandidateFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_BadPFMuonSummer16Filter = cms.Path(process.BadPFMuonSummer16Filter)
process.Flag_muonBadTrackFilter = cms.Path(process.muonBadTrackFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
process.dqmoffline_step = cms.EndPath(process.DQMOfflineCommon)
process.dqmoffline_1_step = cms.EndPath(process.DQMOfflineMuon)
process.dqmoffline_2_step = cms.EndPath(process.DQMOfflineHcal)
process.dqmoffline_3_step = cms.EndPath(process.DQMOfflineJetMET)
process.dqmoffline_4_step = cms.EndPath(process.DQMOfflineEcal)
process.dqmofflineOnPAT_step = cms.EndPath(process.PostDQMOffline)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)
process.AODoutput_step = cms.EndPath(process.AODoutput)
process.MINIAODoutput_step = cms.EndPath(process.MINIAODoutput)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)
process.ALCARECOStreamTkAlMuonIsolatedOutPath = cms.EndPath(process.ALCARECOStreamTkAlMuonIsolated)

process.aodDump = cms.EDAnalyzer('TPTrackMuonSys',
#                                 TrackAssociatorParameterBlock,
                                 MuonSegmentMatcher,
                                 TrackExtractor=cms.PSet(MIsoTrackExtractorBlock),
                                 rootFileName   = cms.untracked.string('CSCPFG_Ineff_DATA_test_1.root'),
                                 CSCUseTimingCorrections = cms.bool( True ),
                                 CSCUseGasGainCorrections = cms.bool( True ),
                                 isMC            = cms.untracked.bool(False),
                                 mcTag           = cms.untracked.InputTag('genParticles'),
                                 vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                 gTracksTag      = cms.untracked.InputTag('generalTracks'),
                                 trackProducer   = cms.InputTag('csctfunpacker:'),
                                 readBadChannels = cms.bool(True),
                                 readBadChambers = cms.bool(True),
                                 hltTag      = cms.untracked.InputTag("TriggerResults","",HLTProcessName),
                                 hltEvTag    = cms.untracked.InputTag("hltTriggerSummaryAOD","",HLTProcessName),
                                 HLTMuTrgNames =  cms.vstring("HLT_Mu?_v*","HLT_Mu??_v*","HLT_Mu???_v*","HLT_IsoMu?_v*","HLT_IsoMu??_v*","HLT_IsoMu???_v*","HLT_L2Mu?_v*","HLT_L2Mu??_v*","HLT_L2Mu???_v*","HLT_SingleMu*","HLT_L1SingleMu*","HLT_IsoTkMu??_v*","HLT_TkMu??_v*"),
                                 HLTDiMuTrgName =  cms.string("HLT_DoubleMu?_v*"),
                                 #                      hltEvTag    = cms.untracked.InputTag("hltTriggerSummaryAOD","","REDIGI36X"),
                                 L1extraTag   = cms.untracked.InputTag("l1extraParticles"),
                                 dedxTag         =  cms.untracked.InputTag('dedxHarmonic2'),
                                 scalersResults = cms.InputTag("scalersRawToDigi","","RECO")
                                 )


process.outputstep = cms.EndPath(process.aodDump)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.pathALCARECOTkAlMuonIsolated,process.eventinterpretaion_step,process.Flag_HBHENoiseFilter,process.Flag_HBHENoiseIsoFilter,process.Flag_CSCTightHaloFilter,process.Flag_CSCTightHaloTrkMuUnvetoFilter,process.Flag_CSCTightHalo2015Filter,process.Flag_globalTightHalo2016Filter,process.Flag_globalSuperTightHalo2016Filter,process.Flag_HcalStripHaloFilter,process.Flag_hcalLaserEventFilter,process.Flag_EcalDeadCellTriggerPrimitiveFilter,process.Flag_EcalDeadCellBoundaryEnergyFilter,process.Flag_goodVertices,process.Flag_eeBadScFilter,process.Flag_ecalLaserCorrFilter,process.Flag_trkPOGFilters,process.Flag_chargedHadronTrackResolutionFilter,process.Flag_muonBadTrackFilter,process.Flag_BadChargedCandidateFilter,process.Flag_BadPFMuonFilter,process.Flag_BadChargedCandidateSummer16Filter,process.Flag_BadPFMuonSummer16Filter,process.Flag_trkPOG_manystripclus53X,process.Flag_trkPOG_toomanystripclus53X,process.Flag_trkPOG_logErrorTooManyClusters,process.Flag_METFilters,process.dqmoffline_step,process.dqmoffline_1_step,process.dqmoffline_2_step,process.dqmoffline_3_step,process.dqmoffline_4_step,process.outputstep)
process.schedule.associate(process.patTask)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(4)
process.options.numberOfStreams=cms.untracked.uint32(0)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.RecoTLR
from Configuration.DataProcessing.RecoTLR import customisePostEra_Run2_2017 

#call to customisation function customisePostEra_Run2_2017 imported from Configuration.DataProcessing.RecoTLR
process = customisePostEra_Run2_2017(process)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllData 

#call to customisation function miniAOD_customizeAllData imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllData(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

