from __future__ import print_function
from __future__ import division 
from __future__ import unicode_literals

import numpy as np
import difflib

from inspect import ismethod
import os
from astropy.io.fits.diff import FITSDiff
import glob


class CompareAbs(object):
  """
  An "abstract" class for comparing some kind of |prodimo| model.
  
  A subclass of this class needs to implement the necessary compare routine(s).
  (example see :class:`Compare`)
  
  """
  def diffArray(self,a,aref,diff):
    """
    Checks the relative difference between two arrays. 
    
    If the arrays do not have the same shape they are considered
    as inequal (return `False`).
    
    Parameters
    ----------
    a : array_like(float,ndim=whatever)
      an array.
      
    aref: array_like(float,ndim=same as a)
      the reference array for comparison.
      
    diff : float
      if the values of the arrays differe only by <diff the are considered
      as equal.
    """
    if a.shape != aref.shape:
      return False,None
    
    da=np.absolute(a/aref-1.0)
    if da.max() >= diff:
      return False,da
    
    return True,da

  def diff(self,val,valref,diff):
    """
    Checks the relative difference between two values.
    
    Parameters
    ----------
    a : float
      a value.
      
    aref: float
      the reference value
      
    diff : float
      if the two values differe only by <diff the are considered
      as equal.
    """
    d=abs(val/valref-1.0)
    if d >= diff: return False,d
     
    return True,d 

  def diffFile(self,fname):
    """
    Compares the file with the name given by `fname` (a file produced by ProDiMo) 
    for the the two models.
    
    Parameters
    ----------
    fname : str
      the Filename to compare, (must exist for both models)
    """
    # check if file exist
    fe=os.path.isfile(self.m.directory+"/"+fname)
    feref=os.path.isfile(self.mref.directory+"/"+fname)
    
    # File does not exist in any model -> that is okay
    if ((not fe) and (not feref)): return True,None 

    # if the file exists in only one model, the routine returns false!        
    if (fe ^ feref): return False,None
    
    # now compare the files
    f=open(self.m.directory+"/"+fname)
    fref=open(self.mref.directory+"/"+fname)
    fcont=f.readlines()
    fcontRef=fref.readlines()
    
    diff=list(difflib.unified_diff(fcont,fcontRef,n=0))
        
    if len(diff) == 0:
      return True,None
    else:
      return False,diff


  def diffFitsFile(self,fname,atol=0.0,rtol=1.e-20):
    """
    Compares two fits Files using the astropy routines.
    
    Parameters
    ----------
    fname : str
      the Filename to compare, (must exist for both models)
    """
    # check if file exist
    fe=os.path.isfile(self.m.directory+"/"+fname)
    feref=os.path.isfile(self.mref.directory+"/"+fname)
    
    # File does not exist in any model -> that is okay
    if ((not fe) and (not feref)): return True,None 

    # if the file exists in only one model, the routine returns false!        
    if (fe ^ feref): return False,None
    
    # FIXME: in restart.dat this CONVERGENCE keywordk makes problems, 
    # I think the KEYWORD name is too long (see the fitsheader of reastart.fits.gz)
    # do not test for MAINIT, so that also models that were rerun can be compared
    try:
      diff=FITSDiff(self.m.directory+"/"+fname,self.mref.directory+"/"+fname,
                    ignore_keywords=['CONVERGENCE',"MAINIT"],
                    numdiffs=5,atol=atol,rtol=rtol)
    except Exception as e:
      print("Exception in FITSDiff: ",e)
      return False,None
    
    if diff.identical:
      return True,None
    else:
      return False,diff.report()
      

  def doAll(self):
    """
    Utility function to call all `compare*` method.
    
    Prints out what function failed and the errors.
    
    Assume a naming convention. The method needs to start
    with `compare`. If the compare method uses the :func:`diffFile`, 
    the method name should start with `compareFile`. 
     
    """
    for name in dir(self):
      if name.startswith("compare"):
        cfun = getattr(self, name)
        if ismethod(cfun):
          print("{:30s}".format(name+": "),end="")
          ok,val=cfun()
          
          if ok:
            print("{:8s}".format("OK"),end="")
          else:
            print("{:8s}".format("FAILED"),end="")
            
          # Special treatment for the case of comparing Files
          if name.startswith("compareFile"):            
            if val is None and not ok:
              print("  File does only exist in one model.")
            elif val is not None:
              for line in val:
                if line.startswith("@@"):
                  print("")
                print(line,end="")
            else:
              print("")
          elif name.startswith("compareFitsFile"):            
            if val is None and not ok:
              print("  File does only exist in one model.")
            elif val is not None:
              print(val)
            else:
              print("") 
          else:
            # TODO: also add the number of wrong points in the array
            if val is not None:
              print("  Max/Avg/Index Max rel. Error: ","{:8.3f}%".format(100.0*np.max(val)),
                    "{:8.3f}%".format(100.0*np.average(val)),
                    "{:4d}".format(np.argmax(val)))
              
              # print the first 10 species (lines) that show the largest differences
              if name.startswith("compareLineEstimates") and not ok:
                sortidx=np.flip(np.argsort(val),axis=0)
                lastIdents=list()
                iprint=0 
                for i in range(len(val)):
                  #if self.m.lineEstimates[sortidx[i]].flux>1.e-24 or self.mref.lineEstimates[sortidx[i]].flux>1.e-24:
                  if not self.m.lineEstimates[sortidx[i]].ident in lastIdents:
                    print("{:40s}".format(str(self.m.lineEstimates[sortidx[i]])),
                          "{:40s}".format(str(self.mref.lineEstimates[sortidx[i]])))
                    lastIdents.append(self.m.lineEstimates[sortidx[i]].ident)
                    iprint+=1
                  if iprint >10: break
                print("")
            elif val is None and not ok:
              print("  Value/array is None in only one model.")
            else:
              print("")


