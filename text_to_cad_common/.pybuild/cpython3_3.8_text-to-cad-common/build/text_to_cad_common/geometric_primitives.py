"""
Filename: geometric_primitives.py
Author: Monica Perez Serrano

Description: 3D Primitive Shapes supported by FreeCAD.

"""

from sys import path as syspath
from typing import Type, TypeVar, Optional, List

syspath.append("/usr/lib/freecad-python3/lib")

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import FreeCAD as App
import Part


# Enum to define supported shapes
class SupportedShapes(Enum):
    PLANE = 1
    CUBE = 2
    BOX = 2
    CYLINDER = 3
    CONE = 4
    SPHERE = 5
    TORUS = 7
    HELIX = 10
    CIRCLE = 12
    # TODO(@monicapserrano) Add support for shapes:
    #    ELLIPSOID = 6
    #    PRISM = 8
    #    WEDGE = 9
    #    SPIRAL = 11
    #    ELLIPSE = 13
    #    POLYGON = 16

    def __str__(self) -> str:
        return str(self.name.lower())


@dataclass
class Parameters:
    """
    Dataclass to store parameters for shapes.

    Attributes:
        shape (SupportedShapes): The shape type.
        length (float): Length of the shape.
        width (float): Width of the shape.
        height (float): Height of the shape.
        radius (float): Radius of the shape.
        radius1 (float): First radius for shapes like cones.
        radius2 (float): Second radius for shapes like cones.
        pitch (float): Pitch for helix shapes.
        angle (float): Angle for shapes requiring an angle parameter.
    """

    shape: SupportedShapes
    length: float = 0
    width: float = 0
    height: float = 0
    radius: float = 0
    radius1: float = 0
    radius2: float = 0
    pitch: float = 0
    angle: float = 0

    def to_list(self) -> List[float]:
        """
        Convert parameters to a list.

        Returns:
            List[float]: List of shape parameters.
        """
        return [
            self.shape.value,
            self.length,
            self.width,
            self.height,
            self.radius,
            self.radius1,
            self.radius2,
            self.pitch,
            self.angle,
        ]


class Shape(ABC):
    """
    Abstract base class for CAD shapes.
    """

    @abstractmethod
    def add_to_doc(self):
        pass


class Translation:
    """
    Class to handle translation of shapes in FreeCAD.

    Attributes:
        x (float): Translation in the x-axis.
        y (float): Translation in the y-axis.
        z (float): Translation in the z-axis.
    """

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def to_app_vector(self) -> App.Vector:
        """
        Convert translation to FreeCAD vector.

        Returns:
            App.Vector: FreeCAD vector representation of the translation.
        """
        return App.Vector(self.x, self.y, self.z)


class RotationEuler:
    """
    Class to handle Euler rotation of shapes in FreeCAD.

    Attributes:
        x_rad (float): Rotation around the x-axis in radians.
        y_rad (float): Rotation around the y-axis in radians.
        z_rad (float): Rotation around the z-axis in radians.
    """

    def __init__(self, x_rad: float, y_rad: float, z_rad: float):
        self.x_rad = x_rad
        self.y_rad = y_rad
        self.z_rad = z_rad

    def to_app_rotation(self) -> App.Rotation:
        """
        Convert Euler rotation to FreeCAD rotation.

        Returns:
            App.Rotation: FreeCAD rotation representation.
        """
        return App.Rotation(self.x_rad, self.y_rad, self.z_rad)


def __add_to_doc(
    obj: Part.Feature,
    shape: Part.Shape,
    translation: Optional[Translation],
    rotation: Optional[RotationEuler],
):
    """
    Add shape to FreeCAD document with optional translation and rotation.

    Args:
        obj (Part.Feature): FreeCAD feature object.
        shape (Part.Shape): Shape to be added.
        translation (Optional[Translation]): Translation to be applied.
        rotation (Optional[RotationEuler]): Rotation to be applied.
    """
    obj.Shape = shape
    obj.Placement = App.Placement(
        translation.to_app_vector() if translation is not None else App.Vector(0, 0, 0),
        rotation.to_app_rotation() if rotation is not None else App.Rotation(0, 0, 0),
    )


