import htt_plot.channels_configs.tt as config

# dask tools
from dask import delayed, compute, visualize

# datasets
import htt_plot.datasets.gael_all as datasets

# output
output_dir = 'delayed_plots_'+config.channel

# binning
from htt_plot.binning import bins

# variables
variables = bins.keys()
variables = ['mt_tot'] # just for testing

# plotting tools
from htt_plot.tools.plotting.plotter import Plotter
from htt_plot.tools.plotting.tdrstyle import setTDRStyle
setTDRStyle(square=False)

# datacards tools
from htt_plot.tools.datacards import make_datacards

# cuts
from htt_plot.tools.cut import Cuts
cuts_against_leptons = Cuts(
    l1_againstleptons = 'l1_againstElectronVLooseMVA6 > 0.5 && l1_againstMuonLoose3 > 0.5',
    l2_againstleptons = 'l2_againstElectronVLooseMVA6 > 0.5 && l2_againstMuonLoose3 > 0.5',
)

basic_cuts = config.basic_cuts + cuts_against_leptons

signal_region_cut = basic_cuts.clone() # + cut_signal
tau_legs = ['l2']
if config.channel == 'tt':
    tau_legs.append('l1')
for leg in tau_legs:
    signal_region_cut += config.cuts_iso[leg+'_Tight']

signal_region_MC = signal_region_cut
signal_region_MC_nofakes = signal_region_MC + ~config.cut_l1_fakejet + ~config.cut_l2_fakejet
signal_region_MC_nofakes_DY = signal_region_MC_nofakes + config.cut_dy_promptfakeleptons
signal_region_MC_nofakes_TT = signal_region_MC_nofakes + config.cut_TT_nogenuine

l1_FakeFactorApplication_Region = basic_cuts + config.cuts_iso['l1_VLoose'] + ~config.cuts_iso['l1_Tight'] + config.cuts_iso['l2_Tight']
l1_FakeFactorApplication_Region_genuinetauMC = l1_FakeFactorApplication_Region + ~config.cut_l1_fakejet

l2_FakeFactorApplication_Region = basic_cuts + config.cuts_iso['l2_VLoose'] + ~config.cuts_iso['l2_Tight'] + config.cuts_iso['l1_Tight']
l2_FakeFactorApplication_Region_genuinetauMC = l2_FakeFactorApplication_Region + ~config.cut_l2_fakejet

#### cuts+weights

signal_region = signal_region_cut * config.weights['weight']
signal_region_Embedded = signal_region_cut * config.weights['weight'] * config.weights['embed']
signal_region_MC = signal_region_MC * config.weights['weight'] * config.weights['MC']
signal_region_MC_nofakes_DY = signal_region_MC_nofakes_DY * config.weights['weight'] * config.weights['MC'] * config.weights['DY'] 
signal_region_MC_nofakes_TT = signal_region_MC_nofakes_TT * config.weights['weight'] * config.weights['MC']
signal_region_MC_nofakes = signal_region_MC_nofakes * config.weights['weight'] * config.weights['MC']
l1_FakeFactorApplication_Region = l1_FakeFactorApplication_Region * config.weights['l1_fake']
l2_FakeFactorApplication_Region = l2_FakeFactorApplication_Region * config.weights['l2_fake']
l1_FakeFactorApplication_Region_genuinetauMC_Embedded = l1_FakeFactorApplication_Region_genuinetauMC * config.weights['weight'] * config.weights['embed'] * config.weights['l1_fake']
l2_FakeFactorApplication_Region_genuinetauMC_Embedded = l2_FakeFactorApplication_Region_genuinetauMC * config.weights['weight'] * config.weights['embed'] * config.weights['l2_fake']
l1_FakeFactorApplication_Region_genuinetauMC = l1_FakeFactorApplication_Region_genuinetauMC * config.weights['weight'] * config.weights['l1_fake']
l2_FakeFactorApplication_Region_genuinetauMC = l2_FakeFactorApplication_Region_genuinetauMC * config.weights['weight'] * config.weights['l2_fake']

#########
# Cfgs and components
#########

from htt_plot.tools.builder import build_cfgs, merge_cfgs, merge_components
from htt_plot.tools.builder import  merge_components as merge_comps

