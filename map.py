#import tkinter as tk
#from PIL import Image, ImageTk

#def show_image(image_path):
#    root = tk.Tk()
#    root.title("Bildanzeige")
#    image = Image.open(image_path)
#    photo = ImageTk.PhotoImage(image)
#    label = tk.Label(root, image=photo)
#    label.image = photo
#    label.pack()
#    root.mainloop()

#image_path = #Pfad

#show_image(image_path)

#import bokeh
import geopandas as gpd
#from bokeh.io import curdoc
from bokeh.io import show
from bokeh.models import HoverTool, ColumnDataSource, TapTool, CustomJS
from bokeh.plotting import figure
#from bokeh.palettes import Viridis6
#from bokeh.models.widgets import Select
#from bokeh.events import Tap
#from bokeh.tile_providers import get_provider, Vendors
#import json
#import matplotlib.pyplot as plt
#tile_provider = get_provider(Vendors.CARTODBPOSITRON)

def anzeigen_shapefile(shapefile_pfad):
    gdf = gpd.read_file(shapefile_pfad)
    print(gdf)
    gdf['x'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[0]), axis = 1)
    gdf['y'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[1]), axis = 1)
   
    #Bokeh Datenquelle
    n = len(gdf)
    source = ColumnDataSource(data=dict(
        x=gdf['x'].tolist(),
        y=gdf['y'].tolist(),
        gemeinde =gdf['GEMNAM'].tolist(), #Spaltenname
        gkz = gdf['GKZ'].tolist(),
        line_color = ['white'] * n,
        line_width = [0.5] * n,
        selected_indices=[None] * n,
        selected_gkz=[None] * n
    ))
    #print(source)
    #Bokeh Figur
    p = figure(title="Kärnten Karte mit Gemeinden", tools = "pan,wheel_zoom,reset,save,tap",
               x_axis_location = None, y_axis_location=None,
               tooltips=[("Gemeinde", "@gemeinde")],
               width =1872, height = 966)
    p.grid.grid_line_color = None
    patches = p.patches('x', 'y', source = source,
              fill_alpha=0.7, line_color='line_color', line_width='line_width',
              fill_color='blue')
    
    #Hover
    hover = HoverTool()
    hover.tooltips = [("Gemeinde", "@gemeinde")]
    hover.renderers = [patches]
    p.add_tools(hover)
    
    #Laden des JS
    with open("callback.js", "r") as f: js_code = f.read()

    #callback für das markieren
    callback = CustomJS(args=dict(source=source), code=js_code)
    
    
    taptool = p.select(type=TapTool)
    taptool.callback = callback
    show(p)

    #fig, ax =plt.subplots()          <----- Matplotlib; Wird nicht mehr benötigt
    #gdf.plot(ax=ax)
    #ax.set_axis_off()
    #plt.subplots_adjust(left = 0, right = 1, top=1, bottom=0)
    #plt.show()
    
if __name__ == "__main__":
    shapefile_pfad = r'W:\STATSICH\Praktikanten Tätigkeiten\Ogris\gembez'
    anzeigen_shapefile(shapefile_pfad)
    #map(shapefile_pfad)
