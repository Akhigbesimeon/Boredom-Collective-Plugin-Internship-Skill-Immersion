bl_info = {
    "name": "Scene Tracker",
    "author": "Akhigbe Simeon",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Scene Tracker",
    "description": "Displays key statistics about the current scene",
    "category": "3D View",
}

import bpy

class SCENETRACKER_PT_panel(bpy.types.Panel):
    bl_label = "Scene Tracker"
    bl_idname = "SCENETRACKER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Scene Tracker'

    def draw(self, context):
        layout = self.layout
        stats = get_scene_stats(context)

        layout.label(text="🧱 Object Stats")
        layout.label(text=f"Total Objects: {stats['total_objects']}")
        layout.label(text=f"Mesh Objects: {stats['mesh_objects']}")
        layout.label(text=f"Cameras: {stats['camera_objects']}")
        layout.label(text=f"Lights: {stats['light_objects']}")

        layout.separator()

        layout.label(text="📊 Geometry Stats")
        layout.label(text=f"Total Vertices: {stats['total_vertices']}")
        layout.label(text=f"Total Faces: {stats['total_faces']}")
        layout.label(text=f"Total Edges: {stats['total_edges']}")

        layout.separator()
        layout.operator("scene_tracker.refresh", icon="FILE_REFRESH")


class SCENETRACKER_OT_refresh(bpy.types.Operator):
    bl_idname = "scene_tracker.refresh"
    bl_label = "Refresh Scene Stats"
    bl_description = "Refresh the scene statistics manually"

    def execute(self, context):
        return {'FINISHED'}

def get_scene_stats(context):
    total_objects = len(context.scene.objects)
    mesh_objects = sum(1 for obj in context.scene.objects if obj.type == 'MESH')
    camera_objects = sum(1 for obj in context.scene.objects if obj.type == 'CAMERA')
    light_objects = sum(1 for obj in context.scene.objects if obj.type == 'LIGHT')

    total_vertices = 0
    total_faces = 0
    total_edges = 0

    for obj in context.scene.objects:
        if obj.type == 'MESH':
            mesh = obj.data
            total_vertices += len(mesh.vertices)
            total_faces += len(mesh.polygons)
            total_edges += len(mesh.edges)

    return {
        "total_objects": total_objects,
        "mesh_objects": mesh_objects,
        "camera_objects": camera_objects,
        "light_objects": light_objects,
        "total_vertices": total_vertices,
        "total_faces": total_faces,
        "total_edges": total_edges,
    }

classes = (
    SCENETRACKER_PT_panel,
    SCENETRACKER_OT_refresh,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
