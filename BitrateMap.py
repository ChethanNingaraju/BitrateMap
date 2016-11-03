import docopt
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

###
# Docopt
###
DOC = """
usage:
   BitrateMap [options] FILE...

options:
     -n, --numFrames=NUMBER        number of frames to be compared
     -o, --overlay=NUMBER          1 = overlay,0 = subplots(default)
     -b, --bitrate=NUMBER          Bitrate in Kbps (If not mentioned delay plot is generated)
"""

###
# Script
###

"""
****************** Startup *****************
"""

# get cmd line arguments
cmdargs = docopt.docopt(DOC, version='bernstein2005 0.1')
if (cmdargs['FILE'] == None) or \
        (cmdargs['--numFrames'] == None):
    print(DOC)
    sys.exit()

inCSVfile= cmdargs['FILE'];
is_overlay = 0;
if (cmdargs['--overlay']) != None:
    is_overlay = int(cmdargs['--overlay']);
bitrate = -1;
##Bitrate plot for the
if (cmdargs['--bitrate']) != None:
    bitrate = int(cmdargs['--bitrate']);

##List to hold the is_coded flag
is_coded = [];
##Holds bits per frame
bits_per_frame = [];
delay_per_frame = [];
##Iternate throug all the files
for numFile in range(0, len(inCSVfile)):
    iscodedColumn = [];
    bits = [];
    delay = [];
    with open(inCSVfile[numFile],"r") as f:
        reader = csv.reader(f);
        for row in reader:
            #print(row);
            if row[0] == "PIC":
                ##The row corresponds to a picture
                if row[2] == "Coded":
                    iscodedColumn.append(1);
                    bits.append(int(row[6]));
                else:
                    iscodedColumn.append(0);
                    bits.append(0);
    if bitrate > 0:
        prev_balance_bits = 0;
        for i in range(0 , len(bits)):
            delay.append((bits[i] + prev_balance_bits) / (bitrate));##Since bitrate is in kbps the output shall be in milli seconds
            prev_balance_bits = prev_balance_bits + bits[i] - (bitrate * 1000/30); #for bits per frame 30 fps is assumed
            ##If it was a skip frame show that in delay plot
            if bits[i] == 0:
                delay[i] = 0;
    #print(sum(bits));
    ##Collect data across all the frames
    is_coded.append(iscodedColumn)
    bits_per_frame.append(bits);
    delay_per_frame.append(delay);



#Generate plots to comapre the results
x_axis = list(range(0,len(bits_per_frame[0])));
if is_overlay == 0:
    fig = plt.figure();
    for i in range(0 , len(inCSVfile)):
        ax = plt.subplot(len(inCSVfile), 1 , i+1);
        ax.plot(x_axis, [x if x != 0 else None for x in bits_per_frame[i]]);
    '''
    for numFile in range(0, len(inCSVfile)):
        ax1 = fig.add_subplot(211);
        ax2 = fig.add_subplot(212);
        ax1.plot(x_axis, [x if x != 0 else None for x in bits_per_frame[0]]);
        ax2.plot(x_axis, [x if x != 0 else None for x in bits_per_frame[1]]);
        '''
    plt.show();
else:
    ##Figure for bitrate plot
    fig = plt.figure();
    axes = plt.gca();
    ##For now remove the top 1% and bottom 1% as outliers
    axes.set_ylim([np.percentile(bits_per_frame[0],1),np.percentile(bits_per_frame[0],99)]);
    for i in range(0, len(inCSVfile)):
        plt.plot(x_axis,[x if x != 0 else None for x in bits_per_frame[i]], linestyle='-', label = inCSVfile[i]);
    legend= plt.legend();
    plt.show();
    ##Figure for delay plot
    fig = plt.figure();
    axes = plt.gca();
    ##For now remove the top 1% and bottom 1% as outliers
    #axes.set_ylim([np.percentile(bits_per_frame[0], 1), np.percentile(bits_per_frame[0], 99)]);
    for i in range(0, len(inCSVfile)):
        plt.plot(x_axis, delay_per_frame[i], linestyle='-', label=inCSVfile[i]);
    legend = plt.legend();
    plt.show();