class Compare(CompareAbs):
  """
  Class for comparing to ProDiMo models of type :class:`~prodimopy.read.Data_ProDiMo`       
  
  Every compare Function returns true or false, and the relative differences
  (in case of arrays these are arrays). 
  
  Can be used in e.g. automatic testing routines or in simple command line
  tools to compare ProDiMo model results. 
  """
  def __init__(self,model,modelref):
    self.m=model
    self.mref=modelref
    # the default allowed difference
    self.d=1.e-2
    self.dcdnmol=0.5  # the allowed differences for the column densities (radial and vertical)
                      # chemistry is difficult and uncertain :) FIXME: this has to become better, there 
                      # a simply some columns which usually fail an require time-dependent chemistry and 
                      # the outcome seems to depend on numerical uncertainties ...
    # (e.g. 7% point in the column density goes crazy ... still oka                   
    self.fcdnmol= 0.1   
    self.dTgas=5e-1   # FIXME: 50% Tgas is also quite sensitive, but lower would be better
    self.dLineFluxes=5.e-2  # 5% for line fluxes
    self.dAbundances=1.e-2  # chemistry is difficult and uncertain :)     
    self.lAbundances=1.e-30
    self.dZetaCR=self.d
    self.dZetaX=3.e-1 # FIXME: 50% , should not be that high
    self.dHX=3.e-1 # FIXME: 50% , should not be that high
    self.lZetaX=1.e-25 # lower limit for the check
