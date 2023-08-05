# Copyright (c) 2020, Manfred Moitzi
# License: MIT License
# Created: 2020-07-10
from typing import TYPE_CHECKING, List, Tuple, Iterable, Sequence
from collections import abc
from enum import Enum
import math
from ezdxf.math import (
    Vector, NULLVEC, Bezier4P, Matrix44, bulge_to_arc, cubic_bezier_from_ellipse,
    ConstructionEllipse, Z_AXIS, BSpline, OCS
)

if TYPE_CHECKING:
    from ezdxf.eztypes import LWPolyline, Polyline, Vertex, Spline, Ellipse, Arc, Circle
    from ezdxf.entities.hatch import PolylinePath, EdgePath

__all__ = ['Path', 'Command']


class Command(Enum):
    LINE_TO = 1
    CURVE_TO = 2


class Path(abc.Sequence):
    def __init__(self, start: 'Vertex' = NULLVEC):
        self._start = Vector(start)
        self._commands: List[Tuple] = []

    def __len__(self):
        return len(self._commands)

    def __getitem__(self, item):
        return self._commands[item]

    def __iter__(self):
        return iter(self._commands)

    @property
    def start(self) -> Vector:
        """ :class:`Path` start point, resetting the start point of an empty path is possible. """
        return self._start

    @start.setter
    def start(self, location: 'Vertex') -> None:
        if len(self._commands):
            raise ValueError('Requires an empty path.')
        else:
            self._start = Vector(location)

    @property
    def end(self) -> Vector:
        """ :class:`Path` end point. """
        if self._commands:
            return self._commands[-1][1]
        else:
            return self._start

    @property
    def is_closed(self) -> bool:
        """ Returns ``True`` if the start point is close to the end point. """
        return self._start.isclose(self.end)

    @classmethod
    def from_vertices(cls, vertices: Iterable['Vertex'], close=False) -> 'Path':
        """ Returns a :class:`Path` from vertices.  """
        vertices = Vector.list(vertices)
        path = cls(start=vertices[0])
        for vertex in vertices[1:]:
            path.line_to(vertex)
        if close:
            path.close()
        return path

    @classmethod
    def from_lwpolyline(cls, lwpolyline: 'LWPolyline') -> 'Path':
        """ Returns a :class:`Path` from a :class:`~ezdxf.entities.LWPolyline` entity, all vertices
        transformed to WCS.
        """
        assert lwpolyline.dxftype() == 'LWPOLYLINE'
        path = cls()
        path._setup_polyline_2d(
            lwpolyline.get_points('xyb'),
            close=lwpolyline.closed,
            ocs=lwpolyline.ocs(),
            elevation=lwpolyline.dxf.elevation,
        )
        return path

    @classmethod
    def from_polyline(cls, polyline: 'Polyline') -> 'Path':
        """ Returns a :class:`Path` from a :class:`~ezdxf.entities.Polyline` entity, all vertices
        transformed to WCS.
        """
        assert polyline.dxftype() == 'POLYLINE'
        path = cls()

        if len(polyline.vertices) == 0:
            return path

        if polyline.is_3d_polyline:
            return cls.from_vertices(polyline.points(), polyline.is_closed)

        points = [vertex.format('xyb') for vertex in polyline.vertices]
        ocs = polyline.ocs()
        if polyline.dxf.hasattr('elevation'):
            elevation = Vector(polyline.dxf.elevation).z
        else:
            # Elevation attribute is mandatory, but you never know,
            # take elevation from first vertex.
            elevation = Vector(polyline.vertices[0].dxf.location).z
        path._setup_polyline_2d(
            points,
            close=polyline.is_closed,
            ocs=ocs,
            elevation=elevation,
        )
        return path

    def _setup_polyline_2d(self, points: Iterable[Sequence[float]], close: bool, ocs: OCS, elevation: float) -> None:
        def bulge_to(p1: Vector, p2: Vector, bulge: float):
            if p1.isclose(p2):
                return
            center, start_angle, end_angle, radius = bulge_to_arc(p1, p2, bulge)
            ellipse = ConstructionEllipse.from_arc(
                center, radius, Z_AXIS,
                math.degrees(start_angle),
                math.degrees(end_angle),
            )
            curves = list(cubic_bezier_from_ellipse(ellipse))
            if curves[0].control_points[0].isclose(p2):
                curves = _reverse_bezier_curves(curves)
            self.add_curves(curves)

        prev_point = None
        prev_bulge = 0
        for x, y, bulge in points:
            point = Vector(x, y)
            if prev_point is None:
                self._start = point
                prev_point = point
                prev_bulge = bulge
                continue

            if prev_bulge:
                bulge_to(prev_point, point, prev_bulge)
            else:
                self.line_to(point)
            prev_point = point
            prev_bulge = bulge

        if close and not self.start.isclose(self.end):
            if prev_bulge:
                bulge_to(self.end, self.start, prev_bulge)
            else:
                self.line_to(self.start)

        if ocs.transform or elevation:
            self._to_wcs(ocs, elevation)

    def _to_wcs(self, ocs: OCS, elevation: float):
        self._start = ocs.to_wcs(self._start.replace(z=elevation))
        for i, cmd in enumerate(self._commands):
            new_cmd = [cmd[0]]
            new_cmd.extend(ocs.points_to_wcs(p.replace(z=elevation) for p in cmd[1:]))
            self._commands[i] = tuple(new_cmd)

    @classmethod
    def from_spline(cls, spline: 'Spline', level: int = 4) -> 'Path':
        """ Returns a :class:`Path` from a :class:`~ezdxf.entities.Spline`. """
        path = cls()
        path.add_spline(spline.construction_tool(), level=level, reset=True)
        return path

    @classmethod
    def from_ellipse(cls, ellipse: 'Ellipse', segments: int = 1) -> 'Path':
        """ Returns a :class:`Path` from a :class:`~ezdxf.entities.Ellipse`. """
        path = cls()
        path.add_ellipse(ellipse.construction_tool(), segments=segments, reset=True)
        return path

    @classmethod
    def from_arc(cls, arc: 'Arc', segments: int = 1) -> 'Path':
        """ Returns a :class:`Path` from an :class:`~ezdxf.entities.Arc`. """
        path = cls()
        ellipse = ConstructionEllipse.from_arc(
            center=arc.dxf.center,
            radius=arc.dxf.radius,
            extrusion=arc.dxf.extrusion,
            start_angle=arc.dxf.start_angle,
            end_angle=arc.dxf.end_angle,
        )
        path.add_ellipse(ellipse, segments=segments, reset=True)
        return path

    @classmethod
    def from_circle(cls, circle: 'Circle', segments: int = 1) -> 'Path':
        """ Returns a :class:`Path` from a :class:`~ezdxf.entities.Circle`. """
        path = cls()
        ellipse = ConstructionEllipse.from_arc(
            center=circle.dxf.center,
            radius=circle.dxf.radius,
            extrusion=circle.dxf.extrusion,
        )
        path.add_ellipse(ellipse, segments=segments, reset=True)
        return path

    @classmethod
    def from_hatch_polyline_path(cls, path: 'PolylinePath') -> 'Path':
        """ Returns a :class:`Path` from a :class:`~ezdxf.entities.Hatch` polyline path. """
        pass

    @classmethod
    def from_hatch_edge_path(cls, path: 'EdgePath') -> 'Path':
        """ Returns a :class:`Path` from a :class:`~ezdxf.entities.Hatch` edge path. """
        pass

    def line_to(self, location: 'Vertex') -> None:
        """ Add a line from actual path end point to `location`.
        """
        self._commands.append((Command.LINE_TO, Vector(location)))

    def curve_to(self, location: 'Vertex', ctrl1: 'Vertex', ctrl2: 'Vertex') -> None:
        """ Add a cubic Bèzier-curve from actual path end point to `location`, `ctrl1` and
        `ctrl2` are the control points for the cubic Bèzier-curve.
        """
        self._commands.append((Command.CURVE_TO, Vector(location), Vector(ctrl1), Vector(ctrl2)))

    def close(self) -> None:
        """ Close path by adding a line segment from the end point to the start point. """
        if not self.is_closed:
            self.line_to(self.start)

    def add_curves(self, curves: Iterable[Bezier4P]) -> None:
        """ Add multiple cubic Bèzier-curves to the path.

        Auto-detect if the path end point is connected to the start- or end point of the curves,
        if none of them is close to the path end point a line from the path end point to the
        curves start point will be added.

        """
        curves = list(curves)
        if not len(curves):
            return
        end = curves[-1].control_points[-1]
        if self.end.isclose(end):
            # connect to new curves end point
            curves = _reverse_bezier_curves(curves)

        for curve in curves:
            start, ctrl1, ctrl2, end = curve.control_points
            if not start.isclose(self.end, abs_tol=1e-9):
                self.line_to(start)
            self.curve_to(end, ctrl1, ctrl2)

    def add_ellipse(self, ellipse: ConstructionEllipse, segments=1, reset=True) -> None:
        """ Add an elliptical arc as multiple cubic Bèzier-curves, use
        :meth:`~ezdxf.math.ConstructionEllipse.from_arc` constructor of class
        :class:`~ezdxf.math.ConstructionEllipse` to add circular arcs.

        Auto-detect connection point, if none is close a line from the path end point to the
        ellipse start point will be added (see :meth:`add_curves`).

        By default the start of an **empty** path is set to the start point of the ellipse,
        setting argument `reset` to ``False`` prevents this behavior.

        Args:
            ellipse: ellipse parameters as :class:`~ezdxf.math.ConstructionEllipse` object
            segments: count of Bèzier-curve segments, at least one segment for each quarter (pi/2),
                      ``1`` for as few as possible.
            reset: set start point to start of ellipse if path is empty

        """
        if len(self) == 0 and reset:
            self.start = ellipse.start_point
        self.add_curves(cubic_bezier_from_ellipse(ellipse, segments))

    def add_spline(self, spline: BSpline, level=4, reset=True) -> None:
        """ Add a B-spline as multiple cubic Bèzier-curves.

        Non-rational B-splines of 3rd degree gets a perfect conversion to cubic bezier
        curves with a minimal count of curve segments, all other B-spline require much
        more curve segments for approximation.

        Auto-detect connection point, if none is close a line from the path end point to the
        spline start point will be added (see :meth:`add_curves`).

        By default the start of an **empty** path is set to the start point of the spline,
        setting argument `reset` to ``False`` prevents this behavior.

        Args:
            spline: B-spline parameters as :class:`~ezdxf.math.BSpline` object
            level: subdivision level of approximation segments
            reset: set start point to start of spline if path is empty

        """
        if len(self) == 0 and reset:
            self.start = spline.point(0)
        if spline.degree == 3 and not spline.is_rational and spline.is_clamped:
            curves = [Bezier4P(points) for points in spline.bezier_decomposition()]
        else:
            curves = spline.cubic_bezier_approximation(level=level)
        self.add_curves(curves)

    def approximate(self, segments: int = 20) -> Iterable[Vector]:
        """ Approximate path by vertices, `segments` is the count of approximation segments
        for each cubic bezier curve.
        """
        if not self._commands:
            return

        start = self._start
        yield start

        for cmd in self._commands:
            type_ = cmd[0]
            end_location = cmd[1]
            if type_ == Command.LINE_TO:
                yield end_location
            elif type_ == Command.CURVE_TO:
                pts = iter(Bezier4P((start, cmd[2], cmd[3], end_location)).approximate(segments))
                next(pts)  # skip first vertex
                yield from pts
            else:
                raise ValueError(f'Invalid command: {type_}')
            start = end_location

    def transform(self, m: 'Matrix44') -> 'Path':
        """ Returns a new transformed path.

        Args:
             m: transformation matrix of type :class:`~ezdxf.math.Matrix44`

        """
        new_path = self.__class__(m.transform(self.start))
        for cmd in self._commands:
            type_ = cmd[0]
            if type_ == Command.LINE_TO:
                new_path.line_to(m.transform(cmd[1]))
            elif type_ == Command.CURVE_TO:
                loc, ctrl1, ctrl2 = m.transform_vertices(cmd[1:])
                new_path.curve_to(loc, ctrl1, ctrl2)
            else:
                raise ValueError(f'Invalid command: {type_}')

        return new_path


def _reverse_bezier_curves(curves: List[Bezier4P]) -> List[Bezier4P]:
    curves = list(c.reverse() for c in curves)
    curves.reverse()
    return curves
