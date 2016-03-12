#!/usr/bin/env python

"""
Script to stack _mesh.log files from grainsweeper into 3D volume
Jette Oddershede, DTU Fysik, April 2013, jeto@fysik.dtu.dk
(Updated 26.02.2015 mkak)
"""

import sys
from string import split
import argparse
import textwrap
import os
import numpy as np
import math

def stacking(args,ndigits):

    #Generat files and trans 
    #For internal algorith purposes it is desirable that files[0] corresponds to 
    #the smallest z-values and thus goes first in the output file
    files = []
    trans = []

    if args.zstep > 0:
        irange = range(args.layer_start,args.layer_end+1)
    else:
        irange = range(args.layer_end,args.layer_start-1,-1)
        args.zstep = abs(args.zstep)


    for i in irange:
        fmtstr = '%s%0' + str(int(ndigits[i])) + 'd%s.log'
        filename = fmtstr % (args.inputstem,i,args.endstem)

        files.append(filename)
        trans.append(args.zstart+args.zstep*(i-irange[0]))
    
    #### Read files and store data in lines
    lines = {}
    nvx = []
    nvy = []
    nvz = []
    xmin = []
    xmax = []
    ymin = []
    ymax = []
    zmin = []
    zmax = []
    dvx = []
    dvy = []
    dvz = []
    for i in range(args.nlayers):
        f=open(files[i],'r')
        lines["%0.3d" %i] = f.readlines()
        f.close()

        nvx.append(eval(split(lines["%0.3d" %i][2])[0]))
        nvy.append(eval(split(lines["%0.3d" %i][2])[1]))
        nvz.append(eval(split(lines["%0.3d" %i][2])[2]))
        xmin.append(eval(split(lines["%0.3d" %i][2])[3]))
        xmax.append(eval(split(lines["%0.3d" %i][2])[4]))
        ymin.append(eval(split(lines["%0.3d" %i][2])[5]))
        ymax.append(eval(split(lines["%0.3d" %i][2])[6]))
        zmin.append(i*args.zstep+eval(split(lines["%0.3d" %i][2])[7]))
        zmax.append(i*args.zstep+eval(split(lines["%0.3d" %i][2])[8]))
        dvx.append((xmax[i]-xmin[i])/(nvx[i]-1))
        dvy.append((ymax[i]-ymin[i])/(nvy[i]-1))
        dvz.append((zmax[i]-zmin[i])/(nvz[i]-1))

    if args.verbose:
        print nvx,nvy,nvz,zmin,zmax,dvx,dvy,dvz


    ### Assert that maps are of same size and determine overlap
    noverlaps = []
    for i in range(1,args.nlayers):
        assert dvx[i] == dvx[i-1], "Pixel size along x does not agree"
        assert dvy[i] == dvy[i-1], "Pixel size along y does not agree"
        assert dvz[i]-dvz[i-1]< 0.0001, "Pixel size along z does not agree %i %i %f %f" %(i-1,i,dvz[i-1],dvz[i])
        assert xmin[i] == xmin[i-1], "xmin does not agree"
        assert ymin[i] == ymin[i-1], "ymin does not agree"
        assert xmax[i] == xmax[i-1], "xmax does not agree"
        assert ymax[i] == ymax[i-1], "ymax does not agree"
        noverlaps.append(int(round((zmax[i-1]-zmin[i])/dvz[i]))+1)

    for i in range(1,len(noverlaps)):
    #    print i,noverlaps[i],noverlaps[i-1]
        assert noverlaps[i] == noverlaps[i-1], "Number of slices to stitch layers is not constant"

    if args.verbose:
        print noverlaps

    #make lists of pixel names and values in xyz
    vid = range(nvx[0]*nvy[0]*(sum(nvz)-sum(noverlaps)))
    xid = []
    yid = []
    zid = []
    xval = []
    yval = []
    zval = []
    zcontrib = []
    for k in range(sum(nvz)-sum(noverlaps)):
        zcontrib.append([])
        for j in range(nvy[0]):
            for i in range(nvx[0]):
                xid.append(i)
                yid.append(j)
                zid.append(k)
                xval.append(xmin[0]+i*dvx[0])
                yval.append(ymin[0]+j*dvy[0])
                zval.append(args.zstart+zmin[0]+k*dvz[0])

    #print vid[0:10],vid[-10:]
    #print xid[0:10],xid[-10:]
    #print yid[0:10],yid[-10:]
    #print zid[0:10],zid[-10:]
    #print xval[0:10],xval[-10:]
    #print yval[0:10],yval[-10:]
    #print zval[0:10],zval[-10:]

    k = 0
    for i in range(args.nlayers):
        for j in range(nvz[0]):
            zcontrib[k].append(i)
            k = k + 1
        k = k - noverlaps[0]

    #if args.verbose:
    #    print zcontrib

    #preample
    outputlines = []
    outputlines.append("file %s\n" % args.output)
    outputlines.append(lines["%0.3d" %0][1])
    outputlines.append("%i %i %i %f %f %f %f %f %f\n" %(nvx[0],nvy[0],sum(nvz)-sum(noverlaps),xmin[0],xmax[0],ymin[0],ymax[0],zmin[0],zmax[-1]))
    for i in range(3,9):
        outputlines.append(lines["%0.3d" %0][i])

    #loop through layers and add info:
    nv = 0
    lineno0 = 9
    lineno1 = 9
    for k in range(len(zcontrib)):
        if args.verbose:
            print k,len(zcontrib),zcontrib[k],lineno0,lineno1,nv
        #non-overlapped
        if len(zcontrib[k])==1:
            for j in range(nvx[0]*nvy[0]):
                nsolutions = eval(split(lines["%0.3d" %zcontrib[k][0]][lineno0])[7])
                outputlines.append("%i %i %i %i %f %f %f %i\n" %(vid[nv],xid[nv],yid[nv],zid[nv],xval[nv],yval[nv],zval[nv],nsolutions))
                lineno0 = lineno0 + 1
                for i in range(3+nsolutions):
                    outputlines.append(lines["%0.3d" %zcontrib[k][0]][lineno0])
                    lineno0 = lineno0 + 1
                del(nsolutions)
                nv = nv + 1        
        #overlapped
        else:
            for j in range(nvx[0]*nvy[0]):
                nsolutions0 = eval(split(lines["%0.3d" %zcontrib[k][0]][lineno0])[7])
                nsolutions1 = eval(split(lines["%0.3d" %zcontrib[k][1]][lineno1])[7])
                #print lines["%0.3d" %zcontrib[k][0]][lineno0],lineno0
                #print lines["%0.3d" %zcontrib[k][1]][lineno1],lineno1
                if nsolutions0 == 0:
                    completeness0 = 0
                    lineno0 = lineno0 + 4
                else:
                    tmp0 = lines["%0.3d" %zcontrib[k][0]][lineno0+2]
                    completeness0 = split(tmp0)[-1]
                    lineno0 = lineno0 + 5
                    if completeness0 == '-nan':
                        completeness0 = 0
                    else:
                        completeness0 = eval(completeness0)
                if nsolutions1 == 0:
                    completeness1 = 0
                    lineno1 = lineno1 + 4
                else:
                    tmp1 = lines["%0.3d" %zcontrib[k][1]][lineno1+2]
                    completeness1 = split(tmp1)[-1]
                    lineno1 = lineno1 + 5
                    if completeness1 == '-nan':
                        completeness1 = 0
                    else:
                        completeness1 = eval(completeness1)
                #print "***",vid[nv],xid[nv],yid[nv],zid[nv],xval[nv],yval[nv],zval[nv],nsolutions0,nsolutions1,completeness0,completeness1
                if completeness0 == 0 and completeness1 == 0:
                    outputlines.append("%i %i %i %i %f %f %f %i\n" %(vid[nv],xid[nv],yid[nv],zid[nv],xval[nv],yval[nv],zval[nv],0))
                    for i in range(3):
                        outputlines.append("\n")
                    #print outputlines[-4:-1]
                else:
                    outputlines.append("%i %i %i %i %f %f %f %i\n" %(vid[nv],xid[nv],yid[nv],zid[nv],xval[nv],yval[nv],zval[nv],1))
                    outputlines.append("\n")
                    if completeness0 > completeness1:
                        outputlines.append(tmp0)
                    else:
                        outputlines.append(tmp1)
                    for i in range(2):
                        outputlines.append("\n")
                    #print outputlines[-5:-1]
                    #break
                nv = nv + 1
            if args.verbose:
                print k,len(zcontrib),zcontrib[k],lineno0,lineno1,nv
            if zcontrib[k] != zcontrib[k+1]:
                lineno0 = lineno1
                lineno1 = 9



    f=open(args.output,'w')
    for i in range(len(outputlines)):
        f.write(outputlines[i])
    f.close()

    #print outputlines

