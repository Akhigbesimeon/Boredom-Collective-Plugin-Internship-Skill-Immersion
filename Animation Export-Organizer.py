bl_info = {
    "name": "Animation Export Organizer",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Export Organizer",
    "description": "Organize and batch export animations with custom settings",
    "category": "Import-Export"
}

import bpy
import os

# Property for each export entry
class ExportEntry(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Shot Name")
    start_frame: bpy.props.IntProperty(name="Start Frame")
    end_frame: bpy.props.IntProperty(name="End Frame")
    filepath: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')
    format: bpy.props.EnumProperty(
        name="Format",
        items=[
            ('FBX', 'FBX', ''),
            ('GLB', 'glTF Binary (.glb)', ''),
            ('ABC', 'Alembic (.abc)', ''),
        ],
        default='FBX'
    )

# UI Panel
class EXPORTORGANIZER_PT_panel(bpy.types.Panel):
    bl_label = "Animation Export Organizer"
    bl_idname = "EXPORTORGANIZER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Export Organizer'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        eo = scene.export_organizer

        layout.operator("export_organizer.add_entry", icon='PLUS')
        layout.separator()

        for i, entry in enumerate(eo.entries):
            box = layout.box()
            box.prop(entry, "name")
            box.prop(entry, "start_frame")
            box.prop(entry, "end_frame")
            box.prop(entry, "filepath")
            box.prop(entry, "format")
            row = box.row()
            row.operator("export_organizer.export_entry", text="Export").index = i
            row.operator("export_organizer.remove_entry", text="", icon='X').index = i

        layout.operator("export_organizer.export_all", icon='EXPORT')

# Operator: Add Entry
class EXPORTORGANIZER_OT_add_entry(bpy.types.Operator):
    bl_idname = "export_organizer.add_entry"
    bl_label = "Add Export Entry"

    def execute(self, context):
        context.scene.export_organizer.entries.add()
        return {'FINISHED'}

# Operator: Remove Entry
class EXPORTORGANIZER_OT_remove_entry(bpy.types.Operator):
    bl_idname = "export_organizer.remove_entry"
    bl_label = "Remove Entry"

    index: bpy.props.IntProperty()

    def execute(self, context):
        context.scene.export_organizer.entries.remove(self.index)
        return {'FINISHED'}

# Operator: Export Single Entry
class EXPORTORGANIZER_OT_export_entry(bpy.types.Operator):
    bl_idname = "export_organizer.export_entry"
    bl_label = "Export Entry"

    index: bpy.props.IntProperty()

    def execute(self, context):
        entry = context.scene.export_organizer.entries[self.index]
        return export_animation(entry)

# Operator: Export All
class EXPORTORGANIZER_OT_export_all(bpy.types.Operator):
    bl_idname = "export_organizer.export_all"
    bl_label = "Export All Animations"

    def execute(self, context):
        for entry in context.scene.export_organizer.entries:
            result = export_animation(entry)
            if result != {'FINISHED'}:
                return result
        self.report({'INFO'}, "All animations exported")
        return {'FINISHED'}

# Core export function
def export_animation(entry):
    bpy.context.scene.frame_start = entry.start_frame
    bpy.context.scene.frame_end = entry.end_frame
    filepath = bpy.path.abspath(entry.filepath)

    if not filepath:
        return {'CANCELLED'}

    if entry.format == 'FBX':
        bpy.ops.export_scene.fbx(filepath=filepath, use_selection=False, bake_anim=True)
    elif entry.format == 'GLB':
        bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    elif entry.format == 'ABC':
        bpy.ops.wm.alembic_export(filepath=filepath)

    return {'FINISHED'}

# Property Group for entries
class ExportOrganizerSettings(bpy.types.PropertyGroup):
    entries: bpy.props.CollectionProperty(type=ExportEntry)

# Registration
classes = (
    ExportEntry,
    ExportOrganizerSettings,
    EXPORTORGANIZER_PT_panel,
    EXPORTORGANIZER_OT_add_entry,
    EXPORTORGANIZER_OT_remove_entry,
    EXPORTORGANIZER_OT_export_entry,
    EXPORTORGANIZER_OT_export_all,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.export_organizer = bpy.props.PointerProperty(type=ExportOrganizerSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.export_organizer

if __name__ == "__main__":
    register()
