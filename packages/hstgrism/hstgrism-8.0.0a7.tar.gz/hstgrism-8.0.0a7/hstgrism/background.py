# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from polynomial2d.polynomial2d import Polynomial2D
import os,glob,copy
import json

class Background:
    def __init__(self,container,norder=0,objname='None',gfile=None,tfile='None',
                 automask=True,
                 params_bbox = {'padxleft':15,'padxright':15,'padyup':15,'halfdyup':20,'halfdylow':20,'padylow':15,'adjustx':0,'adjusty':0},
                 rescale=(False,None,None,None),
                 sigclip=(False,None,None)
                ):
        self.container = container
        self.data = {'objname':objname,
                     'gfile':gfile,
                     'tfile':tfile,
                     'automask':automask,
                     'rescale':rescale[0],
                     'rescale_x1':rescale[1],
                     'rescale_x2':rescale[2],
                     'rescale_y':rescale[3],
                     'sigclip':sigclip[0],
                     'sigclip_niter':sigclip[1],
                     'sigclip_sigma':sigclip[2]
                    }
        self.trace = self._trace()
        self.bbox = params_bbox
        self.bbox['bbox'] = self._bbox()
        self.bkg = self._bkg()
        self.bkg.model['NORDER'] = norder
    def _bkg(self):
        rescale = (self.data['rescale'],self.data['rescale_x1'],self.data['rescale_x2'],self.data['rescale_y'])
        sigclip = (self.data['sigclip'],self.data['sigclip_niter'],self.data['sigclip_sigma'])
        tmpdata = fits.open(self.data['gfile'][0])[self.data['gfile'][1]].data
        bb0x,bb1x = self.bbox['bbox']['BBX']
        bb0y,bb1y = self.bbox['bbox']['BBY']
        xg,yg = self.bbox['bbox']['XG'],self.bbox['bbox']['YG']
        tmpp = tmpdata[bb0y:bb1y,bb0x:bb1x]
        ny,nx = tmpp.shape
        x1 = np.arange(nx)
        x2 = np.arange(ny)
        x1v,x2v = np.meshgrid(x1,x2)
        obj = Polynomial2D(x1=x1v,x2=x2v,y=tmpp,rescale=rescale,sigclip=sigclip)
        obj.data['MASK'] = self._mask(obj)
        return obj
    def _mask(self,obj):
        if self.data['automask']:
            tmpmask = np.full_like(obj.data['Y'],False,dtype=bool)
            halfdyup,halfdylow = self.bbox['halfdyup'],self.bbox['halfdylow']
            xgn = (self.bbox['bbox']['XG'] - self.bbox['bbox']['BBX'][0]).astype(int)
            ygn = (self.bbox['bbox']['YG'] - self.bbox['bbox']['BBY'][0]).astype(int)
            minx = int(self.trace['XG'].min()) - self.bbox['bbox']['BBX'][0]
            maxx = int(self.trace['XG'].max()) - self.bbox['bbox']['BBX'][0]
            tracex = np.arange(minx,maxx+1)
            for i,ii in enumerate(xgn):
                if xgn[i] in tracex:
                    tmpx,tmpy = int(xgn[i]),int(ygn[i])
                    tmpmask[tmpy-halfdylow:tmpy+halfdyup+1,tmpx] = True
            return tmpmask
        else:
            tmpmask = np.full_like(obj.data['Y'],False,dtype=bool)
            return tmpmask
    def _trace(self):
        tmp = pd.read_csv(self.data['tfile'])
        mdydx = np.isfinite(tmp['DYDX'].values)
        mdldp = np.isfinite(tmp['DLDP'].values)
        tmpp = {'XREF':tmp['XREF'].values[0],
                'YREF':tmp['YREF'].values[0],
                'XG':tmp['XG'].values,
                'YG':tmp['YG'].values,
                'WW':tmp['WW'].values,
                'DYDX':tmp['DYDX'].values[mdydx],
                'DLDP':tmp['DLDP'].values[mdldp]
               }
        return tmpp
    def _bbox(self):
        xref,yref = self.trace['XREF'],self.trace['YREF']
        maxy,miny = self.trace['YG'].max(),self.trace['YG'].min()
        bb0y,bb1y = int(miny-self.bbox['halfdylow']-self.bbox['padylow']),int(1+maxy+self.bbox['halfdyup']+self.bbox['padyup'])
        maxx,minx = self.trace['XG'].max(),self.trace['XG'].min()
        bb0x,bb1x = int(minx-self.bbox['padxleft']),int(maxx+self.bbox['padxright'])
        xg = np.arange(bb0x,bb1x)
        xh = xg - int(xref)
        dydx = self.trace['DYDX']
        dldp = self.trace['DLDP']
        yh = np.full_like(xh,0.,dtype=float)
        for i,ii in enumerate(dydx):
            yh += ii * np.power(xh,i)
        yg = yh + yref
        ww = np.full_like(xh,0.,dtype=float)
        for i,ii in enumerate(dldp):
            ww += ii * np.power(xh,i)
        return {'BBX':(bb0x,bb1x),'BBY':(bb0y,bb1y),'XG':xg,'YG':yg,'WW':ww}   
    ##########
    ##########
    ##########
    def save(self):
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        # save bkg sub as _sub.fits
        string = './{1}/{0}_sub.fits'.format(saveprefix,savefolder)
        os.system('cp {0} {1}'.format(self.data['gfile'][0],string))
        tmpp = fits.open(string)
        tmppdata = tmpp[self.data['gfile'][1]].data
        bb0x,bb1x = self.bbox['bbox']['BBX']
        bb0y,bb1y = self.bbox['bbox']['BBY']
        y,yfit = self.bkg.data['Y'],self.bkg.model['YFIT']
        ysub = y-yfit
        tmppdata[bb0y:bb1y,bb0x:bb1x] = ysub.copy()
        tmpp.writeto(string,overwrite=True)
        print('Save {0}'.format(string))
        # save bbox
        tmpp = {}
        for j in self.bbox:
            if j!='bbox':
                tmpp[j] = self.bbox[j]
            elif j=='bbox':
                tmpp['BBX'] = self.bbox[j]['BBX']
                tmpp['BBY'] = self.bbox[j]['BBY']
        tmppp = json.dumps(tmpp)
        string = './{1}/{0}_bkgbbox.json'.format(saveprefix,savefolder)
        f = open(string,'w')
        f.write(tmppp)
        f.close()
        print('Save {0}'.format(string))
        # save only bkg replaced in the original as _bkg.fits
        string = './{1}/{0}_bkg.fits'.format(saveprefix,savefolder)
        os.system('cp {0} {1}'.format(self.data['gfile'][0],string))
        tmpp = fits.open(string)
        tmppdata = tmpp[self.data['gfile'][1]].data
        bb0x,bb1x = self.bbox['bbox']['BBX']
        bb0y,bb1y = self.bbox['bbox']['BBY']
        yfit = self.bkg.model['YFIT']
        tmppdata[bb0y:bb1y,bb0x:bb1x] = yfit.copy()
        tmpp.writeto(string,overwrite=True)
        print('Save {0}'.format(string))
        # save self.data
        tmp = copy.deepcopy(self.data)
        tmppp = json.dumps(tmp)
        string = './{1}/{0}_bkgdata.json'.format(saveprefix,savefolder)
        f = open(string,'w')
        f.write(tmppp)
        f.close()
        print('Save {0}'.format(string))
        # save coef
        coef = self.bkg.model['COEF']
        norder = self.bkg.model['NORDER']
        tmp = np.full((norder+1,norder+1),fill_value=None,dtype=float)
        for i in coef:
            tmp[i[0],i[1]] = coef[i]
        string = './{1}/{0}_bkgcoef.csv'.format(saveprefix,savefolder)
        pd.DataFrame(tmp).to_csv(string,index=True)        
        print('Save {0}'.format(string)) 
        # save pcov
        pcov = self.bkg.model['pcov']
        string = './{1}/{0}_bkgpcov.csv'.format(saveprefix,savefolder)
        pd.DataFrame(pcov).to_csv(string,index=True)        
        print('Save {0}'.format(string)) 
        # save maskfit
        maskfit = self.bkg.model['MASKFIT']
        string = './{1}/{0}_bkgmaskfit.csv'.format(saveprefix,savefolder)
        pd.DataFrame(maskfit).to_csv(string,index=True)        
        print('Save {0}'.format(string)) 
    ##########
    ##########
    ##########
    def show_1d(self,save=False,
                params={'figsize':(10,10),
                        'minmax':(5.,99.),
                        'cmap':'rainbow',
                        'fontsize':12,
                        'xpertick':50,
                        'color':'red',
                        'marker':'x',
                        'ls':':',
                        'rotation':90.,
                        'annotate_level':0.
                       }
               ):
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        saveformat = self.container.data['plotformat']
        figsize = params['figsize']
        xpertick = params['xpertick']
        color = params['color']
        marker = params['marker']
        fontsize = params['fontsize']
        rotation = params['rotation']
        annotate_level = params['annotate_level']
        ls = params['ls']
        minmax = params['minmax']
        cmap = params['cmap']
        xref = self.trace['XREF']
        yref = self.trace['YREF']
        tmp = self.bkg.data['Y'] - self.bkg.model['YFIT']
        tmpp = tmp.sum(axis=0)
        tmppp = tmp.sum(axis=1)
        m = np.isfinite(tmp)
        vmin,vmax = np.percentile(tmp[m],minmax[0]),np.percentile(tmp[m],minmax[1])
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(2,2,1)
        ax.imshow(tmp,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        ax.set_title('{0}_bkgsub'.format(saveprefix),fontsize=fontsize)
        ax.set_ylabel('pixY - {0}'.format(int(yref)),fontsize=fontsize)
        ax2 = fig.add_subplot(2,2,2,sharey=ax)
        tmpx = np.arange(len(tmppp))
        ax2.plot(tmppp,tmpx)
        ax2.plot(np.full_like(tmppp,0.,dtype=float),tmpx,':')
        ax2.set_xlabel('cps',fontsize=fontsize)
        ax = fig.add_subplot(2,2,3,sharex=ax)
        ax.plot(tmpp)
        tmpx = np.arange(tmpp.shape[0])
        tmpy = np.full_like(tmpx,annotate_level,dtype=float)
        ww = self.bbox['bbox']['WW']
        ax.plot(tmpx,tmpy,color=color,ls=ls)
        for i,ii in enumerate(tmpx):
            if (i in {0,len(tmpx)-1}) or (np.mod(i,xpertick)==0):
                label = '{0}A'.format(int(ww[i]))
                ax.plot(tmpx[i],tmpy[i],color=color,marker=marker)
                ax.annotate(label,(tmpx[i],tmpy[i]),
                             textcoords='offset points',
                             xytext=(0,10),
                             ha='center',
                             fontsize=fontsize,
                             rotation=rotation,
                             color=color
                            )
        ax.set_frame_on(False)
        ax.grid()
        ax.set_ylabel('cps',fontsize=fontsize)
        ax.set_xlabel('pixX - {0}'.format(int(xref)),fontsize=fontsize)
        fig.tight_layout()
        if save:
            string = './{2}/{0}_1d.{1}'.format(saveprefix,saveformat,savefolder)
            fig.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
    ##########
    ##########
    ##########
    def show_bkg2dsub(self,save=False,
                      params={'figsize':(30,10),
                              'minmax_y':(10.,99.),
                              'minmax_ysub':(5.,99.),
                              'cmap':'rainbow',
                              'fontsize':12
                             }
                     ):
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        saveformat = self.container.data['plotformat']
        figsize = params['figsize']
        minmax_y = params['minmax_y']
        minmax_ysub = params['minmax_ysub']
        cmap = params['cmap']
        fontsize = params['fontsize']
        y,yfit = self.bkg.data['Y'],self.bkg.model['YFIT']
        ysub = y-yfit
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(1,3,1)
        vmin,vmax = np.percentile(y,minmax_y[0]),np.percentile(y,minmax_y[1])
        ax.imshow(y,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        ax.set_title(saveprefix,fontsize=fontsize)
        ax = fig.add_subplot(1,3,2)
        ax.imshow(yfit,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        ax.set_title('fit',fontsize=fontsize)
        ax = fig.add_subplot(1,3,3)
        vmin,vmax = np.percentile(ysub,minmax_ysub[0]),np.percentile(ysub,minmax_ysub[1])
        ax.imshow(ysub,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        ax.set_title('sub',fontsize=fontsize)
        fig.tight_layout()               
        if save:
            string = './{2}/{0}_bkg2dsub.{1}'.format(saveprefix,saveformat,savefolder)
            plt.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
    def show_bkg3d(self,save=False,
                   params={'figsize':(20,10),
                           'cmap':'rainbow',
                           'minmax':(5.,99.),
                           'view_init_y':(90.,-90.),
                           'view_init_mask':(90.,-90.),
                           'fontsize':12
                          }
                  ):
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        saveformat = self.container.data['plotformat']
        figsize = params['figsize']
        cmap = params['cmap']
        view_init_y = params['view_init_y']
        view_init_mask = params['view_init_mask']
        fontsize = params['fontsize']
        minmax = params['minmax']
        x1,x2,y = self.bkg.data['X1'],self.bkg.data['X2'],self.bkg.data['Y']
        m = np.isfinite(y)
        vmin,vmax = np.percentile(y,minmax[0]),np.percentile(y,minmax[1])
        if self.bkg.model['MASKFIT'] is None:
            self.bkg.model['MASKFIT'] = self.bkg.data['MASK'].copy()
        mask = self.bkg.model['MASKFIT']
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(2,1,1,projection='3d')
        ax.plot_surface(x1,x2,y,cmap=cmap,vmin=vmin,vmax=vmax)
        ax.view_init(*view_init_y)
        ax.set_title(saveprefix,fontsize=fontsize)
        ax = fig.add_subplot(2,1,2,projection='3d')
        tmpy = y.copy()
        tmpy[mask] = np.nan
        ax.plot_surface(x1,x2,tmpy,cmap=cmap,vmin=vmin,vmax=vmax)
        ax.view_init(*view_init_mask)
        ax.set_title('with MASKFIT',fontsize=fontsize)
        fig.tight_layout()               
        if save:
            string = './{2}/{0}_bkg3d.{1}'.format(saveprefix,saveformat,savefolder)
            plt.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
    def show_bbox2d(self,save=False,savesuffix=None,
                    params={'figsize':(10,10),
                            'minmax':(10.,80.),
                            'xpertick':10,
                            'fontsize':12,
                            'rotation':30.,
                            'color':'r',
                            'cmap':'viridis',
                            'lw':2,
                            'ls':':',
                            'marker':'o',
                            'alpha':0.6,
                            'border_x':50,
                            'border_y':50
                           }
                   ):
        saveprefix = self.container.data['saveprefix']
        savefolder = self.container.data['savefolder']
        saveformat = self.container.data['plotformat']
        if savesuffix is None:
            savesuffix = 'bbox2d'
        tmpdata = fits.open(self.data['gfile'][0])[self.data['gfile'][1]].data
        minmax = params['minmax']
        cmap = params['cmap']
        figsize = params['figsize']
        color = params['color']
        ls = params['ls']
        lw = params['lw']
        alpha = params['alpha']
        border_x = params['border_x']
        border_y = params['border_y']
        fontsize = params['fontsize']
        xpertick = params['xpertick']
        marker = params['marker']
        rotation = params['rotation']
        m = np.isfinite(tmpdata)
        vmin,vmax = np.percentile(tmpdata[m],minmax[0]),np.percentile(tmpdata[m],minmax[1])
        xg,yg,ww = self.trace['XG'],self.trace['YG'],self.trace['WW']
        bb0x,bb1x = self.bbox['bbox']['BBX']
        bb0y,bb1y = self.bbox['bbox']['BBY']
        plt.figure(figsize=figsize)
        plt.imshow(tmpdata,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        # plot trace with annotate for wavelength
        plt.plot(xg,yg,color=color,ls=ls,lw=lw,alpha=alpha)
        for i,ii in enumerate(xg):
            if (i in {0,len(xg)-1}) or (np.mod(i,xpertick)==0):
                label = '{0}A'.format(int(ww[i]))
                plt.plot(xg[i],yg[i],color=color,marker=marker)
                plt.annotate(label,(xg[i],yg[i]),
                             textcoords='offset points',
                             xytext=(0,10),
                             ha='center',
                             fontsize=fontsize,
                             rotation=rotation,
                             color=color
                            )
        # plot cutout region for background section
        plt.plot([bb0x,bb1x,bb1x,bb0x,bb0x],[bb0y,bb0y,bb1y,bb1y,bb0y],color=color,ls='-')        
        # plot object mask region
        tmpx,tmpyup,tmpylow = [],[],[]
        for i,ii in enumerate(xg):
            tmpx.append(xg[i])
            tmpylow.append(yg[i]-self.bbox['halfdylow'])
            tmpyup.append(yg[i]+1+self.bbox['halfdyup'])
        m_min = np.argwhere(tmpx==min(tmpx)).flatten()[0]
        m_max = np.argwhere(tmpx==max(tmpx)).flatten()[0]    
        plt.plot(tmpx,tmpyup,color=color,ls='--')
        plt.plot(tmpx,tmpylow,color=color,ls='--')
        plt.plot([tmpx[m_min],tmpx[m_min]],[tmpyup[m_min],tmpylow[m_min]],color=color,ls='--')
        plt.plot([tmpx[m_max],tmpx[m_max]],[tmpyup[m_max],tmpylow[m_max]],color=color,ls='--')
        # set frame
        plt.xlim(bb0x-border_x,bb1x+border_x)
        plt.ylim(bb0y-border_y,bb1y+border_y)
        plt.title(saveprefix,fontsize=fontsize) 
        plt.tight_layout()
        if save:
            string = './{2}/{0}_{3}.{1}'.format(saveprefix,saveformat,savefolder,savesuffix)
            plt.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
            