#    self.specCompare=("e-","H2","CO","H2O","Ne+","Ne++","H+")
#    self.specCompare=("N2","N2#","CO#","H2O#","H3","H3+","HCO+","HN2+","SO2","SiO")
#    self.specCompare=("CO","CN")

    self.specCompare=("e-","H2","CO","H2O","N2","N2#","CO#","H2O#","H3+","HCO+","HN2+","SO2","SiO",
                      "Ne+","Ne++","H+","OH","C+","S+","Si+","N+","CN","HCN","NH3")

      
  def compareLineFluxes(self): 
    '''
    Compares the line fluxes
    Currently assumes that both models include the same lines in the same order.
    '''
    if self.m.lines is None and self.mref.lines is None: return True,None
    
    if self.m.lines is not None and self.mref.lines is None: return False,None
    
    if self.m.lines is None and self.mref.lines is not None: return False,None       

    mFluxes=np.array([x.flux for x in self.m.lines])
    mrefFluxes=np.array([x.flux for x in self.mref.lines])
    f,d=self.diffArray(mFluxes, mrefFluxes, self.dLineFluxes)
    if f == False:
      return False,d
  
    return True,d
  
  def compareLineEstimates(self): 
    '''
    Compares the fluxes from the line estimates
    Currently assumes that both models include the same lines in the same order.
    
    TODO: can actually be merged with compareLineFluxes
    '''
    if self.m.lineEstimates is None and self.mref.lineEstimates is None: return True,None
    
    if self.m.lineEstimates is not None and self.mref.lineEstimates is None: return False,None
    
    if self.m.lineEstimates is None and self.mref.lineEstimates is not None: return False,None       

    mFluxes=np.array([x.flux for x in self.m.lineEstimates])
    mrefFluxes=np.array([x.flux for x in self.mref.lineEstimates])
    f,d=self.diffArray(mFluxes, mrefFluxes, self.dLineFluxes)
    if f == False:
      return False,d
  
    return True,d
  
    
  def compareSED(self):
    """
    Compares the SEDs 
    """
    if self.m.sed is None and self.mref.sed is None: return True,None
    if self.m.sed is not None and self.mref.sed is None: return False,None
    if self.m.sed is None and self.mref.sed is not None: return False,None
    f,d=self.diffArray(self.m.sed.fnuErg, self.mref.sed.fnuErg, self.d)
    
    if f == False:
      return False,d
    
    return True,d  
  
  def compareContinuumImages(self):
    """
    Compares some of the continuum images.  
    """
    if self.m.contImages is None and self.mref.contImages is None: return True,None
    if self.m.contImages is not None and self.mref.contImages is None: return False,None
    if self.m.contImages is None and self.mref.contImages is not None: return False,None
    
    
    for wl in [1,10,100,1000]:
      imm,immwl=self.m.contImages.getImage(wl)
      imref,imrefwl=self.mref.contImages.getImage(wl)    
    
      f,d=self.diff(immwl, imrefwl, self.d)
      if f == False:
        return False,d
    
      f,d=self.diffArray(imm, imref, self.d)
    
      if f == False:
        return False,d
    
    return True,d  
  
  
  def compareCdnmol(self):
    ''' 
    checks the vertical column densities
    only the outermost points are checked
    '''    
    specidxM=[self.m.spnames[idx] for idx in self.specCompare if idx in self.m.spnames]    
    #print(specidxM)    
    specidxMref=[self.mref.spnames[idx] for idx in self.specCompare if idx in self.mref.spnames] 
    
    ok,diffarray= self.diffArray(self.m.cdnmol[:,0,specidxM],self.mref.cdnmol[:,0,specidxMref],self.dcdnmol)
    
    # if false check if it is only a certain fraction of the columns, it than can 
    # be still okay
    # is not really elegant I would say
    # TODO: also somehow return the number of failed columns
    # TODO: maybe merge rcdnmol
    if ok is False and diffarray is not None:
      ok=True # and check if any columns faild    
      for i in range(len(specidxMref)):
        faildcolumns=(diffarray[:,i]>self.dcdnmol).sum()
        if ((float(faildcolumns)/float(len(diffarray[:,i])))>self.fcdnmol):
          ok=False
                
    return ok,diffarray

  def compareRcdnmol(self):
    ''' 
    checks the radial column densities
    only the outermost points are checked
    ''' 
    
    specidxM=[self.m.spnames[idx] for idx in self.specCompare if idx in self.m.spnames]    
    #print(specidxM)    
    specidxMref=[self.mref.spnames[idx] for idx in self.specCompare if idx in self.mref.spnames] 

    ok,diffarray= self.diffArray(self.m.rcdnmol[-1,:,specidxM],self.mref.rcdnmol[-1,:,specidxMref],self.dcdnmol)

    # if false check if it is only a certain fraction of the columns, it than can 
    # be still okay
    # is not really elegant I would say
    # TODO: also somehow return the number of failed columns
    # TODO: maybe merge Cdnmol
    if ok is False and diffarray is not None:
      ok=True # and check if any columns faild    
      for i in range(len(specidxMref)):
        faildcolumns=(diffarray[:,i]>self.dcdnmol).sum()
        if ((float(faildcolumns)/float(len(diffarray[:,i])))>self.fcdnmol):
          ok=False

    return ok,diffarray 
  
  def compareDustOpacEnv(self):
    '''
    Compares the dust opacities for an envelope model (optional output).
    '''    
    if self.m.env_dust is None and self.mref.env_dust is None: return True,None
    if self.m.env_dust is not None and self.mref.env_dust is None: return False,None
    if self.m.env_dust is None and self.mref.env_dust is not None: return False,None
    
    return self.diffArray(self.m.env_dust.kext, self.mref.env_dust.kext, self.d)

  def compareDustOpac(self):
    '''
    Compares the dust opacities.
    '''    
    return self.diffArray(self.m.dust.kext, self.mref.dust.kext, self.d)

  
  def compareStarSpec(self):
    '''
    Compares the input Stellar spectrum, from X-rays to mm
    '''
    f,d=self.diffArray(self.m.starSpec.Inu, self.mref.starSpec.Inu, self.d)
    
    if f is False:
      return False,d
  
    return True,d

  def compareNHtot(self):
    '''
    checks the total hydrogen number density
    '''
    return self.diffArray(self.m.nHtot,self.mref.nHtot,self.d)

  def compareRhog(self):
    '''
    checks the gas density
    '''
    return self.diffArray(self.m.rhog,self.mref.rhog,self.d)

  def compareRhod(self):
    '''
    checks the dust density
    '''
    return self.diffArray(self.m.rhod,self.mref.rhod,self.d)

  def compareTg(self):
    '''
    checks the gas Temperature
    '''
    return self.diffArray(self.m.tg,self.mref.tg,self.dTgas)  

  def compareTd(self):
    '''
    checks the dust Temperature
    '''
    return self.diffArray(self.m.td,self.mref.td,self.d) 
  
  def compareZetaCR(self):
    '''
    checks the cosmic ray ionisation rate
    '''
    return self.diffArray(self.m.zetaCR,self.mref.zetaCR,self.dZetaCR) 
  
  def compareZetaX(self):
    '''
    checks the Xray ionisation rate
    '''
        # set low values to zero 
    self.m.zetaX[self.m.zetaX < self.lZetaX]=self.lZetaX
    self.mref.zetaX[self.mref.zetaX < self.lZetaX]=self.lZetaX
    
    return self.diffArray(self.m.zetaX,self.mref.zetaX,self.dZetaX)

  def compareHX(self):
    '''
    checks the Xray energy deposition rate
    '''
        # set low values to zero 
