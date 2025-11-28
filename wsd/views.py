from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pysheds.grid import Grid
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
from django.shortcuts import render

def main(request):
    return render(request,"wsd.html")

# class WatershedProcessor:
    def __init__(self):
        # Initialize variables
        self.grid = None
        self.dem = None
        self.pit_filled_dem = None
        self.flooded_dem = None
        self.inflated_dem = None
        self.fdir = None
        self.acc = None
        self.dirmap = (64, 128, 1, 2, 4, 8, 16, 32)

    def initialize(self):
        # Load and preprocess DEM (runs only once)
        print("Initializing DEM and preprocessing...")
        self.grid = Grid.from_raster(r"/home/nextlevel/Downloads/local-server/pythoncoding/Hydraulics/wsd/static/output_SRTMGL1.tif")
        self.dem = self.grid.read_raster(r"/home/nextlevel/Downloads/local-server/pythoncoding/Hydraulics/wsd/static/output_SRTMGL1.tif")

        # Preprocess DEM
        self.pit_filled_dem = self.grid.fill_pits(self.dem)
        self.flooded_dem = self.grid.fill_depressions(self.pit_filled_dem)
        self.inflated_dem = self.grid.resolve_flats(self.flooded_dem)

        # Compute flow direction
        self.fdir = self.grid.flowdir(self.inflated_dem, dirmap=self.dirmap)

        # Compute flow accumulation
        self.acc = self.grid.accumulation(self.fdir, dirmap=self.dirmap)

        print("DEM initialization complete.")

    def generate_plots(self, lat, lon):
        try:
            # Snap pour point to high accumulation cell
            x_snap, y_snap = self.grid.snap_to_mask(self.acc > 20000, (lon, lat))

            # Delineate the catchment
            catch = self.grid.catchment(x=x_snap, y=y_snap, fdir=self.fdir, dirmap=self.dirmap, xytype='coordinate')
            # self.grid.clip_to(catch)
            # dem_array = self.dem.copy()
            # clipped_catch = np.where(catch, dem_array, np.nan)

            self.grid.clip_to(catch)
            clipped_catch = self.grid.view(catch)

            # clipped_catch = self.grid.view(catch)

            # Extract river network (D8 channels)
            branches = self.grid.extract_river_network(self.fdir, self.acc > 500, dirmap=self.dirmap)

            # Compute flow distance
            dist = self.grid.distance_to_outlet(x=x_snap, y=y_snap, fdir=self.fdir, dirmap=self.dirmap, xytype='coordinate')

            # Generate Delineated Catchment Plot
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            plt.grid('on', zorder=0)
            im1 = ax1.imshow(np.where(clipped_catch, clipped_catch, np.nan), extent=self.grid.extent, zorder=1, cmap='Greys_r')
            plt.plot(lon, lat, 'r*')  # Mark the pour point
            plt.title('Delineated Catchment', size=14)
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            buf1 = io.BytesIO()
            canvas1 = FigureCanvas(fig1)
            canvas1.print_png(buf1)
            plt.close(fig1)
            buf1.seek(0)
            catchment_plot_base64 = base64.b64encode(buf1.read()).decode('utf-8')
            buf1.close()

            # Generate D8 Channels Plot
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            plt.xlim(self.grid.bbox[0], self.grid.bbox[2])
            plt.ylim(self.grid.bbox[1], self.grid.bbox[3])
            ax2.set_aspect('equal')
            for branch in branches['features']:
                line = np.asarray(branch['geometry']['coordinates'])
                plt.plot(line[:, 0], line[:, 1])
            plt.title('D8 Channels', size=14)
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            buf2 = io.BytesIO()
            canvas2 = FigureCanvas(fig2)
            canvas2.print_png(buf2)
            plt.close(fig2)
            buf2.seek(0)
            d8_channels_plot_base64 = base64.b64encode(buf2.read()).decode('utf-8')
            buf2.close()

            # Generate Flow Distance Plot
            fig3, ax3 = plt.subplots(figsize=(8, 6))
            plt.grid('on', zorder=0)
            im3 = ax3.imshow(dist, extent=self.grid.extent, zorder=2, cmap='cubehelix_r')
            plt.colorbar(im3, ax=ax3, label='Distance to outlet (cells)')
            plt.title('Flow Distance', size=14)
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            buf3 = io.BytesIO()
            canvas3 = FigureCanvas(fig3)
            canvas3.print_png(buf3)
            plt.close(fig3)
            buf3.seek(0)
            flow_distance_plot_base64 = base64.b64encode(buf3.read()).decode('utf-8')
            buf3.close()

            # Return all three plots as base64 strings
            return {
                'catchment': catchment_plot_base64,
                'channels': d8_channels_plot_base64,
                'distance': flow_distance_plot_base64
            }
        except Exception as e:
            return {'error': str(e)}

# Instantiate the processor and initialize it (runs only once)
# watershed_processor = WatershedProcessor()
# watershed_processor.initialize()

# import traceback  # Import for detailed error tracing

# from django.http import JsonResponse

@csrf_exempt
def wsd(request):
    if request.method == 'POST':
        try:
            lat = float(request.POST.get('lat'))
            lon = float(request.POST.get('long'))

            # Validate inputs
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                return JsonResponse({'error': 'Latitude must be between -90 and 90, and longitude must be between -180 and 180.'})

            # Generate plots
            plots = watershed_processor.generate_plots(lat, lon)

            # Check for errors
            if 'error' in plots:
                return JsonResponse({'error': plots['error']})

            # Return the plots
            return JsonResponse({
                'images': {
                    'catchment': plots['catchment'],
                    'channels': plots['channels'],
                    'distance': plots['distance']
                }
            })
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'})
    elif request.method == 'GET':
        # Return an empty response for GET requests
        return JsonResponse({'error': 'Invalid request method. Use POST to submit data.'})