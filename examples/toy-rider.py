from pathlib import Path

from build123d import *
from ocp_vscode import *
from threejs_materials import PbrProperties
from bd_materials import metals, plastics, textile, glass, finishes, wood

try:
    model = import_step(Path.home() / "Downloads" / "Toy Rider S2022 ASM stp.STEP")
except:
    raise RuntimeError(
        "Download STEP file from https://grabcad.com/library/toy-rider-car-1 first to ~/Downloads"
    )

show(Rot(90, 0, 0) * model)
# %%

#
# materials definition
#

car_red = metals.stainless(finish=finishes.spray_paint(color=(0.5, 0, 0)))
chrome = metals.stainless(finish=finishes.chrome())
rubber = plastics.rubber(color=(0.06, 0.06, 0.06))
glass_ = glass.soda_lime()
steel = metals.stainless(finish=finishes.brushed())
fabric = textile.custom_textile(
    "heavy", 1.0, pbr=PbrProperties.from_gpuopen("Midnight Blue Heavy Fabric")
)
alu = metals.aluminum(finish=finishes.brushed())
alu_matte = metals.aluminum(finish=finishes.fine_sanding())
leather = textile.leather()
wood_ = wood.custom_wood(
    "mahagony", 1.0, pbr=PbrProperties.from_gpuopen("Mahogany Varnished")
)
plastic = plastics.petg(color="black")
acrylic_white = plastics.pc(color="white")
acrylic_red = plastics.pc(color="red")


# %%

#
# Add materials
#


def convert(model):
    color_mapping = {
        "RiderToy": car_red,
        "Trim": car_red,
        "Hood": car_red,
        "Door": car_red,
        "Cover": plastic,
        "Axle": steel,
        "Supportin": steel,
        "FloorBoards": steel,
        "Trunk_Storage": steel,
        "Grill": chrome,
        "Bumper": chrome,
        "Gear": chrome,
        "Peddle": chrome,
        "Bucket": leather,
        "DashandConsole": wood_,
        "Floor": fabric,
        "Radio": plastic,
        "Visor": plastic,
        "Head_Lamp": acrylic_white,
        "TailLamp": acrylic_red,
        "Streeing": leather,
    }

    def walk(obj, ind=""):
        if hasattr(obj, "children") and obj.children:
            children = []
            for child in obj.children:
                if obj.label == "Windshield_ASM" and child.label == "WindShield":
                    child.label = "Windshield"  # subtle renaming

                sub_assembly = walk(child, ind + "  ")
                if sub_assembly is not None:
                    children.append(sub_assembly)

            return Compound(label=obj.label, children=children)

        else:
            if "wheel" in obj.label:
                objects = list(obj)
                objects[0].material = chrome
                objects[1].material = rubber
                obj = Compound(label=obj.label, children=objects)
            elif "Windshield" in obj.label:
                objects = list(obj)
                objects[0].label = "WindShield"
                objects[1].label = "Frame"
                objects[0].material = glass_
                objects[1].material = chrome
                obj = Compound(label=obj.label, children=objects)
            elif "WindShield" in obj.label:
                return None
            else:
                for k, v in color_mapping.items():
                    if k in obj.label:
                        obj.material = v
            return obj

    return walk(model)


model2 = Rot(90, 0, 0) * convert(model)
show(model2)
