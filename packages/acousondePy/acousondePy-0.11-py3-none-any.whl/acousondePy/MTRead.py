# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 17:20:02 2020

@author: sven
"""



from scipy.io.wavfile import write
import numpy as np
import pandas as pd
from datetime import datetime,date, timedelta
#import warnings
from os import path
from struct import unpack
import matplotlib.pyplot as plt

def MTread(fn,slMode='s',leng=0,start=0, wav_out=None, outpath='Default Folder',header=None):
    """
     Reads Acousonde MT files
    
    Read in Acousonde MT files either from start to end or within a range

    Parameters
    ----------
    fn : str
        Path to the MT file.
    slMode : str, optional
        Start and length mode, defines the input units for 
        length (leng) and start. Either 'p' for points or 
        's' for seconds. 
        The default is 's'.
    leng : int, optional
        length of the datapoints to be read in. Defaults to 0 
        which reads in the entire dataset. Units are either 
        in seconds or in number of points dependent on 
        slMode. The default is 0.
    start : int, optional
        Starting point. Defaults to 0, which starts from the 
        beginning of the file.Units are either in seconds 
        or in number of points dependent on slMode. The default is 0.
    wav_out : str, optional
        Path and filename to the wav file to be written. 
        None - doesn't create an output. The default is None.

    Returns
    -------
    
    float64: results
    
    dict: Header
                - totalhdrs - total number of headers 
                - abbrev - abbrevation HiFreuency or Low Frequency etc. 
                - stationcode - Station Code A two digit    code 
                - title - Title defined during recording
                - Date and time info: month, day, year, hours, minutes, seconds, msec
                - sampling_period - Sampling Periond in seconds
                - samplebits - size of each sample
                - wordsize and caltype define the binary coding and endian type
                - calmin and calmax tune the output
                - calunits - the output units)
    dict: Metadata 
                - filename
                - filesize
                - srate - sampling rate 
                - when - start of recording
                - datenumber - numeric datetime
                - whenC - time of first sample
                - nsamp - number of samples in files, seconds - duration of file
  
    """
    #check variables
    try:
        fn
    except NameError:
        raise Warning('Filename fn needs to be defined!')
        
    try:
        slMode
    except NameError:
        warnings.warn('slMode - the start and length mode was not defined...defaulting to s for seconds')
        slMode = 's'
    if slMode.upper() not in ['S','P']:
        warnings.warn('slMode - the start and length mode has to be either s for seconds or p for points...defaulting to s for seconds')
        slMode = 's'
    
    try:
        leng
    except NameError:
        warnings.warn('leng - the length of the data to be read in was not defined...defaulting to leng = 0, reading in all data')
        leng = 0
    if type(leng) != int:
        warnings.warn('leng - the length of the data has to be an integer...defaulting to leng = 0, reading in all data')
        leng = 0
        
    try:
        start
    except NameError:
        warnings.warn('start - the starting point or time was not defined...defaulting to start = 0, reading from the start')
        start = 0
    if type(leng) != int:
        warnings.warn('start - the starting point or time was not defined...defaulting to start = 0, reading from the start')
        start = 0
    
    # Create empty dictionaries
    HEADER = {}
    INFO = {}
    
    if leng==0: leng = np.inf
    
    #check if auxiliary data
    vcode = path.basename(fn)[2]
    aux = True if vcode in ['I','J','K','P','T','X','Y','Z'] else False
       
    #open the binary file and start reading
    with open(fn, "rb") as f:
        magicstring = f.read(8).decode('ascii').strip().strip('\x00')
        if magicstring == 'DATA':
            print(datetime.now().strftime("%H:%M:%S") + ' - Found Data...')
            print(datetime.now().strftime("%H:%M:%S") + ' - Getting Header information...')
            HEADER['totalhdrs'] = int(f.read(3).decode('ascii').strip().strip('\x00'))
            HEADER['abbrev   '] = f.read(8).decode('ascii').strip().strip('\x00')
            HEADER['stationcode'] = f.read(3).decode('ascii').strip().strip('\x00')
            HEADER['title'] = f.read(82).decode('ascii').strip().strip('\x00')
            HEADER['month'] = (f.read(3).decode('ascii').strip().strip('\x00'))
            HEADER['day'] = (f.read(3).decode('ascii').strip().strip('\x00'))
            HEADER['year'] = (f.read(5).decode('ascii').strip().strip('\x00'))
            HEADER['hours'] = (f.read(3).decode('ascii').strip().strip('\x00'))
            HEADER['minutes'] = (f.read(3).decode('ascii').strip().strip('\x00'))
            HEADER['seconds'] = (f.read(3).decode('ascii').strip().strip('\x00'))
            HEADER['msec'] = (f.read(4).decode('ascii').strip().strip('\x00'))
            HEADER['sampling_period'] = float(f.read(15).decode('ascii').strip().strip('\x00'))
            HEADER['samplebits'] = int(f.read(3).decode('ascii').strip().strip('\x00'))
            HEADER['wordsize'] = int(f.read(2).decode('ascii').strip().strip('\x00'))
            
            #if HEADER['wordsize'] < HEADER['samplebits']/8:
                #warnings.warn('The samplebits field Does not fit the wordsize field. --- This file may be bad. ')
            HEADER['typemark'] = f.read(1).decode('ascii').strip().strip('\x00')
        
            HEADER['swapping'] = f.read(1).decode('ascii').strip().strip('\x00')
            
            HEADER['signing'] = f.read(1).decode('ascii').strip().strip('\x00')
            HEADER['caltype'] = f.read(1).decode('ascii').strip().strip('\x00')
            HEADER['calmin'] = float(f.read(15).decode('ascii').strip().strip('\x00'))
            HEADER['calmax'] = float(f.read(15).decode('ascii').strip().strip('\x00'))
            HEADER['calunits'] = f.read(40).decode('ascii').strip().strip('\x00')
            HEADER['recordsize'] = int(f.read(6).decode('ascii').strip().strip('\x00'))
            HEADER['sourcevers'] = f.read(9).decode('ascii').strip().strip('\x00')
            HEADER['sourcesn'] = f.read(16).decode('ascii').strip().strip('\x00')
            print(HEADER)
        
            print(datetime.now().strftime("%H:%M:%S") + ' - Getting Meta data...')
            INFO['filename'] = fn
            INFO['filesize'] = path.getsize(fn)
            INFO['srate'] = 1/HEADER['sampling_period']
            INFO['when'] = datetime.strptime(HEADER['year'] + '/' + HEADER['month'] + '/' + HEADER['day'] + ' ' +  HEADER['hours'] + ':' + HEADER['minutes'] + ':'  + HEADER['seconds'] + '.' + HEADER['msec'],'%Y/%m/%d %H:%M:%S.%f')
            INFO['datenumber'] = date.toordinal(INFO['when'])
            
            print(datetime.now().strftime("%H:%M:%S") + ' - Reading Data...')
            if slMode.upper() == 'P':      # Start & Length specified in # Points (samples)
                INFO['whenC'] = INFO['when'] + timedelta(seconds=start/INFO['srate'])
                INFO['datenumber'] = INFO['datenumber'] + (start/INFO['srate']/24/3600)
            else:
                INFO['whenC'] = INFO['when'] + timedelta(seconds=start) # Corrected start time (with offset)
                INFO['datenumber'] = INFO['datenumber'] + start/24/3600
            
            if 'wordsize' in HEADER:
                if HEADER['wordsize'] == '':
                    HEADER['wordsize'] = 2
            else:
                HEADER['wordsize'] = 2
            
            INFO['nsamp'] = int((INFO['filesize'] - 512 * HEADER['totalhdrs']) / HEADER['wordsize'])
            INFO['seconds'] = INFO['nsamp'] / INFO['srate']
            
        if leng > 0:  #  Only load data if it's been asked for.
            if any(x in HEADER['swapping'] for x in ['S','L','s','l']):
                mode = '<'
            else:
                mode = '>'
                
        status = 0
        if slMode.upper() == 'P':    # specified start time in sample 'P'oints rather than time
            try:
                f.seek(int(512 * HEADER['totalhdrs']) + int(start) * HEADER['wordsize']) # Skip by samples/points
            except:
                status = 1
        else:
            try:
                f.seek(int(512 * HEADER['totalhdrs']) + round(start * INFO['srate'] * HEADER['wordsize'])) # skip by time (seconds)
            except:
                status = 1
        
        if status == 0: # If status is nonzero, we probably went past the end of the file.
            if HEADER['caltype'].upper() == 'F':
                if not any(x == HEADER['wordsize'] for x in [4,8]):
                    f.close(f)
                    #raise Warning('Invalid word size! Only valid Float sizes are four or eight bytes.')
                binType = 'float' + str(HEADER['wordsize'] * 8)
            else:
                binType = 'bit' + str(HEADER['wordsize'] * 8)
                if any(x in HEADER['signing'] for x in ['U','u']):
                    binType = 'u' + binType
            
            
            if slMode.upper() == 'P':
                if leng == np.inf:
                    fi = f.read()
                else:
                    fi = f.read(leng)
                
            else:
                if leng == np.inf:
                    fi = f.read()
                else:
                    fi = f.read(int(leng*INFO['srate'])*2)
            if aux:
                fmt = '%c%iH' %(mode,len(fi)/2)
            else:
                fmt = '%c%ih' %(mode,len(fi)/2)
            p = unpack(fmt,fi)
                
            calmax = HEADER['calmax']
            calmin = HEADER['calmin']
            
            if (type(calmin) == float and type(calmax) == float and ((calmin + np.spacing(1)) < calmax) and HEADER['caltype'].upper() != 'F'):
                calmax = HEADER['calmax']
                calmin = HEADER['calmin']
                if HEADER['signing'].upper() == 'U':
                    bitmin = 0
                    bitmax = 2**HEADER['samplebits'] - 1
                else:
                    bitmin = -(2**(HEADER['samplebits']-1))
                    bitmax = (2**(HEADER['samplebits']-1)) - 1
                    
                
                multiplier = (calmax - calmin) / (bitmax - bitmin)
                p = (np.array(p) - bitmin) * multiplier + calmin
            else:
                p = []# Output an empty matrix if requested data is beyond the length of the current file
            
        else:
            p = [] # Also output an empty matrix of zero length LENGTH input is requested (ie, only return header/info values)
            INFO['count'] = 0
    print(datetime.now().strftime("%H:%M:%S") + ' - Returning data...')
    
    #check if it is a data or aux file
    
    if aux:
        p = pd.DataFrame({'Value':p})
        p['VarCode'] = vcode
        p['mission'] = HEADER['title'].split('-')[0]   
        p['sampling_rate'] = HEADER['sampling_period']
        p['nSample'] = np.arange(1,p.shape[0]+1)
        p['start_time'] = pd.to_datetime(HEADER["year"] + "-" + HEADER["month"] + "-" + HEADER["day"] + " " + HEADER["hours"] + ":" +\
          HEADER["minutes"] + ":" + HEADER["seconds"] + "." + HEADER["msec"])
        p['sec_since_start'] = p['nSample'] * p['sampling_rate']
        p['Time'] = p['start_time'] + pd.to_timedelta(p['sec_since_start'], unit='s')
        return(p,HEADER,'aux')
    else:
        if wav_out != None:
            print(datetime.now().strftime("%H:%M:%S") + ' - Saving wav file...' + HEADER['title'].split('-')[0] )
            if 'p':
                if outpath=='Default Folder':
                    outpath = path.dirname(fn)
                outfn = outpath +'\\' + INFO['when'].strftime('D%m%d%YT%H%M%S') + '_' + path.basename(fn)[:-3]  + '.wav'
                sr = int(INFO['srate'])
                data = p
                write(outfn,int(sr), np.int16(data/(abs(data).max())*np.iinfo(np.int16).max))
        
        if header != None:
            if outpath=='Default Folder':
                outpath = path.dirname(fn)
            hh = pd.DataFrame.from_dict(HEADER, orient='index')
            hh.to_csv( outpath +'\\' + INFO['when'].strftime('D%m%d%YT%H%M%S') + '_' + path.basename(fn)[:-3] + '.csv')
        if 'p':
            return p,HEADER,INFO
        
        


def spec_plot(p,head,inf,mode='psd',cmap='inferno',NFFT=512, noverlap=128, detrend='none', cmin=None,cmax=None, plot = False):
    """
    Creates a plot
    
    Plots raw data and spectrogram
    
    Parameters
    ----------
    p : float64
        raw data as generted by MTread().
    head : dict
        Header information as generated by MTread().
    inf : dict
        Meta data as generated by MTread().
    mode : TYPE, optional
        psd - power spectral density
        magnitude
        angle
        phase.
        
        The default is 'psd'.
    cmap : str, optional
        name of colormap for spctrogram . The default is 'inferno'.
    NFFT : int, optional
        The number of data points used in each block for the FFT. (power 2 most effictient). The default is 512.
    noverlap : int, optional
        The number of points of overlap between blocks.. The default is 128.
    detrend : str, optional
        function applied before fft-ing: none for none, mean for dtrend_mean, linear for dtrend_linear. The default is 'none'.
    cmin : float, optional
        minimum color value, None - takes the data minimum . The default is None.
    cmax : float, optional
        aximum color value, None - takes the data maximum. The default is None.
    plot : boolean, optional
        Show plot. The default is False.

    Returns
    -------
    - spectrum (2D array): successive time segments (columns) by frequencies (rows)
    - freqs (1D array): frequencies corresponding to the rows in the spectrum
    - t (1D array): times corresponding to the midpoints of the segments in the spectrum
    - im (AxesImage): the spectrogram image
    
    """
    
    #get time which is the sample number x the sampling period
    t=np.arange(0,len(p)) * head['sampling_period']
    
    #create a new plot
    if plot is True:
        fig, axes = plt.subplots(figsize=(13.6, 7.68))
        
    #define data axis
    # (4,60) - 4 for rows, apanning over 3 and 60 for columns, spanning over 57 to have a small legend
    # (1,0) - starting at row 1 and column 0
    ax1 = plt.subplot2grid((40, 60), (0, 0), rowspan=9,  colspan=57)
    ax1.plot(t[1:], p[1:],color='k')
    
    #define spectrogram axis
    # (4,60) - 4 for rows, apanning over 3 and 60 for columns, spanning over 57 to have a small legend
    # (1,0) - starting at row 1 and column 0
    ax2 = plt.subplot2grid((40, 60), (12, 0), rowspan=28,  colspan=57)
    #create spectrogram
    Pxx, freqs, bins, im = ax2.specgram(p[1:], NFFT=NFFT, 
                                        Fs=inf['srate'], 
                                        mode=mode,
                                        noverlap=noverlap,
                                        detrend=detrend, 
                                        cmap=cmap)
    if cmin or cmax is None: 
        if mode == 'psd': 
            vals = 10 * np.log10(Pxx) 
        elif mode == 'magnitude':
            vals = 20 * np.log10(Pxx)
        else: 
            vals = Pxx
        if cmin is None: cmin = np.floor(np.min(vals))
        if cmax is None: cmax = np.ceil(np.max(vals))
    
    im.set_clim(cmin,cmax)
    #set x limits to ensure same scale
    ax1.set_xlim([np.floor(t.min()),np.ceil(t.max())])
    ax2.set_xlim([np.floor(t.min()),np.ceil(t.max())])
    
    
    #colorbar
    ax3 = plt.subplot2grid((4, 60), (1, 59),rowspan=3)
    cbar = plt.colorbar(im, cax=ax3)
    
    #Axes labels and titles
    ax1.set_ylabel('Amplitude')
    
    ax2.set_xlabel('Time [s] since ' + str(inf['whenC']))
    ax2.set_ylabel('Frequency [Hz]')
    if mode == 'magnitude':
        ax2.set_title('Magnitude Spectrogram')
    elif mode == 'angle':
        ax2.set_title('Angular Spectrogram')
    elif mode == 'phase':
        ax2.set_title('Phase Spectrogram')
    elif mode == 'psd':
        ax2.set_title('Power Spectral Density')
    if plot is True:
        plt.show()
    
    return Pxx, freqs, bins, im

def read_multiple_MT(fns, op='Default Path', header=True,wav_out=True, aux_out=True):
    """
    Reads multiple Acousonde MT files
    
    Read in full Acousonde MT


    Parameters
    ----------
    fns : list
        List of MT file paths.
    op : character, optional
        Output directory, path to where the output files should be saved. The default is 'Default Path'.
    header : boolean, optional
        If True, heade rinformation will be saved in the output directory as a csv files. The default is True.
    wav_out : boolean, optional
        If True, a wav file will be saved in the output directory. The default is True.
    aux_out : boolean, optional
        If True, auxiliary information for all files will be concatenated and saved as cav file. The default is True.

    Returns
    -------
    None.

    """
    aux = pd.DataFrame()
    for fn in fns:
        if op=='Default Path':
            op = path.dirname(fn)
        h = 'HEADER' if header else None
        w = 'out' if wav_out else None
        
        p, header, info = MTread(fn,slMode='s',leng=0,start=0, wav_out=w,outpath=op,header=h)
        
        if info == 'aux':
            aux = pd.concat([aux,p])
        
    print(datetime.now().strftime("%H:%M:%S") + ': Reshaping data to get one column for each dataset')
    if aux_out:
        if len(aux) > 0:
            aux = aux.pivot_table(index = ['mission','Time','sampling_rate'], columns='VarCode', values='Value')
            aux.rename(columns={'I':'acc_X'}, inplace=True)
            aux.rename(columns={'J':'acc_Y'}, inplace=True)
            aux.rename(columns={'K':'acc_Z'}, inplace=True)
            aux.rename(columns={'P':'Pressure'}, inplace=True)
            aux.rename(columns={'T':'Temperature'}, inplace=True)
            aux.rename(columns={'X':'comp_X'}, inplace=True)
            aux.rename(columns={'Y':'comp_Y'}, inplace=True)
            aux.rename(columns={'Z':'comp_Z'}, inplace=True)
            aux = pd.DataFrame(aux)
            aux.to_csv(path.normpath(op + '/' + aux.reset_index()['Time'].min().strftime('D%m%d%YT%H%M%S') + '_auxiliary.csv'))