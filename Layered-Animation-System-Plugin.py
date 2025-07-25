bl_info = {
    "name": "Layered Animation System",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Anim Layers",
    "description": "Enables layered animation workflow using NLA tracks",
    "category": "Animation"
}

import bpy

# Property group for managing layer names
class AnimLayerSettings(bpy.types.PropertyGroup):
    layer_name: bpy.props.StringProperty(name="Layer Name", default="New Layer")

# Panel UI
class ANIMLAYER_PT_panel(bpy.types.Panel):
    bl_label = "Animation Layers"
    bl_idname = "ANIMLAYER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Anim Layers'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.anim_layer_props

        layout.prop(props, "layer_name")
        layout.operator("anim_layer.add", icon="ADD")
        layout.operator("anim_layer.remove", icon="REMOVE")
        layout.operator("anim_layer.mute_all", icon="HIDE_OFF")
        layout.operator("anim_layer.unmute_all", icon="HIDE_ON")

# Operator to add a new NLA track as a layer
class ANIMLAYER_OT_add(bpy.types.Operator):
    bl_idname = "anim_layer.add"
    bl_label = "Add Animation Layer"
    bl_description = "Adds a new animation layer (NLA track)"

    def execute(self, context):
        obj = context.object
        props = context.scene.anim_layer_props

        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "Select an armature object")
            return {'CANCELLED'}

        action = bpy.data.actions.new(name=props.layer_name)
        obj.animation_data_create()
        obj.animation_data.action = action

        nla_track = obj.animation_data.nla_tracks.new()
        nla_track.name = props.layer_name
        strip = nla_track.strips.new(action.name, 1, action)
        strip.blend_type = 'ADD'
        strip.use_animated_influence = True

        return {'FINISHED'}

# Operator to remove selected NLA track
class ANIMLAYER_OT_remove(bpy.types.Operator):
    bl_idname = "anim_layer.remove"
    bl_label = "Remove Active Layer"
    bl_description = "Removes the active NLA track"

    def execute(self, context):
        obj = context.object

        if not obj or not obj.animation_data:
            self.report({'WARNING'}, "No animation data to remove")
            return {'CANCELLED'}

        for track in obj.animation_data.nla_tracks:
            if track.select:
                obj.animation_data.nla_tracks.remove(track)
                return {'FINISHED'}

        self.report({'WARNING'}, "No selected NLA track")
        return {'CANCELLED'}

# Operator to mute all layers
class ANIMLAYER_OT_mute_all(bpy.types.Operator):
    bl_idname = "anim_layer.mute_all"
    bl_label = "Mute All Layers"

    def execute(self, context):
        obj = context.object
        if obj and obj.animation_data:
            for track in obj.animation_data.nla_tracks:
                track.mute = True
        return {'FINISHED'}

# Operator to unmute all layers
class ANIMLAYER_OT_unmute_all(bpy.types.Operator):
    bl_idname = "anim_layer.unmute_all"
    bl_label = "Unmute All Layers"

    def execute(self, context):
        obj = context.object
        if obj and obj.animation_data:
            for track in obj.animation_data.nla_tracks:
                track.mute = False
        return {'FINISHED'}

# Registering classes
classes = (
    AnimLayerSettings,
    ANIMLAYER_PT_panel,
    ANIMLAYER_OT_add,
    ANIMLAYER_OT_remove,
    ANIMLAYER_OT_mute_all,
    ANIMLAYER_OT_unmute_all,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.anim_layer_props = bpy.props.PointerProperty(type=AnimLayerSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.anim_layer_props

if __name__ == "__main__":
    register()
