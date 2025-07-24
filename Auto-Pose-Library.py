bl_info = {
    "name": "Auto Pose Library",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Auto Pose Library",
    "description": "Save and apply poses for rigged characters",
    "category": "Animation"
}

import bpy
import json

class PoseEntry(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Pose Name")
    data: bpy.props.StringProperty(name="Pose Data")

class POSELIBRARY_PT_panel(bpy.types.Panel):
    bl_label = "Auto Pose Library"
    bl_idname = "POSELIBRARY_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Auto Pose Library'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        lib = scene.auto_pose_library

        layout.prop(lib, "pose_name")
        layout.operator("pose_library.save_pose", icon='PLUS')
        layout.separator()

        for i, pose in enumerate(lib.poses):
            box = layout.box()
            box.label(text=pose.name)
            row = box.row()
            row.operator("pose_library.apply_pose", text="Apply").index = i
            row.operator("pose_library.delete_pose", text="", icon='X').index = i

class POSELIBRARY_OT_save(bpy.types.Operator):
    bl_idname = "pose_library.save_pose"
    bl_label = "Save Current Pose"
    bl_description = "Save the current pose of the active armature"

    def execute(self, context):
        obj = context.object
        lib = context.scene.auto_pose_library
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "Select an armature to save pose")
            return {'CANCELLED'}

        pose_data = {}
        for bone in obj.pose.bones:
            pose_data[bone.name] = {
                "location": list(bone.location),
                "rotation_quaternion": list(bone.rotation_quaternion),
                "scale": list(bone.scale)
            }

        new_pose = lib.poses.add()
        new_pose.name = lib.pose_name
        new_pose.data = json.dumps(pose_data)
        lib.pose_name = ""
        return {'FINISHED'}

class POSELIBRARY_OT_apply(bpy.types.Operator):
    bl_idname = "pose_library.apply_pose"
    bl_label = "Apply Pose"
    bl_description = "Apply saved pose to the active armature"

    index: bpy.props.IntProperty()

    def execute(self, context):
        obj = context.object
        lib = context.scene.auto_pose_library
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "Select an armature to apply pose")
            return {'CANCELLED'}

        pose_data = json.loads(lib.poses[self.index].data)

        for bone_name, transform in pose_data.items():
            if bone_name in obj.pose.bones:
                bone = obj.pose.bones[bone_name]
                bone.location = transform["location"]
                bone.rotation_quaternion = transform["rotation_quaternion"]
                bone.scale = transform["scale"]

        return {'FINISHED'}

class POSELIBRARY_OT_delete(bpy.types.Operator):
    bl_idname = "pose_library.delete_pose"
    bl_label = "Delete Pose"
    bl_description = "Delete selected pose"

    index: bpy.props.IntProperty()

    def execute(self, context):
        context.scene.auto_pose_library.poses.remove(self.index)
        return {'FINISHED'}

class AutoPoseLibrarySettings(bpy.types.PropertyGroup):
    poses: bpy.props.CollectionProperty(type=PoseEntry)
    pose_name: bpy.props.StringProperty(name="Pose Name")

classes = (
    PoseEntry,
    AutoPoseLibrarySettings,
    POSELIBRARY_PT_panel,
    POSELIBRARY_OT_save,
    POSELIBRARY_OT_apply,
    POSELIBRARY_OT_delete,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.auto_pose_library = bpy.props.PointerProperty(type=AutoPoseLibrarySettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.auto_pose_library

if __name__ == "__main__":
    register()
