# Boredom Collective Blender Plugins (Skill Immersion) – Plugin Collection

This repository contains a set of custom Blender add-ons developed to streamline animation workflows and improve production efficiency for artists and animators. These tools are tailored for internal studio use, focusing on automation, organization, and creative flexibility.

---

## Plugins Included

### 1. **Shot Manager**
Manage multiple shots in a single Blender file. Define shot names, assign frame ranges and cameras, and auto-switch cameras during playback.

**Key Features:**
- Add, rename, and delete shots
- Assign start/end frames and cameras
- Jump to shot range quickly
- Auto-switch cameras during playback

---

### 2. **Scene Cleanup Assistant**
Clean and optimize Blender scenes by removing unused data, hidden objects, and empty collections.

**Key Features:**
- Delete hidden objects
- Remove empty collections
- Purge orphaned data (optional)

---

### 3. **Scene Tracker**
Monitor the scene statistics including total objects, vertices, edges, and polygons.

**Key Features:**
- Display live object count
- Show vertex and polygon totals
- Helpful for optimization and performance checks

---

### 4. **Auto Keyframe Helper**
Automatically inserts keyframes for location, rotation, and scale when objects are moved.

**Key Features:**
- Toggle auto-keying in the viewport
- Choose transform channels to key
- Visual indication of auto-keying status

---

### 5. **Animation Export Organizer**
Batch export animations or objects with structured naming and folder organization.

**Key Features:**
- Set export directory
- Define export format (e.g., FBX, OBJ)
- Batch process multiple selected objects

---

### 6. **Object Namer**
Quickly rename selected objects using a base name and auto-numbering.

**Key Features:**
- Base name + starting number input
- Renames all selected objects
- Helps with naming conventions and scene clarity

---

### 7. **Auto Background Cycler**
Cycle background HDRIs or images during animation or frame changes.

**Key Features:**
- Load multiple HDRIs
- Automatically change backgrounds per frame/interval
- Add variety for lighting previews or test renders

---

### 8. **Pose Transfer Tool**
Copy poses from one armature and apply them to another, even across different scenes.

**Key Features:**
- Copy pose from source rig
- Paste to target rig
- Useful for reusing animation across characters

---

### 9. **Layered Animation System**
Enables additive animation layering using Blender's NLA system for better control and non-destructive animation editing.

**Key Features:**
- Add, remove, mute, and unmute NLA layers
- Create custom animation layers with additive blending
- Supports armature-based workflows

---

## Installation

1. Download the `.py` file for any plugin.
2. Open Blender and go to **Edit > Preferences > Add-ons**.
3. Click **Install**, then select the plugin `.py` file.
4. Enable the checkbox for the installed add-on.
5. Access the plugin from the **Sidebar (N-panel)** in the 3D Viewport.

---

## Development Notes

- All plugins are built with Blender 3.0+ API.
- Each plugin uses `bpy` and standard Python to interact with the Blender data API.
- Custom properties are managed with `PropertyGroup` classes.
- Panels are added to the `VIEW_3D` sidebar for accessibility.

---

## Usage

This code is available to use for anybody or organization

---

## Authors

Created by Akhigbe Simeon as part of an animation technology internship to streamline animator workflows and build production-ready tools.

---

