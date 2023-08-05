#! usr/bin/python3.6
"""
    Module initially auto generated using V5Automation files from CATIA V5 R28 on 2020-06-11 12:40:47.360445

    .. warning::
        The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
        They are there as a guide as to how the visual basic / catscript functions work
        and thus help debugging in pycatia.

"""

from pycatia.system_interfaces.any_object import AnyObject
from pycatia.system_interfaces.system_service import SystemService


class Analyze(AnyObject):
    """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)

                | System.IUnknown
                |     System.IDispatch
                |         System.CATBaseUnknown
                |             System.CATBaseDispatch
                |                 System.AnyObject
                |                     Analyze
                |
                | Represents the analysis object associated with a product.

    """

    def __init__(self, com_object):
        super().__init__(com_object)
        self.analyze = com_object

    @property
    def mass(self) -> float:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property Mass() As double (Read Only)
                |
                |     Returns the product mass value.
                |
                |     Example:
                |
                |           This example retrieves MassValue from
                |
                |          the Analyze object associated with myProduct:
                |
                |
                |          MassValue = myProduct.Analyze.Mass

        :return: float
        :rtype: float
        """

        return self.analyze.Mass

    @property
    def volume(self) -> float:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property Volume() As double (Read Only)
                |
                |     Returns the product volume value.
                |
                |     Example:
                |
                |           This example retrieves VolumeValue from
                |
                |          the Analyze object associated with myProduct:
                |
                |
                |          VolumeValue = myProduct.Analyze.Volume

        :return: float
        :rtype: float
        """

        return self.analyze.Volume

    @property
    def wet_area(self) -> float:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property WetArea() As double (Read Only)
                |
                |     Returns the product wet area (outer volume).
                |
                |
                |     Note:
                |     This method uses mm2 instead of default Catia V5 unit.
                |
                |     Example:
                |
                |           This example retrieves WetAreaValue from
                |
                |          the Analyze object associated with myProduct:
                |
                |
                |          WetAreaValue = myProduct.Analyze.WetArea

        :return: float
        :rtype: float
        """

        return self.analyze.WetArea

    def get_gravity_center(self):
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Sub GetGravityCenter(CATSafeArrayVariant
                | oGravityCenterCoordinatesArray)
                |
                |     Returns the gravity center coordinates of product.
                |
                |     Parameters:
                |
                |         Coordinates
                |             The array storing the three gravity center coordinates. This array
                |             must be previously initialized.
                |
                |     Example:
                |
                |           This example retrieves the gravity center coordinates
                |           in
                |          oGravityCenterCoordinatesArray from
                |          the Analyze object associated with myProduct:
                |
                |          ' Coordinates array initialization
                |          Dim oGravityCenterCoordinatesArray ( 2 )
                |          ' Get value in array
                |          Myproduct.Analyze.GetGravityCenter
                |          oGravityCenterCoordinatesArray

        :return: None
        """
        # return self.analyze.GetGravityCenter(o_gravity_center_coordinates_array)
        # # # # Autogenerated comment:
        # some methods require a system service call as the methods expects a vb array object
        # passed to it and there is no way to do this directly with python. In those cases the following code
        # should be uncommented and edited accordingly. Otherwise completely remove all this.
        vba_function_name = 'get_gravity_center'
        vba_code = """
        Public Function get_gravity_center(analyze)
            Dim oGravityCenterCoordinatesArray (2)
            analyze.GetGravityCenter oGravityCenterCoordinatesArray
            get_gravity_center = oGravityCenterCoordinatesArray
        End Function
        """

        system_service = self.application.system_service
        return system_service.evaluate(vba_code, 0, vba_function_name, [self.com_object])

    def get_inertia(self):
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Sub GetInertia(CATSafeArrayVariant oInertiaMatrixArray)
                |
                |     Returns the inertia matrix array of product.
                |
                |     Parameters:
                |
                |         oInertiaMatrixArray
                |             The array storing successively the three columns of inertia matrix.
                |             This array must be previously initialized.
                |
                |     Example:
                |
                |           This example retrieves the inertia matrix components
                |           in
                |          oInertiaMatrixArray from
                |          the Analyze object associated with myProduct:
                |
                |
                |          ' Components array initialization
                |          Dim oInertiaMatrixArray ( 8 )
                |          ' Get value in array
                |          Myproduct.Analyze.GetInertia oInertiaMatrixArray
                |          ' oInertiaMatrixArray ( 0 ) is the Ixx component
                |          ' oInertiaMatrixArray ( 1 ) is the Ixy component
                |          ' oInertiaMatrixArray ( 2 ) is the Ixz component
                |          ' oInertiaMatrixArray ( 3 ) is the Iyx component
                |          ' oInertiaMatrixArray ( 4 ) is the Iyy component
                |          ' oInertiaMatrixArray ( 5 ) is the Iyz component
                |          ' oInertiaMatrixArray ( 6 ) is the Izx component
                |          ' oInertiaMatrixArray ( 7 ) is the Izy component
                |          ' oInertiaMatrixArray ( 8 ) is the Izz component

        :return: tuple
        """
        # return self.analyze.GetInertia(o_inertia_matrix_array)
        # # # Autogenerated comment:
        # some methods require a system service call as the methods expects a vb array object
        # passed to it and there is no way to do this directly with python. In those cases the following code
        # should be uncommented and edited accordingly. Otherwise completely remove all this.
        vba_function_name = 'get_inertia'
        vba_code = """
        Public Function get_inertia(analyze)
            Dim oInertiaMatrixArray (8)
            analyze.GetInertia oInertiaMatrixArray
            get_inertia = oInertiaMatrixArray
        End Function
        """

        system_service = self.application.system_service
        return system_service.evaluate(vba_code, 0, vba_function_name, [self.com_object])

    def __repr__(self):
        return f'Analyze(name="{self.name}")'
