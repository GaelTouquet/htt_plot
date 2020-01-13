from htt_plot.tools.builder import build_cfgs, merge, create_component, build_cfg

def add_processes_per_component(cfgs,component_name,baseprocesses,datasets,variable,basecut,process_cuts_dict,fake1_cut,fake2_cut,bins, mergedict={}, fakes = True):
    for process in baseprocesses:
        if process not in process_cuts_dict:
            dc_cut = None
            for name, cut in process_cuts_dict:
                if process in name:
                    dc_cut = cut
        else:
            dc_cut = process_cuts_dict[process]
        cfgs[process+'_cfgs'] = build_cfgs(
            [dataset.name+'_{}'.format(process) for dataset in datasets],
            datasets, variable,
            basecut & dc_cut, bins)
        if component_name == 'data_obs':
            for cfg in cfgs[process+'_cfgs']:
                cfg.stack = False
        cfgs[process] = merge(process,cfgs[process+'_cfgs'])
    for mergedname, names_to_merge in mergedict.iteritems():        cfgs[mergedname] = merge(mergedname,[cfgs[name] for name in names_to_merge])
    if fakes:
        cfgs['fakes{}_l1'.format(component_name)] = build_cfgs(['fakes{}_l1_{}'.format(component_name,dataset.name) for dataset in datasets],
                                                               datasets, variable,
                                                               fake1_cut, bins)
        if component_name != 'data_obs':
            for cfg in cfgs['fakes{}_l1'.format(component_name)]:
                cfg['scale'] = -1.
        cfgs['fakes{}_l2'.format(component_name)] = build_cfgs(['fakes{}_l2_{}'.format(component_name,dataset.name) for dataset in datasets],
                                                               datasets, variable,
                                                               fake2_cut, bins)
        if component_name != 'data_obs':
            for cfg in cfgs['fakes{}_l2'.format(component_name)]:
                cfg['scale'] = -1.
        cfgs['fakes_{}'.format(component_name)] = merge('fakes{}'.format(component_name),
                                                        cfgs['fakes{}_l1'.format(component_name)]+cfgs['fakes{}_l2'.format(component_name)])

def add_simple_process(cfgs,name,dataset,variable,cut,bins):
    cfgs[name+'_cfg'] = build_cfg(name,dataset,variable,cut,bins)
    cfgs[name] = create_component(cfgs[name+'_cfg'])

def add_process(cfgs,name,datasets,variable,cut,bins,scale=None):
    cfgs[name+'_cfgs'] = build_cfgs([dataset.name+'_{}'.format(name) for dataset in datasets],
                                       datasets, variable,
                                       cut, bins)
    if scale != None:
        for cfg in cfgs[name+'_cfgs']:
            cfg['scale'] = scale
    cfgs[name] = merge(name, cfgs[name+'_cfgs'])
