from dask import delayed

from htt_plot.datasets.gael_all import *
from htt_plot.tools.cut import Cut
from htt_plot.cuts.mt import *
from htt_plot.tools.plot import build_component, build_components, merge_components, scale_component
from htt_plot.cuts.generic import *
from htt_plot.cuts.mt import cuts_mt
from htt_plot.cuts.tt_triggers import triggers


from htt_plot.tools.plotting.plotter import Plotter
from htt_plot.tools.plotting.tdrstyle import setTDRStyle
setTDRStyle(square=False)


import copy

output_dir = 'plots_1912_tt'
variables = ['mt_tot']
from htt_plot.binning import bins

## MC
fake_components_MC_1 = build_components(['fakesMC1'], 
                                     mc_datasets,
                                     variables, l1_FakeFactorApplication_Region_genuinetauMC, bins)
fake_components_MC_2 = build_components(['fakesMC2'], 
                                     mc_datasets,
                                     variables, l2_FakeFactorApplication_Region_genuinetauMC, bins)


MC_components = build_components(['WJetsToLNu','WJetsToLNu_ext',
                                  'WW','WZ',
                                  'ZZTo4L','ZZTo4L_ext','ZZTo2L2Nu','ZZTo2L2Q',
                                  'TBar_tch','TBar_tWch','T_tch','T_tWch'], 
                                 mc_datasets,
                                 variables, signal_region_MC_nofakes, bins)

TT = build_components(['TTHad_pow','TTLep_pow','TTSemi_pow'], 
                      TT_datasets,
                      variables, signal_region_MC_nofakes_TT, bins)

DY = build_components(['DYJetsToLL_M50','DYJetsToLL_M50_ext'],#,
                       # 'DY1JetsToLL_M50','DY1JetsToLL_M50_ext',
                       # 'DY2JetsToLL_M50','DY2JetsToLL_M50_ext',
                       # 'DY3JetsToLL_M50','DY3JetsToLL_M50_ext',
                       # 'DY4JetsToLL_M50'],
                      [DYJetsToLL_M50,DYJetsToLL_M50_ext],#,
                       # DY1JetsToLL_M50,DY1JetsToLL_M50_ext,
                       # DY2JetsToLL_M50,DY2JetsToLL_M50_ext,
                       # DY3JetsToLL_M50,DY3JetsToLL_M50_ext,
                       # DY4JetsToLL_M50],
                      variables, signal_region_MC_nofakes_DY, bins)

MC_components.extend(DY)
MC_components.extend(TT)

### Merging components
TTBar = []
singleTop = []
DY = []
WJ = []
Diboson = []
for component in MC_components:
    if component.name in ['TTHad_pow','TTLep_pow','TTSemi_pow']:
        TTBar.append(component)
    elif component.name in ['TBar_tch','TBar_tWch','T_tch','T_tWch']:
        singleTop.append(component)
    elif component.name in ['DYJetsToLL_M50','DYJetsToLL_M50_ext','DY1JetsToLL_M50','DY1JetsToLL_M50_ext','DY2JetsToLL_M50','DY2JetsToLL_M50_ext','DY3JetsToLL_M50','DY3JetsToLL_M50_ext','DY4JetsToLL_M50']:
        DY.append(component)
    elif component.name in ['WJetsToLNu','WJetsToLNu_ext']:
        WJ.append(component)
    elif component.name in ['WW','WZ','ZZTo4L','ZZTo4L_ext','ZZTo2L2Nu','ZZTo2L2Q']:
        Diboson.append(component)
    else:
        print component.name, component
        import pdb;pdb.set_trace()

TTBar = merge_components('TTBar',TTBar)
singleTop = merge_components('singleTop',singleTop)
DY = merge_components('DY',DY)
WJ = merge_components('WJ',WJ)
Diboson = merge_components('Diboson',Diboson)

MC_components = [TTBar,DY,singleTop,Diboson,WJ]

#### data

data_components = build_components(['data'],[data_datasets],variables,signal_region, bins)

#### Embedded

Embedded_components = build_components(['Embedded'],[Embedded_datasets],variables,signal_region_Embedded, bins)# embedded signal region

fake_component_Embedded_1 = build_components(['fakesEmbedded1'],[Embedded_datasets],variables,l1_FakeFactorApplication_Region_genuinetauMC_Embedded, bins)# embedded signal region
fake_component_Embedded_2 = build_components(['fakesEmbedded2'],[Embedded_datasets],variables,l2_FakeFactorApplication_Region_genuinetauMC_Embedded, bins)# embedded signal region

#### fakes

fake_components_1 = build_components(['fakesB1','fakesC1','fakesD1','fakesE1','fakesF1'], 
                                     data_datasets,
                                     variables, l1_FakeFactorApplication_Region, bins)
fake_components_2 = build_components(['fakesB2','fakesC2','fakesD2','fakesE2','fakesF2'], 
                                     data_datasets,
                                     variables, l2_FakeFactorApplication_Region, bins)

for component in fake_components_MC_1+fake_components_MC_2+fake_component_Embedded_1+fake_component_Embedded_2:
    for var in variables:
        component.histogram[var].Scale(-1.)

fakes = merge_components('fakes',fake_components_1+fake_components_2+fake_component_Embedded_1+fake_component_Embedded_2+fake_components_MC_1+fake_components_MC_2)

from ROOT import TFile

ftest = TFile('test.root','recreate')

fakes.histogram[variables[0]].SetName('jetFakes')
fakes.histogram[variables[0]].SetTitle('jetFakes')
fakes.histogram[variables[0]].Write()

Embedded_components[0].histogram[variables[0]].SetName('EMB')
Embedded_components[0].histogram[variables[0]].SetTitle('EMB')
Embedded_components[0].histogram[variables[0]].Write()

DY.histogram[variables[0]].SetName('ZL')
DY.histogram[variables[0]].SetTitle('ZL')
DY.histogram[variables[0]].Write()

VVL = merge_components('VVL',[singleTop,Diboson])
VVL.histogram[variables[0]].SetName('VVL')
VVL.histogram[variables[0]].SetTitle('VVL')
VVL.histogram[variables[0]].Write()

W = WJ
W.histogram[variables[0]].SetName('W')
W.histogram[variables[0]].SetTitle('W')
W.histogram[variables[0]].Write()

TTL = merge_components('TTL',[TTBar])
TTL.histogram[variables[0]].SetName('TTL')
TTL.histogram[variables[0]].SetTitle('TTL')
TTL.histogram[variables[0]].Write()

data_obs = data_components[0]
data_obs.histogram[variables[0]].SetName('data_obs')
data_obs.histogram[variables[0]].SetTitle('data_obs')
data_obs.histogram[variables[0]].Write()
