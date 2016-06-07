# Quick script to overplot power colour values
# Written by David Gardenier, davidgardenier@gmail.com, 2015-2016

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from pyx import *


def path(o):
    return '/scratch/david/master_project/' + o + '/info/database_' + o + '.csv'


ns = [('4u_1705_m44', '4U 1705-44'),
        ('4U_0614p09', '4U 0614+09'),
        ('4U_1636_m53', '4U 1636-53'),
        ('4U_1702m43', '4U 1702-43'),
        ('4U_1728_34', '4U 1728-34'),
        ('aquila_X1', 'Aql X-1'),
        #('cir_x1', 'Cir X-1'), #strange behaviour
        ('cyg_x2', 'Cyg X-2'),
        #('EXO_0748_676', 'EXO 0748-676'), #Strange behaviour
        ('gx_5m1', 'GX 5-1'), #Only 5 points
        ('gx_17p2', 'GX 17+2'), #Only has 4 points
        #('gx_339_d4', 'GX 339-4'), #BH system
        ('gx_340p0', 'GX 340+0'), #Only 5 points
        #('gx_349p2', 'GX 349+2'), #Only 3 points
        ('HJ1900d1_2455', 'HETE J1900.1-2455'),
        ('IGR_J00291p5934', 'IGR J00291+5934'),
        ('IGR_J17480m2446', 'IGR J17480-2446'),
        #('IGR_J17498m2921', 'IGR J17498-2921'), #Only 1 point
        #('IGR_J17511m3057', 'IGR J17511-3057'), #Same as XTE J1751
        ('J1701_462', 'XTE J1701-462'),
        ('KS_1731m260', 'KS 1731-260'),
        ('sco_x1', 'Sco X-1'),
        ('sgr_x1', 'Sgr X-1'),
        ('sgr_x2', 'Sgr X-2'),
        ('S_J1756d9m2508', 'SWIFT J1756.9-2508'),
        ('v4634_sgr', 'V4634 Sgr'),
        ('XB_1254_m690', 'XB 1254-690'),
        ('xte_J0929m314', 'XTE J0929-314'),
        #('xte_J1550m564', 'XTE J1550-564'), #BH system
        ('xte_J1751m305', 'XTE J1751-305'),
        ('xte_J1807m294', 'XTE J1807-294'), #Only 4 points
        ('xte_J1808_369', 'SAX J1808.4-3648'),
        ('xte_J1814m338', 'XTE J1814-338')]

x_ns = []
y_ns = []

for i, o in enumerate(ns):
    name = o[-1]
    o = o[0]
    p = path(o)
    db = pd.read_csv(p)
    db = db[np.isfinite(db['flux_i3t16_s6p4t9p7_h9p7t16'])]
    x = db.flux_i3t16_s6p4t9p7_h9p7t16.values
    y = db.hardness_i3t16_s6p4t9p7_h9p7t16.values
    x_ns.extend(x)
    y_ns.extend(y)

bursters = [('4U_0614p09',414.7),
            ('4U_1636_m53',581.9),
            ('4U_1702m43',330),
            ('4U_1728_34',364),
            ('aquila_X1',550.3),
            ('EXO_0748_676',552.5),
            ('KS_1731m260',524)]

pulsars = [('HJ1900d1_2455',377.3),
            ('IGR_J17480m2446',11),
            ('xte_J1751m305',244.8),
            ('xte_J1807m294',190.6),
            ('xte_J1808_369',401)]

