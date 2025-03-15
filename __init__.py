"""
    Blender 2.81+ addon for importing and exporting Nintendo Switch Pokémon Animation files.
"""
import os
import sys
import ensurepip
import sysconfig
import subprocess
from importlib import import_module
import bpy
from bpy.props import *
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper, ExportHelper

# pylint: disable=import-outside-toplevel, wrong-import-position, import-error

bl_info = {
    "name": "Nintendo Switch Pokémon Animation (GFBANM/TRANM) format",
    "author": "Shararamosh, Mvit & ElChicoEevee",
    "blender": (2, 81, 0),
    "version": (1, 0, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Nintendo Switch Pokémon Animation data",
    "category": "Import-Export",
    "doc_url": "https://github.com/Shararamosh/io_scene_gfbanm"
}


class ImportGfbanm(bpy.types.Operator, ImportHelper):
    """
    Class for operator that imports Pokémon Animation files.
    """
    bl_idname = "import_scene.gfbanm"
    bl_label = "Import GFBANM/TRANM"
    bl_description = "Import one or multiple Nintendo Switch Pokémon Animation files"
    directory: StringProperty()
    filter_glob: StringProperty(default="*.gfbanm;*.tranm", options={"HIDDEN"})
    files: CollectionProperty(type=bpy.types.PropertyGroup)
    ignore_origin_location: BoolProperty(
        name="Ignore Origin Location",
        description="Whether to ignore location transforms for bone named Origin",
        default=False
    )
    use_scene_start: BoolProperty(
        name="Start at Scene range",
        description="Use Scene playback range start frame as first frame of animation",
        default=False
    )
    anim_offset: FloatProperty(
        name="Animation Offset",
        description="Offset to apply to animation during import, in frames",
        default=1.0
    )

    def execute(self, context: bpy.types.Context) -> set[str]:
        """
        Executing import menu.
        :param context: Blender's context.
        :return: Result.
        """
        if not attempt_install_flatbuffers(self):
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
                    import_animation(context, file_path, self.ignore_origin_location,
                                     context.scene.frame_start if self.use_scene_start
                                     else self.anim_offset)
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
            import_animation(context, self.filepath, self.ignore_origin_location,
                             context.scene.frame_start if self.use_scene_start
                             else self.anim_offset)
        except OSError as e:
            self.report({"ERROR"}, f"Failed to import {self.filepath}. {str(e)}")
            return {"CANCELLED"}
        return {"FINISHED"}

    def draw(self, _context: bpy.types.Context):
        """
        Drawing importer's menu.
        :param _context: Blender's context.
        """
        self.layout.prop(self, "ignore_origin_location")
        self.layout.prop(self, "use_scene_start")
        sub = self.layout.column()
        sub.enabled = not self.use_scene_start
        sub.prop(self, "anim_offset")


def on_export_format_changed(struct: bpy.types.bpy_struct, context: bpy.types.Context):
    """
    Called when export format was updated.
    :param struct: Struct that was changed.
    :param context: Blender's Context.
    """
    if isinstance(struct.id_data, bpy.types.Collection):
        struct.filepath = ExportGfbanm.ensure_filepath_matches_export_format(
            struct.filepath,
            struct.export_format
        )
    if not isinstance(context.space_data, bpy.types.SpaceFileBrowser):
        return
    if not context.space_data.active_operator:
        return
    if context.space_data.active_operator.bl_idname != "EXPORT_SCENE_OT_gfbanm":
        return
    context.space_data.params.filename = ExportGfbanm.ensure_filepath_matches_export_format(
        context.space_data.params.filename,
        struct.export_format,
    )
    if struct.export_format == "TRANM":
        context.space_data.params.filter_glob = "*.tranm"
    else:
        context.space_data.params.filter_glob = "*.gfbanm"
    bpy.ops.file.refresh()


class ExportGfbanm(bpy.types.Operator, ExportHelper):
    """
    Class for operator that exports GFBANM/TRANM files.
    """
    bl_idname = "export_scene.gfbanm"
    bl_label = "Export GFBANM/TRANM"
    bl_description = "Export current action as Nintendo Switch Pokémon Animation file"
    bl_options = {"PRESET", "UNDO"}
    filename_ext = ""
    filter_glob: StringProperty(default="*.gfbanm", options={"HIDDEN"})
    filepath: StringProperty(subtype="FILE_PATH")

    export_format: EnumProperty(
        name="Format",
        items=(("GFBANM", "GFBANM (.gfbanm)",
                "Exports action in format used by Pokémon Sword/Shield."),
               ("TRANM", "TRANM (.tranm)",
                "Exports action in format used by Pokémon Legends: Arceus and "
                "Pokémon Scarlet/Violet.")),
        description="Output format for action",
        default=0,
        update=on_export_format_changed
    )

    does_loop: BoolProperty(
        name="Looping",
        description="Export as looping animation",
        default=False
    )

    use_action_range: BoolProperty(
        name="Use action's frame range",
        description="If available, use action's frame range instead of scene's",
        default=False
    )

    @staticmethod
    def ensure_filepath_matches_export_format(filepath: str, export_format: str) -> str:
        """
        Ensures file path matches export format.
        :param filepath: File path string.
        :param export_format: Export format string.
        :return: Modified file path string.
        """
        filename = os.path.basename(filepath)
        if not filename:
            return filepath
        stem, ext = os.path.splitext(filename)
        if stem.startswith(".") and not ext:
            stem, ext = "", stem
        desired_ext = ".tranm" if export_format == "TRANM" else ".gfbanm"
        ext_lower = ext.lower()
        if ext_lower not in [".gfbanm", ".tranm"]:
            return filepath + desired_ext
        if ext_lower != desired_ext:
            filepath = filepath[:-len(ext)]
            return filepath + desired_ext
        return filepath

    def check(self, _context: bpy.types.Context) -> bool:
        """
        Checks if operator needs to be updated.
        :param _context: Blender's Context.
        :return: True if update is needed, False otherwise.
        """
        old_filepath = self.filepath
        self.filepath = ExportGfbanm.ensure_filepath_matches_export_format(self.filepath,
                                                                           self.export_format)
        return self.filepath != old_filepath

    def invoke(self, context: bpy.types.Context, _event: bpy.types.Event) -> set[str]:
        """
        Called when operator is invoked by user.
        :param context: Blender's Context.
        :param _event: Event invoked.
        :return: Result.
        """
        directory = os.path.dirname(self.filepath)
        filename = os.path.splitext(os.path.basename(context.blend_data.filepath))[0]
        obj = context.object
        if obj and obj.animation_data and obj.animation_data.action:
            filename = obj.animation_data.action.name
        self.filepath = ExportGfbanm.ensure_filepath_matches_export_format(
            os.path.join(directory, filename), self.export_format)
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def draw(self, _context: bpy.types.Context):
        """
        Drawing exporter's menu.
        :param _context: Blender's context.
        """
        self.layout.prop(self, "export_format")
        self.layout.prop(self, "does_loop")
        self.layout.prop(self, "use_action_range")

    def execute(self, context: bpy.types.Context) -> set[str]:
        """
        Executing export menu.
        :param context: Blender's context.
        :return: Result.
        """
        if not attempt_install_flatbuffers(self):
            return {"CANCELLED"}
        if context.active_object is None or context.active_object.type != "ARMATURE":
            self.report({"ERROR"}, "No Armature is selected for action export.")
            return {"CANCELLED"}
        directory = os.path.dirname(self.filepath)
        from .gfbanm_exporter import export_animation
        data = export_animation(context, self.does_loop, self.use_action_range)
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
    operator.layout.operator(ImportGfbanm.bl_idname, text="Pokémon Animation (.gfbanm/.tranm)")


def menu_func_export(operator: bpy.types.Operator, _context: bpy.types.Context):
    """
    Function that adds GFBANM/TRANM export operators.
    :param operator: Blender's operator.
    :param _context: Blender's Context.
    :return:
    """
    operator.layout.operator(ExportGfbanm.bl_idname,
                             text="Pokémon Animation (.gfbanm/.tranm)")


def register():
    """
    Registering addon.
    """
    register_class(ImportGfbanm)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    register_class(ExportGfbanm)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    """
    Unregistering addon.
    :return:
    """
    unregister_class(ImportGfbanm)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    unregister_class(ExportGfbanm)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


def attempt_install_flatbuffers(operator: bpy.types.Operator = None) -> bool:
    """
    Attempts installing flatbuffers library if it's not installed using pip.
    :return: True if flatbuffers was found or successfully installed, False otherwise.
    """
    if are_flatbuffers_installed():
        return True
    ensurepip.bootstrap()
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "flatbuffers"])
    if are_flatbuffers_installed():
        msg = "Successfully installed flatbuffers library."
        if operator is not None:
            operator.report({"INFO"}, msg)
        else:
            print(msg)
        return True
    platlib_path = sysconfig.get_path("platlib")
    msg = ("Failed to install flatbuffers library using pip. "
           f"To use this addon, put Python flatbuffers library folder "
           f"to this path: {platlib_path}.")
    if operator is not None:
        operator.report({"ERROR"}, msg)
    else:
        print(msg)
    return False


def are_flatbuffers_installed() -> bool:
    """
    Checks if flatbuffers library is installed.
    :return: True or False.
    """
    try:
        import_module("flatbuffers")
    except ModuleNotFoundError:
        return False
    return True


if __name__ == "__main__":
    register()
