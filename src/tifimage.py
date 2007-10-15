#!/usr/bin/env python
"""

Authors: Henning O. Sorensen & Erik Knudsen
         Center for Fundamental Research: Metal Structures in Four Dimensions
         Risoe National Laboratory
         Frederiksborgvej 399
         DK-4000 Roskilde
         email:henning.sorensen@risoe.dk

mods for fabio by JPW

"""

from PIL import Image
import Numeric

from fabio.fabioimage import fabioimage

TIFF_TO_NUMERIC = { "I;16": Numeric.Int16 ,
                   
                    }
                    

class tifimage(fabioimage):
    """
    Images in TIF format
    Wraps PIL
    """
    def _readheader(self, filename):
        """
        Don't know how to read tiff tags yet...
        """
        self.header = { "filename" : filename }

    def read(self, fname):
        """
        The fabian read was reading a PIL image
        We convert this to a Numeric (numpy) array
        """
        infile = self._open(fname)
        self._readheader(infile)
        infile.seek(0)
        self.pilimage = Image.open(infile)
        
        # For some odd reason the getextrema does not work on unsigned 16 bit
        # but it does on 32 bit images, hence convert if 16 bit
        if TIFF_TO_NUMERIC.has_key(self.pilimage.mode) and self.pilimage.mode != "I;16":
            self.data = Numeric.fromstring(
                self.pilimage.tostring(),
                TIFF_TO_NUMERIC[self.pilimage.mode])
            self.bpp = len(Numeric.ones(1,
                          TIFF_TO_NUMERIC[self.pilimage.mode]).tostring())
            self.dim1, self.dim2 = self.pilimage.size
        else:
            temp = self.pilimage.convert("I") # 32 bit signed
            self.data = Numeric.fromstring(
                temp.tostring(),
                Numeric.Int32)
            self.bpp = 4
            self.dim1, self.dim2 = self.pilimage.size
            self.pilimage = temp
        
        self.dim1, self.dim2 = self.pilimage.size
        self.data.shape = (self.dim1, self.dim2)
        self.resetvals()
        return self 

    def write(self, fname):
        """
        ... at least try ...
        """
        if self.pilimage is None:
            self.toPIL16()
        self.pilimage.save(fname, "TIFF")
        