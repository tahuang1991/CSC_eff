import FWCore.ParameterSet.Config as cms

process = cms.Process("dumpLHE")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/hdfs/store/user/senka/MG5_WZ13TeV_v242/MGNLO_aTGC/step2_MG242_pythia8FxFx_part1.root')
)

process.dummy = cms.EDAnalyzer("DummyLHEAnalyzer",
    src = cms.InputTag("source")
)

process.p = cms.Path(process.dummy)
