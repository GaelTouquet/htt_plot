#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-c", "--cfg", dest = "cfg_name",
                  default="tt",
                  help='Name of the config file to use, must be in htt_plot/channels_configs/')
parser.add_option("-o", "--output", dest = "output_dir",
                  default="delayed_plots",
                  help='Output directory base name, channel is added')
parser.add_option("-C", "--category", dest = "category",
                  default="inclusive",
                  help='Category to process: inclusive, btag, nobtag.')
parser.add_option("-e", "--embedding", action = "store_true",
                  default=False,
                  help='Category to process: inclusive, btag, nobtag.')


(options,args) = parser.parse_args()

cfg = __import__("htt_plot.channels_configs.{}".format(options.cfg_name), fromlist=[''])

# variables

variable = 'mt_tot'

output_dir = '_'.join([options.output_dir, cfg.channel])

# category
category = options.category # 'nobtag'#'nobtag','btag','inclusive'
if category == 'inclusive':
    cut_signal = cfg.cut_signal
    basic_cuts =  cfg.basic_cuts
elif category == 'nobtag':
    from array import array
    cfg.bins['mt_tot'] = (33, array('d',[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,600,700,800,900,4000]))
    cut_signal = cfg.cut_signal_nobtag
    basic_cuts =  cfg.basic_cuts_nobtag
elif category == 'btag':
    # from array import array
    # cfg.bins['mt_tot'] = (16, array('d',[0,20,40,60,80,100,120,140,160,180,200,250,300,350,400,500,4000]))
    cut_signal = cfg.cut_signal_btag
    basic_cuts =  cfg.basic_cuts_btag
else:
    raise ValueError('category must be inclusive, nobtag or btag')


# mass_points = [400,450,600,800]#[80,90,110,120]#[80,90,110,120,130,180,250,300,400,450,600,800,900,1200,1400,1600,1800,2000,2300,2600,2900]#<=new working amcatnlo bbh mass points [80,100,110,120,130]#[80,100,110,120,130]#[140,180,200,250]#[300,400,450,600,700]#[800,900,1200,1400,1500]#[2300,2600,2900,3200]#90,350,1600,1800,2000#,,,


# cfg.datasets.signal_datasets = cfg.datasets.build_signals(mass_points)
# for sys, dataset_list in cfg.datasets.signal_datasets.iteritems() :
#     for name, dataset in dataset_list.iteritems():
#         dataset.compute_weight(cfg.datasets.data_lumi)



# dask tools
from dask import delayed, compute, visualize

# plotting tools
from htt_plot.tools.plotting.plotter import Plotter
from htt_plot.tools.plotting.tdrstyle import setTDRStyle
setTDRStyle(square=False)

# datacards tools
from htt_plot.tools.datacards import make_datacards

#### cuts


basic_ABCD_cut = cfg.cuts_flags.all() & cfg.cuts_vetoes.all() & cfg.cut_triggers & cfg.cuts_against_leptons.all()
if category == 'nobtag':
    basic_ABCD_cut = basic_ABCD_cut & cfg.cut_nobtag
elif category == 'btag':
    basic_ABCD_cut = basic_ABCD_cut & cfg.cut_btag
anti_isolated_os_region_cut = basic_ABCD_cut & cfg.cut_os & ~(cfg.cuts_iso['l1_Tight'] & cfg.cuts_iso['l2_Tight']) & (cfg.cuts_iso['l1_VLoose'] & cfg.cuts_iso['l2_VLoose'])
isolated_ss_region_cut = basic_ABCD_cut & ~(cfg.cut_os) & cfg.cuts_iso['l1_Tight'] & cfg.cuts_iso['l2_Tight'] & (cfg.cuts_iso['l1_VLoose'] & cfg.cuts_iso['l2_VLoose'])
anti_isolated_ss_region_cut = basic_ABCD_cut & ~(cfg.cut_os) & ~(cfg.cuts_iso['l1_Tight'] & cfg.cuts_iso['l2_Tight']) & (cfg.cuts_iso['l1_VLoose'] & cfg.cuts_iso['l2_VLoose'])

    
# cuts + weights

