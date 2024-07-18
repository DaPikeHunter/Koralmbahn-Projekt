import geopandas as gpd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, TapTool
from bokeh.layouts import column

def anzeigen_shapefile(shapefile_pfad, gkz_list):
    selected: str = "#ff0000"
    unselected: str = "#d2b48c"
    # Read the shapefile using GeoPandas
    gdf = gpd.read_file(shapefile_pfad)

    # Extract x and y coordinates from the geometry
    gdf['x'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[0]), axis=1)
    gdf['y'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[1]), axis=1)

    # Prepare data for Bokeh
    n = len(gdf)
    source = ColumnDataSource(data=dict(
        x=gdf['x'].tolist(),
        y=gdf['y'].tolist(),
        gemeinde=gdf['GEMNAM'].tolist(),  # Adjust the column name if different
        gkz=gdf['GKZ'].tolist(),
        line_color=['black'] * n,
        line_width=[0.5] * n,
        fill_color=[selected if gkz in gkz_list else unselected for gkz in gdf['GKZ']],
        selected_gkz=gkz_list  # Pass the initial selected GKZs
    ))

    # Create a Bokeh figure
    p = figure(
        #title="Kärnten Karte mit Gemeinden"
        title="", tools="pan,wheel_zoom,reset,save,tap",
        x_axis_location=None, y_axis_location=None,
        tooltips=[("", "@gemeinde")],
        width=1872//4, height=966//4
    )
    p.grid.grid_line_color = None

    # Add patches to the figure

    patches = p.patches(
        'x', 'y', source=source,
        fill_alpha=1, line_color='line_color', line_width='line_width',
        fill_color='fill_color'
    )

# Customize the selection and non-selection glyphs
    patches.selection_glyph = patches.glyph.clone()
    patches.selection_glyph.fill_alpha = 1  # Fully opaque when selected
    patches.selection_glyph.line_width = 0.5    # Thicker border when selected

    patches.nonselection_glyph = patches.glyph.clone()
    patches.nonselection_glyph.fill_alpha = 1  # More transparent when not selected
    #patches.nonselection_glyph.line_alpha = 1.0  # Dimmed border when not selected
    patches.nonselection_glyph.line_width = 0.5    # Thicker border when selected

    # Add hover tool
    hover = HoverTool()
    hover.tooltips = [("", "@gemeinde")]
    hover.renderers = [patches]
    #hover.renderers = [patches2]
    p.add_tools(hover)


    with open("callback2.js", "r") as f:
        js_code = f.read()
    #print(js_code)  # Verify the contents

    # Define the callback for the tap tool
    callback = CustomJS(args=dict(source=source), code=js_code)
    #callback2 = CustomJS(args=dict(source2=source2), code=js_code)
    taptool = p.select(type=TapTool)
    taptool.callback = callback
    p.toolbar.logo = None
    p.toolbar_location = None
    #taptool.callback = callback2

    #print(callback)  # Verify the CustomJS object

    # Return the Bokeh layout
    return column(p)

gkz_list = ['']*132
#gkz_list2 = ['']*132

layout = anzeigen_shapefile( r'W:\STATSICH\Praktikanten Tätigkeiten\Ogris\gembez', gkz_list)
show(layout)