T_Plane = TypeVar("T_Plane", bound="Plane")


class Plane(Shape):
    """
    Class to create and handle a Plane shape in FreeCAD.

    Attributes:
        name (str): Name of the plane.
        length (float): Length of the plane.
        width (float): Width of the plane.
    """

    def __init__(self, name: str, length: float, width: float) -> Part.Shape:
        self.name = name
        self.plane = Part.makePlane(length, width)

    @classmethod
    def from_parameters(
        cls: Type[T_Plane], name: str, parameters: Parameters
    ) -> Type[T_Plane]:
        """
        Create a Plane instance from Parameters.

        Args:
            name (str): Name of the plane.
            parameters (Parameters): Parameters to define the plane.

        Returns:
            Plane: An instance of the Plane class.
        """
        return cls(
            name=name,
            length=parameters.length,
            width=parameters.width,
        )

    def add_to_doc(
        self,
        doc: App.Document,
        translation: Optional[Translation],
        rotation: Optional[RotationEuler],
    ):
        """
        Add the plane to a FreeCAD document.

        Args:
            doc (App.Document): FreeCAD document.
            translation (Optional[Translation]): Translation to be applied.
            rotation (Optional[RotationEuler]): Rotation to be applied.
        """
        obj = doc.addObject("Part::Plane", f"Plane_{self.name}")
        __add_to_doc(
            obj=obj, shape=self.plane, translation=translation, rotation=rotation
        )
        doc.recompute()


T_Box = TypeVar("T_Box", bound="Box")


class Box(Shape):
    """
    Class to create and handle a Box shape in FreeCAD.

    Attributes:
        name (str): Name of the box.
        length (float): Length of the box.
        width (float): Width of the box.
        height (float): Height of the box.
    """

    def __init__(
        self, name: str, length: float, width: float, height: float
    ) -> Part.Shape:
        self.name = name
        self.box = Part.makeBox(length, width, height)

    @classmethod
    def from_parameters(
        cls: Type[T_Box], name: str, parameters: Parameters
    ) -> Type[T_Box]:
        """
        Create a Box instance from Parameters.

        Args:
            name (str): Name of the box.
            parameters (Parameters): Parameters to define the box.

        Returns:
            Box: An instance of the Box class.
        """
        return cls(
            name=name,
            length=parameters.length,
            width=parameters.width,
            height=parameters.height,
        )

    def add_to_doc(
        self,
        doc: App.Document,
        translation: Optional[Translation],
        rotation: Optional[RotationEuler],
    ):
        """
        Add the box to a FreeCAD document.

        Args:
            doc (App.Document): FreeCAD document.
            translation (Optional[Translation]): Translation to be applied.
            rotation (Optional[RotationEuler]): Rotation to be applied.
        """
        obj = doc.addObject("Part::Box", f"Box_{self.name}")
        __add_to_doc(
            obj=obj, shape=self.box, translation=translation, rotation=rotation
        )
        doc.recompute()


T_Cylinder = TypeVar("T_Cylinder", bound="Cylinder")


class Cylinder(Shape):
    """
    Class to create and handle a Cylinder shape in FreeCAD.

    Attributes:
        name (str): Name of the cylinder.
        radius (float): Radius of the cylinder.
        height (float): Height of the cylinder.
    """

    def __init__(self, name: str, radius: float, height: float) -> Part.Shape:
        self.name = name
        self.cylinder = Part.makeCylinder(radius, height)

    @classmethod
    def from_parameters(
        cls: Type[T_Cylinder], name: str, parameters: Parameters
    ) -> Type[T_Cylinder]:
        """
        Create a Cylinder instance from Parameters.

        Args:
            name (str): Name of the cylinder.
            parameters (Parameters): Parameters to define the cylinder.

        Returns:
            Cylinder: An instance of the Cylinder class.
        """
        return cls(
            name=name,
            radius=parameters.radius,
            height=parameters.height,
        )

    def add_to_doc(
        self,
        doc: App.Document,
        translation: Optional[Translation],
        rotation: Optional[RotationEuler],
    ):
        """
        Add the cylinder to a FreeCAD document.

        Args:
            doc (App.Document): FreeCAD document.
            translation (Optional[Translation]): Translation to be applied.
            rotation (Optional[RotationEuler]): Rotation to be applied.
        """
        obj = doc.addObject("Part::Cylinder", f"Cylinder_{self.name}")
        __add_to_doc(
            obj=obj, shape=self.cylinder, translation=translation, rotation=rotation
        )
        doc.recompute()