signal_region = cut_signal * cfg.weights['weight']
anti_isolated_os_region = anti_isolated_os_region_cut * cfg.weights['weight']
isolated_ss_region = isolated_ss_region_cut * cfg.weights['weight']
anti_isolated_ss_region = anti_isolated_ss_region_cut * cfg.weights['weight']

signal_region_MC = cut_signal * cfg.weights['weight'] * cfg.weights['MC']
anti_isolated_os_region_MC = anti_isolated_os_region_cut * cfg.weights['weight'] * cfg.weights['MC']
isolated_ss_region_MC = isolated_ss_region_cut * cfg.weights['weight'] * cfg.weights['MC']
anti_isolated_ss_region_MC = anti_isolated_ss_region_cut * cfg.weights['weight'] * cfg.weights['MC']

if options.embedding:
    signal_region_MC = (cut_signal & cfg.cut_not_embed) * cfg.weights['weight'] * cfg.weights['MC']
    anti_isolated_os_region_MC = (anti_isolated_os_region_cut & cfg.cut_not_embed)* cfg.weights['weight'] * cfg.weights['MC']
    isolated_ss_region_MC = (isolated_ss_region_cut & cfg.cut_not_embed) * cfg.weights['weight'] * cfg.weights['MC']
    anti_isolated_ss_region_MC = (anti_isolated_ss_region_cut & cfg.cut_not_embed ) * cfg.weights['weight'] * cfg.weights['MC']

    signal_region_embed = cut_signal * cfg.weights['embed']
    anti_isolated_os_region_embed = anti_isolated_os_region_cut * cfg.weights['embed']
    isolated_ss_region_embed = isolated_ss_region_cut * cfg.weights['embed']
    anti_isolated_ss_region_embed = anti_isolated_ss_region_cut * cfg.weights['embed']
    
### start of plot building
from htt_plot.tools.utils import add_process
from htt_plot.tools.builder import build_cfgs, merge, ABCD

cfgs = {}
bins = cfg.bins[variable]

# MC
add_process(cfgs,'MC',
	cfg.datasets.singleTop_datasets['nominal']+cfg.datasets.WJ_datasets['nominal']+cfg.datasets.Diboson_datasets['nominal']+cfg.datasets.TT_datasets['nominal']+cfg.datasets.DY_datasets['nominal']+cfg.datasets.EWK_datasets['nominal'],
		variable,signal_region_MC,bins)


add_process(cfgs,'MC_aiso_os',
	cfg.datasets.singleTop_datasets['nominal']+cfg.datasets.WJ_datasets['nominal']+cfg.datasets.Diboson_datasets['nominal']+cfg.datasets.TT_datasets['nominal']+cfg.datasets.DY_datasets['nominal']+cfg.datasets.EWK_datasets['nominal'],
		variable,anti_isolated_os_region_MC,bins,scale=-1.)
add_process(cfgs,'MC_iso_ss',
	cfg.datasets.singleTop_datasets['nominal']+cfg.datasets.WJ_datasets['nominal']+cfg.datasets.Diboson_datasets['nominal']+cfg.datasets.TT_datasets['nominal']+cfg.datasets.DY_datasets['nominal']+cfg.datasets.EWK_datasets['nominal'],
		variable,isolated_ss_region_MC,bins,scale=-1.)
add_process(cfgs,'MC_aiso_ss',
	cfg.datasets.singleTop_datasets['nominal']+cfg.datasets.WJ_datasets['nominal']+cfg.datasets.Diboson_datasets['nominal']+cfg.datasets.TT_datasets['nominal']+cfg.datasets.DY_datasets['nominal']+cfg.datasets.EWK_datasets['nominal'],
		variable,anti_isolated_ss_region_MC,bins,scale=-1.)

