import time

from build123d import *
from ocp_vscode import *
from threejs_materials import PbrProperties
from bd_materials import metals, plastics, glass, finishes

mc = (Align.MIN, Align.CENTER)
ccm = (Align.CENTER, Align.CENTER, Align.MIN)
ccM = (Align.CENTER, Align.CENTER, Align.MAX)

#
# Material setup
#

# Use a GPUOpen material
alu_hex = metals.custom_metal(
    "alu_hex", 2700, pbr=PbrProperties.from_gpuopen("Aluminum Hexagon")
)

# Use a GPUOpen material and override the glass behavior
glass_ = glass.soda_lime(thickness_mm=0.8)

# Use an AmbientCG material, and scale the texture to 2 in u and v direction
metal = metals.stainless(finish=finishes.brushed())

# Use a PhysicallyBased material and override color for two material instances
light = plastics.pc(color=(1, 0, 0))


#
# The object
#

e = Ellipse(10, 3)
e2 = offset(e, -0.2)
e -= e2
e -= Rectangle(12, 6, align=mc)

e3 = offset(e2, -0.1)
e2 -= e3
e2 -= Rectangle(12, 6, align=mc)

body = Rot(90, 0, 0) * revolve(e.face(), Axis.Y)
inner = Rot(90, 0, 0) * revolve(e2.face(), Axis.Y)
mask = Cylinder(4, 3, align=ccm)
body = body - mask
inner = inner - mask

window = Pos(0, 0, 2.55) * (
    Rot(0, 90, 0) * (Sphere(4) - Sphere(3.98)) - Box(10, 10, 10, align=ccM)
)
lights = [loc * Rot(0, 0, 180) * Sphere(0.5) for loc in PolarLocations(9.8, 6)]
body -= lights

body.label = "body"
inner.label = "inner"
window.label = "window"
for i, l in enumerate(lights):
    l.label = f"light_{i}"

#
# The object
#

body.material = metal
inner.material = alu_hex
window.material = glass_

for i, l in enumerate(lights):
    l.material = light

# %%

#
# Visualisation
#


# show and use a custom env map, rotated by 180°
show(
    body,
    inner,
    window,
    lights,
    studio_environment="https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/4k/suburban_garden_4k.hdr",
    studio_env_rotation=275,
    position=[53.93, -36.89, 24.07],
    quaternion=[0.49075, 0.26839, 0.38282, 0.73522],
    target=[0.78, -1.22, -1.76],
)

time.sleep(1)
