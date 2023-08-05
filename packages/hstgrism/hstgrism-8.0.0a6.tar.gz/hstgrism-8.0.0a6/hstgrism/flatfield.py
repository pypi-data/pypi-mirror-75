# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class FlatField:
    '''
    FlatField (using python 3) computes a flatfield image in aXe definition.
    This requires flatfile produced for aXe, and tracefile produced by hstgrism package.
    flat.flatfile to see the path to flatfile.
    flat.data to see inputs for the computation.
    flat.compute() to compute the flatfield image.
    flat.flatfield to see the flatfield image array.
    flat.show(...) to imshow flatfield.
    flat.save(...) to save as *_flat.fits.
    '''
    def __init__(self,container,flatfile,tracefile):
        self.container = container
        self.flatfile = flatfile
        self.tracefile = tracefile
        self.data = {'WMIN':None,
                     'WMAX':None,
                     'FLAT':None,
                     'NAX1':None,
                     'NAX2':None,
                     'WW':None
                    }
        self.flatfield = None
        self._get()
    def _get(self):
        # basic info
        tmp = fits.open(self.flatfile)
        wmin,wmax = tmp[0].header['WMIN'],tmp[0].header['WMAX']
        nax1,nax2 = tmp[0].header['NAXIS1'],tmp[0].header['NAXIS2']
        self.data['WMIN'] = wmin
        self.data['WMAX'] = wmax
        self.data['NAX1'] = nax1
        self.data['NAX2'] = nax2
        # flat
        n = len(tmp)
        tmpp = {}
        for i in range(n):
            tmpp[i] = tmp[i].data.copy()
        self.data['FLAT'] = copy.deepcopy(tmpp)
        # wavelength
        tmp = pd.read_csv(self.tracefile)
        dldp = tmp['DLDP']
        m = np.isfinite(dldp)
        dldp = dldp[m].values
        xg = np.arange(self.data['NAX1'])
        xref = tmp['XREF'][0]
        xh = xg-xref
        ww = np.full_like(xh,0.,dtype=float)
        for i,ii in enumerate(dldp):
            ww += ii * np.power(xh,i)
        self.data['WW'] = ww
        self.data['XG'] = xg
        self.data['XREF'] = xref
    ##########
    ##########
    ##########
    def compute(self):
        # dimension test
        if self.data['WW'].shape[0] != self.data['NAX1']:
            raise ValueError('Dimension of WW != NAX1')
        # set parametric wavelength [0,1]
        wmin,wmax,ww = self.data['WMIN'],self.data['WMAX'],self.data['WW']
        paramww = (ww-wmin)/(wmax-wmin)
        paramww[paramww<0.] = 0.
        paramww[paramww>1.] = 1.
        paramww,_ = np.meshgrid(paramww,np.arange(self.data['NAX2']))
        # compute
        tmp = self.data['FLAT']
        tmpp = np.full_like(paramww,0.,dtype=float)
        for i in tmp:
            tmpp += tmp[i] * np.power(paramww,i)
        self.flatfield = tmpp.copy()
    ##########
    ##########
    ##########
    def save(self):
        hdu = fits.PrimaryHDU()
        hdul = fits.HDUList([hdu])
        hdul[0].header['NAXIS'] = 2
        hdul[0].header['EXTEND'] = False
        hdul[0].header['DESC'] = 'Flatfield for hstgrism'
        hdul[0].header['NAX1'] = self.data['NAX1']
        hdul[0].header['NAX2'] = self.data['NAX2']
        hdul[0].header['FLAT'] = self.flatfile
        hdul[0].header['TRACE'] = self.tracefile
        hdul[0].data = self.flatfield.copy()
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        string = './{1}/{0}_flat.fits'.format(saveprefix,savefolder)
        hdul.writeto(string,overwrite=True)
        print('Save {0}'.format(string))
    ##########
    ##########
    ##########
    def show(self,save=False,
             params={'figsize':(10,10),
                     'minmax':(5.,99.),
                     'cmap':'viridis',
                     'fontsize':12
                    }
            ):
        figsize = params['figsize']
        minmax = params['minmax']
        cmap = params['cmap']
        fontsize = params['fontsize']
        plt.figure(figsize=figsize)
        tmpp = self.flatfield
        vmin,vmax = np.percentile(tmpp,minmax[0]),np.percentile(tmpp,minmax[1])
        plt.imshow(self.flatfield,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        saveformat = self.container.data['plotformat']
        string = './{1}/{0}_flat.fits'.format(saveprefix,savefolder)
        plt.title(string,fontsize=fontsize)
        plt.tight_layout()
        if save:
            string = './{2}/{0}_flat.{1}'.format(saveprefix,saveformat,savefolder)
            plt.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
    
    