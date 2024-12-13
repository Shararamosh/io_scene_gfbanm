"""
    Init for GFBANM Importer addon.
"""
import os
import sys
import subprocess
import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper

bl_info = {
    "name": "GFBANM/TRANM Import",
    "author": "Shararamosh, Mvit & ElChicoEevee",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "location": "File > Import-Export",
    "description": "Import GFBANM/TRANM data",
    "category": "Import-Export",
}


class ImportGfbanm(bpy.types.Operator, ImportHelper):
    """
    Class for operator that imports GFBANM files.
    """
    bl_idname = "import.gfbanm"
    bl_label = "Import GFBANM/TRANM"
    bl_description = "Import one or multiple GFBANM/TRANM files"
    directory: StringProperty()
    filter_glob: StringProperty(default="*.gfbanm;*.tranm", options={'HIDDEN'})
    files: CollectionProperty(type=bpy.types.PropertyGroup)
    zxy_location_mode: BoolProperty(
        name="Use ZXY",
        description="Use ZXY instead of XYZ for Location",
        default=False
    )
    invert_z_location: BoolProperty(
        name="Invert Z Location (Only if ZXY)",
        description="Invert the Z Location",
        default=False
    )

    def execute(self, context: bpy.types.Context):
        if not attempt_install_flatbuffers(self):
            self.report({"ERROR"}, "Failed to install flatbuffers library using pip. "
                                   "To use this addon, put Python flatbuffers library folder "
                                   "to this path: " + get_site_packages_path() + ".")
            return {"CANCELLED"}
        from .gfbanm_importer import import_animation
        if self.files:
            b = False
            for file in self.files:
                try:
                    import_animation(context, os.path.join(str(self.directory), file.name),
                                     self.zxy_location_mode, self.invert_z_location)
                except OSError as e:
                    self.report({"INFO"}, "Failed to import " + file + ".\n" + str(e))
                else:
                    b = True
                finally:
                    pass
            if b:
                return {"FINISHED"}
            return {"CANCELLED"}
        try:
            import_animation(context, self.filepath, self.zxy_location_mode, self.invert_z_location)
        except OSError as e:
            self.report({"ERROR"}, "Failed to import " + self.filepath + ".\n" + str(e))
            return {"CANCELLED"}
        return {"FINISHED"}

    @classmethod
    def poll(cls, _context: bpy.types.Context):
        """
        Checking if operator can be active.
        :param _context: Blender's Context.
        :return: True if active, False otherwise.
        """
        return True

    def draw(self, _context: bpy.types.Context):
        """
        Drawing importer's menu.
        :param _context: Blender's context.
        """
        box = self.layout.box()
        box.prop(self, "zxy_location_mode", text="ZXY Axis")
        box.prop(self, "invert_z_location", text="Invert Z Location (Only if ZXY)")

def menu_func_import(operator: bpy.types.Operator, _context: bpy.types.Context):
    """
    Function that adds GFBANM import operator.
    :param operator: Blender's operator.
    :param _context: Blender's Context.
    :return:
    """
    operator.layout.operator(ImportGfbanm.bl_idname, text="GFBANM/TRANM (.gfbanm, .tranm)")


def register():
    """
    Registering addon.
    """
    register_class(ImportGfbanm)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    """
    Unregistering addon.
    :return:
    """
    unregister_class(ImportGfbanm)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


def attempt_install_flatbuffers(operator: bpy.types.Operator = None) -> bool:
    """
    Attempts installing flatbuffers library if it's not installed using pip.
    :return: True if flatbuffers was found or successfully installed, False otherwise.
    """
    if are_flatbuffers_installed():
        return True
    target = get_site_packages_path()
    subprocess.call([sys.executable, "-m", 'ensurepip'])
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "flatbuffers", "-t", target])
    if are_flatbuffers_installed():
        if operator is not None:
            operator.report({"INFO"},
                            "Successfully installed flatbuffers library to " + target + ".")
        else:
            print("Successfully installed flatbuffers library to " + target + ".")
        return True
    return False


def are_flatbuffers_installed() -> bool:
    """
    Checks if flatbuffers library is installed.
    :return: True or False.
    """
    try:
        import flatbuffers
    except ModuleNotFoundError:
        return False
    return True


def get_site_packages_path():
    """
    Returns file path to lib/site-packages folder.
    :return: File path to lib/site-packages folder.
    """
    return os.path.join(sys.prefix, "lib", "site-packages")


if __name__ == "__main__":
    register()
