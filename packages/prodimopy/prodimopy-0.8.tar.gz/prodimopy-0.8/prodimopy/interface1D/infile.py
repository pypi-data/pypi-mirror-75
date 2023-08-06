import astropy.units as u
import numpy as np


def writeV1(fname,r,sdg,g2dratio):
  '''
  Produces an input file for the 1D interface (version 1) to ProDiMo.
  
  All array input parameters need to have the same length.

  Parameters
  ----------

  fname : string
    The filename (path) to be use for the input file. 
  
  r : array_like(float,ndim=1)
    radial gridpoints (distance to the star) for the disk.
    `UNIT:` cm
    
  sdg : array_like(float,ndim=1)
    The total gas surface density profile (the sum of both sides of the disk)
    `UNIT:` |gcm^-2|
    
  g2dratio: array_like(float,ndim=1)
    The gas to dust mass ratio as function of radius.
  
  '''
  fp=open(fname,"w")
  fp.write("# number of radii\n")
  fp.write(str(len(r))+"\n") 
  fp.write("# Rin(au)\n")
  fp.write(str((r[0]*u.cm).to(u.au).value)+"\n")
  fp.write("# Rout(au)\n")
  fp.write(str((r[-1]*u.cm).to(u.au).value)+"\n")
  fp.write("# normalization factor\n")
  fp.write("-2.0\n")
  fp.write("# R [cm]   gas surface density [gcm^-2]   gas to dust mass ratio \n")
  
  # FIXME: workaround 
  # if the first two entries are equal fix the the second one a bit larger
  if r[0]==r[1]:
      r[1]=10**(np.log10(r[0])+(np.log10(r[2])-np.log10(r[0]))/2.0)
      
  
  for rl,pl,g2dl in zip(r,sdg,g2dratio):
      fp.write("{:18.10e}".format(rl))
      fp.write(" ")
      fp.write("{:18.10e}".format(pl))
      fp.write(" ")
      fp.write("{:18.10e}".format(g2dl))
      fp.write("\n")
  
  fp.close()


def writeV2(fname,r,sdg,sdd_small,sdd_large,amax):
  '''
  Produces an input file for the 1D interface (version 2) to ProDiMo.
  
  All array input parameters need to have the same length.
  
  This is format that is used for E. Vorobyovs code.
  
  However, one should use the newer more flexible, (but compatible) format.
  see :meth:`~writeV3`
    
  
  Parameters
  ----------
  
  fname : string
    The filename (path) to be use for the input file. 
  
  r : array_like(float,ndim=1)
    The radius array. 
    `UNIT:` cm

  sdg : array_like(float,ndim=1)
    The gas surface density profile. 
    `UNIT:` |gcm^-2|
    
  sdd_small : array_like(float,ndim=1)
    The dust surface density of the small grain dust popoulation
    `UNIT:` |gcm^-2|
  
  sdd_large : array_like(float,ndim=1)
    The dust surface density of the large grain dust popoulation
    `UNIT:` |gcm^-2|
  
  amax : array_like(float,ndim=1)
    the maxium grain size at each radial grid point
    `UNIT:` cm
      
  '''
  fp=open(fname,"w")
  fp.write("# number of radii\n")
  fp.write(str(len(r))+"\n") 
  fp.write("# Rin(au)\n")
  fp.write(str((r[0]*u.cm).to(u.au).value)+"\n")
  fp.write("# Rout(au)\n")
  fp.write(str((r[-1]*u.cm).to(u.au).value)+"\n")
  fp.write("# file version \n")
  fp.write("2\n")
  fp.write("# R [au]   gas surface density [gcm^-2]   sd dust small [gcm^-2]   sd dust large [gcm^-2]   amax [cm]\n")
  
  # FIXME: workaround 
  # if the first two entries are equal fix the the second one a bit larger
  if r[0]==r[1]:
      r[1]=10**(np.log10(r[0])+(np.log10(r[2])-np.log10(r[0]))/2.0)
      
  
  for rl,pl,sdsmalll,sdlargel,amaxl in zip(r,sdg,sdd_small,sdd_large,amax):
    fp.write("{:18.10e}".format((rl*u.cm).to(u.au).value))
    fp.write(" ")
    fp.write("{:18.10e}".format(pl))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdsmalll))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdlargel))
    fp.write(" ")
    fp.write("{:18.10e}".format(amaxl))
    fp.write("\n")
  
  fp.close()


