
from section_property.member_properties import DesignProperty, ISectionRolled
from analysis import partial_safety_factors


class BendingCheck:
    def __init__(self, name):

        self.Ymo = partial_safety_factors.y_m_0

        if not isinstance(name, DesignProperty):
            raise ValueError(f"argument is not valid {DesignProperty} object: {repr(name)}")
        self.name = name
        self.l_lt = name.ll_t
        self.cant = name.cant
        self.lat = name.lat
        if self.l_lt is None or self.lat is None or self.cant is None:
            raise ValueError(f"l_lt, lat and cant can not be {None} for class: {__class__.__name__}")

        self.zp_zz = name.zp_zz
        self.ze_zz = name.ze_zz
        self.fy = name.fy
        self.m_cr = name.m_cr
        self.a_lt = name.a_lt
        self.shear_lag = name.shear_lag
        self.web_buckling = name.web_buckling
        self.section_class = name.critical_class

        if self.section_class == 'plastic' or 'compact':
            self.Bb = 1.0
        elif self.section_class == 'semi_compact':
            self.Bb = self.ze_zz / self.zp_zz
        else:
            raise ValueError(f"can not design for slender section: {__class__.__name__}")

        if self.shear_lag:
            raise ValueError(f"limits for shear lag effect exceeded. clause 8.2.1.5")
        if self.web_buckling:
            raise ValueError(f"web is susceptible to web buckling")

    def analyse(self):
        if self.lat == 1:
            if self.cant == 1:
                return min(self.Bb * self.zp_zz * self.fy / self.Ymo,
                           1.5 * self.ze_zz * self.fy / self.Ymo)
            else:
                return min(self.Bb * self.zp_zz * self.fy / self.Ymo,
                           1.2 * self.ze_zz * self.fy / self.Ymo)
        else:
            nd_sr = min((self.Bb * self.zp_zz * self.fy / self.m_cr) ** 0.5,
                        (1.2 * self.ze_zz * self.fy / self.m_cr) ** 0.5)
            o_lt = 0.5 * (1 + self.a_lt * (nd_sr - 0.2) + nd_sr ** 2)
            x_lt = min((1 / (o_lt + (o_lt ** 2 - nd_sr ** 2) ** 0.5)), 1)
            fbd = x_lt * self.fy / self.Ymo
            return self.Bb * self.zp_zz * fbd


class ShearCheck:
    def __init__(self, name, tension_field_action=False):
        self.Ymo = partial_safety_factors.y_m_0

        if not isinstance(name, DesignProperty):
            raise ValueError(f"argument is not valid {DesignProperty} object: {repr(name)}")
        self.shear_area = name.shear_area
        self.fyw = name.fyw  # yield strength of the web
        self.fy = name.fy
        self.t_cre = name.t_cre
        self.web_buckling = name.web_buckling
        self.c = name.c
        self.d = name.d
        self.tension_field_action = tension_field_action
        if self.c / self.d < 1.0 and self.tension_field_action:
            raise ValueError(f"if tension_field_action = True, then c/d shall be >= 1.0")

    def analyse(self):
        if self.web_buckling:
            if self.tension_field_action:
                pass
            else:
                nd_sr = (self.fyw / (self.t_cre * (3 ** 0.5))) ** 0.5
                if nd_sr <= 0.8:
                    t_b = self.fyw / (3 ** 0.5)
                elif nd_sr >= 1.2:
                    t_b = self.fyw / ((3 ** 0.5) * (nd_sr ** 2))
                else:
                    t_b = (1 - 0.8 * (nd_sr - 0.8)) * (self.fyw / (3 ** 0.5))
                return self.shear_area * t_b / self.Ymo

        else:
            return (self.shear_area * self.fyw / (3 ** 0.5)) / self.Ymo


class CompressionCheck:
    def __init__(self, name):
        self.Ymo = partial_safety_factors.y_m_0

        if not isinstance(name, DesignProperty):
            raise ValueError(f"argument is not valid {DesignProperty} object: {repr(name)}")

        self.lz = name.lz_compression
        self.ly = name.ly_compression
        if self.lz is None or self.ly is None or self.lz <= 0 or self.ly <= 0:
            raise ValueError(f"lz, ly can not be {None} or 0 for class: {__class__.__name__}")

        self.section_class = name.critical_class
        if self.section_class == 'slender':
            raise ValueError(f"can not design for slender section: {__class__.__name__}")

        self.a_e = name.a_e
        self.fy = name.fy

        self.f_cc_zz = name.f_cc['f_cc_zz']
        self.f_cc_yy = name.f_cc['f_cc_yy']

        self.alpha_zz = name.imperfection_factor['alpha_zz']  # buckling class imperfection factor, clause 7.1.2.2
        self.alpha_yy = name.imperfection_factor['alpha_yy']  # buckling class imperfection factor, clause 7.1.2.2

    def analyse(self):
        nd_sr_zz = (self.fy / self.f_cc_zz) ** 0.5
        o_zz = 0.5 * (1 + self.alpha_zz * (nd_sr_zz - 0.2) + nd_sr_zz ** 2)
        f_cd_zz = (self.fy / self.Ymo) / (o_zz + (o_zz ** 2 - nd_sr_zz ** 2) ** 0.5)

        nd_sr_yy = (self.fy / self.f_cc_yy) ** 0.5
        o_yy = 0.5 * (1 + self.alpha_yy * (nd_sr_yy - 0.2) + nd_sr_yy ** 2)
        f_cd_yy = (self.fy / self.Ymo) / (o_yy + (o_yy ** 2 - nd_sr_yy ** 2) ** 0.5)

        return min(f_cd_zz * self.a_e, f_cd_yy * self.a_e)


if __name__ == "__main__":
    section_name = ISectionRolled(name='ismb_350', country='indian', fy_Mpa=250)
    member_design_prop = DesignProperty(name=section_name,
                                        ll_t=3, lat=0, cant=0, c=0.0,
                                        lz_compression=6, ly_compression=3)

    abc = ShearCheck(name=member_design_prop, tension_field_action=False)
    pqr = BendingCheck(name=member_design_prop)
    xyz = CompressionCheck(name=member_design_prop)
    print(xyz.analyse())
