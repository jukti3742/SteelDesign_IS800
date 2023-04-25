from analysis.analysis import ShearCheck, BendingCheck, CompressionCheck
from section_property.member_properties import ISectionRolled, DesignProperty

if __name__ == "__main__":
    section_name = ISectionRolled(name='ismb_550', country='indian', fy_Mpa=250)
    member_design_prop = DesignProperty(name=section_name,
                                        ll_t=7, lat=1, cant=0, c=0.0,
                                        lz_compression=7, ly_compression=3.5)

    abc = ShearCheck(name=member_design_prop, tension_field_action=False)
    pqr = BendingCheck(name=member_design_prop)
    xyz = CompressionCheck(name=member_design_prop)

    print(abc.analyse())
    print(pqr.analyse())
    print(xyz.analyse())