#    self.m.Hx[self.m.zetaX < self.lZetaX]=self.lZetaX
#    self.mref.Hx[self.mref.zetaX < self.lZetaX]=self.lZetaX
    
    return self.diffArray(self.m.Hx,self.mref.Hx,self.dHX)  

  
  def compareFileReactionsOut(self):
    '''
    Makes a file comparison with Reactions.out.
    '''    
    return self.diffFile("Reactions.out") 

  
  def compareFileSpeciesOut(self):
    '''
    Makes a file comparison with Species.out
    '''    
    return self.diffFile("Species.out") 

  
  def compareFileElementsOut(self):
    '''
    Makes a file comparison with Elements.out
    '''    
    return self.diffFile("Elements.out") 
  
  
  def compareFileCheckNetworkLog(self):
    '''
    Makes a file comparison with CheckNetwork.log
    '''    
    return self.diffFile("CheckNetwork.log") 

  def compareFileCheckChemLog(self):
    '''
    Makes a file comparison with CheckChem.log
    '''    
    return self.diffFile("CheckChem.log") 


  def compareFitsFileRestart(self):
    '''
    Makes a fits file comparison with restart.fits.gz
    '''    
    return self.diffFitsFile("restart.fits.gz",rtol=2.e-7) 

  def compareFitsFileMie(self):
    '''
    Makes a fits file comparison with Mie.fits.gz
    '''    
    return self.diffFitsFile("Mie.fits.gz",rtol=2.e-7) 

  def compareFitsFileLineCubes(self):
    '''
    Makes a fits file comparison with Mie.fits.gz
    '''    
    fcubes=glob.glob(self.m.directory+"/LINE_3D_???.fits")

    # FIXME: this deos not work if the other model actually has linecubes
    # e.g. it would say that it is okay
    if fcubes is not None:
      for fname in fcubes:
        ok,val=self.diffFitsFile(os.path.basename(fname),rtol=2.e-7)
        if not ok: # stop the whole thing if one cube went wron
          return ok,val 
    
    return True,None
    

