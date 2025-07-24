bl_info = {
    "name": "Shot Manager",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Shot Manager",
    "description": "Manage multiple shots within a Blender scene",
    "category": "Animation"
}

import bpy
class ShotEntry(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Shot Name")
    start_frame: bpy.props.IntProperty(name="Start Frame")
    end_frame: bpy.props.IntProperty(name="End Frame")
    camera: bpy.props.PointerProperty(name="Camera", type=bpy.types.Object)

class SHOTMANAGER_PT_panel(bpy.types.Panel):
    bl_label = "Shot Manager"
    bl_idname = "SHOTMANAGER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shot Manager'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        sm = scene.shot_manager

        layout.operator("shot_manager.add_shot", icon='PLUS')
        layout.separator()

        for i, shot in enumerate(sm.shots):
            box = layout.box()
            box.prop(shot, "name")
            box.prop(shot, "start_frame")
            box.prop(shot, "end_frame")
            box.prop(shot, "camera")
            row = box.row()
            row.operator("shot_manager.jump_to_shot", text="Jump to Shot").index = i
            row.operator("shot_manager.remove_shot", text="", icon="X").index = i

class SHOTMANAGER_OT_add_shot(bpy.types.Operator):
    bl_idname = "shot_manager.add_shot"
    bl_label = "Add New Shot"
    bl_description = "Add a new shot entry"

    def execute(self, context):
        context.scene.shot_manager.shots.add()
        return {'FINISHED'}

class SHOTMANAGER_OT_remove_shot(bpy.types.Operator):
    bl_idname = "shot_manager.remove_shot"
    bl_label = "Remove Shot"
    bl_description = "Remove selected shot"
    
    index: bpy.props.IntProperty()

    def execute(self, context):
        sm = context.scene.shot_manager
        sm.shots.remove(self.index)
        return {'FINISHED'}

class SHOTMANAGER_OT_jump_to_shot(bpy.types.Operator):
    bl_idname = "shot_manager.jump_to_shot"
    bl_label = "Jump to Shot"
    bl_description = "Set timeline to shot range"

    index: bpy.props.IntProperty()

    def execute(self, context):
        shot = context.scene.shot_manager.shots[self.index]
        context.scene.frame_start = shot.start_frame
        context.scene.frame_end = shot.end_frame
        context.scene.frame_current = shot.start_frame
        if shot.camera:
            context.scene.camera = shot.camera
        return {'FINISHED'}

def auto_camera_switch(scene):
    current_frame = scene.frame_current
    for shot in scene.shot_manager.shots:
        if shot.start_frame <= current_frame <= shot.end_frame:
            if shot.camera and scene.camera != shot.camera:
                scene.camera = shot.camera
            break

class ShotManagerSettings(bpy.types.PropertyGroup):
    shots: bpy.props.CollectionProperty(type=ShotEntry)

classes = (
    ShotEntry,
    ShotManagerSettings,
    SHOTMANAGER_PT_panel,
    SHOTMANAGER_OT_add_shot,
    SHOTMANAGER_OT_remove_shot,
    SHOTMANAGER_OT_jump_to_shot,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.shot_manager = bpy.props.PointerProperty(type=ShotManagerSettings)
    bpy.app.handlers.frame_change_pre.append(auto_camera_switch)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.shot_manager
    bpy.app.handlers.frame_change_pre.remove(auto_camera_switch)

if __name__ == "__main__":
    register()
