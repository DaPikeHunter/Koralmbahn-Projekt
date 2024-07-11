import geopandas as gpd
def anzeigen_shapefile(shapefile_pfad):
    gdf = gpd.read_file(shapefile_pfad)
    print(gdf)
if __name__ == "__main__":
    shapefile_pfad = 'W:\STATSICH\Praktikanten Tätigkeiten\Ogris\gembezwinners'
    anzeigen_shapefile(shapefile_pfad)