# Quick script to overplot power colour values
# Written by David Gardenier, davidgardenier@gmail.com, 2015-2016

import os
import glob
import pandas as pd
from math import atan2, degrees, pi, log10, sqrt
import matplotlib.pyplot as plt
import math
from pyx import *


def path(o):
    return '/scratch/david/master_project/' + o + '/info/database_' + o + '.csv'


def findbestres(res):
    '''Find the smallest resolution from a list of resolutions'''

    # Split resolutions into values and units
    heads = []
    tails = []
    for s in res:
        unit = s.strip('0123456789')
        num = s[:-len(unit)]
        heads.append(num)
        tails.append(unit)

    # Sort by unit, then by value
    unitorder = ['ms','us','s']
    for u in unitorder:
        if u in tails:
            indices = [i for i, x in enumerate(tails) if x==u]
            sameunits = [heads[i] for i in indices]
            sortvalues = sorted(sameunits)
            return sortvalues[0]+u


def findbestdataperobsid(df):
    '''Select the data with best mode and resolution'''
    ordering = ['gx1','event','binned','std2']
    for mode in ordering:
        if mode in df.modes.values:
            df = df[df.modes==mode]
            if df.shape[0] > 1:
                bestres = findbestres(df.resolutions.values)
                return df[df.resolutions==bestres].iloc[0]
            else:
                return df.iloc[0]


def findbestdata(db):
    # Apply constraint to the data
    db = db[(db.pc1.notnull() & db.lt3sigma==True)]
    db = db.groupby('obsids').apply(findbestdataperobsid)
    return db

def cal_hue(x,y,xerr,yerr):
    '''
    Function to calculate the hue on basis of power colour-ratio values.

    Assuming:
     - errors symmetric along either axis
     - errors uncorrelated with each other
     - errors given relative to a value

    Returns:
     - [tuple] hue, hue_error
    '''
    # Central point
    x0 = 4.51920
    y0 = 0.453724

    x = float(x)
    y = float(y)

    # Angles are defined in log-space
    dx = log10(x) - log10(x0)
    dy = log10(y) - log10(y0)

    # Calculate angle
    rads = atan2(dy,dx)
    rads %= 2*pi
    # Add 135 degrees as the hue angle is defined
    # from the line extending in north-west direction
    degs = -(rads*(180/pi)) + 135
    # Fixing things with minus degrees
    if degs < 0:
        degs = (180 - abs(degs)) + 180

    # Calculate errors with error propagation
    above = (yerr*x*log10(x/x0))**2+(xerr*y*log10(y/y0))**2
    below = (x*y*(log10(x/x0)**2 + log10(y/y0)**2))**2
    radserr = sqrt(above/float(below))
    radserr %= 2*pi
    degserr = radserr*180/pi

    return degs, degserr


