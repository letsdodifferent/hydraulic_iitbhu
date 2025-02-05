from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw
import io

# #%%
# import pysheds
# import pyproj
# import matplotlib.pyplot as plt

# # Specify the path to your DEM file
# dem_path = "J:\My Drive\IITBHU\Consultancy\Technical Vetting of DPR for hydrology report (excluding guide bunds)\output_SRTMGL1.tif"
# # Specify the pour point coordinates (latitude, longitude)
# pour_point_coords = (29.752962, 78.480269)

# # Create a PySheds model
# model = pysheds.grid.Grid.from_raster(dem_path)

# # Set up the projection for your coordinates and the DEM
# crs_wgs84 = pyproj.CRS("EPSG:4326")  # WGS84 coordinate reference system
# crs_dem = pyproj.CRS(model.crs)      # DEM coordinate reference system

# transformer = pyproj.Transformer.from_crs(crs_wgs84, crs_dem, always_xy=True)

# # Convert pour point coordinates to row and column indices
# col_index, row_index = transformer.transform(*pour_point_coords)

# # Delineate the catchment
# catchment = model.catchment((row_index, col_index), xy=(col_index, row_index), dirmap=model.flowdir)

# # Get the delineated catchment mask
# catchment_mask = catchment > 0

# # Plot the DEM and catchment boundary
# plt.imshow(model.read_raster(), cmap='terrain', extent=model.extent)
# plt.contour(catchment_mask, colors='blue', linewidths=0.5, extent=model.extent)
# plt.show()


#%%

# import pysheds
# import matplotlib.pyplot as plt

# # Specify the path to your DEM file
# dem_path = "J:\My Drive\IITBHU\Consultancy\Technical Vetting of DPR for hydrology report (excluding guide bunds)\output_SRTMGL1.tif"
# # Specify the pour point coordinates (latitude, longitude)
# pour_point_coords = (29.627844537849292, 78.2585262578929)

# # Create a PySheds model
# model = pysheds.grid.from_raster(dem_path)

# # Convert pour point coordinates to row and column indices
# row_index, col_index = model.latlon_to_rowcol(*pour_point_coords)

# # Delineate the catchment
# catchment = model.catchment((row_index, col_index))

# # Get the delineated catchment mask
# catchment_mask = catchment > 0

# # Plot the DEM and catchment boundary
# plt.imshow(model.dem, cmap='terrain', extent=model.extent)
# plt.contour(catchment_mask, colors='blue', linewidths=0.5, extent=model.extent)
# plt.show()

#%%
# import pysheds
# import matplotlib.pyplot as plt

# # Specify the path to your DEM file
# dem_path = "J:\My Drive\IITBHU\Consultancy\Technical Vetting of DPR for hydrology report (excluding guide bunds)\output_SRTMGL1.tif"

# # Specify the pour point coordinates (e.g., the outlet of the stream)
# pour_point = (row_index, col_index)

# # Create a PySheds model
# model = pysheds.grid.from_raster(dem_path)

# # Delineate the catchment
# catchment = model.catchment(pour_point)

# # Get the delineated catchment mask
# catchment_mask = catchment > 0

# # Plot the DEM and catchment boundary
# plt.imshow(model.dem, cmap='terrain', extent=model.extent)
# plt.contour(catchment_mask, colors='blue', linewidths=0.5, extent=model.extent)
# plt.show()


#%%


def main(request):
    return render(request, "wsd.html")

