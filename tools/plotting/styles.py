import fnmatch

from ROOT import TColor, kBlack

from cpyroot.tools.style import *

qcdcol = TColor.GetColor(250,202,255)
embedcol =  TColor.GetColor(248,206,104)
dycol = TColor.GetColor(0,150,255)
wcol = TColor.GetColor(222,90,106)
ttcol = TColor.GetColor(155,152,204)
zlcol = TColor.GetColor(100,182,232)
dibosoncol = TColor.GetColor(222,90,106)

sqcd = Style(markerColor=qcdcol, markerSize=1, lineColor=1, fillColor=qcdcol, fillStyle=1001)
sdy = Style(markerColor=dycol, markerSize=1, lineColor=1, fillColor=dycol, fillStyle=1001)
sembed = Style(markerColor=embedcol, markerSize=1, lineColor=1, fillColor=embedcol, fillStyle=1001)
swj = Style(markerColor=wcol, markerSize=1, lineColor=1, fillColor=wcol, fillStyle=1001)
stt = Style(markerColor=ttcol, markerSize=1, lineColor=1, fillColor=ttcol, fillStyle=1001)
sDiboson = Style(markerColor=dibosoncol, markerSize=1, lineColor=1, fillColor=dibosoncol, fillStyle=1001)
ssingletop = Style(markerColor=ttcol, markerSize=1, lineColor=1, fillColor=ttcol, fillStyle=1001)
sfakes = Style(markerColor=5, markerSize=1, lineColor=1, fillColor=8, fillStyle=1001)
sdata = sData
sunc = Style(fillColor=17, fillStyle=3144)
ssig = Style(fillColor=0, fillStyle=0, lineColor=2)
ssig2 = Style(fillColor=0, fillStyle=0, lineColor=4)
ssig3 = Style(fillColor=0, fillStyle=0, lineColor=5)
ssig4 = Style(fillColor=0, fillStyle=0, lineColor=6)
ssig5 = Style(fillColor=0, fillStyle=0, lineColor=7)
ssig6 = Style(fillColor=0, fillStyle=0, lineColor=8)
sQCD = sfakes

histPref = {
    'DY': {'style':sdy, 'layer':12, 'legend':'Z #rightarrow ll (l #rightarrow #tau_{h})', 'stack': True},
    'Embedded': {'style':sembed, 'layer':35, 'legend':'#mu #rightarrow embedded', 'stack': True},
    'WJ': {'style':swj, 'layer':9, 'legend':'WJ', 'stack': True},
    'TTBar': {'style':stt, 'layer':2, 'legend':'TTBar', 'stack': True},
    'Diboson': {'style':sDiboson, 'layer':3, 'legend':'Diboson', 'stack': True},
    'singleTop': {'style':ssingletop, 'layer':4, 'legend':'singleTop', 'stack': True},
    'VV': {'style':sDiboson, 'layer':4, 'legend':'VV', 'stack': True},
    'EWK': {'style':sDiboson, 'layer':5, 'legend':'EWK', 'stack': True},
    'data_obs': {'style':sdata, 'layer':0, 'legend':'data', 'stack': False},
    'QCD': {'style':sfakes, 'layer':16, 'legend':'QCD', 'stack': True},
    'MC': {'style':sdy, 'layer':14, 'legend':'Simulation', 'stack': True},
    'fakes': {'style':sfakes, 'layer':15, 'legend':'jet #rightarrow #tau_{h} fakes', 'stack': True},
    'jetFakes': {'style':sfakes, 'layer':15, 'legend':'jet #rightarrow #tau_{h} fakes', 'stack': True},
    'data_obs_aiso_os': {'style':sQCD, 'layer':15, 'legend':'QCD', 'stack': True},
    'VVL': {'style':sDiboson, 'layer':4, 'legend':'Diboson-singleTop #rightarrow ll (l #rightarrow #tau_{h})', 'stack': True},
    'TTL': {'style':stt, 'layer':2, 'legend':'t#bar{t} #rightarrow ll (l #rightarrow #tau_{h})', 'stack': True},
    'ZL': {'style':sdy, 'layer':12, 'legend':'Z #rightarrow ll (l #rightarrow #tau_{h})', 'stack': True},
    'total_background': {'style':sunc, 'layer':1, 'legend':'systematic uncertainties', 'stack': False},
    'signal_H600': {'style':ssig, 'layer':0, 'legend':'#phi #rightarrow #tau#tau (m_{#phi}=600 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_bbH600': {'style':ssig2, 'layer':0, 'legend':'bb#phi (m_{#phi}=600 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_ggH600': {'style':ssig, 'layer':0, 'legend':'gg#phi (m_{#phi}=600 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_bbH800': {'style':ssig3, 'layer':0, 'legend':'bb#phi (m_{#phi}=800 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_ggH800': {'style':ssig4, 'layer':0, 'legend':'gg#phi (m_{#phi}=800 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_bbH900': {'style':ssig5, 'layer':0, 'legend':'bb#phi (m_{#phi}=900 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_ggH900': {'style':ssig6, 'layer':0, 'legend':'gg#phi (m_{#phi}=900 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'EMB': {'style':sembed, 'layer':35, 'legend':'#mu #rightarrow embedded', 'stack': True},
    'signal_bbH400': {'style':ssig2, 'layer':0, 'legend':'bb#phi (m_{#phi}=400 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_bbH450': {'style':ssig2, 'layer':0, 'legend':'bb#phi (m_{#phi}=450 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_bbH1400': {'style':ssig2, 'layer':0, 'legend':'bb#phi (m_{#phi}=1400 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_bbH1800': {'style':ssig2, 'layer':0, 'legend':'bb#phi (m_{#phi}=1800 GeV, #sigma#timesBR=1 pb)', 'stack': False},
    'signal_bbH2000': {'style':ssig2, 'layer':0, 'legend':'bb#phi (m_{#phi}=2000 GeV, #sigma#timesBR=1 pb)', 'stack': False},
}

histPref['W'] = histPref['WJ']
histPref['TT'] = histPref['TTBar']
histPref['ZLL'] = histPref['DY']

def set_style(comp):
    found=False
    for key, pref in histPref.iteritems():
        if fnmatch.fnmatch(comp.name, key):
            comp.style = pref['style']
            found = True
    if not found:
        comp.style = sData