class CompareMc(CompareAbs): 
  """
  Class for comparing two ProDiMo models of type :class:`~prodimopy.read_mc.Data_mc`       
  
  Every compare Function returns true or false, and the relative differences
  (in case of arrays these are arrays). 
  
  Can be used in e.g. automatic testing routines or in simple command line
  tools to compare ProDiMo model results. 
  """
 
  def __init__(self,model,modelref):
    self.m=model
    self.mref=modelref
    # the allowed relative difference between two values 
    self.d=1.e-10
    self.dabundance=1.e-5
    self.drc=1.e-10 # the difference for the rate coefficients
    
  
  def compareAbundances(self):
    """
    Compares the abundances of two molecular cloud (0D chemistry) models. 
    
    Assumes that both models used the same number of ages and species in the same order.
    """    
    # Do not consider the first age entry at it is the initial conditions 
    # that can vary from model two model and are not really a result
    
    return self.diffArray(self.m.abundances[1:,:],self.mref.abundances[1:,:],self.dabundance)

  def compareRatecoefficients(self):
    """
    Compares the rate coefficients of two molecular cloud (0D chemistry) models. 
    
    Assumes that both models have exactly the same chemical reactions in the same order.
    """    
    return self.diffArray(self.m.ratecoefficients,self.mref.ratecoefficients,self.drc)


def eval_model_type(modelDir):
  """
  Try to guess the model type (e.g. mc, full prodimo etc.).
  Default is always prodimo.
  
  Possible types: 
  
    `prodimo` .... full prodimo model (:class:`prodimopy.read.Data_ProDiMo`) 
  
    `mc` ......... molecular cloud model (:class:`prodimopy.read_mc.Data_mc`) 
  
  Returns
  -------
    str either `prodimo` or `mc`  
  
  FIXME: this is maybe not the best place for this routine
  FIXME: provide constants for the values (what's the best way to do this in pyhton?)
  FIXME: this is just a quick hack, it would be better to use the parameters in Parameter.in
  
  """

  
  if os.path.isfile(modelDir+"/ProDiMo_01.out"):
    mtype = "prodimoTD"
  
  elif os.path.isfile(modelDir+"/Molecular_Cloud_Input.in"):
    mtype="mc"
  else:
      mtype="prodimo"
  
  return mtype



#   def compareFlineEstimates(self):
#     '''
#     Compares the FlineEstimaes    
#     '''
#     
#     if len(self.m.lineEstimates) !=len(self.mref.lineEstimates):
#       return False,None     
#     
#     
#     self.diff(self.m.lineEstimate[i].flux, self.mref.lineEstimate[i].flux, self.dLineFluxes)
#     
#     # Compare fluxes    
#     for i in range(len(self.m.lines)):
#         f,d=
#         if f == False:
#           return False,d
#   
#     return True,None
#   
#   def compareAbundances(self):
#     if self.m.nspec != self.mref.nspec: return False,None
#     
#     # set low values to zero 
#     self.m.nmol[self.m.nmol < self.lAbundances]=self.lAbundances
#     self.mref.nmol[self.mref.nmol < self.lAbundances]=self.lAbundances
#     
#     #print(self.m.nmol[:,0,0])
#     #print(self.mref.nmol[:,0,0])
#     # only check a small selection of species
#     spec=("H2","CO","H2O","CO#","H2O#","H3+")
#     specidxM=[self.m.spnames[idx] for idx in spec if idx in self.m.spnames]    
#     #print(specidxM)    
#     specidxMref=[self.mref.spnames[idx] for idx in spec if idx in self.mref.spnames]    
#     #print(specidxMref)    
#   
#     return self.diffArray(self.m.nmol[:,:,specidxM],self.mref.nmol[:,:,specidxMref],self.dAbundances)  
          
