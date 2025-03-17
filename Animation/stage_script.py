#舞台生成与渲染测试
#此脚本需输入blender进行使用
import bpy

# 清理当前场景
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 创建舞台（立方体）
bpy.ops.mesh.primitive_cube_add(size=10, location=(0, 0, -1))
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

# 创建多个人物
people = []
for i in range(5):
    x = i * 3 - 6  # 坐标分布
    person = create_person(location=(x, 0, 1))  # 在舞台上放置
    people.append(person)

# 给每个人物添加动画（简单的左右移动）
frame_start = 1
frame_end = 250

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
bpy.context.scene.render.ffmpeg.codec = 'H.264'
bpy.context.scene.render.ffmpeg.video_bitrate = 10000

# 渲染动画
bpy.ops.render.render(animation=True)