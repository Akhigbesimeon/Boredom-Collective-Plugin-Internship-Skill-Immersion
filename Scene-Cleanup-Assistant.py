bl_info = {
    "name": "Scene Cleanup Assistant",
    "author": "Akhigbe Simeon",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Cleanup",
    "description": "Automatically remove unused and unnecessary data from your scene",
    "category": "Utility"
}

import bpy

class CLEANUP_OT_cleanup_scene(bpy.types.Operator):
    bl_idname = "cleanup.perform_cleanup"
    bl_label = "Clean Scene"
    bl_description = "Remove unused data blocks, hidden/empty objects, and more"

    def execute(self, context):
        removed_objects = 0
        removed_materials = 0

        for obj in list(bpy.data.objects):
            if obj.type == 'EMPTY' or (obj.type == 'MESH' and obj.data is None):
                bpy.data.objects.remove(obj)
                removed_objects += 1

        for obj in list(bpy.context.scene.objects):
            if obj.hide_get():
                bpy.data.objects.remove(obj)
                removed_objects += 1

        for mat in list(bpy.data.materials):
            if mat.users == 0:
                bpy.data.materials.remove(mat)
                removed_materials += 1

        for datablock in (
            bpy.data.meshes, bpy.data.materials, bpy.data.images,
            bpy.data.textures, bpy.data.curves, bpy.data.lights,
            bpy.data.cameras, bpy.data.actions, bpy.data.nodes
        ):
            for block in datablock:
                if block.users == 0:
                    datablock.remove(block)

        self.report({'INFO'}, f"Removed {removed_objects} objects and {removed_materials} materials")
        return {'FINISHED'}

class CLEANUP_PT_panel(bpy.types.Panel):
    bl_label = "Scene Cleanup Assistant"
    bl_idname = "CLEANUP_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cleanup'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Scene Cleanup")
        layout.operator("cleanup.perform_cleanup", icon='TRASH')

classes = (
    CLEANUP_OT_cleanup_scene,
    CLEANUP_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
