bl_info = {
    "name": "Object Namer",
    "author": "Akhigbe Simeon",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Object Namer",
    "description": "Renames selected objects using a base name and numbering",
    "category": "Object",
}

import bpy

class OBJECTNAMER_Props(bpy.types.PropertyGroup):
    base_name: bpy.props.StringProperty(name="Base Name", default="Object")
    start_number: bpy.props.IntProperty(name="Start Number", default=1)

class OBJECTNAMER_PT_panel(bpy.types.Panel):
    bl_label = "Object Namer"
    bl_idname = "OBJECTNAMER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Object Namer'

    def draw(self, context):
        layout = self.layout
        props = context.scene.object_namer_props

        layout.prop(props, "base_name")
        layout.prop(props, "start_number")
        layout.operator("objectnamer.rename", icon="OUTLINER_OB_OBJECT")

class OBJECTNAMER_OT_rename(bpy.types.Operator):
    bl_idname = "objectnamer.rename"
    bl_label = "Rename Selected Objects"
    bl_description = "Renames selected objects with base name and number"

    def execute(self, context):
        props = context.scene.object_namer_props
        selected = context.selected_objects

        number = props.start_number
        for obj in selected:
            obj.name = f"{props.base_name}_{number:03}"
            number += 1

        return {'FINISHED'}

classes = (
    OBJECTNAMER_Props,
    OBJECTNAMER_PT_panel,
    OBJECTNAMER_OT_rename,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.object_namer_props = bpy.props.PointerProperty(type=OBJECTNAMER_Props)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.object_namer_props

if __name__ == "__main__":
    register()
