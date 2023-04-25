def rect_plate_area(w, t):
    return w * t


def rect_plate_ixx(w, t):
    return w * t ** 3 / 12


import sectionproperties.pre.library.steel_sections as steel_sections
from sectionproperties.analysis.section import Section

# create geometry of the cross-section
geometry = steel_sections.channel_section(d=200, b=75, t_f=12, t_w=6, r=12, n_r=8)

# generate a finite element mesh
geometry.create_mesh(mesh_sizes=[10])

# create a Section object for analysis
section = Section(geometry)

# calculate various cross-section properties
section.calculate_geometric_properties()
section.calculate_plastic_properties()
# section.calculate_warping_properties()

section.display_results(fmt='.3f')

