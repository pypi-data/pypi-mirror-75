def copy_style():
  """
  Installation of the default prodimopy.mplstyle
  """

  import os
  import matplotlib
  import distutils

  from pkg_resources import resource_string

  files = [
    'stylelib/prodimopy.mplstyle',
  ]

  for fname in files:
    path = os.path.join(matplotlib.get_configdir(),fname)
    # create directory if it does not exist
    distutils.dir_util.mkpath(os.path.dirname(path))    
    text = resource_string(__name__,fname).decode()
    open(path,'w').write(text)
    print("Installed prodimopy style in: "+path)
    