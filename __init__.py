"""
    Blender 2.80+ addon for importing and exporting GFBANM/TRANM animation files.
"""
import os
import sys
import subprocess
import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper, ExportHelper

# pylint: disable=import-outside-toplevel, wrong-import-position, import-error, unused-import

bl_info = {
    "name": "GFBANM/TRANM Import and Export",
    "author": "Shararamosh, Mvit & ElChicoEevee",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "location": "File > Import-Export",
    "description": "Import and Export GFBANM/TRANM data",
    "category": "Import-Export",
}


class ImportGfbanm(bpy.types.Operator, ImportHelper):
    """
    Class for operator that imports GFBANM/TRANM files.
    """
    bl_idname = "import.gfbanm"
    bl_label = "Import GFBANM/TRANM"
    bl_description = "Import one or multiple GFBANM/TRANM files"
    directory: StringProperty()
    filter_glob: StringProperty(default="*.gfbanm;*.tranm", options={"HIDDEN"})
    files: CollectionProperty(type=bpy.types.PropertyGroup)
    ignore_origin_location: BoolProperty(
        name="Ignore Origin Location",
        description="Ignore Origin Location",
        default=False
    )

    def execute(self, context: bpy.types.Context):
        """
        Executing import menu.
        :param context: Blender's context.
        """
        if not attempt_install_flatbuffers(self):
            self.report({"ERROR"}, "Failed to install flatbuffers library using pip. "
                                   "To use this addon, put Python flatbuffers library folder "
                                   f"to this path: {get_site_packages_path()}.")
            return {"CANCELLED"}
        if context.active_object is None or context.active_object.type != "ARMATURE":
            self.report({"ERROR"}, "No Armature is selected for action import.")
            return {"CANCELLED"}
        from .gfbanm_importer import import_animation
        if self.files:
            b = False
            for file in self.files:
                file_path = os.path.join(str(self.directory), file.name)
                try:
                    import_animation(context, file_path, self.ignore_origin_location)
                except OSError as e:
                    self.report({"INFO"}, f"Failed to import {file_path}. {str(e)}")
                else:
                    b = True
                finally:
                    pass
            if b:
                return {"FINISHED"}
            return {"CANCELLED"}
        try:
            import_animation(context, self.filepath, self.ignore_origin_location)
        except OSError as e:
            self.report({"ERROR"}, f"Failed to import {self.filepath}. {str(e)}")
            return {"CANCELLED"}
        return {"FINISHED"}

    def draw(self, _context: bpy.types.Context):
        """
        Drawing importer's menu.
        :param _context: Blender's context.
        """
        box = self.layout.box()
        box.prop(self, "ignore_origin_location", text="Ignore Origin Location")


class ExportGfbanm(bpy.types.Operator, ExportHelper):
    """
    Class for operator that exports GFBANM files.
    """
    bl_idname = "export.gfbanm"
    bl_label = "Export GFBANM (WIP)"
    bl_description = "Export current action as GFBANM file"
    bl_options = {"PRESET", "UNDO"}
    filename_ext = ".gfbanm"
    does_loop: BoolProperty(
        name="Looping action",
        description="Export as looping action",
        default=False,
    )

    def draw(self, _context: bpy.types.Context):
        """
        Drawing exporter's menu.
        :param _context: Blender's context.
        """
        layout = self.layout
        box = layout.box()
        box.prop(self, "does_loop")

    def execute(self, context: bpy.types.Context):
        """
        Executing export menu.
        :param context: Blender's context.
        """
        if not attempt_install_flatbuffers(self):
            self.report({"ERROR"}, "Failed to install flatbuffers library using pip. "
                                   "To use this addon, put Python flatbuffers library folder "
                                   f"to this path: {get_site_packages_path()}.")
            return {"CANCELLED"}
        if context.active_object is None or context.active_object.type != "ARMATURE":
            self.report({"ERROR"}, "No Armature is selected for action export.")
            return {"CANCELLED"}
        directory = os.path.dirname(self.filepath)
        from .gfbanm_exporter import export_animation
        data = export_animation(context, self.does_loop)
        file_path = os.path.join(directory, self.filepath)
        with open(file_path, "wb") as file:
            file.write(data)
            print(f"Armature action successfully exported to {file_path}.")
        return {"FINISHED"}


class ExportTranm(bpy.types.Operator, ExportHelper):
    """
    Class for operator that exports TRANM files.
    """
    bl_idname = "export.tranm"
    bl_label = "Export TRANM (WIP)"
    bl_description = "Export current action as TRANM file"
    filename_ext = ".tranm"
    does_loop: BoolProperty(
        name="Looping action",
        description="Export as looping action",
        default=False,
    )

    def draw(self, _context: bpy.types.Context):
        """
        Drawing exporter's menu.
        :param _context: Blender's context.
        """
        layout = self.layout
        box = layout.box()
        box.prop(self, "does_loop")

    def execute(self, context: bpy.types.Context):
        """
        Executing export menu.
        :param context: Blender's context.
        """
        if not attempt_install_flatbuffers(self):
            self.report({"ERROR"}, "Failed to install flatbuffers library using pip. "
                                   "To use this addon, put Python flatbuffers library folder "
                                   f"to this path: {get_site_packages_path()}.")
            return {"CANCELLED"}
        if context.active_object is None or context.active_object.type != "ARMATURE":
            self.report({"ERROR"}, "No Armature is selected for action export.")
            return {"CANCELLED"}
        directory = os.path.dirname(self.filepath)
        from .gfbanm_exporter import export_animation
        data = export_animation(context, self.does_loop)
        file_path = os.path.join(directory, self.filepath)
        with open(file_path, "wb") as file:
            file.write(data)
            print(f"Armature action successfully exported to {file_path}.")
        return {"FINISHED"}


def menu_func_import(operator: bpy.types.Operator, _context: bpy.types.Context):
    """
    Function that adds GFBANM/TRANM import operator.
    :param operator: Blender's operator.
    :param _context: Blender's Context.
    :return:
    """
    operator.layout.operator(ImportGfbanm.bl_idname, text="Pokémon Switch Action (.gfbanm, .tranm)")


def menu_func_export(operator: bpy.types.Operator, _context: bpy.types.Context):
    """
    Function that adds GFBANM and TRANM export operators.
    :param operator: Blender's operator.
    :param _context: Blender's Context.
    :return:
    """
    operator.layout.operator(ExportGfbanm.bl_idname, text="Pokémon Sword/Shield Action (.gfbanm)")
    operator.layout.operator(ExportTranm.bl_idname, text="Pokémon Trinity Action (.tranm)")


def register():
    """
    Registering addon.
    """
    register_class(ImportGfbanm)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    register_class(ExportGfbanm)
    register_class(ExportTranm)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    """
    Unregistering addon.
    :return:
    """
    unregister_class(ImportGfbanm)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    unregister_class(ExportGfbanm)
    unregister_class(ExportTranm)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


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
