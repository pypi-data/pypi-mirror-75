
from osgeo import gdal, gdalnumeric, ogr
import os
from PIL import Image, ImageDraw
import os
import operator
from functools import reduce
import matplotlib.pyplot as plt
from hjn.mkNCHJN import LeftTopCornerPairArr,envelope
import numpy as np
import netCDF4 as nc
import copy


class maskClip():
    def __init__(self,ncPath,step):
        with nc.Dataset(ncPath) as data:
            self.dem = data["dem"][:]
            self.latArr = data["lat"][:]
            self.lonArr = data["lon"][:]

        oriStep=np.abs((self.latArr[0]-self.latArr[-1])/(len(self.latArr)-1))
        range=int(step/oriStep)
        self.dem=self.dem[::range,::range]

        self.ltc = envelope(self.latArr[0], self.latArr[-1], self.lonArr[0], self.lonArr[-1])
        self.step = step

    def world2Pixel(self,ltc, x, y):
        """
        Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
        the pixel location of a geospatial coordinate
        """
        ulX = ltc.w
        ulY = ltc.n
        xDist = self.step

        pixel = int((x - ulX) / xDist)
        line = int((ulY - y) / xDist)
        return (pixel, line)

    def imageToArray(self,i):
        """
        Converts a Python Imaging Library array to a
        gdalnumeric image.
        """
        a=gdalnumeric.fromstring(i.tobytes(),'b')
        a.shape=i.im.size[1], i.im.size[0]
        return a

    def clip(self,shapefile_path):

        print(self.latArr[0], self.lonArr[0])

        # Create an OGR layer from a boundary shapefile
        shapef = ogr.Open(shapefile_path)
        lyr = shapef.GetLayer(os.path.split(os.path.splitext(shapefile_path)[0])[1])
        poly = lyr.GetNextFeature()

        # Convert the layer extent to image pixel coordinates
        minX, maxX, minY, maxY = lyr.GetExtent()

        ulX, ulY = self.world2Pixel(self.ltc,  minX, maxY)
        lrX, lrY = self.world2Pixel(self.ltc, maxX, minY)

        # Calculate the pixel size of the new image
        pxWidth = int(lrX - ulX)
        pxHeight = int(lrY - ulY)

        # clip = srcArray[ulY:lrY, ulX:lrX]

        # EDIT: create pixel offset to pass to new image Projection info
        #
        xoffset = ulX
        yoffset = ulY
        print("Xoffset, Yoffset = ( %f, %f )" % (xoffset, yoffset))

        ltc1 = copy.copy(self.ltc)
        ltc1.n = maxY
        ltc1.w = minX

        # Map points to pixels for drawing the
        # boundary on a blank 8-bit,
        # black and white, mask image.
        points = []
        pixels = []
        geom = poly.GetGeometryRef()
        pts = geom.GetGeometryRef(0)
        for p in range(pts.GetPointCount()):
            points.append((pts.GetX(p), pts.GetY(p)))
        for p in points:
            pixels.append(self.world2Pixel(ltc1,  p[0], p[1]))
        rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
        rasterize = ImageDraw.Draw(rasterPoly)
        rasterize.polygon(pixels, 0)
        mask = self.imageToArray(rasterPoly)

        latOffset0 = int((self.ltc.n - maxY) / self.step)
        latOffset1 = self.dem.shape[0] - int((self.ltc.n - minY) / self.step)
        lonOffset0 = int((minX - self.ltc.w) / self.step)
        lonOffset1 = self.dem.shape[1] - int((maxX - self.ltc.w) /self.step)
        ndarray = np.pad(mask, ((latOffset0, latOffset1),
                                (lonOffset0, lonOffset1)), 'constant', constant_values=(1, 1))

        # print(dem.shape)
        # print(ndarray.shape)

        # plt.imshow(ndarray)
        # plt.show()

        clip = copy.copy(self.dem)

        clip[ndarray != 0] = np.nan
        
        return clip
        # plt.imshow(clip)
        # plt.show()