# MC
ZTT_cfgs = build_cfgs(
    [dataset.name+'_ZTT' for dataset in datasets.DY_datasets], 
    datasets.DY_datasets, variables,
    signal_region_MC_nofakes_DY * config.cuts_datacards['ZTT'], bins)
ZTT_comp = merge_cfgs('ZTT', ZTT_cfgs)

ZL_cfgs = build_cfgs(
    [dataset.name+'_ZL' for dataset in datasets.DY_datasets], 
    datasets.DY_datasets, variables,
    signal_region_MC_nofakes_DY * config.cuts_datacards['ZL'], bins)
ZL_comp = merge_cfgs('ZL', ZL_cfgs)

ZJ_cfgs = build_cfgs(
    [dataset.name+'_ZJ' for dataset in datasets.DY_datasets], 
    datasets.DY_datasets, variables,
    signal_region_MC_nofakes_DY * config.cuts_datacards['ZJ'], bins)
ZJ_comp = merge_cfgs('ZJ', ZJ_cfgs)

ZLL_comp = merge_comps('ZLL', [ZL_comp, ZJ_comp])
DY_comp = merge_comps('DY', [ZLL_comp, ZTT_comp])

TTT_cfgs = build_cfgs(
    [dataset.name+'_TTT' for dataset in datasets.TT_datasets], 
    datasets.TT_datasets, variables,
    signal_region_MC_nofakes_TT * config.cuts_datacards['TTT'], bins)
TTT_comp = merge_cfgs('TTT', TTT_cfgs)

TTJ_cfgs = build_cfgs(
    [dataset.name+'_TTJ' for dataset in datasets.TT_datasets], 
    datasets.TT_datasets, variables,
    signal_region_MC_nofakes_TT * config.cuts_datacards['TTJ'], bins)
TTJ_comp = merge_cfgs('TTJ', TTJ_cfgs)

TT_comp = merge_comps('TT', [TTT_comp, TTJ_comp])

Diboson_VVT_cfgs = build_cfgs(
    [dataset.name+'_VVT' for dataset in datasets.Diboson_datasets], 
    datasets.Diboson_datasets, variables,
    signal_region_MC_nofakes * config.cuts_datacards['VVT'], bins)
Diboson_VVT_comp = merge_cfgs('Diboson_VVT', Diboson_VVT_cfgs)

Diboson_VVJ_cfgs = build_cfgs(
    [dataset.name+'_VVJ' for dataset in datasets.Diboson_datasets], 
    datasets.Diboson_datasets, variables,
    signal_region_MC_nofakes * config.cuts_datacards['VVJ'], bins)
Diboson_VVJ_comp = merge_cfgs('Diboson_VVJ', Diboson_VVJ_cfgs)

singleTop_VVT_cfgs = build_cfgs(
    [dataset.name+'_VVT' for dataset in datasets.singleTop_datasets], 
    datasets.singleTop_datasets, variables,
    signal_region_MC_nofakes * config.cuts_datacards['VVT'], bins)
singleTop_VVT_comp = merge_cfgs('singleTop_VVT', singleTop_VVT_cfgs)

singleTop_VVJ_cfgs = build_cfgs(
    [dataset.name+'_VVJ' for dataset in datasets.singleTop_datasets], 
    datasets.singleTop_datasets, variables,
    signal_region_MC_nofakes * config.cuts_datacards['VVJ'], bins)
singleTop_VVJ_comp = merge_cfgs('singleTop_VVJ', singleTop_VVJ_cfgs)

VVT_comp = merge_comps('VVT', [singleTop_VVT_comp, Diboson_VVT_comp])
VVJ_comp = merge_comps('VVJ', [singleTop_VVJ_comp, Diboson_VVJ_comp])
VV_comp = merge_comps('VV', [VVT_comp, VVJ_comp])

Diboson_comp = merge_comps('Diboson', [Diboson_VVT_comp, Diboson_VVJ_comp])
singleTop_comp = merge_comps('singleTop', [singleTop_VVT_comp, singleTop_VVJ_comp])

W_cfgs = build_cfgs(
    [dataset.name+'_W' for dataset in datasets.WJ_datasets], 
    datasets.WJ_datasets, variables,
    signal_region_MC_nofakes * config.cuts_datacards['W'], bins)
W_comp = merge_cfgs('W', W_cfgs)