T_Cone = TypeVar("T_Cone", bound="Cone")


class Cone(Shape):
    """
    Class to create and handle a Cone shape in FreeCAD.

    Attributes:
        name (str): Name of the cone.
        radius1 (float): Radius of the cone at the base.
        radius2 (float): Radius of the cone at the top.
        height (float): Height of the cone.
    """

    def __init__(
        self,
        name: str,
        radius1: float,
        radius2: float,
        height=float,
    ) -> Part:
        self.name = name
        self.cone = Part.makeCone(radius1, radius2, height)

    @classmethod
    def from_parameters(
        cls: Type[T_Cone], name: str, parameters: Parameters
    ) -> Type[T_Cone]:
        """
        Create a Cone instance from Parameters.

        Args:
            name (str): Name of the cone.
            parameters (Parameters): Parameters to define the cone.

        Returns:
            Cone: An instance of the cone class.
        """
        return cls(
            name=name,
            radius1=parameters.radius1,
            radius2=parameters.radius2,
        )

    def add_to_doc(
        self,
        doc: App,
        translation: Optional[Translation],
        rotation: Optional[RotationEuler],
    ):
        """
        Add the cone to a FreeCAD document.

        Args:
            doc (App.Document): FreeCAD document.
            translation (Optional[Translation]): Translation to be applied.
            rotation (Optional[RotationEuler]): Rotation to be applied.
        """
        obj = doc.addObject("Part::Cone", f"Cone_{self.name}")
        __add_to_doc(
            obj=obj, shape=self.cone, translation=translation, rotation=rotation
        )
        doc.recompute()


T_Sphere = TypeVar("T_Sphere", bound="Sphere")


class Sphere(Shape):
    """
    Class to create and handle a Sphere shape in FreeCAD.

    Attributes:
        name (str): Name of the sphere.
        radius (float): Radius of the sphere.
    """

    def __init__(self, name: str, radius: float) -> Part.Shape:
        self.name = name
        self.sphere = Part.makeSphere(radius)

    @classmethod
    def from_parameters(
        cls: Type[T_Sphere], name: str, parameters: Parameters
    ) -> Type[T_Sphere]:
        """
        Create a Sphere instance from Parameters.

        Args:
            name (str): Name of the sphere.
            parameters (Parameters): Parameters to define the sphere.

        Returns:
            Sphere: An instance of the Sphere class.
        """
        return cls(
            name=name,
            radius=parameters.radius,
        )

    def add_to_doc(
        self,
        doc: App.Document,
        translation: Optional[Translation],
        rotation: Optional[RotationEuler],
    ):
        """
        Add the sphere to a FreeCAD document.

        Args:
            doc (App.Document): FreeCAD document.
            translation (Optional[Translation]): Translation to be applied.
            rotation (Optional[RotationEuler]): Rotation to be applied.
        """
        obj = doc.addObject("Part::Sphere", f"Sphere_{self.name}")
        __add_to_doc(
            obj=obj, shape=self.sphere, translation=translation, rotation=rotation
        )
        doc.recompute()


T_Torus = TypeVar("T_Torus", bound="Torus")


