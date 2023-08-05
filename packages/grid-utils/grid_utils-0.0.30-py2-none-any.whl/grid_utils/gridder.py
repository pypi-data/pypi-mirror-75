# -*- coding:utf-8 -*-

import six
import numpy as np
from pyproj import Proj
import operator

from .exceptions import *


class NullProj(object):
    """
    Similar to pyproj.Proj, but NullProj does not do actual conversion.
    """
    @property
    def srs(self):
        return ''

    def __call__(self, x, y, **kwargs):
        return x, y


class GridderBase(object):
    """Gridder is a helper for i, j <-> x, y conversion, etc."""
    def i2x(self, *args):
        """Convert i, j, ... -> x, y, ..."""
        raise NotImplementedError

    def x2i(self, *args, **kwargs):
        """Convert x, y, ... -> i, j, ..."""
        raise NotImplementedError

    def copy(self, **kwargs):
        kws = self.dump()
        kws.update(kwargs)
        new_gridder = self.__class__(**kws)
        return new_gridder

    def calibrate(self, x0, y0, x1=None, y1=None):
        return

    def dump(self):
        return {}


class XYGridderBase(GridderBase):
    """
    Requires self.X & self.Y.
    """
    @property
    def bbox(self):
        return (np.min(self.X), np.min(self.Y), np.max(self.X), np.max(self.Y))

    def get_bounding_ij(self, x1, y1, x2, y2, **kwargs):
        bbox = self.bbox
        if x1 is None:
            x1 = bbox[0]
        if y1 is None:
            y1 = bbox[1]
        if x2 is None:
            x2 = bbox[2]
        if y2 is None:
            y2 = bbox[3]

        bad = ~((self.X >= x1) & (self.X <= x2) & (self.Y >= y1) & (self.Y <= y2))
        x_bad = np.alltrue(bad, axis=0)
        y_bad = np.alltrue(bad, axis=1)
        x_points = np.argwhere(np.diff(np.r_[True, x_bad, True])).reshape(-1, 2)
        y_points = np.argwhere(np.diff(np.r_[True, y_bad, True])).reshape(-1, 2)
        i1, i2 = (-1, -1) if x_points.shape[0] == 0 else x_points[0]
        j1, j2 = (-1, -1) if y_points.shape[0] == 0 else y_points[0]
        return i1, j1, i2, j2

    def check_bound(self, i, j, int_index=True):
        start = -0.5
        subtracted = 1
        if int_index:
            start = 0
            if int_index in ('lowerleft', 'll'):
                subtracted = 2
        if np.isscalar(i):
            if (i >= start and i <= self.nx-subtracted) and (j >= start and j <= self.ny-subtracted):
                return i, j
            else:
                raise OutOfGridBound("i: {}, j: {} is out of bound!".format(i, j))
        else:
            i = np.where((i >= start) & (i <= self.nx - subtracted), i, np.nan)
            j = np.where((j >= start) & (j <= self.ny - subtracted), j, np.nan)
            return i, j