def writeV3(fname,r,sdg,sdd_small,sdd_large,amin, atrans,amax):
  '''
  Produces an input file for the 1D interface (version 3) to ProDiMo.
  
  All array input parameters need to have the same length.

  Parameters
  ----------
  
  fname : string
    The filename (path) to be use for the input file. 
  
  r : array_like(float,ndim=1)
    The radius array. 
    `UNIT:` cm

  sdg : array_like(float,ndim=1)
    The gas surface density profile. 
    `UNIT:` |gcm^-2|
    
  sdd_small : array_like(float,ndim=1)
    The dust surface density of the small grain dust popoulation
    `UNIT:` |gcm^-2|
  
  sdd_large : array_like(float,ndim=1)
    The dust surface density of the large grain dust popoulation
    `UNIT:` |gcm^-2|
  
  amax : array_like(float,ndim=1)
    the maxium grain size at each radial grid point
    `UNIT:` cm
      
  '''
  fp=open(fname,"w")
  fp.write("# number of radii\n")
  fp.write(str(len(r))+"\n") 
  fp.write("# Rin(au)\n")
  fp.write(str((r[0]*u.cm).to(u.au).value)+"\n")
  fp.write("# Rout(au)\n")
  fp.write(str((r[-1]*u.cm).to(u.au).value)+"\n")
  fp.write("# file version \n")
  fp.write("3\n")
  fp.write("# R [cm]   gas surface density [gcm^-2]   sd dust small [gcm^-2]")
  fp.write("   sd dust large [gcm^-2]   amin [cm]   atrans [cm]   amax [cm]\n")
  
  # FIXME: workaround 
  # if the first two entries are equal fix the the second one a bit larger
  if r[0]==r[1]:
      r[1]=10**(np.log10(r[0])+(np.log10(r[2])-np.log10(r[0]))/2.0)
  
  for rl,pl,sdsmalll,sdlargel,aminl,atransl,amaxl in zip(r,sdg,sdd_small,sdd_large,amin,atrans,amax):
    fp.write("{:18.10e}".format(rl))
    fp.write(" ")
    fp.write("{:18.10e}".format(pl))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdsmalll))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdlargel))
    fp.write(" ")
    fp.write("{:18.10e}".format(aminl))
    fp.write(" ")
    fp.write("{:18.10e}".format(atransl))
    fp.write(" ")
    fp.write("{:18.10e}".format(amaxl))
    fp.write("\n")

  fp.close() 


def writeV4(fname,r,sdg,g2dratio,agrid,fsize):
  '''
  Produces an input file for the 1D interface (version 4) to ProDiMo.
  
  This routine requires a full size distribution given by the grain size grid
  `a` and the size distribution `fsize`. `fsize` should contain the surface density
  as function of radius for each grain size bin.

  Parameters
  ----------

  fname : string
    The filename (path) to be use for the input file. 
  
  r : array_like(float,ndim=1)
    The radius array. 
    `UNIT:` cm

  sdg : array_like(float,ndim=1)
    The gas surface density profile. 
    `UNIT:` |gcm^-2|

  g2dratio: array_like(float,ndim=1)
    The gas to dust mass ratio as function of radius.
    
  agrid : array_like(float,ndim=1)
    The grain size grid. 
    `UNIT:` cm
    
  fsize : array_like(float,ndim=2)
    The grain size distribution given as surface density per grain size bin.
    The dimension is (`len(a),len(r)`). `UNIT:` |gcm^-2|
  
  '''
  fp=open(fname,"w")
  fp.write("# number of radii\n")
  fp.write(str(len(r))+"\n") 
  fp.write("# Rin(au)\n")
  fp.write(str((r[0]*u.cm).to(u.au).value)+"\n")
  fp.write("# Rout(au)\n")
  fp.write(str((r[-1]*u.cm).to(u.au).value)+"\n")
  fp.write("# file version \n")
  fp.write("4\n")
  fp.write("# number of grain size bins \n")
  fp.write(str(len(agrid))+"\n")
  fp.write("# grain size grid [cm] \n")
  fp.write(("{:18.10e}"*len(agrid)).format(*agrid))
  fp.write("\n")
  fp.write("# R [cm]   gas surface density [gcm^-2]   gas to dust mass ratio   fsize [gcm^-2] \n")

  # FIXME: workaround 
  # if the first two entries are equal fix the the second one a bit larger
  if r[0]==r[1]:
      r[1]=10**(np.log10(r[0])+(np.log10(r[2])-np.log10(r[0]))/2.0)

  for i in range(len(r)):    
    fp.write("{:18.10e}".format(r[i]))
    fp.write(" ")
    fp.write("{:18.10e}".format(sdg[i]))
    fp.write(" ")
    fp.write("{:18.10e}".format(g2dratio[i]))
    fp.write(" ")
    fp.write(("{:18.10e}"*len(agrid)).format(*fsize[:,i]))
    fp.write("\n")
  fp.close()


def generate_sdd_twopop(twopp_res,atrans):
  ''''
  Generates a small and large dust surface density profile for the given atrans, from 
  the two-pop-py results. 
  
  Parameters
  ----------

  twopp_res : two-pop-py results
  
  atrans : array_like(float,ndim=1)
    The transition radius from the small to the large population.
    `UNIT:` cm

  '''
  
  sdsmall=twopp_res.x[:]*0.0
  sdlarge=twopp_res.x[:]*0.0
  sdsmall[:]=1.e-150
  sdlarge[:]=1.e-150

  # for each r we have atrans now, so separate the small and large one for each r
  for ix in range(len(twopp_res.x)):
    itrans= np.argmin(np.abs(twopp_res.a-atrans[ix]))
    sdsmall[ix]=np.sum(twopp_res.sig_sol[0:itrans,ix],axis=0)
    sdlarge[ix]=np.sum(twopp_res.sig_sol[itrans:-1,ix],axis=0)

#    print("{:5.3f} ".format(twopp_res.x[ix]/AU),itrans,("{:5.3e}  "*6).format(twopp_res.a[itrans],a_max[ix],sdsmall[ix],sdlarge[ix],twopp_res.sigma_d[-1,ix],
#                                  (sdsmall[ix]+sdlarge[ix])/twopp_res.sigma_d[-1,ix])) 
  
  sdsmall[sdsmall<1.e-100]=1.e-100
  sdlarge[sdlarge<1.e-100]=1.e-100
  
  return sdsmall,sdlarge