ns = [('4u_1705_m44', '4U 1705-44'),
        ('4U_0614p09', '4U 0614+09'),
        ('4U_1636_m53', '4U 1636-53'),
        ('4U_1702m43', '4U 1702-43'),
        ('4U_1728_34', '4U 1728-34'),
        ('aquila_X1', 'Aql X-1'),
        #('cir_x1', 'Cir X-1'), #strange behaviour
        ('cyg_x2', 'Cyg X-2'),
        #('EXO_0748_676', 'EXO 0748-676'), #Strange behaviour
        ('gx_3p1', 'GX 3+1'),
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
xerror_ns = []
yerror_ns = []

for i, o in enumerate(ns):
    name = o[-1]
    o = o[0]
    p = path(o)
    db = pd.read_csv(p)
    # Determine pc values
    bestdata = findbestdata(db)
    # Calculate hues
    hues = []
    hues_err = []
    for i in range(len(bestdata.pc1.values)):
        # Determine input parameters
        pc1 = bestdata.pc1.values[i]
        pc2 = bestdata.pc2.values[i]
        pc1err = bestdata.pc1_err.values[i]
        pc2err = bestdata.pc2_err.values[i]
        hue, hue_err = cal_hue(pc1,pc2,pc1err,pc2err)
        hues.append(hue)
        hues_err.append(hue_err)

    # Determine hardness values
    hardness = []
    hardness_err = []
    for obsid, group in bestdata.groupby('obsids'):
        df = db[db.obsids==obsid].dropna(subset=['flux_i3t16_s6p4t9p7_h9p7t16'])
        hardness.append(df.hardness_i3t16_s6p4t9p7_h9p7t16.values[0])
        hardness_err.append(df.hardness_err_i3t16_s6p4t9p7_h9p7t16.values[0])

    # Plot details
    index_to_del = []
    for ih, h in enumerate(hues_err):
        if h > 30:
            index_to_del.append(ih)
    hues = [i for j, i in enumerate(hues) if j not in index_to_del]
    hues_err = [i for j, i in enumerate(hues_err) if j not in index_to_del]
    hardness = [i for j, i in enumerate(hardness) if j not in index_to_del]
    hardness_err = [i for j, i in enumerate(hardness_err) if j not in index_to_del]

    x_ns.extend(hues)
    y_ns.extend(hardness)
    xerror_ns.extend(hues_err)
    yerror_ns.extend(hardness_err)


names = {'4u_1705_m44':'4U 1705-44',
        '4U_0614p09':'4U 0614+09',
        '4U_1636_m53':'4U 1636-53',
        '4U_1702m43':'4U 1702-43',
        '4U_1728_34':'4U 1728-34',
        'aquila_X1':'Aql X-1',
        'cir_x1':'Cir X-1', #strange behaviour
        'cyg_x2':'Cyg X-2',
        'EXO_0748_676':'EXO 0748-676', #Strange behaviour
        'gx_3p1':'GX 3+1',
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

def plotpcpane(objects, nr):

    # Set up plot details
    c=canvas.canvas()

    if len(objects) == 12:
        xposition=[0.0,6.0,12.0, 0.0,6.0,12.0, 0.0,6.0,12.0,   0.0,6.0,12.0]
        yposition=[0.0,0.0,0.0,  6.0,6.0,6.0,  12.0,12.0,12.0, 18.0,18.0,18.0]
        order = [10,11,12,7,8,9,4,5,6,1,2,3]
    if len(objects) == 7:
        xposition=[0.0, 0.0,6.0,12.0, 0.0,6.0,12.0]
        yposition=[0.0, 6.0,6.0,6.0,  12.0,12.0,12.0]
        order = [7,4,5,6,1,2,3]
    if len(objects) == 3:
        xposition=[0.0,6.0,12.0]
        yposition=[0.0,0.0,0.0]
        order = [1,2,3]
    objcts = [objects[j-1] for j in order]

    print str(nr), '\n=========================='
    for z in range(len(objcts)):
        obj = objcts[z]
        print names[obj]

        p = path(obj)
        db = pd.read_csv(p)
        # Determine pc values
        bestdata = findbestdata(db)
        # Calculate hues
        hues = []
        hues_err = []
        for i in range(len(bestdata.pc1.values)):
            # Determine input parameters
            pc1 = bestdata.pc1.values[i]
            pc2 = bestdata.pc2.values[i]
            pc1err = bestdata.pc1_err.values[i]
            pc2err = bestdata.pc2_err.values[i]
            hue, hue_err = cal_hue(pc1,pc2,pc1err,pc2err)
            hues.append(hue)
            hues_err.append(hue_err)

        # Determine hardness values
        hardness = []
        hardness_err = []
        for obsid, group in bestdata.groupby('obsids'):
            df = db[db.obsids==obsid].dropna(subset=['flux_i3t16_s6p4t9p7_h9p7t16'])
            hardness.append(df.hardness_i3t16_s6p4t9p7_h9p7t16.values[0])
            hardness_err.append(df.hardness_err_i3t16_s6p4t9p7_h9p7t16.values[0])

        # Plot details
        index_to_del = []
        for ih, h in enumerate(hues_err):
            if h > 30:
                index_to_del.append(ih)
        hues = [i for j, i in enumerate(hues) if j not in index_to_del]
        hues_err = [i for j, i in enumerate(hues_err) if j not in index_to_del]
        hardness = [i for j, i in enumerate(hardness) if j not in index_to_del]
        hardness_err = [i for j, i in enumerate(hardness_err) if j not in index_to_del]
        
        # Plot details
        x = hues
        y = hardness
        xerror = hues_err
        yerror = hardness_err
        values = graph.data.values(x=x, y=y, dx=xerror, dy=yerror)

        myticks = []

        if yposition[z]!=0.0:
            xtitle = ""
            xtexter=empty()
        else:
            xtitle = "Hue ($^{\circ}$)"
            xtexter=graph.axis.texter.mixed()
        if xposition[z]!=0.0:
            ytitle = ""
            ytexter=empty()
        else:
            ytitle="Hardness"
            ytexter=graph.axis.texter.mixed()
        if len(objects) == 7 and yposition[z]==6.0 and xposition[z]==6:
            xtitle = "Hue ($^{\circ}$)"
            xtexter=graph.axis.texter.mixed()
            myticks = [graph.axis.tick.tick(0, label=" ", labelattrs=[text.mathmode])]
        if len(objects) == 7 and yposition[z]==6.0 and xposition[z]==12:
            xtitle = "Hue ($^{\circ}$)"
            xtexter=graph.axis.texter.mixed()

        g=c.insert(graph.graphxy(width=6.0,
                                 height=6.0,
                                 xpos=xposition[z],
                                 ypos=yposition[z],
                                 x=graph.axis.lin(min=0, max=360,title=xtitle,texter=xtexter,manualticks=myticks),
                                 y=graph.axis.lin(min=0.5, max=1.9,title=ytitle,texter=ytexter)))

        # Plot Neutron Stars
        grey= color.cmyk(0,0,0,0.5)
        nsstyle = [graph.style.symbol(size=0.1, symbolattrs=[grey])]
        g.plot(graph.data.values(x=x_ns, y=y_ns), nsstyle)

        g.plot(values,[graph.style.symbol(symbolattrs=[color.rgb.red],size=0.1), graph.style.errorbar(errorbarattrs=[color.rgb.red])])
        xtext, ytext = g.pos(345, 1.85)
        g.text(xtext,ytext, names[obj], [text.halign.boxright, text.valign.top])

    # title = huerange.replace('_', '$^{\circ}$-') + '$^{\circ}$'
    # c.text(6.0,yposition[-1]+6.5,title,
    #        [text.halign.center, text.valign.bottom, text.size.Large])

    outputfile = '/scratch/david/master_project/plots/publication/hh/pane_%i' %nr
    c.writePDFfile(outputfile)
    os.system('convert -density 300 '+outputfile+'.pdf -quality 90 '+outputfile+'.png')


if __name__=='__main__':

    nr = 1
    pane = ['4U_0614p09',
            '4U_1636_m53',
            '4U_1702m43',
            '4u_1705_m44',
            '4U_1728_34',
            'aquila_X1',
            'cir_x1',
            'cyg_x2',
            'EXO_0748_676',
            'gx_17p2',
            'gx_3p1',
            'gx_340p0']
    plotpcpane(pane, nr)

    nr = 2
    pane = ['gx_349p2',
            'gx_5m1',
            'HJ1900d1_2455',
            'IGR_J00291p5934',
            'IGR_J17480m2446',
            'IGR_J17498m2921',
            'KS_1731m260',
            'xte_J1808_369',
            'S_J1756d9m2508',
            'sco_x1',
            'sgr_x1',
            'sgr_x2']
    plotpcpane(pane, nr)

    nr = 3
    pane = ['v4634_sgr',
            'XB_1254_m690',
            'xte_J0929m314',
            'J1701_462',
            'xte_J1751m305',
            'xte_J1807m294',
            'xte_J1814m338']
    plotpcpane(pane, nr)

    nr = 4
    pane = ['gx_339_d4','H1743m322','xte_J1550m564']
    plotpcpane(pane, nr)