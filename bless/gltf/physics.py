

import bpy



## hooks found and implemented by michaeljared from this original gist:
## https://gist.github.com/bikemurt/0c36561a29527b98220230282ab11181


# TODO: old testing exporter... per object. archive soon.

# class bless_glTF2Extension:

#     def __init__(self):
#         pass

#     def gather_gltf_extensions_hook(self, gltf_plan, export_settings):
#         if gltf_plan.extensions is None:
#             gltf_plan.extensions = {}
        
#         extension_name = "OMI_physics_shape"
#         shape_array = []

#         for obj in bpy.context.scene.objects:
#             try:
#                 shape_data = obj[extension_name]
#             except KeyError:
#                 continue
#             else:
#                 shape_array.append(shape_data)

#         gltf_plan.extensions[extension_name] = self.Extension(
#             name=extension_name,
#             extension={"shapes": shape_array},
#             required=False
#         )


#     def gather_node_hook(self, gltf2_object, blender_object, export_settings):
#         if gltf2_object.extensions is None:
#             gltf2_object.extensions = {}

#         # store possible options as an array, iterate, and then tag the gltf data
#         n = "OMI_physics_body"
#         if n in blender_object:
#             gltf2_object.extensions[n] = self.Extension(
#                 name=n,
#                 extension=blender_object[n],
#                 required=False
#             )

# TODO expand...

class OMI_physics_shape(bpy.types.PropertyGroup):

    # possibly needed for internal for gd3d
    is_collision: bpy.props.BoolProperty(default=False)  # type: ignore

    # 
    index: bpy.props.IntProperty(default=0, description="index of the physics shape") # type: ignore

    shape_types: bpy.props.EnumProperty(
        name="",
        description="collider shape types",
        default="convex",
        items=[
            ("box", "Box", "", 1),
            ("sphere", "Sphere", "", 1<<1),
            ("capsule", "Capsule", "", 1<<2),
            ("cylinder", "Cylinder", "", 1<<3),
            ("convex", "Convex", "", 1<<4),
            ("trimesh", "Trimesh", "", 1<<5)
            ])  # type: ignore
    
    
    size: bpy.props.FloatVectorProperty(subtype="XYZ_LENGTH", description="size of the shape in meters", default=[1.0, 1.0, 1.0]) # type: ignore
    radius: bpy.props.FloatProperty(subtype="DISTANCE", description="radius of the shape in meters", default=0.5) # type: ignore 
    height: bpy.props.FloatProperty(subtype="DISTANCE", description="height of the shape in meters", default=2.0) # type: ignore
    
    # The index of the glTF mesh in the document to use as a mesh shape.
    mesh: bpy.props.IntProperty(default=-1) # type: ignore
    


## https://github.com/omigroup/gltf-extensions/tree/main/extensions/2.0/OMI_physics_body

class OMI_physics_body(bpy.types.PropertyGroup):
    shape_index: bpy.props.IntProperty(default=-1) # type: ignore

    # https://github.com/omigroup/gltf-extensions/blob/main/extensions/2.0/OMI_physics_body/README.motion.md
    is_motion: bpy.props.BoolProperty(default=False)  # type: ignore

    # https://github.com/omigroup/gltf-extensions/blob/main/extensions/2.0/OMI_physics_body/README.trigger.md
    is_trigger: bpy.props.BoolProperty(default=False)  # type: ignore
    
    #https://github.com/omigroup/gltf-extensions/blob/main/extensions/2.0/OMI_physics_body/README.collider.md
    is_collision: bpy.props.BoolProperty(default=False)  # type: ignore


    motion_types: bpy.props.EnumProperty(
        name="Body Types",
        description="physics body types",
        default="static",
        items=[
            ("static", "Static", "", 1),
            ("dynamic", "Dynamic", "", 1<<1),
            ("kinematic", "Kinematic", "", 1<<2)
        ])  # type: ignore

    mass: bpy.props.FloatProperty(default=1.0)  # type: ignore

    linear_velocity: bpy.props.FloatVectorProperty(subtype="VELOCITY", default=[0.0, 0.0, 0.0]) # type: ignore 
    angular_velocity: bpy.props.FloatVectorProperty(subtype="VELOCITY", default=[0.0, 0.0, 0.0]) # type: ignore 
    center_of_mass: bpy.props.FloatVectorProperty(default=[0.0, 0.0, 0.0]) # type: ignore



## NOTE temporary operator.

class ApplyProps(bpy.types.Operator):
    """Apply Props"""
    bl_idname = "object.gd3d_apply_props"
    bl_label = "Apply Props"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        objects = context.selected_objects
        scene = context.scene
        body = scene.body_properties
        shape = scene.shape_properties
        
        # retired debug operator. TODO - archive or reuse soon! 

        # for obj in objects:
        #     if body.is_motion:
        #         body_data = build_body_dictionary(body)
        #         obj["OMI_physics_body"] = body_data
        # for obj in objects:

        #     shape_data = build_shape_dictionary(body, shape)
        #     obj["OMI_physics_shape"] = shape_data

        return {'FINISHED'}




class PhysicsPanel(bpy.types.Panel):
    bl_label = "Physics"
    bl_idname = "VIEW3D_PT_object_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bless'

    def draw(self, context):
        layout = self.layout.row()
        body_properties = context.scene.body_properties
        shape_properties = context.scene.shape_properties

        layout.separator(factor=2.0)
        

        if (context.object is not None):
            indented_layout = layout.column()

            indented_layout.row().operator("object.gd3d_apply_props", text="apply")

            indented_layout.label(text="Shape Properties:")
            
            
            prop_indented_layout = indented_layout.row()
            prop_indented_layout.separator(factor=2.0)

            prop_column = prop_indented_layout.column()
            row = prop_column.row()
            row.prop(shape_properties, "is_collision", text="collision object")
            row.prop(shape_properties, "index")

            prop_column.row().prop(shape_properties, "shape_types", text="")

            prop_column.row().prop(shape_properties, "size")

            row = prop_column.row()
            row.prop(shape_properties, "radius")
            row.prop(shape_properties, "height")

            prop_column.row().prop(shape_properties, "mesh")

            row = prop_column.row()
            row.prop(body_properties, "is_motion", text="motion object")
            row.prop(body_properties, "is_trigger", text="trigger object")

            prop_column.row().prop(body_properties, "motion_types")

            prop_column.row().prop(body_properties, "mass")

            prop_column.row().prop(body_properties, "linear_velocity", text="linear velocity")

            prop_column.row().prop(body_properties, "angular_velocity", text="angular velocity")
  
            prop_column.row().prop(body_properties, "center_of_mass", text="center of mass")

            prop_column.row().prop(body_properties, "shape_index", text="shape index")



