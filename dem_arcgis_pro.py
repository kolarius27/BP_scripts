import arcpy
import os


def dem_generator():
    arcpy.env.workspace = "C:\\Users\\michal\\Desktop\\_BP"
    arcpy.env.overwriteOutput = 1
    print("Creating list of las files...")
    las_pasy = []
    for root, dirs, files in os.walk(r'C:\Users\michal\Desktop\_BP\Krkonose\LiDAR\area_81'):
        for file in files:
            if file.endswith('.las'):
                pas = ("Krkonose\\LiDAR\\area_81\\" + file, "gis\\las_pasy_dem\\arcgis\\area_n81\\" + file[:-4] + "_dem.tif")
                las_pasy.append(pas)
    print("List of las files created!")

    for las in las_pasy:
        print("Rasterizing: ", las[0])
        arcpy.env.snapRaster = "Krkonose\\2019_06_14_Lucni_2_DSM.tif"
        arcpy.env.cellSize = "Krkonose\\2019_06_14_Lucni_2_DSM.tif"
        arcpy.env.extent = "MAXOF"
        arcpy.LasDatasetToRaster_conversion(las[0], las[1], "ELEVATION", "TRIANGULATION LINEAR MINIMUM 0,05",
                                            "FLOAT", "CELLSIZE", 0.05, 1)
        arcpy.env.extent = "Krkonose\\area_n81.shp"
        arcpy.LasDatasetToRaster_conversion(las[0], las[2], "ELEVATION", "TRIANGULATION LINEAR MINIMUM 0,05",
                                            "FLOAT", "CELLSIZE", 0.05, 1)
        print("Done!")

    print("DEMs generated.")


def dem2dem_comparision():
    arcpy.env.workspace = "C:\\Users\\michal\\Desktop\\_BP"
    arcpy.env.overwriteOutput = 1
    print("Creating list of DEM files...")
    dem_pasy = []
    for root, dirs, files in os.walk(r'C:\Users\michal\Desktop\_BP\gis\las_pasy_dem\arcgis\full'):
        for file in files:
            if file.endswith('_dem.tif'):
                pas = ("gis\\las_pasy_dem\\arcgis\\full\\" + file, "gis\\las_pasy_dem\\arcgis\\full\\dem2dem\\" + file[:-8] + "_dem2dem.tif",
                       "gis\\las_pasy_dem\\arcgis\\area_n81\\dem2dem\\" + file[:-8] + "_area81_dem2dem.tif")
                dem_pasy.append(pas)
    print("List of DEM files created!")

    krnap_dem = arcpy.Raster("Krkonose\\2019_06_14_Lucni_2_DSM.tif")
    for dem in dem_pasy:
        print("Calculating DEM difference: ", dem[0])
        os.chdir("C:\\Users\\michal\\Desktop\\_BP")
        arcpy.env.snapRaster = "Krkonose\\2019_06_14_Lucni_2_DSM.tif"
        arcpy.env.cellSize = "Krkonose\\2019_06_14_Lucni_2_DSM.tif"
        arcpy.env.extent = dem[0]
        las_dem = arcpy.Raster(dem[0])
        dem2dem = las_dem - krnap_dem
        dem2dem.save(dem[1])
        arcpy.env.extent = "Krkonose\\area_n81.shp"
        las_dem = arcpy.Raster(dem[0])
        dem2dem = las_dem - krnap_dem
        dem2dem.save(dem[2])
        print("Done!")


def hillshade_generator():
    arcpy.env.workspace = "C:\\Users\\michal\\Desktop\\_BP"
    arcpy.env.overwriteOutput = 1
    print("Creating list of DEM files...")
    dem_pasy2 = []
    for root, dirs, files in os.walk(r'C:\Users\michal\Desktop\_BP\gis\las_pasy_dem\arcgis\full'):
        for file in files:
            if file.endswith('_dem.tif'):
                pas = ("gis\\las_pasy_dem\\arcgis\\full\\" + file,
                       "gis\\las_pasy_dem\\arcgis\\full\\hillshade\\" + file[:-8] + "_hillshade.tif",
                       "gis\\las_pasy_dem\\arcgis\\area_n81\\hillshade\\" + file[:-8] + "_area81_hillshade.tif")
                dem_pasy2.append(pas)
    print("List of DEM files created!")

    for dem in dem_pasy2:
        print("Generating hillshade: ", dem[0])
        arcpy.env.snapRaster = "Krkonose\\2019_06_14_Lucni_2_DSM.tif"
        arcpy.env.cellSize = "Krkonose\\2019_06_14_Lucni_2_DSM.tif"
        arcpy.env.extent = "MAXOF"
        arcpy.HillShade_3d(dem[0], dem[1])
        arcpy.env.extent = "Krkonose\\area_n81.shp"
        arcpy.HillShade_3d(dem[0], dem[2])
        print("Done!")


hillshade_generator()