class Watershed_delineation():
    def __init__(self,lat,long):
        self.lat = lat
        self.long = long
        from pysheds.grid import Grid

        grid = Grid.from_raster(r"C:\Users\aryan\OneDrive\Documents\Coading\Django\ug_project\ug\wsd\static\output_SRTMGL1.tif")
        dem = grid.read_raster(r"C:\Users\aryan\OneDrive\Documents\Coading\Django\ug_project\ug\wsd\static\output_SRTMGL1.tif")

        #%%
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib import colors
        import seaborn as sns

        fig, ax = plt.subplots(figsize=(8,6))
        fig.patch.set_alpha(0)

        # plt.imshow(dem, extent=grid.extent, cmap='terrain', zorder=1)
        # plt.colorbar(label='Elevation (m)')
        # plt.grid(zorder=0)
        # plt.title('Digital elevation map', size=14)
        # plt.xlabel('Longitude')
        # plt.ylabel('Latitude')
        # plt.tight_layout()

        #%%
        pit_filled_dem = grid.fill_pits(dem)

        # Fill depressions in DEM
        flooded_dem = grid.fill_depressions(pit_filled_dem)
            
        # Resolve flats in DEM
        inflated_dem = grid.resolve_flats(flooded_dem)


        dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
            
        # Compute flow directions
        # -------------------------------------
        fdir = grid.flowdir(inflated_dem, dirmap=dirmap)

        #%%

        fig = plt.figure(figsize=(8,6))
        fig.patch.set_alpha(0)

        # plt.imshow(fdir, extent=grid.extent, cmap='viridis', zorder=2)
        # boundaries = ([0] + sorted(list(dirmap)))
        # plt.colorbar(boundaries= boundaries,values=sorted(dirmap))
        # plt.xlabel('Longitude')
        # plt.ylabel('Latitude')
        # plt.title('Flow direction grid', size=14)
        # plt.grid(zorder=-1)
        # plt.tight_layout()

        #%%]

        acc = grid.accumulation(fdir, dirmap=dirmap)

        # fig, ax = plt.subplots(figsize=(8,6))
        # fig.patch.set_alpha(0)
        # plt.grid('on', zorder=0)
        # im = ax.imshow(acc, extent=grid.extent, zorder=2,cmap='cubehelix',norm=colors.LogNorm(1, acc.max()),interpolation='bilinear')
        # plt.colorbar(im, ax=ax, label='Upstream Cells')
        # plt.title('Flow Accumulation', size=14)
        # plt.xlabel('Longitude')
        # plt.ylabel('Latitude')
        # plt.tight_layout()


        #%%
    
    def delineation(self):
        # Delineate a catchment
        # ---------------------
        # Specify pour point
        # x, y = 78.53736389, 29.75851111
        x, y = self.long,self.lat


        # Snap pour point to high accumulation cell
        x_snap, y_snap = grid.snap_to_mask(acc > 200000, (x, y))

        # Delineate the catchment
        catch = grid.catchment(x=x_snap, y=y_snap, fdir=fdir, dirmap=dirmap, xytype='coordinate')

        # Crop and plot the catchment
        # ---------------------------
        # Clip the bounding box to the catchment
        grid.clip_to(catch)
        clipped_catch = grid.view(catch)



        # Plot the catchment
        fig, ax = plt.subplots(figsize=(8,6))
        fig.patch.set_alpha(0)

        plt.grid('on', zorder=0)
        im = ax.imshow(np.where(clipped_catch, clipped_catch, np.nan), extent=grid.extent,
                    zorder=1, cmap='Greys_r')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.plot(x,y,'r*')

        plt.title('Delineated Catchment', size=14)

        #%%

        branches = grid.extract_river_network(fdir, acc > 500, dirmap=dirmap)


        sns.set_palette('husl')
        fig, ax = plt.subplots(figsize=(8.5,6.5))

        plt.xlim(grid.bbox[0], grid.bbox[2])
        plt.ylim(grid.bbox[1], grid.bbox[3])
        ax.set_aspect('equal')

        for branch in branches['features']:
            line = np.asarray(branch['geometry']['coordinates'])
            plt.plot(line[:, 0], line[:, 1])
            
        _ = plt.title('D8 channels', size=14)


        #%%

        dist = grid.distance_to_outlet(x=x_snap, y=y_snap, fdir=fdir, dirmap=dirmap,xytype='coordinate')

        fig, ax = plt.subplots(figsize=(8,6))
        fig.patch.set_alpha(0)
        plt.grid('on', zorder=0)
        im = ax.imshow(dist, extent=grid.extent, zorder=2,cmap='cubehelix_r')
        plt.colorbar(im, ax=ax, label='Distance to outlet (cells)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Flow Distance', size=14)





def wsd(request):
    if request.method == 'POST':
        lat = float(request.POST.get('lat'))
        long = float(request.POST.get('long'))
        obj = Watershed_delineation(lat,long)
        obj.delineation()
    return render(request, "wsd.html")




















#def generate_image(request):
#     text = request.GET.get('text', 'Hello World')
    
#     # Create an image with PIL
#     image = Image.new('RGB', (200, 100), color=(73, 109, 137))
#     draw = ImageDraw.Draw(image)
#     draw.text((10, 10), text, fill=(255, 255, 0))

#     # Save the image to a bytes buffer
#     buffer = io.BytesIO()
#     image.save(buffer, format='PNG')
#     buffer.seek(0)

#     return HttpResponse(buffer, content_type='image/png')