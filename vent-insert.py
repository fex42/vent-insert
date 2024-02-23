from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

vent_h = 190.0
vent_w = 240.0
vent_b = 36.0
wall_thickness = 2.5
pipe_height = 16.0
flange_dia = 128.0
holes_dia = 119.0
hole_dia = 4.6
apothema = 8.0

with BuildPart() as wall_flange:
    with BuildSketch():
        Rectangle(vent_w, vent_h)
        Rectangle(vent_w-wall_thickness, vent_h-wall_thickness, mode=Mode.SUBTRACT)
    extrude(amount=pipe_height)
    with BuildSketch():
        Rectangle(vent_w+vent_b, vent_h+vent_b)
        Rectangle(vent_w, vent_h, mode=Mode.SUBTRACT)
    extrude(amount=wall_thickness)

    # fillet on outer flange/pipe edge makes it hopefully more stable
    edge = wall_flange.edges().filter_by_position(axis=Axis.Z, minimum=wall_thickness, maximum=wall_thickness)[0]
    fillet(objects=edge, radius=1.0)
    # hexagon grid
    with BuildSketch() as grid_sk:
        Rectangle(vent_w+vent_b, vent_h+vent_b)
        with HexLocations(apothema, 18, 14):
            RegularPolygon(apothema, 6, mode=Mode.SUBTRACT)
    extrude(amount=wall_thickness)
    # screw holes
    with BuildSketch():
        with Locations(
            (0, +vent_h/2 + vent_b/4),
            (0, -vent_h/2 - vent_b/4),
            (+vent_w/2 + vent_b/4, +vent_h/4),
            (-vent_w/2 - vent_b/4, +vent_h/4),
            (+vent_w/2 + vent_b/4, -vent_h/4),
            (-vent_w/2 - vent_b/4, -vent_h/4)
        ):
             Circle(hole_dia/2)
    extrude(amount=2*wall_thickness, mode=Mode.ADD)

show_object(wall_flange)

wall_flange.part.export_step("vent-insert.step")