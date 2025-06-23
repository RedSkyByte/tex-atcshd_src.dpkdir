import bpy
import os

# A placeholder hack to obtain specular from color texture

def prep_graph():
    bpy.context.scene.use_nodes = True

    node_tree = bpy.context.scene.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    for n in nodes:
        nodes.remove(n)

    node_chain = {
            'img':'CompositorNodeImage',
            'to_bw':'CompositorNodeRGBToBW',
            'mix': "CompositorNodeMixRGB",
            'hue_sat':'CompositorNodeHueSat',
            'out':'CompositorNodeOutputFile',
    }

    margin = 20.
    node_pos = -margin

    for name, ntype in node_chain.items():
        node = nodes.new(ntype)
        node.location = (node_pos, 0.)
        node_pos += node.width + margin
        globals()[name] = node

    links.new(img.outputs[0], to_bw.inputs[0])
    links.new(to_bw.outputs[0], mix.inputs[1])
    links.new(img.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], hue_sat.inputs[0])
    links.new(hue_sat.outputs[0], out.inputs[0])

prep_graph()
if not os.path.isfile(__file__): # if is not running in shell
    print(f'{__file__} is not a file. Exiting.')
    exit()

dirname = os.path.dirname(__file__)
texdir = os.path.realpath(os.path.join(dirname, '../textures/atcshd'))
print('dirname =', dirname)
print('texdir =', texdir)


def render_spec(img_filename, sat=0.2, value = 0.8):
    mix.inputs[0].default_value = sat
    hue_sat.inputs[3].default_value = value

    img_name = os.path.splitext(img_filename)[0]

    img_filepath = os.path.abspath(
            os.path.join(texdir, img_filename)
            )

    img.image = bpy.data.images.load(img_filepath)

    out.base_path = os.path.abspath(
            os.path.join(dirname, 'build')
            )
            
    out.format.file_format = 'PNG'
    out.format.color_mode = 'RGB'
    bpy.ops.render.render()

    os.replace(
        os.path.join(out.base_path, 'Image0001.png'),
        os.path.join(out.base_path, f'{img_name}_s.png')
        )

ignore_list = (
    'eq2_baselt03b_blue.blend.jpg',
    'eq2_bmtl_03_light.blend.jpg',
    'fog_p.webp',
    'force_field.jpg',
    'force_grid.jpg',
    'sparkle_blue.jpg',
    'sparkle_red.jpg',
    'steam.webp',
    'black.jpg',
    'bulb_red.webp',
    'cubelight_32_blue.blend.jpg',
    'cubelight_32_red.blend.jpg',
    'cubelight_32_white.blend.jpg',
    'eq2_baselt03_blue.blend.jpg',
    'eq2_baselt03b.blend.jpg',
)

with os.scandir(texdir) as scan:
    for item in scan:
        if item.is_file() and item.name not in ignore_list:
            print(f'rendering {item.name}')
            render_spec(item.name)
