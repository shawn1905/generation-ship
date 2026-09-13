"""Blender background generator. Outputs go to explicitly supplied directory.

blender -b --factory-startup --python scripts/build_cargo_asset.py -- --output DIR
No network, add-ons, or external assets. All dimensions are metres.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--length', type=float)
parser.add_argument('--skip-render', action='store_true')
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
cfg = json.loads((ROOT/'world/造物/EXP-LUN-CARGO-001/parameters.json').read_text())
if args.length is not None:
    cfg['length_m'] = args.length
L, W, H, T = [cfg[k] for k in ('length_m','width_m','height_m','wall_m')]
assert .45 <= L <= 1.0 and .25 <= W <= .6 and .2 <= H <= .5
out = Path(args.output).resolve()
out.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x, scene.render.resolution_y = 1400, 1100
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.world.color = (.15, .15, .15)
scene.view_settings.view_transform = 'AgX'
asset = bpy.data.collections.new('EXP-LUN-CARGO-001')
scene.collection.children.link(asset)
parts, groups = [], {}


def mat(name, color, metallic=0, rough=.5):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Metallic'].default_value = metallic
    bs.inputs['Roughness'].default_value = rough
    return m


shell = mat('Unpainted aluminium / concept', (.43,.48,.51), .65, .38)
frame = mat('Structural rails / dark anodised', (.075,.1,.12), .6, .4)
lidmat = mat('Lid aluminium', (.57,.61,.63), .65, .36)
rubber = mat('Replaceable seal / black', (.024,.028,.03), 0, .75)
liner = mat('Removable liner / grey', (.19,.22,.23), 0, .8)
orange = mat('Manual release / oxide orange', (.65,.18,.035), .25, .45)
steel = mat('Pin and fastener / steel', (.3,.33,.35), .8, .3)
white = mat('Identification', (.78,.82,.8), .1, .6)


def finish(obj, name, material, group, bevel=0):
    obj.name = name
    for c in list(obj.users_collection): c.objects.unlink(obj)
    asset.objects.link(obj)
    obj.data.materials.append(material)
    obj['component_id'] = name
    obj['assembly_group'] = group
    obj['evidence_status'] = 'experimental_geometry'
    if bevel:
        mod = obj.modifiers.new('Manufacturing edge radius', 'BEVEL')
        mod.width, mod.segments = bevel, 3
    parts.append(obj)
    groups.setdefault(group, []).append(obj)
    return obj


def box(name, dims, pos, material, group, bevel=.001):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    obj = bpy.context.object
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(obj,name,material,group,bevel)


def cylinder(name, radius, depth, pos, material, group, axis='Z'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=depth, location=pos)
    obj = bpy.context.object
    if axis == 'X': obj.rotation_euler[1] = math.pi/2
    if axis == 'Y': obj.rotation_euler[0] = math.pi/2
    return finish(obj,name,material,group,.0005)


def bore(obj, position, radius=.0046):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=.09, location=position, rotation=(0,math.pi/2,0))
    cutter=bpy.context.object
    mod=obj.modifiers.new('Functional retention pin bore', 'BOOLEAN')
    mod.operation='DIFFERENCE'; mod.object=cutter
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter,do_unlink=True)


def text_mesh(name, text, pos, size, material):
    bpy.ops.object.text_add(location=pos, rotation=(math.pi/2,0,0))
    o=bpy.context.object
    o.data.body, o.data.size, o.data.extrude = text, size, .00012
    o.data.align_x='CENTER'
    bpy.ops.object.convert(target='MESH')
    return finish(bpy.context.object,name,material,'identification')


z0=.09
lid_t=.012
wall_h=H-lid_t-T
box('shell_floor',(L,W,T),(0,0,z0+T/2),shell,'body')
for s in (-1,1):
    box(f'shell_long_{s}',(L,T,wall_h),(0,s*(W-T)/2,z0+T+wall_h/2),shell,'body')
    box(f'shell_end_{s}',(T,W-2*T,wall_h),(s*(L-T)/2,0,z0+T+wall_h/2),shell,'body')
    for x in (-L*.27,0,L*.27):
        box(f'panel_rib_{s}_{x:.3f}',(.014,.005,wall_h-.08),(x,s*(W/2+.0025),z0+H/2),shell,'body')
    # fixed handle has a real open finger space, not a decorative solid block
    for x in (-.065,.065):
        box(f'handle_standoff_{s}_{x}',(.016,.05,.016),(x,s*(W/2+.025),z0+.155),frame,'handle')
    cylinder(f'handle_grip_{s}',.01,.146,(0,s*(W/2+.055),z0+.155),frame,'handle','X')

interfaces=[]
for sx in (-1,1):
    for sy in (-1,1):
        tag=f'{sx}_{sy}'
        x,y=sx*(L/2-.024),sy*(W/2-.024)
        interfaces.append({'id':'dock_'+tag,'position_m':[x,y,.055],
                           'insertion_axis':[0,0,-1],'release_axis':[sx,0,0],
                           'receiver_clearance_m':.0015})
        box('corner_post_'+tag,(.023,.023,H-lid_t),(x,y,z0+(H-lid_t)/2),frame,'body')
        # Open U receiver: front/back cheeks guide a foot; pin is behind foot.
        foot=box('foot_'+tag,(.02,.024,.045),(x,y,.0675),frame,'body')
        bore(foot,(x,y,.07))
        for dx in (-.013,.013):
            cheek=box(f'receiver_{tag}_{dx}',(.003,.045,.04),(x+dx,y,.065),steel,'base')
            bore(cheek,(x,y,.07))
        cylinder('retention_pin_'+tag,.004,.04,(x,y,.07),orange,'dock_lock','X')
        cylinder('pin_head_'+tag,.007,.004,(x+sx*.022,y,.07),orange,'dock_lock','X')

# Base bears load through two longitudinal rails and cross members.
for sy in (-1,1):
    box(f'base_rail_{sy}',(L+.06,.055,.028),(0,sy*(W/2-.024),.031),frame,'base')
for sx in (-1,1):
    box(f'base_cross_{sx}',(.045,W+.05,.018),(sx*(L/2-.024),0,.013),frame,'base')
    for sy in (-1,1):
        cylinder(f'floor_anchor_{sx}_{sy}',.008,.006,(sx*(L/2-.024),sy*(W/2+.012),.025),steel,'base')

lid=box('lid_plate',(L,W,lid_t),(0,0,z0+H-lid_t/2),lidmat,'lid')
gap=cfg['lid_clearance_m']
for sy in (-1,1):
    box(f'lid_inner_lip_y_{sy}',(L-.07,.002,.009),(0,sy*(W/2-T-gap-.001),z0+H-lid_t-.0045),lidmat,'lid',.0003)
    box(f'lid_seal_y_{sy}',(L-.075,.003,.002),(0,sy*(W/2-.014),z0+H-lid_t-.001),rubber,'lid',.0003)
    box(f'lid_stiffener_{sy}',(L-.1,.016,.007),(0,sy*.11,z0+H+.0035),lidmat,'lid')
for sx in (-1,1):
    box(f'lid_inner_lip_x_{sx}',(.002,W-.07,.009),(sx*(L/2-T-gap-.001),0,z0+H-lid_t-.0045),lidmat,'lid',.0003)
    # sliding lid retainers; release outwards along X before lifting lid
    box(f'latch_guide_{sx}',(.015,.065,.055),(sx*(L/2+.01),0,z0+H-.025),frame,'body')
    box(f'latch_slider_{sx}',(.043,.036,.009),(sx*(L/2+.008),0,z0+H+.005),orange,'lid_lock')
    cylinder(f'latch_knob_{sx}',.009,.012,(sx*(L/2+.017),0,z0+H+.015),orange,'lid_lock')

box('liner_floor',(L-.065,W-.065,.008),(0,0,z0+T+.006),liner,'liner')
for sy in (-1,1):
    box(f'liner_wall_{sy}',(L-.07,.006,.105),(0,sy*(W/2-.036),z0+.064),liner,'liner')
for sx in (-1,1):
    box(f'liner_end_{sx}',(.006,W-.07,.105),(sx*(L/2-.036),0,z0+.064),liner,'liner')
box('identity_plate',(.23,.003,.043),(0,-W/2-.006,z0+.067),frame,'identification')
text_mesh('identity_text','LUN / CARGO 001',(0,-W/2-.0077,z0+.067),.014,white)
text_mesh('identity_subtext','EXP  /  NON-PRESSURISED',(0,-W/2-.0077,z0+.051),.006,white)
bpy.context.view_layer.update()


def bounds(objects):
    dg=bpy.context.evaluated_depsgraph_get()
    points=[o.matrix_world @ Vector(v) for orig in objects for o in [orig.evaluated_get(dg)] for v in o.bound_box]
    lo=[min(v[i] for v in points) for i in range(3)]
    hi=[max(v[i] for v in points) for i in range(3)]
    return {'min_m':lo,'max_m':hi,'size_m':[hi[i]-lo[i] for i in range(3)]}


def overlap(a,b,eps=.0001):
    return all(min(a['max_m'][i],b['max_m'][i])-max(a['min_m'][i],b['min_m'][i])>eps for i in range(3))


original={o.name:o.location.copy() for o in parts}
# Moving geometry check: release sliders, then lift lid; small intended seal contacts excluded.
for o in groups['lid_lock']: o.location.x += .06*(1 if o.location.x>0 else -1)
checks=[]
obstacles=groups['body']+groups['handle']+groups['lid_lock']
for lift in (.012,.025,.05,.1,.18):
    for o in groups['lid']: o.location=original[o.name]+Vector((0,0,lift))
    bpy.context.view_layer.update()
    hits=[(a.name,b.name) for a in groups['lid'] for b in obstacles if overlap(bounds([a]),bounds([b]))]
    checks.append({'lid_lift_m':lift,'aabb_intersections':hits})
for o in parts: o.location=original[o.name]
bpy.context.view_layer.update()
report={'asset':cfg,'interfaces':interfaces,'assembly_bounds':bounds(parts),
        'lid_plate_bounds':bounds([lid]),'components':[{'id':o.name,'group':o['assembly_group'],'bounds':bounds([o])} for o in parts],
        'lid_lift_checks':checks,'handle_clearance_m':.045,
        'limits':['AABB sampled coarse screening only, not continuous collision certification',
                  'Dock pin bores modelled with 0.6mm radial clearance; locking detent and load ratings remain undeveloped',
                  'No strength, leak, thermal, vibration or dust certification',
                  'No hinge: release two sliders, remove lid vertically',
                  'Mass estimate covers ideal five flat shell panels only; assembly mass not established'],
        'ideal_shell_panels_mass_kg':2700*T*(L*W+2*L*wall_h+2*(W-2*T)*wall_h),
        'source_sha256':hashlib.sha256((ROOT/cfg['source_path']).read_bytes()).hexdigest(),
        'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(out/'parameters.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active=lid
bpy.ops.export_scene.gltf(filepath=str(out/'cargo.glb'),export_format='GLB',use_selection=True,export_apply=True)
report['glb_sha256']=hashlib.sha256((out/'cargo.glb').read_bytes()).hexdigest()
# Exact evaluated meshes for an offline Unity import path, avoiding extra packages.
meshdata=[]
dg=bpy.context.evaluated_depsgraph_get()
for o in parts:
    ev=o.evaluated_get(dg); mesh=ev.to_mesh(); mesh.calc_loop_triangles()
    vertices=[ev.matrix_world @ v.co for v in mesh.vertices]
    meshdata.append({'name':o.name,'group':o['assembly_group'],
        'vertices':[{'x':v.x,'y':v.z,'z':v.y} for v in vertices],
        'triangles':[i for tri in mesh.loop_triangles for i in reversed(tri.vertices)],
        'color':list(o.data.materials[0].diffuse_color)})
    ev.to_mesh_clear()
(out/'unity_meshes.json').write_text(json.dumps({'parts':meshdata},separators=(',',':')))

# Neutral presentation stage; not part of exported asset.
floor=mat('Studio floor',(.12,.14,.16),.1,.7)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.005))
bpy.context.object.name='PRESENTATION_floor'
bpy.context.object.data.materials.append(floor)
for name,loc,power,size in [('Key',(1,-2,3),170,2),('Fill',(-2,-1,1),80,2),('Rim',(1,2,2),230,1.5)]:
    data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.shape='DISK'; data.size=size
    o=bpy.data.objects.new(name,data); scene.collection.objects.link(o); o.location=loc
    o.rotation_euler=(Vector((0,0,.2))-o.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('Inspection camera'); cam=bpy.data.objects.new('Inspection camera',data)
scene.collection.objects.link(cam); scene.camera=cam; data.type='ORTHO'; data.ortho_scale=max(1.05,L*1.65)


def render(name,pos,target=(0,0,.22),scale=None):
    cam.location=pos; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    data.ortho_scale=scale or max(1.05,L*1.65)
    if not args.skip_render:
        scene.render.filepath=str(out/(name+'.png')); bpy.ops.render.render(write_still=True)


render('01_assembly',(1,-1.35,1))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'cargo.blend'))
render('02_front',(0,-3,.22))
render('03_side',(3,0,.22))
render('04_top',(0,0,3),target=(0,0,0))
for o in parts:
    g=o['assembly_group']
    if g=='lid': o.location.z+=.30
    elif g=='liner': o.location.z+=.14
    elif g=='base': o.location.z-=.12
    elif g=='dock_lock': o.location.x+=.08*(1 if o.location.x>0 else -1)
    elif g=='lid_lock': o.location.x+=.09*(1 if o.location.x>0 else -1)
bpy.context.view_layer.update()
bpy.data.objects['PRESENTATION_floor'].hide_render=True
render('05_exploded',(1,-1.35,1),target=(0,0,.33),scale=max(1.55,L*1.85))
for o in parts: o.location=original[o.name]
bpy.context.view_layer.update()
(out/'inspection.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('CARGO_RESULT',json.dumps({'parts':len(parts),'bounds':report['assembly_bounds'],
      'lid_intersection_count':sum(len(c['aabb_intersections']) for c in checks),'output':str(out)}))