class Torus(Shape):
    """
    Class to create and handle a Torus shape in FreeCAD.

    Attributes:
        name (str): Name of the torus.
        radius1 (float): Major radius of the torus.
        radius2 (float): Minor radius of the torus.
    """

    def __init__(self, name: str, radius1: float, radius2: float) -> Part.Shape:
        self.name = name
        self.torus = Part.makeTorus(radius1, radius2)

    @classmethod
    def from_parameters(
        cls: Type[T_Torus], name: str, parameters: Parameters
    ) -> Type[T_Torus]:
        """
        Create a Torus instance from Parameters.

        Args:
            name (str): Name of the torus.
            parameters (Parameters): Parameters to define the torus.

        Returns:
            Torus: An instance of the Torus class.
        """
        return cls(
            name=name,
            radius1=parameters.radius1,
            radius2=parameters.radius2,
        )

    def add_to_doc(
        self,
        doc: App.Document,
        translation: Optional[Translation],
        rotation: Optional[RotationEuler],
    ):
        """
        Add the torus to a FreeCAD document.

        Args:
            doc (App.Document): FreeCAD document.
            translation (Optional[Translation]): Translation to be applied.
            rotation (Optional[RotationEuler]): Rotation to be applied.
        """
        obj = doc.addObject("Part::Torus", f"Torus_{self.name}")
        __add_to_doc(
            obj=obj, shape=self.torus, translation=translation, rotation=rotation
        )
        doc.recompute()


T_Helix = TypeVar("T_Helix", bound="Helix")


class Helix(Shape):
    """
    Class to create and handle a Helix shape in FreeCAD.

    Attributes:
        name (str): Name of the helix.
        pitch (float): Pitch of the helix.
        height (float): Height of the helix.
        radius (float): Radius of the helix.
        angle (float): Angle of the helix.
    """

    def __init__(
        self, name: str, pitch: float, height: float, radius: float, angle: float
    ) -> Part.Shape:
        self.name = name
        self.helix = Part.makeHelix(pitch, height, radius, angle)

    @classmethod
    def from_parameters(
        cls: Type[T_Helix], name: str, parameters: Parameters
    ) -> Type[T_Helix]:
        """
        Create a Helix instance from Parameters.

        Args:
            name (str): Name of the helix.
            parameters (Parameters): Parameters to define the helix.

        Returns:
            Helix: An instance of the Helix class.
        """
        return cls(
            name=name,
            pitch=parameters.pitch,
            height=parameters.height,
            radius=parameters.radius,
            angle=parameters.angle,
        )

    def add_to_doc(
        self,
        doc: App.Document,
        translation: Optional[Translation],
        rotation: Optional[RotationEuler],
    ):
        """
        Add the helix to a FreeCAD document.

        Args:
            doc (App.Document): FreeCAD document.
            translation (Optional[Translation]): Translation to be applied.
            rotation (Optional[RotationEuler]): Rotation to be applied.
        """
        obj = doc.addObject("Part::Helix", f"Helix_{self.name}")
        __add_to_doc(
            obj=obj, shape=self.helix, translation=translation, rotation=rotation
        )
        doc.recompute()


T_Circle = TypeVar("T_Circle", bound="Circle")


class Circle(Shape):
    """
    Class to create and handle a Circle shape in FreeCAD.

    Attributes:
        name (str): Name of the circle.
        radius (float): Radius of the circle.
    """

    def __init__(self, name: str, radius: float) -> Part.Shape:
        self.name = name
        self.circle = Part.makeCircle(radius)

    @classmethod
    def from_parameters(
        cls: Type[T_Circle], name: str, parameters: Parameters
    ) -> Type[T_Circle]:
        """
        Create a Circle instance from Parameters.

        Args:
            name (str): Name of the circle.
            parameters (Parameters): Parameters to define the circle.

        Returns:
            Circle: An instance of the Circle class.
        """
        return cls(
            name=name,
            radius=parameters.radius,
        )

    def add_to_doc(
        self,
        doc: App.Document,
        translation: Optional[Translation],
        rotation: Optional[RotationEuler],
    ):
        """
        Add the circle to a FreeCAD document.

        Args:
            doc (App.Document): FreeCAD document.
            translation (Optional[Translation]): Translation to be applied.
            rotation (Optional[RotationEuler]): Rotation to be applied.
        """
        obj = doc.addObject("Part::Circle", f"Circle_{self.name}")
        __add_to_doc(
            obj=obj, shape=self.circle, translation=translation, rotation=rotation
        )
        doc.recompute()