class XYProjGridder(XYGridderBase):
    def __init__(self, proj=None, x=None, y=None, nx=None, ny=None, dx=None, dy=None, x_orig=0.0, y_orig=0.0, **kwargs):
        self.proj = proj
        self._reset_raw_xy()
        if x is not None and y is not None:
            self.set_xy(x, y)
        else:
            self._init_with_para(nx, ny, dx, dy, x_orig, y_orig)

    @property
    def proj(self):
        return self._proj
    @proj.setter
    def proj(self, p):
        if p is None:
            self._proj = NullProj()
        elif isinstance(p, (Proj, NullProj)):
            self._proj = p
        elif isinstance(p, dict):
            self._proj = Proj(**p)
        else:  # Treat as proj_string
            self._proj = Proj(str(p))  # TODO: check PY3 compatibility.

        self._reset_raw_xy()
        if all([hasattr(self, attr) for attr in ('_nx', '_ny', '_dx', '_dy', '_x_orig', '_y_orig')]):
            self._updateXY()

    @property
    def X(self):
        return self._X
    @X.setter
    def X(self, x):
        if self._raw_y is None:
            raise ValueError("Cannot set x alone when no raw y presents.")

        ndim_x = np.ndim(x)
        if ndim_x == 1 and np.ndim(self._raw_y) == 1:
            self.set_xy(x, self._raw_y)
        elif ndim_x == 2 and np.shape(x) == np.shape(self.Y):
            self.set_xy(x, self.Y)
        else:
            self._raise_invalid_shape(x, self.Y)

    @property
    def Y(self):
        return self._Y
    @Y.setter
    def Y(self, y):
        if self._raw_x is None:
            raise ValueError("Cannot set y alone when no raw x presents.")

        ndim_y = np.ndim(y)
        if ndim_y == 1 and np.ndim(self._raw_x) == 1:
            self.set_xy(self._raw_x, y)
        elif ndim_y == 2 and np.shape(y) == np.shape(self.X):
            self.set_xy(self.X, y)
        else:
            self._raise_invalid_shape(self.X, y)

    @property
    def CX(self):
        return self._CX

    @property
    def CY(self):
        return self._CY

    @property
    def x(self):
        return self._raw_x if self._raw_x is not None else self._X

    @property
    def y(self):
        return self._raw_y if self._raw_y is not None else self._Y

    @property
    def cx(self):
        return self._raw_cx if self._raw_cx is not None else self._CX

    @property
    def cy(self):
        return self._raw_cy if self._raw_cy is not None else self._CY

    @property
    def nx(self):
        return self._nx
    @nx.setter
    def nx(self, value):
        self._nx = value
        self._reset_raw_xy()
        self._updateXY()

    @property
    def ny(self):
        return self._ny
    @ny.setter
    def ny(self, value):
        self._ny = value
        self._reset_raw_xy()
        self._updateXY()

    @property
    def dx(self):
        return self._dx
    @dx.setter
    def dx(self, value):
        self._dx = value
        self._reset_raw_xy()
        self._updateXY()

    @property
    def dy(self):
        return self._dy
    @dy.setter
    def dy(self, value):
        self._dy = value
        self._reset_raw_xy()
        self._updateXY()

    @property
    def x_orig(self):
        return self._x_orig
    @x_orig.setter
    def x_orig(self, value):
        self._x_orig = value
        self._reset_raw_xy()
        self._updateXY()

    @property
    def y_orig(self):
        return self._y_orig
    @y_orig.setter
    def y_orig(self, value):
        self._y_orig = value
        self._reset_raw_xy()
        self._updateXY()

    @property
    def bbox(self):
        return self._bbox

    @property
    def cbox(self):
        """corner box"""
        return self._cbox

    def _init_with_para(self, nx, ny, dx, dy, x_orig, y_orig):
        self._nx = nx
        self._ny = ny
        self._dx = dx
        self._dy = dy
        self._x_orig = x_orig
        self._y_orig = y_orig

        self._updateXY()

    @property
    def has_null_proj(self):
        return isinstance(self.proj, NullProj)

    def set_xy(self, x, y):
        ndim_x, ndim_y = np.ndim(x), np.ndim(y)
        if ndim_x == 1 and ndim_y == 1:
            self._nx, self._ny = len(x), len(y)
        elif ndim_x == 2 and ndim_y == 2:
            self._ny, self._nx = np.shape(x)
        else:
            self._raise_invalid_shape(x, y)

        self._raw_x, self._raw_y = np.asarray(x), np.asarray(y)
        self.calibrate(x, y)

    def _raise_invalid_shape(self, x, y):
        raise ValueError("Invalid x, y shape: {}, {}".format(np.shape(x), np.shape(y)))

    def _reset_raw_xy(self):
        self._raw_x, self._raw_y = None, None

    def _updateXY(self):
        jj, ii = np.mgrid[0:self.ny, 0:self.nx]
        cjj, cii = np.mgrid[-0.5:self.ny, -0.5:self.nx]
        xx, yy = self.i2x(ii, jj)
        cxx, cyy = self.i2x(cii, cjj)

        self._X, self._Y = xx, yy
        self._CX, self._CY = cxx, cyy

        if self._raw_x is not None and self._raw_x.ndim == 1:
            self._raw_cx = self._CX[0]
        else:
            self._raw_cx = None

        if self._raw_y is not None and self._raw_y.ndim == 1:
            self._raw_cy = self._CY[:, 0]
        else:
            self._raw_cy = None

        self._bbox = (np.min(self._X), np.min(self._Y), np.max(self._X), np.max(self._Y))
        self._cbox = (np.min(self._CX), np.min(self._CY), np.max(self._CX), np.max(self._CY))

        return xx, yy

    def i2x(self, i, j):
        px = i * self.dx + self.x_orig
        py = j * self.dy + self.y_orig
        return self.proj(px, py, inverse=True)

    def x2i(self, x, y, int_index=True, check_bound=None):
        px, py = self.proj(x, y)
        i = (px - self.x_orig) / self.dx
        j = (py - self.y_orig) / self.dy
        if int_index:
            if int_index in ('lowerleft', 'll'):
                i = np.floor(i)
                j = np.floor(j)
            else:
                i = np.round(i)
                j = np.round(j)
            if np.isscalar(i):
                i = int(i)
                j = int(j)
            else:
                i = i.astype('i')
                j = j.astype('i')

        if check_bound:
            return self.check_bound(i, j, int_index=int_index)
        else:
            return i, j

    def calibrate(self, x, y, x1=None, y1=None):
        ndim_x, ndim_y = np.ndim(x), np.ndim(y)
        if ndim_x == 0 and ndim_y == 0:
            x0, y0 = x, y
        if ndim_x == 1 and ndim_y == 1:
            x0, x1 = x[0], x[1]
            y0, y1 = y[0], y[1]
        elif ndim_x == 2 and ndim_y == 2:
            x0, x1 = x[0, 0], x[1, 1]
            y0, y1 = y[0, 0], y[1, 1]
        else:
            self._raise_invalid_shape(x, y)

        px0, py0 = self.proj(x0, y0)

        self._x_orig = px0
        self._y_orig = py0

        if x1 is not None and y1 is not None:
            px1, py1 = self.proj(x1, y1)
            self._dx = px1 - px0
            self._dy = py1 - py0

        self._updateXY()

    def dump(self):
        return {
            "proj": self.proj.srs,
            "nx": self.nx, "ny": self.ny, "dx": self.dx, "dy": self.dy,
            "x_orig": self.x_orig, "y_orig": self.y_orig
        }


