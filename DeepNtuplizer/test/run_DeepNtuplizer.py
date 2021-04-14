import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing
### parsing job options 
import sys

options = VarParsing.VarParsing()

options.register('inputScript','',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"input Script")
options.register('outputFile','output',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"output File (w/o .root)")
options.register('maxEvents',-1,VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.int,"maximum events")
options.register('skipEvents', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "skip N events")
options.register('job', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "job number")
options.register('nJobs', 1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "total jobs")
options.register('release','11_2_0', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"release number (w/o CMSSW)")

print("Using release "+options.release)


if hasattr(sys, "argv"):
    options.parseArguments()




process = cms.Process("DNNFiller")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.Services_cff')

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_mc_FULL', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

#Set GT by hand:                                                                                                                                            
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_mc_FULL','')#
'''
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')
process.load("Configuration.StandardSequences.MagneticField_cff")
'''
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.options = cms.untracked.PSet(
   allowUnscheduled = cms.untracked.bool(True),  
   wantSummary=cms.untracked.bool(False)
)

from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValTTbarPileUpMINIAODSIM

process.source = cms.Source('PoolSource',
    fileNames=cms.untracked.vstring (filesRelValTTbarPileUpMINIAODSIM),
)

if options.inputScript != '' and options.inputScript != 'DeepNTuples.DeepNtuplizer.samples.TEST':
    process.load(options.inputScript)

numberOfFiles = len(process.source.fileNames)
numberOfJobs = options.nJobs
jobNumber = options.job


process.source.fileNames = process.source.fileNames[jobNumber:numberOfFiles:numberOfJobs]
if options.nJobs > 1:
    print ("running over these files:")
    print (process.source.fileNames)
process.source.fileNames = ['file:/afs/cern.ch/work/m/mnguyen/public/deepCSV_hiMiniAOD_testFiles/bjet_hiMiniAOD_100evts.root']
process.source.fileNames = ['/store/mc/RunIISummer19UL18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v11_L1v1-v2/260000/00C28834-56C0-2343-B436-AA8521756E9E.root']
process.source.fileNames = ['file:/eos/cms/store/relval/CMSSW_10_6_14/RelValZprimeToTT_M2000_W600_13UP17/MINIAODSIM/PU25ns_106X_mc2017_realistic_v7_HS-v1/20000/7505AF8E-18E8-F343-8FDC-478FC0ADC8F9.root']
process.source.fileNames = ['file:/afs/cern.ch/work/g/gkrintir/private/DeepNTuple/CMSSW_11_2_0_pre8/src/test_deep_flavour_MINIAODSIM.root']
process.source.fileNames = ['/store/mc/RunIISummer19UL18MiniAOD/BcToJPsiMuNu_TuneCP5_13TeV-bcvegpy2-pythia8-evtgen/MINIAODSIM/106X_upgrade2018_realistic_v11_L1v1_ext1-v2/100000/15B49BB1-67C7-6D4E-BB05-BD1D27C94BD1.root']
process.source.fileNames = ['file:/afs/cern.ch/work/g/gkrintir/private/DeepNTuple/CMSSW_11_2_0_pre8/src/test_deep_flavour_MINIAODSIM.root']

process.source.skipEvents = cms.untracked.uint32(options.skipEvents)
process.maxEvents  = cms.untracked.PSet( 
    input = cms.untracked.int32 (options.maxEvents) 
)


if int(options.release.replace("_",""))>=840 :
 bTagInfos = [
        'pfImpactParameterTagInfos',
        'pfInclusiveSecondaryVertexFinderTagInfos',
        'pfDeepCSVTagInfos',
 ]
else :
 bTagInfos = [
        'pfImpactParameterTagInfos',
        'pfInclusiveSecondaryVertexFinderTagInfos',
        'deepNNTagInfos',
 ]


if int(options.release.replace("_",""))>=840 :
 bTagDiscriminators = [
     #'softPFMuonBJetTags',
     #'softPFElectronBJetTags',
     'pfJetBProbabilityBJetTags',
     'pfJetProbabilityBJetTags',
     'pfCombinedInclusiveSecondaryVertexV2BJetTags',
         'pfDeepCSVJetTags:probudsg', #to be fixed with new names
         'pfDeepCSVJetTags:probb',
         'pfDeepCSVJetTags:probc',
         'pfDeepCSVJetTags:probbb',
         'pfDeepCSVJetTags:probcc',
 ]
