"""Run with Blender -b --python ... -- --directory DIR. Re-import exported GLB."""
import argparse, hashlib, json, sys
from pathlib import Path
import bpy
from mathutils import Vector

p=argparse.ArgumentParser(); p.add_argument('--directory',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]); directory=Path(a.directory)
report=json.loads((directory/'inspection.json').read_text())
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(directory/'cargo.glb'))
parts=[o for o in bpy.context.scene.objects if o.type=='MESH']
points=[o.matrix_world@Vector(v) for o in parts for v in o.bound_box]
size=[max(v[i] for v in points)-min(v[i] for v in points) for i in range(3)]
assert len(parts)==len(report['components'])
assert all(abs(x-y)<1e-5 for x,y in zip(size,report['assembly_bounds']['size_m']))
assert hashlib.sha256((directory/'cargo.glb').read_bytes()).hexdigest()==report['glb_sha256']
s=bpy.context.scene; s.render.engine='BLENDER_EEVEE'; s.render.resolution_x=1000; s.render.resolution_y=800; s.render.resolution_percentage=100
s.world.color=(.2,.2,.2)
ld=bpy.data.lights.new('Reference key','AREA'); ld.energy=200; ld.size=2
lo=bpy.data.objects.new('Reference key',ld); s.collection.objects.link(lo); lo.location=(1,-2,3)
lo.rotation_euler=(Vector((0,0,.2))-lo.location).to_track_quat('-Z','Y').to_euler()
cd=bpy.data.cameras.new('Reimport camera'); co=bpy.data.objects.new('Reimport camera',cd); s.collection.objects.link(co); s.camera=co
cd.type='ORTHO'; cd.ortho_scale=1.15
for label,loc in [('06_reimport_front',(1,-1,1)),('07_reimport_rear',(-1,1,.8))]:
 co.location=loc; co.rotation_euler=(Vector((0,0,.2))-co.location).to_track_quat('-Z','Y').to_euler()
 s.render.filepath=str(directory/(label+'.png')); bpy.ops.render.render(write_still=True)
(directory/'roundtrip.json').write_text(json.dumps({'status':'passed','parts':len(parts),'bounds_m':size,'glb_sha256':report['glb_sha256'],'views':['06_reimport_front.png','07_reimport_rear.png']},indent=2))
print('GLB_ROUNDTRIP_PASS',size)
