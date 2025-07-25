bl_info = {
    "name": "Auto Background Cycler",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "World Properties > Background Cycler",
    "description": "Cycle HDRIs automatically over frames for testing and look development",
    "category": "Lighting"
}

import bpy
import random

class BACKGROUNDCYCLER_Settings(bpy.types.PropertyGroup):
    hdri_paths: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    interval: bpy.props.IntProperty(name="Frame Interval", default=10, min=1)
    randomize: bpy.props.BoolProperty(name="Randomize", default=False)
    last_switch_frame: bpy.props.IntProperty(default=-1)

class BACKGROUNDCYCLER_OT_add_hdri(bpy.types.Operator):
    bl_idname = "background_cycler.add_hdri"
    bl_label = "Add HDRI"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        item = context.scene.bg_cycler.hdri_paths.add()
        item.name = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class BACKGROUNDCYCLER_PT_panel(bpy.types.Panel):
    bl_label = "Background Cycler"
    bl_idname = "BACKGROUNDCYCLER_PT_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "world"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.bg_cycler

        layout.prop(settings, "interval")
        layout.prop(settings, "randomize")
        layout.operator("background_cycler.add_hdri")

        layout.label(text="HDRI List:")
        for i, item in enumerate(settings.hdri_paths):
            layout.label(text=f"{i+1}: {item.name}")


def switch_background(scene):
    settings = scene.bg_cycler
    current_frame = scene.frame_current

    if not settings.hdri_paths or current_frame == settings.last_switch_frame:
        return

    if current_frame % settings.interval == 0:
        if settings.randomize:
            next_index = random.randint(0, len(settings.hdri_paths) - 1)
        else:
            next_index = (current_frame // settings.interval) % len(settings.hdri_paths)

        hdri_path = settings.hdri_paths[next_index].name
        apply_hdri_to_world(hdri_path)
        settings.last_switch_frame = current_frame


def apply_hdri_to_world(hdri_path):
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world

    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links

    nodes.clear()
    output = nodes.new(type='ShaderNodeOutputWorld')
    bg = nodes.new(type='ShaderNodeBackground')
    env = nodes.new(type='ShaderNodeTexEnvironment')

    env.image = bpy.data.images.load(hdri_path, check_existing=True)

    links.new(env.outputs['Color'], bg.inputs['Color'])
    links.new(bg.outputs['Background'], output.inputs['Surface'])



classes = (
    BACKGROUNDCYCLER_Settings,
    BACKGROUNDCYCLER_OT_add_hdri,
    BACKGROUNDCYCLER_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bg_cycler = bpy.props.PointerProperty(type=BACKGROUNDCYCLER_Settings)
    bpy.app.handlers.frame_change_pre.append(switch_background)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bg_cycler
    bpy.app.handlers.frame_change_pre.remove(switch_background)

if __name__ == "__main__":
    register()