#data
add_process(cfgs,'data_obs',
	cfg.datasets.data_datasets,
		variable,signal_region,bins)


add_process(cfgs,'data_aiso_os',
	cfg.datasets.data_datasets,
		variable,anti_isolated_os_region,bins)
add_process(cfgs,'data_iso_ss',
	cfg.datasets.data_datasets,
		variable,isolated_ss_region,bins)
add_process(cfgs,'data_aiso_ss',
	cfg.datasets.data_datasets,
		variable,anti_isolated_ss_region,bins)


if options.embedding:
    #embedding
    add_process(cfgs,'Embedded',
	        cfg.datasets.Embedded_datasets['nominal'],
		variable,signal_region_embed,bins)
    
    add_process(cfgs,'Embedded_aiso_os',
	        cfg.datasets.Embedded_datasets['nominal'],
		variable,anti_isolated_os_region_embed,bins,scale=-1.)
    add_process(cfgs,'Embedded_iso_ss',
	        cfg.datasets.Embedded_datasets['nominal'],
		variable,isolated_ss_region_embed,bins,scale=-1.)
    add_process(cfgs,'Embedded_aiso_ss',
	        cfg.datasets.Embedded_datasets['nominal'],
		variable,anti_isolated_ss_region_embed,bins,scale=-1.)
    
    cfgs['QCD_aiso_os'] = merge('QCD_aiso_os',[cfgs['data_aiso_os'],cfgs['MC_aiso_os']])
    cfgs['QCD_aiso_ss'] = merge('QCD_aiso_ss',[cfgs['data_aiso_ss'],cfgs['MC_aiso_ss']])
    cfgs['QCD_iso_ss'] = merge('QCD_iso_ss',[cfgs['data_iso_ss'],cfgs['MC_iso_ss']])

    cfgs['QCD'] = ABCD(cfgs['QCD_iso_ss'],cfgs['QCD_aiso_ss'],cfgs['QCD_aiso_os'],'QCD')

else:
    
    #QCD
    cfgs['QCD_aiso_os'] = merge('QCD_aiso_os',[cfgs['data_aiso_os'],cfgs['MC_aiso_os']])
    cfgs['QCD_aiso_ss'] = merge('QCD_aiso_ss',[cfgs['data_aiso_ss'],cfgs['MC_aiso_ss']])
    cfgs['QCD_iso_ss'] = merge('QCD_iso_ss',[cfgs['data_iso_ss'],cfgs['MC_iso_ss']])

cfgs['QCD'] = ABCD(cfgs['QCD_iso_ss'],cfgs['QCD_aiso_ss'],cfgs['QCD_aiso_os'],'QCD')

    
components = [cfgs['QCD'],cfgs['data_obs'],cfgs['MC']]

if options.embedding:
    components.append(cfgs['Embedded'])

processes= []

def write_plots(plotter, variable, output_dir):
    varname = cfg.var_name_dict[variable] if variable in cfg.var_name_dict else variable
    plotter.draw(varname, 'Number of events')
    plotter.write('{}/{}/{}.png'.format(output_dir, category, varname))
    plotter.write('{}/{}/{}.tex'.format(output_dir, category, varname))
    plotter.write('{}/{}/{}.root'.format(output_dir, category, varname))
    print plotter.plot
    
processes.append(
	 delayed(write_plots)(
             delayed(Plotter)(components, cfg.datasets.data_lumi),
                variable,
            	output_dir
            	)		
        	)


import os
# os.system('rm -rf {}'.format(output_dir))
if not os.path.exists(output_dir):
    os.system('mkdir -p {}'.format(output_dir))
if not os.path.exists('{}/{}'.format(output_dir,category)):
    os.system('mkdir -p {}/{}'.format(output_dir,category))
        

compute(*processes)