MC_comps = [DY_comp, TT_comp, singleTop_comp, Diboson_comp, W_comp]

# data
data_cfgs = build_cfgs(
    [dataset.name for dataset in datasets.data_datasets], 
    datasets.data_datasets, variables, signal_region, bins)
for cfg in data_cfgs:
    cfg.stack = False
data_comp = merge_cfgs('data', data_cfgs)

# Embedded
Embedded_cfgs = build_cfgs(
    [dataset.name for dataset in datasets.Embedded_datasets], 
    datasets.Embedded_datasets, variables, signal_region_Embedded, bins)
Embedded_comp = merge_cfgs('Embedded', Embedded_cfgs)

# fakes
datasets_MC_fakes = datasets.WJ_datasets + datasets.Diboson_datasets + datasets.singleTop_datasets + datasets.DY_datasets + datasets.TT_datasets
fake_cfgs_MC_1 = build_cfgs(['fakesMC1'], datasets_MC_fakes, variables, l1_FakeFactorApplication_Region_genuinetauMC, bins)
fake_cfgs_MC_2 = build_cfgs(['fakesMC2'], datasets_MC_fakes, variables, l2_FakeFactorApplication_Region_genuinetauMC, bins)

fake_cfgs_1 = build_cfgs(
    ['fakes'+dataset.name[-1]+'1' for dataset in datasets.data_datasets], 
    datasets.data_datasets, variables, l1_FakeFactorApplication_Region, bins)
fake_cfgs_2 = build_cfgs(
    ['fakes'+dataset.name[-1]+'2' for dataset in datasets.data_datasets], 
    datasets.data_datasets, variables, l2_FakeFactorApplication_Region, bins)

fake_cfgs_Embedded_1 = build_cfgs(
    ['fakesEmbedded'+dataset.name[-1]+'1' for dataset in datasets.Embedded_datasets], 
    datasets.Embedded_datasets, variables, l1_FakeFactorApplication_Region_genuinetauMC_Embedded, bins)
fake_cfgs_Embedded_2 = build_cfgs(
    ['fakesEmbedded'+dataset.name[-1]+'2' for dataset in datasets.Embedded_datasets], 
    datasets.Embedded_datasets, variables, l2_FakeFactorApplication_Region_genuinetauMC_Embedded, bins)

data_fakes_cfgs = fake_cfgs_1 + fake_cfgs_2
nondata_fakes_cfgs = fake_cfgs_Embedded_1 + fake_cfgs_Embedded_2 + fake_cfgs_MC_1 + fake_cfgs_MC_2

data_fakes_comp = merge_cfgs('jetFakes', data_fakes_cfgs)

for cfg in nondata_fakes_cfgs:
    cfg.scale = -1.
nondata_fakes_comp = merge_cfgs('fakes_nondata', nondata_fakes_cfgs)
    
fakes_comp = merge_comps('fakes', [data_fakes_comp, nondata_fakes_comp])

# Plotting & datacards

all_comp =  MC_comps + [data_comp, Embedded_comp, fakes_comp]

plotter = delayed(Plotter)(all_comp, datasets.data_lumi)

datacards = delayed(make_datacards)(output_dir, 'mt_tot',
                                    ZTT = ZTT_comp,
                                    ZL = ZL_comp,
                                    ZJ = ZJ_comp,
                                    ZLL = ZLL_comp,
                                    TTT = TTT_comp,
                                    TTJ = TTJ_comp,
                                    TT = TT_comp,
                                    VVT = VVT_comp,
                                    VVJ = VVJ_comp,
                                    VV = VV_comp,
                                    W = W_comp,
                                    jetFakes = data_fakes_comp,
                                    data_obs = data_comp,
                                    embedded = Embedded_comp
)

def write_plots(plotter, variables, output_dir):
    for var in variables:
        plotter.draw(var, 'Number of events')
        plotter.write('{}/{}.png'.format(output_dir,var))
        plotter.write('{}/{}.tex'.format(output_dir,var))
        print plotter.plot

writter = delayed(write_plots)(plotter, variables, output_dir)

import os
os.system('rm -rf {}'.format(output_dir))
os.system('mkdir {}'.format(output_dir))

def get_processes(processes_list):
    return processes_list

processes = delayed(get_processes)([writter, datacards])
        
visualize(processes)
#compute(process)
