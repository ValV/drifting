#!/usr/bin/env python
"""
Oil 3d (vertical mixing)
==================================
"""

from datetime import timedelta
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.openoil3D import OpenOil3D


o = OpenOil3D(loglevel=20)  # Set loglevel to 0 for debug information

ncfile = 'oil3Dmixing.nc'
import_file = False  # Set to True to import previous run

if import_file is True:
    o.io_import_file(ncfile)
else:
    reader_arome = reader_netCDF_CF_generic.Reader('http://thredds.met.no/thredds/dodsC/meps25files/meps_det_extracted_2_5km_latest.nc')
    reader_norkyst = reader_netCDF_CF_generic.Reader('http://thredds.met.no/thredds/dodsC/sea/norkyst800m/1h/aggregate_be')

    o.add_reader([reader_norkyst, reader_arome])

    # Seed oil elements at defined position and time
    o.seed_elements(lon=4.9, lat=62.1, z=0, radius=1000, number=2000,
                    time=reader_arome.start_time)

    # Adjusting some configuration
    o.set_config('processes:evaporation', False)
    o.set_config('processes:turbulentmixing', True)
    o.set_config('processes:dispersion', False)
    #o.set_config('turbulentmixing:diffusivitymodel', 'windspeed_Sundby1983')

    # Running model
    o.run(end_time=reader_arome.start_time + timedelta(hours=12),
          time_step=900, time_step_output=1800, outfile=ncfile)

###########################
# Print and plot results
###########################
print(o)

o.plot(linecolor='z', fast=True)
o.plot_property('z')
o.plot_oil_budget()
o.animation(filename='oil3d_verticalmixing.gif', fast=True)

#%%
# .. image:: /gallery/animations/oil3d_verticalmixing.gif
