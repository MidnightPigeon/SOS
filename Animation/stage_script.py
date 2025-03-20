#舞台生成与渲染测试
#此脚本需输入blender进行使用
import bpy

# 清理当前场景
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 创建舞台（立方体）
bpy.ops.mesh.primitive_cube_add(size=20, location=(0, 0, 0))
stage = bpy.context.object
stage.name = "Stage"
stage.scale = (1, 1, 0.1)

# 创建一个简单的人物（圆柱体）
def create_person(location):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, location=location)
    person = bpy.context.object
    person.name = "Person"
    person.scale = (0.5, 0.5, 1)
    return person

#Camera add
def create_camera(location,rotation):
    # 创建一个摄像机
    bpy.ops.object.camera_add()
    # 获取当前选择的摄像机对象
    camera = bpy.context.active_object
    # 设置摄像机的位置 (坐标 x, y, z)
    camera.location = location
    # 设置摄像机的朝向 (方向可以通过旋转来控制，采用欧拉角方式)
    camera.rotation_euler = rotation  # 绕 X, Y, Z 轴旋转
    # 设置当前场景使用新创建的摄像机
    bpy.context.scene.camera = camera

# 创建多个人物
people = []
for i in range(5):
    x = i * 3 - 6  # 坐标分布
    person = create_person(location=(x, 0, 1))  # 在舞台上放置
    people.append(person)

# 给每个人物添加动画（简单的左右移动）
frame_start = 1
frame_end = 250

#add camera
create_camera((10,0,5),(1.2,0,1.57))

for i, person in enumerate(people):
    # 起始位置（动画开始时）
    person.location = (i * 3 - 6, 0, 1)
    person.keyframe_insert(data_path="location", frame=frame_start)

    # 结束位置（动画结束时）
    person.location = (i * 3 - 6, 5, 1)
    person.keyframe_insert(data_path="location", frame=frame_end)

# 设置舞台动画
stage.location = (0, 0, -1)
stage.keyframe_insert(data_path="location", frame=frame_start)
stage.location = (0, 0, -2)
stage.keyframe_insert(data_path="location", frame=frame_end)

# 设置渲染参数
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.fps = 24
bpy.context.scene.render.filepath = "/tmp/animation_output.mp4"
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'
bpy.context.scene.render.ffmpeg.video_bitrate = 10000