def main(args):

    if args.layer_start < 0 or args.layer_end < 0:
        raise IOError('Layer number cannot be negative.')
    if args.layer_start > args.layer_end :
        raise IOError('Layer start must be less than layer end. Try using a negative sign for zstep.')

    if not args.endstem:
        args.endstem = '_mesh'
    args.nlayers = args.layer_end+1-args.layer_start
    
    ## Creates an array of integers indicating number of digits in file name
    ndigits = np.zeros( ( args.layer_end+1) )
    for i in range(args.layer_start,args.layer_end+1):
        if i > 9: 
            digits = int(math.log10(i))+1
        else:
            digits = 1
        for j in range(digits,7):            
            fmtstr = '%s%0' + str(j) + 'd%s.log'
            first_im_name = fmtstr % (args.inputstem, i,args.endstem)
            if os.path.exists(first_im_name):
                ndigits[i] = j
                if args.verbose:
                    print('Found file: %s' % first_im_name)
                break
        if ndigits[i] == 0:
            raise RuntimeError('No file found matching format %s#%s.log for layer %i.' % (args.inputstem,args.endstem,i))

    if not args.output:
        args.output = "merged_%s_%0.3d_%0.3d.log" %(args.inputstem.split('_')[0],args.layer_start,args.layer_end)
    if os.path.exists(args.output) and args.force is False:
        raise IOError('%s already exists.' % args.output)
        
    stacking(args,ndigits)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='stack_layers.py',
        description='Finds peaks in area detector image series.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog=textwrap.dedent('''
#             examples:
# 
#             $ 
#             $ stack_layers.py 1 2 0 -0.1 austenite1_l
#             ''')
        )

    parser = argparse.ArgumentParser(
        prog='stack_layers',
        description='Meshes together layer files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
         )
    parser.add_argument(
        'layer_start', type=int, help='number of first layer'
        )
    parser.add_argument(
        'layer_end', type=int, help='number of last layer'
        )
    parser.add_argument(
        'zstart', type=float, help='z position of first layer (mm)'
        )
    parser.add_argument(
        'zstep', type=float, help='step in z between layers (mm)'
        )
    parser.add_argument(
        'inputstem', type=str, help='stem of file names, must end #_mesh.log'
        )
    parser.add_argument(
        '-e','--endstem', type=str, default=False,
        help='specify if end of log file is not #_mesh.log'
        )
    parser.add_argument(
        '-o', '--output', type=str, help='output file name',
        )
    parser.add_argument(
        '-f', '--force', default=False, action='store_true',
        help='force removal of report file'
        )  
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='report progress in terminal'
        )
    args = parser.parse_args()
    main(args)
