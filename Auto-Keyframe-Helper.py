bl_info = {
    "name": "Auto Keyframe Helper",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Auto Keyframe",
    "description": "Adds keyframes only when values change to reduce timeline clutter",
    "category": "Animation",
}

import bpy

# Store the last frame's transform data
previous_transforms = {}

# Add-on properties
class AutoKeyframeSettings(bpy.types.PropertyGroup):
    enable_auto_keyframe: bpy.props.BoolProperty(
        name="Enable Auto Keyframe",
        description="Insert keyframes only when transform values change",
        default=False
    )

# Panel UI
class AUTOKEYFRAME_PT_panel(bpy.types.Panel):
    bl_label = "Auto Keyframe Helper"
    bl_idname = "AUTOKEYFRAME_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Auto Keyframe"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.auto_keyframe_settings
        layout.prop(settings, "enable_auto_keyframe")


# Frame change handler
def auto_keyframe_handler(scene):
    if not scene.auto_keyframe_settings.enable_auto_keyframe:
        return

    obj = scene.objects.active if hasattr(scene.objects, 'active') else scene.view_layers[0].objects.active
    if obj is None or obj.animation_data is None or not obj.animation_data.action:
        return

    global previous_transforms
    current_frame = scene.frame_current
    key = obj.name

    # Get current transform
    current_transform = (
        tuple(obj.location),
        tuple(obj.rotation_euler),
        tuple(obj.scale)
    )

    # Compare and insert keyframe if changed
    if key not in previous_transforms or previous_transforms[key] != current_transform:
        obj.keyframe_insert(data_path="location", frame=current_frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=current_frame)
        obj.keyframe_insert(data_path="scale", frame=current_frame)
        previous_transforms[key] = current_transform


# Register / Unregister
classes = (
    AutoKeyframeSettings,
    AUTOKEYFRAME_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.auto_keyframe_settings = bpy.props.PointerProperty(type=AutoKeyframeSettings)
    bpy.app.handlers.frame_change_post.append(auto_keyframe_handler)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.auto_keyframe_settings
    if auto_keyframe_handler in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(auto_keyframe_handler)

if __name__ == "__main__":
    register()
