from datetime import date
import numpy as np

import netCDF4 as nc
#-------------------------------------------------
class ncoutput:
  def __init__(self, nx, ny, lats, lons, name):
    self.name  = name
    self.nx    = nx
    self.ny    = ny
    self.lats  = lats
    self.lons  = lons
    self.count = 0
    self.var   = []

  def ncoutput(self, fname):
    self.ncfile = nc.Dataset(fname, mode='w', format='NETCDF4')

    #Generic global header info:
    self.ncfile.title = fname
    self.ncfile.setncattr("geospatial_lon_max","{:f}".format(self.lons.max() )  )
    self.ncfile.setncattr("geospatial_lon_min","{:f}".format(self.lons.min() )  )
    self.ncfile.setncattr("geospatial_lat_max","{:f}".format(self.lats.max() )  )
    self.ncfile.setncattr("geospatial_lat_min","{:f}".format(self.lats.min() )  )
    tmp = date.today()
    self.ncfile.setncattr("date_created",tmp.strftime("%Y-%m-%d") )

    #More specialized:
    self.ncfile.setncattr("contributor_name","Robert Grumbine")
    self.ncfile.setncattr("contributor_email","Robert.Grumbine@gmail.com")
    self.ncfile.setncattr("creator_name","Robert Grumbine")
    self.ncfile.setncattr("creator_email","Robert.Grumbine@gmail.com")

    self.lat_dim = self.ncfile.createDimension('lat', self.ny)
    self.lon_dim = self.ncfile.createDimension('lon', self.nx)
    # Create variables to hold values for those referenced dimensions
    self.lat = self.ncfile.createVariable('lat', np.float32, ('lat',))
    self.lat.units = 'degrees_north'
    self.lat.long_name = 'latitude'
    self.lat[:] = self.lats[:]

    self.lon = self.ncfile.createVariable('lon', np.float32, ('lon',))
    self.lon.units = 'degrees_east'
    self.lon.long_name = 'longitude'
    self.lon[:] = self.lons[:]

    #debug: print("leaving ncoutput", flush=True)

  def addvar(self, vname, dtype):
    #debug print('dtype = ',dtype, flush=True)
    #if (dtype == 'uint8'):
    #  fill = 255
    #else:
    #  print("failed type test")
    #  fill = 255
    fill = -999.0

    #try:
    tmp = self.ncfile.createVariable(vname, dtype, ( 'lat','lon'), fill_value=fill)
    #except:
    #  return
    self.var.append(tmp)
    self.var[self.count].long_name = vname
    self.count += 1
    #debug: print("leaving addvar", flush=True)

  def encodevar(self, allvalues, vname):
    #debug: print("entering encodevar")
    if (self.nx*self.ny != 0) :
      self.ncfile.variables[vname][:,:] = allvalues

  def close(self):
    # close netcdf file associated w. patch
    self.ncfile.close()

#-------------------------------------------------