class LonLatSurroundingGridder(XYGridderBase):
    def __init__(self, lon0, lat0, rmin, rmax, nr, ntheta, theta0=0.0, r_earth=6371):
        self.lon0 = lon0
        self.lat0 = lat0
        self.rmin = rmin
        self.rmax = rmax
        self.nr = nr
        self.ntheta = ntheta
        self.theta0 = theta0
        self.r_earth = r_earth

        self.dtheta = np.pi * 2 / self.ntheta
        self.dr = (self.rmax - self.rmin) / (self.nr - 1)
        self._updateXY()

    def _updateXY(self):
        r = np.linspace(self.rmin, self.rmax, self.nr)
        theta = np.arange(self.ntheta) * self.dtheta + self.theta0

        THETA, R = np.meshgrid(theta, r)
        LON, LAT = self.r_theta_to_lon_lat(R, THETA)

        self._X = LON
        self._Y = LAT

        return self._X, self._Y

    def r_theta_to_lon_lat(self, r, theta):
        r_ = r / self.r_earth
        sin_r = np.sin(r_)
        cos_r = np.cos(r_)
        lat0_ = np.deg2rad(self.lat0)
        lon0_ = np.deg2rad(self.lon0)
        sin_lat0 = np.sin(lat0_)
        cos_lat0 = np.cos(lat0_)

        sin_lat = sin_lat0 * cos_r + cos_lat0 * sin_r * np.cos(theta)
        lat_ = np.arcsin(sin_lat)
        lon_ = lon0_ + np.arctan2(np.sin(theta) * sin_r * cos_lat0, cos_r - sin_lat0 * sin_lat)

        lon = np.rad2deg(lon_)
        lat = np.rad2deg(lat_)
        return lon, lat

    @property
    def nx(self):
        return self.ntheta

    @property
    def ny(self):
        return self.nr

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def x(self):
        return self._X

    @property
    def y(self):
        return self._Y

    def i2x(self, i, j):
        theta = self.theta0 + i * self.dtheta
        r = self.rmin + j * self.dr
        lon, lat = self.r_theta_to_lon_lat(r, theta)
        return lon, lat

    def x2i(self, x, y, int_index=True, check_bound=None):
        lon2, lat2 = np.deg2rad(x), np.deg2rad(y)
        lon1, lat1 = np.deg2rad(self.lon0), np.deg2rad(self.lat0)
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        sin_dlon = np.sin(dlon)
        cos_dlon = np.cos(dlon)
        sin_lat1 = np.sin(lat1)
        cos_lat1 = np.cos(lat1)
        sin_lat2 = np.sin(lat2)
        cos_lat2 = np.cos(lat2)

        a = cos_lat2 * sin_dlon
        b = cos_lat1 * sin_lat2 - sin_lat1 * cos_lat2 * cos_dlon

        theta = np.arctan2(a, b)

        c = np.sin(dlat / 2) ** 2 + cos_lat1 * cos_lat2 * np.sin(dlon / 2) ** 2
        d = 2 * np.arcsin(np.sqrt(c))

        r = d * self.r_earth

        i = (theta - self.theta0) / self.dtheta % self.ntheta
        j = (r - self.rmin) / self.dr

        if int_index:
            i = np.round(i)
            j = np.round(j)

            if np.isscalar(i):
                i = int(i)
                j = int(j)
            else:
                i = i.astype('i')
                j = j.astype('i')

        if check_bound:
            return self.check_bound(i, j, int_index=int_index)
        else:
            return i, j


class XYIrregularGridder(XYGridderBase):
    # TODO: use kdtree.
    def __init__(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        if X.ndim == 1:
            self.X, self.Y = np.meshgrid(X, Y)
        else:
            self.X, self.Y = X, Y

        self.ny, self.nx = X.shape

    def i2x(self, i, j, *args, **kwargs):
        return self.X[j, i], self.Y[j, i]

    def x2i(self, x, y, *args, **kwargs):
        distances = np.hypot(self.X-x, self.Y-y)
        flat_i = np.argmin(distances)
        nx = self.X.shape[1]
        return flat_i / self.nx, flat_i % self.nx

    def dump(self):
        return {
            "X": self.X,
            "Y": self.Y,
            "nx": self.nx,
            "ny": self.ny,
        }
