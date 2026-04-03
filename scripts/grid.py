import xarray as xr

ds = xr.open_dataset("pollution_grid.nc", engine="netcdf4")
print(ds)