names = {'4u_1705_m44':'4U 1705-44',
        '4U_0614p09':'4U 0614+09',
        '4U_1636_m53':'4U 1636-53',
        '4U_1702m43':'4U 1702-43',
        '4U_1728_34':'4U 1728-34',
        'aquila_X1':'Aql X-1',
        'cir_x1':'Cir X-1', #strange behaviour
        'cyg_x2':'Cyg X-2',
        'EXO_0748_676':'EXO 0748-676', #Strange behaviour
        'gx_5m1':'GX 5-1', #Only 5 points
        'gx_17p2':'GX 17+2', #Only has 4 points
        'gx_339_d4':'GX 339-4', #BH system
        'gx_340p0':'GX 340+0', #Only 5 points
        'gx_349p2':'GX 349+2', #Only 3 points
        'HJ1900d1_2455':'HETE J1900.1-2455',
        'H1743m322':'H1743-322',
        'IGR_J00291p5934':'IGR J00291+5934',
        'IGR_J17480m2446':'IGR J17480-2446',
        'IGR_J17498m2921':'IGR J17498-2921', #Only 1 point
        'IGR_J17511m3057':'IGR J17511-3057', #Same as XTE J1751
        'J1701_462':'XTE J1701-462',
        'KS_1731m260':'KS 1731-260',
        'sco_x1':'Sco X-1',
        'sgr_x1':'Sgr X-1',
        'sgr_x2':'Sgr X-2',
        'S_J1756d9m2508':'SWIFT J1756.9-2508',
        'v4634_sgr':'V4634 Sgr',
        'XB_1254_m690':'XB 1254-690',
        'xte_J0929m314':'XTE J0929-314',
        'xte_J1550m564':'XTE J1550-564', #BH system
        'xte_J1751m305':'XTE J1751-305',
        'xte_J1807m294':'XTE J1807-294', #Only 4 points
        'xte_J1808_369':'SAX J1808.4-3648',
        'xte_J1814m338':'XTE J1814-338',
        'xte_J2123_m058':'XTE J2123-058'} # No pc points


class empty:

	def __init__(self):
		pass
	def labels(self, ticks):
		for tick in ticks:
			tick.label=""

def plotpcpane():

    # Set up plot details
    c=canvas.canvas()

    xposition=[0.0,6.0]
    yposition=[0.0,0.0]

    for i in range(len(xposition)):

        if i == 0:
            objs = bursters
        if i == 1:
            objs = pulsars
        objs = sorted(objs, key=lambda x: x[1])

        myticks = [graph.axis.tick.tick(1e-12, label=" ", labelattrs=[text.mathmode]),
                   graph.axis.tick.tick(1e-10, label=" ", labelattrs=[text.mathmode]),
                   graph.axis.tick.tick(1e-8, label=" ", labelattrs=[text.mathmode]),
                   graph.axis.tick.tick(1e-6, label=" ", labelattrs=[text.mathmode])]

    	if yposition[i]!=0.0:
            xtitle = ""
            xtexter=empty()
    	else:
            xtitle = "Intensity (photons$\ $ergs$\ $cm$^{-2}$ s$^{-1}$)"
            xtexter=graph.axis.texter.mixed()
    	if xposition[i]!=0.0:
            ytitle = ""
            ytexter=empty()
    	else:
            ytitle="Hardness"
            ytexter=graph.axis.texter.mixed()

    	g=c.insert(graph.graphxy(width=6.0,
                                 height=6.0,
                                 xpos=xposition[i],
                                 ypos=yposition[i],
	                             x=graph.axis.log(min=1e-12,max=1e-6,title=xtitle,texter=xtexter,manualticks=myticks),
	                             y=graph.axis.lin(min=0.0,max=2.75,title=ytitle,texter=ytexter),
                                 key=graph.key.key(pos='tr', dist=0.1, textattrs=[text.size.tiny])))

        scatterstyle= [graph.style.symbol( size=0.1, symbolattrs=[color.gradient.Rainbow])]

        # Plot Neutron Stars
        grey= color.cmyk(0,0,0,0.5)
        nsstyle = [graph.style.symbol(size=0.1, symbolattrs=[grey])]
        g.plot(graph.data.values(x=x_ns, y=y_ns, title='NSs'), nsstyle)

        for o in objs:

            xs = []
            ys = []

            print o[0]
            name = str(o[-1])
            o = o[0]
            p = path(o)
            db = pd.read_csv(p)
            db = db[np.isfinite(db['flux_i2t20_s2t6_h9t20'])]
            x = db.flux_i2t20_s2t6_h9t20.values
            y = db.hardness_i2t20_s2t6_h9t20.values
            xs.extend(x)
            ys.extend(y)

            g.plot(graph.data.values(x=xs, y=ys, title=name + ' Hz'), scatterstyle)
    # title = huerange.replace('_', '$^[\circ]$-') + '$^[\circ]$'
    # c.text(6.0,yposition[-1]+6.5,title,
    #        [text.halign.center, text.valign.bottom, text.size.Large])

    outputfile = '/scratch/david/master_project/plots/publication/hi/bursters_pulsars'
    c.writePDFfile(outputfile)
    # os.system('convert -density 300 '+outputfile+'.pdf -quality 90 '+outputfile+'.png')


if __name__=='__main__':
    plotpcpane()
