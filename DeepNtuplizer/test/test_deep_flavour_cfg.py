import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask

process = cms.Process("PATtest")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring()
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_forppRef5TeV')
#process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
#process.GlobalTag.toGet.extend([
#    cms.PSet(record = cms.string("BTagTrackProbability3DRcd"),
#             tag = cms.string("JPcalib_MC103X_2018PbPb_v4"),                                                                                                                                      connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
             
#         )
#])

process.load("Configuration.StandardSequences.MagneticField_cff")

## Output Module Configuration (expects a path 'p')
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('patTuple.root'),
                               ## save only events passing the full path
                               #SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               ## save PAT output; you need a '*' to unpack the list of commands
                               ## 'patEventContent'
                               outputCommands = cms.untracked.vstring('drop *', *patEventContentNoCleaning )
                               )

patAlgosToolsTask = getPatAlgosToolsTask(process)
#process.load("DeepNTuples.DeepNtuplizer.candidateBtaggingMiniAOD_cff")
#process.p = cms.Path(process.candidateBtagging)
process.outpath = cms.EndPath(process.out, patAlgosToolsTask)

## and add them to the event content
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

bTagInfos = [
        'pfImpactParameterTagInfos',
        'pfInclusiveSecondaryVertexFinderTagInfos',
        'pfSecondaryVertexTagInfos',
        'pfDeepCSVTagInfos',
]

updateJetCollection(
   process,
   labelName = "DeepFlavour",
   jetSource = cms.InputTag('slimmedJets'),
        pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
        svSource = cms.InputTag('slimmedSecondaryVertices'),#,'','PATf'),
   jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
   #btagInfos = bTagInfos,
   btagDiscriminators = [
      'pfJetProbabilityBJetTags',
      'pfCombinedInclusiveSecondaryVertexV2BJetTags',
      'pfCombinedSecondaryVertexV2BJetTags',
      'pfDeepCSVJetTags:probudsg', 
      'pfDeepCSVJetTags:probb', 
      'pfDeepCSVJetTags:probc', 
      'pfDeepCSVJetTags:probbb', 
       #'pfDeepCSVJetTags:probcc'      
   ]
   )

if hasattr(process,'updatedPatJetsTransientCorrectedDeepFlavour'):
        print 'exei!!'
        process.updatedPatJetsTransientCorrectedDeepFlavour.addTagInfos = cms.bool(True)
        process.updatedPatJetsTransientCorrectedDeepFlavour.addBTagInfo = cms.bool(True)

from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValTTbarPileUpMINIAODSIM

process.source.fileNames = filesRelValTTbarPileUpMINIAODSIM
process.source.fileNames = cms.untracked.vstring('/store/himc/RunIIpp5Spring18MiniAOD/QCD_Pt-20toInf_MuEnrichedPt15_TuneCP5_5p02TeV_pythia8/MINIAODSIM/94X_mc2017_realistic_forppRef5TeV-v1/60000/228DD92E-51C1-E811-A3FB-E0071B7AC770.root')


#Setup FWK for multithreaded                                                                                                                                                                                
process.options.numberOfThreads=cms.untracked.uint32(8)
process.options.numberOfStreams=cms.untracked.uint32(0)

from Configuration.EventContent.EventContent_cff import MINIAODSIMEventContent
process.out.outputCommands = MINIAODSIMEventContent.outputCommands
process.out.outputCommands.append('keep *_selectedUpdatedPatJets*_*_*')
#process.out.outputCommands.append('keep *_offlineSlimmedPrimaryVerticesRecovery*_*_*')
process.out.outputCommands.append('keep *_centrality*_*_*')
process.out.outputCommands.append('keep *_slimmedSecondaryVertices*_*_*')
process.out.outputCommands.append('keep *_packedPFCandidates*_*_*')
process.out.outputCommands.append('keep *_pfDeepCSVTagInfos*_*_*')
process.out.outputCommands.append('keep *_pfDeepFlavourTagInfos*_*_*')
process.out.outputCommands.append('keep *_pfDeepFlavourJetTags*_*_*')
process.out.outputCommands.append('keep *_updatedPatJets*_*_*')

process.out.fileName = 'test_deep_flavour_MINIAODSIM.root'

#                                         ##
#   process.options.wantSummary = False   ##  (to suppress the long output at the end of the job)
# process.add_(cms.Service("InitRootHandlers", DebugLevel =cms.untracked.int32(3)))