else :
  bTagDiscriminators = [
     'softPFMuonBJetTags',
     'softPFElectronBJetTags',
     'pfJetBProbabilityBJetTags',
     'pfJetProbabilityBJetTags',
     'pfCombinedInclusiveSecondaryVertexV2BJetTags',
         'deepFlavourJetTags:probudsg', #to be fixed with new names
         'deepFlavourJetTags:probb',
         'deepFlavourJetTags:probc',
         'deepFlavourJetTags:probbb',
         'deepFlavourJetTags:probcc',
 ]



jetCorrectionsAK4 = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')

'''
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
updateJetCollection(
        process,
        labelName = "DeepFlavour",
        jetSource = cms.InputTag('slimmedJets'),#'ak4Jets'
        jetCorrections = jetCorrectionsAK4,
        pfCandidates = cms.InputTag('packedPFCandidates'),
        pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
        svSource = cms.InputTag('slimmedSecondaryVertices'),
        muSource = cms.InputTag('slimmedMuons'),
        elSource = cms.InputTag('slimmedElectrons'),
        btagInfos = bTagInfos,
        btagDiscriminators = bTagDiscriminators,
        explicitJTA = False
)

if hasattr(process,'updatedPatJetsTransientCorrectedDeepFlavour'):
        print 'exei!!'
	process.updatedPatJetsTransientCorrectedDeepFlavour.addTagInfos = cms.bool(True) 
	process.updatedPatJetsTransientCorrectedDeepFlavour.addBTagInfo = cms.bool(True)
else:
	raise ValueError('I could not find updatedPatJetsTransientCorrectedDeepFlavour to embed the tagInfos, please check the cfg')
'''

# QGLikelihood
process.load("DeepNTuples.DeepNtuplizer.QGLikelihood_cfi")
process.es_prefer_jec = cms.ESPrefer("PoolDBESSource", "QGPoolDBESSource")
process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets   = cms.InputTag("slimmedJets")
process.QGTagger.jetsLabel = cms.string('QGL_AK4PFchs')


from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
process.ak4GenJetsWithNu = ak4GenJets.clone(src = 'packedGenParticles')
 
 ## Filter out neutrinos from packed GenParticles
process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"))
 ## Define GenJets
process.ak4GenJetsRecluster = ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNu')
 
 
process.patGenJetMatchWithNu = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
    src         = cms.InputTag("slimmedJets"),      # RECO jets (any View<Jet> is ok) 
    matched     = cms.InputTag("ak4GenJetsWithNu"),        # GEN jets  (must be GenJetCollection)              
    mcPdgId     = cms.vint32(),                      # n/a   
    mcStatus    = cms.vint32(),                      # n/a   
    checkCharge = cms.bool(False),                   # n/a   
    maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
    #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
    resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
    resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
)

process.patGenJetMatchRecluster = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
    src         = cms.InputTag("slimmedJets"),      # RECO jets (any View<Jet> is ok) 
    matched     = cms.InputTag("ak4GenJetsRecluster"),        # GEN jets  (must be GenJetCollection)              
    mcPdgId     = cms.vint32(),                      # n/a   
    mcStatus    = cms.vint32(),                      # n/a   
    checkCharge = cms.bool(False),                   # n/a   
    maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
    #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
    resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
    resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
)

process.genJetSequence = cms.Sequence(process.packedGenParticlesForJetsNoNu*process.ak4GenJetsWithNu*process.ak4GenJetsRecluster*process.patGenJetMatchWithNu*process.patGenJetMatchRecluster)
 

outFileName = options.outputFile + '_' + str(options.job) +  '.root'
print ('Using output file ' + outFileName)

process.TFileService = cms.Service("TFileService", 
                                   fileName = cms.string(outFileName))

# DeepNtuplizer
process.load("DeepNTuples.DeepNtuplizer.DeepNtuplizer_cfi")

process.deepntuplizer.jets = cms.InputTag('slimmedJets');
process.deepntuplizer.bDiscriminators = bTagDiscriminators 

if int(options.release.replace("_",""))>=840 :
   process.deepntuplizer.tagInfoName = cms.string('pfDeepCSV')

process.p = cms.Path(
    process.QGTagger + 
    process.genJetSequence*  
    process.deepntuplizer
)


