from random import random
import bpy
from math import pi

#元素清除器
def delete_object(name):
    # try to find the object by name
    if name in bpy.data.objects:
        # if it exists, select it and delete it
        obj = bpy.data.objects[name]
        obj.select_set(True)
        bpy.ops.object.delete(use_global=False)

#创建轨道
def create_torus(radius, obj_name):
    # (same as the create_sphere method)
    obj = bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0),
        major_radius=radius,
        minor_radius=0.1,
        major_segments=60
    )
    bpy.context.object.name = obj_name
    # apply smooth shading
    bpy.ops.object.shade_smooth()
    return bpy.context.object

#创建球体
def create_sphere(radius, distance_to_sun, obj_name):
    # instantiate a UV sphere with a given
    # radius, at a given distance from the
    # world origin point
    obj = bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        location=(distance_to_sun, 0, 0),
        scale=(1, 1, 1)
    )
    # rename the object
    bpy.context.object.name = obj_name
    # apply smooth shading
    bpy.ops.object.shade_smooth()
    # return the object reference
    return bpy.context.object

#创建材质
def create_emission_shader(color, strength, mat_name):
    # create a new material resource (with its
    # associated shader)
    mat = bpy.data.materials.new(mat_name)
    # enable the node-graph edition mode
    mat.use_nodes = True
    
    # clear all starter nodes
    nodes = mat.node_tree.nodes
    nodes.clear()

    # add the Emission node
    node_emission = nodes.new(type="ShaderNodeEmission")
    # (input[0] is the color)
    node_emission.inputs[0].default_value = color
    # (input[1] is the strength)
    node_emission.inputs[1].default_value = strength
    
    # add the Output node
    node_output = nodes.new(type="ShaderNodeOutputMaterial")
    
    # link the two nodes
    links = mat.node_tree.links
    link = links.new(node_emission.outputs[0], node_output.inputs[0])

    # return the material reference
    return mat

#主程序区域

#预设数值
N_PLANETS = 8
START_FRAME = 1
END_FRAME = 200

# clean scene + planet materials
delete_object("Sun")
for n in range(N_PLANETS):
    delete_object("Planet-{:02d}".format(n))
    delete_object("Radius-{:02d}".format(n))
for m in bpy.data.materials:
    bpy.data.materials.remove(m)

ring_mat = create_emission_shader(
    (1, 1, 1, 1), 1, "RingMat"
)

for n in range(N_PLANETS):
    # get a random radius (a float in [1, 5])
    r = 1 + random() * 4
    # get a random distace to the origin point:
    # - an initial offset of 30 to get out of the sun's sphere
    # - a shift depending on the index of the planet
    # - a little "noise" with a random float
    d = 30 + n * 12 + (random() * 4 - 2)
    # instantiate the planet with these parameters
    # and a custom object name
    planet = create_sphere(r, d, "Planet-{:02d}".format(n))
    planet.data.materials.append(
        create_emission_shader(
            (random(), random(), 1, 1),
            2,
            "PlanetMat-{:02d}".format(n)
        )
    )
    # add the radius ring display
    ring = create_torus(d, "Radius-{:02d}".format(n))
    ring.data.materials.append(ring_mat)

    # set planet as active object
    bpy.context.view_layer.objects.active = planet
    planet.select_set(True)
    # set object origin at world origin
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    # setup the planet animation data
    planet.animation_data_create()
    planet.animation_data.action = bpy.data.actions.new(name="RotationAction")
    fcurve = planet.animation_data.action.fcurves.new(
        data_path="rotation_euler", index=2
    )
    k1 = fcurve.keyframe_points.insert(
        frame=START_FRAME,
        value=0
    )
    k1.interpolation = "LINEAR"
    k2 = fcurve.keyframe_points.insert(
        frame=END_FRAME,
        value=(2 + random() * 2) * pi
    )
    k2.interpolation = "LINEAR"

#add the sun sphere
sun = create_sphere(12, 0, "Sun")
sun.data.materials.append(
    create_emission_shader(
        (1, 0.66, 0.08, 1), 10, "SunMat"
    )
)
