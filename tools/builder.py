from htt_plot.tools.cut import Cuts
from htt_plot.tools.component import Component, Component_cfg
from dask import delayed
import copy
from ROOT import TH1F

def build_cfg(name, dataset, variable, cut, bins):
    '''Allows to pass non-str cuts'''
    if not isinstance(cut, str):
        cut = str(cut)
    cfg = Component_cfg(
        name = name,
        dataset = dataset,
        variable = variable,
        cut = cut,
        bins = bins,
    )
    return cfg

def build_cfgs(names, datasets, variable, cut, bins):
    cfgs = []
    for name, dataset in zip(names, datasets):
        cfgs.append(build_cfg(name,dataset,variable,cut,bins))
    return cfgs

def create_component(cfg):
    ''' Creates a component object and fills its histogram
    following its configuration file '''
    comp = Component(cfg)
    project(comp)
    return comp

create_component = delayed(create_component)

def merge_cfgs(name, cfgs):
    ''' Returns a component which is the merged component of all components
    that would have been created with all cfgs '''
    comps = [create_component(cfg) for cfg in cfgs]
    return merge_components(name, comps)

def merge_components(name, comps):
    ''' Take components and returns a new component, which histogram
    contains all the intial components histograms '''
    merged = comps[0].Clone(name)
    comps.remove(comps[0])
    for comp in comps:
        merged.histogram.Add(comp.histogram)
    return merged

merge_components = delayed(merge_components)

def merge(name, objs):
    '''transparent function to use regardless of whether
    objs are cfgs or comps'''
    if all([isinstance(obj,Component_cfg) for obj in objs]):
        return merge_cfgs(name, objs)
    else:
        return merge_components(name, objs)

def ABCD(cfg1,cfg2,cfg3,name):
    CD_ratio = cfg1.histogram.Integral()/cfg2.histogram.Integral()
    cfg4 = cfg3.Clone(name)
    cfg4.histogram.Scale(CD_ratio)
    return cfg4

ABCD = delayed(ABCD)

def project(comp):
    ''' fills a component histogram following its configuration file '''
    dataset = comp.cfg['dataset']
    var = comp.var
    histo = TH1F(comp.name+dataset.name, comp.name+dataset.name, *comp.cfg['bins'])
    dataset.tree.Project(comp.name+dataset.name, var, comp.cfg['cut'])
    histo.Scale(dataset.weight * comp.cfg['scale'])
    comp.histogram.Add(histo)
