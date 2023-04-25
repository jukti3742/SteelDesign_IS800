import math
from section_property.utilities import z_plastic_symmetrical_i_section, class_of_section, most_critical_class
from material import steel
from section_property.effective_length import effective_length_bending
from section_property.steel_table import ismb_table


class Angle:
    pass


class ISectionRolled:
    def __init__(self, name, country='indian', fy_Mpa=250):
        self.name = name
        self.country = country
        self.fy = steel.steel_yield_tensile_stress(grade_in_Mpa=fy_Mpa)[1]

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(section={self.name!r}, " \
               f"country={self.country!r}, " \
               f"details={self.all_geometrical_property})"

    @property
    def all_geometrical_property(self) -> dict:
        if self.country == 'indian':
            if self.name in ismb_table.keys():
                return {'unit': 'kg, meter',
                        'tot_height': ismb_table[self.name][0] / 1000,
                        'web_thk': ismb_table[self.name][4] / 1000,
                        'flange_width': ismb_table[self.name][1] / 1000,
                        'flange_thk': ismb_table[self.name][2] / 1000,
                        'area': ismb_table[self.name][5] / (100 ** 2),
                        'i_zz': ismb_table[self.name][7] / (100 ** 4),
                        'i_yy': ismb_table[self.name][8] / (100 ** 4),
                        'ze_zz': ismb_table[self.name][9] / (100 ** 3),
                        'ze_yy': ismb_table[self.name][10] / (100 ** 3),
                        'r_zz': ismb_table[self.name][11] / 100,
                        'r_yy': ismb_table[self.name][12] / 100}
            else:
                raise ValueError(f'section_name: {self.name} is not a valid SECTION-NAME for country_code: '
                                 f'{self.country}')
        else:
            raise ValueError(f'no such country_code exists: {self.country}')

    @property
    def zp_zz(self):
        return z_plastic_symmetrical_i_section(flange_width=self.all_geometrical_property['flange_width'],
                                               tf=self.all_geometrical_property['flange_thk'],
                                               tot_height=self.all_geometrical_property['tot_height'],
                                               tw=self.all_geometrical_property['web_thk'])[0]

    @property
    def zp_yy(self):
        return z_plastic_symmetrical_i_section(flange_width=self.all_geometrical_property['flange_width'],
                                               tf=self.all_geometrical_property['flange_thk'],
                                               tot_height=self.all_geometrical_property['tot_height'],
                                               tw=self.all_geometrical_property['web_thk'])[1]

    @property
    def d(self):
        return self.all_geometrical_property['tot_height'] - 2 * self.all_geometrical_property['flange_thk']

    @property
    def fyw(self):  # yield strength of the web
        return self.fy

    @property
    def shear_area(self):
        return self.all_geometrical_property['tot_height'] * self.all_geometrical_property['web_thk']

    def shear_buckling_coefficient_kv(self, c):  # clause 8.4.2.2
        if c > 0 and c / self.d < 1:
            return 4 + 5.35 / ((c / self.d) ** 2)
        elif c > 0 and c / self.d >= 1:
            return 5.35 + 4 / ((c / self.d) ** 2)
        elif c == 0:
            return 5.35

    def t_cre(self, kv):  # elastic critical shear stress, clause 8.4.2.2
        if kv is not None:
            u = steel.poisson_ratio_for_steel
            return kv * (math.pi ** 2) * steel.E / (
                    12 * (1 - u ** 2) * (self.d / self.all_geometrical_property['web_thk']) ** 2)

    @property
    def class_of_section(self):
        e_flange = (250 * (10 ** 6) / self.fy) ** 0.5
        e_web = e_flange
        flange_width = self.all_geometrical_property['flange_width']
        tf = self.all_geometrical_property['flange_thk']
        tw = self.all_geometrical_property['web_thk']
        tot_height = self.all_geometrical_property['tot_height']
        web_height = tot_height - 2 * tf

        effective_width_flange = (flange_width - tw) / 2
        effective_tk_flange = tf
        b_by_tf = effective_width_flange / effective_tk_flange

        effective_height_web = web_height
        effective_tk_web = tw
        d_by_tw = effective_height_web / effective_tk_web

        if b_by_tf <= 9.4 * e_flange:
            result_flange = class_of_section[0]
        elif 9.4 * e_flange < b_by_tf <= 10.5 * e_flange:
            result_flange = class_of_section[1]
        elif 10.5 * e_flange < b_by_tf <= 15.7 * e_flange:
            result_flange = class_of_section[2]
        else:
            result_flange = class_of_section[3]

        if d_by_tw <= 84 * e_web:
            result_web = class_of_section[0]
        elif 84 * e_web < d_by_tw <= 105 * e_web:
            result_web = class_of_section[1]
        elif 105 * e_web < d_by_tw <= 126 * e_web:
            result_web = class_of_section[2]
        else:
            result_web = class_of_section[3]
        result = [result_flange, result_web, most_critical_class([result_flange, result_web], high_value_critical=True)]
        return result[2]

    def m_cr(self, l_lt):
        e = steel.E
        i_yy = self.all_geometrical_property['i_yy']
        r_yy = self.all_geometrical_property['r_yy']
        tf = self.all_geometrical_property['flange_thk']
        hf = self.all_geometrical_property['tot_height'] - tf
        return ((math.pi ** 2) * e * i_yy * hf * (1 + (1 / 20) * ((l_lt / r_yy) / (hf / tf)) ** 2) ** 0.5) / (
                2 * l_lt ** 2)

    @property
    def a_lt(self):  # imperfection factor for bending check, clause 8.2.2
        return 0.21

    def web_buckling_susceptible(self, c):  # sections with webs susceptible to shear buckling before yielding,
        # clause 8.2.1.1, 8.4.2.1
        d = self.d
        tw = self.all_geometrical_property['web_thk']
        e = (250 * (10 ** 6) / self.fy) ** 0.5
        if c == 0 and d / tw > 67 * e:
            return True
        elif c > 0 and d / tw > 67 * e * (self.shear_buckling_coefficient_kv(c=c) / 5.35) ** 0.5:
            return True
        else:
            return False

    def shear_lag_effect(self, Lo):  # shear lag effects. clause 8.2.1.5
        bo = (self.all_geometrical_property['flange_width'] - self.all_geometrical_property['web_thk']) / 2
        # bi = False
        if bo:
            if bo > Lo / 20:
                return True
            else:
                return False
        # if bi:
        #     if bi > Lo / 10:
        #         return True
        #     else:
        #         return False


available_member_class = (ISectionRolled, Angle)


class DesignProperty:

    def __init__(self, name, ll_t=None, lat=None, cant=None, c=0.0):
        self.lat = lat
        self.cant = cant
        self.ll_t = effective_length_bending(length=ll_t, cant=self.cant)
        self.c = c
        if self.c < 0:
            raise ValueError(f"c can not be < 0. c: {self.c}")

        if not isinstance(name, available_member_class):
            raise ValueError(f"argument is not valid {available_member_class} object: {repr(name)}")
        self.name = name

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}: {self.name.__repr__()})"

    @property
    def fy(self) -> float:
        return self.name.fy

    @property
    def d(self) -> float:
        return self.name.d

    @property
    def area(self) -> float:
        return self.name.all_geometrical_property['area']

    @property
    def i_zz(self) -> float:
        return self.name.all_geometrical_property['i_zz']

    @property
    def i_yy(self) -> float:
        return self.name.all_geometrical_property['i_yy']

    @property
    def ze_zz(self) -> float:
        return self.name.all_geometrical_property['ze_zz']

    @property
    def ze_yy(self) -> float:
        return self.name.all_geometrical_property['ze_yy']

    @property
    def zp_zz(self) -> float:
        return self.name.zp_zz

    @property
    def zp_yy(self) -> float:
        return self.name.zp_yy

    @property
    def r_zz(self) -> float:
        return self.name.all_geometrical_property['r_zz']

    @property
    def r_yy(self) -> float:
        return self.name.all_geometrical_property['r_yy']

    @property
    def critical_class(self) -> float:
        return self.name.class_of_section

    @property
    def m_cr(self) -> float:
        return self.name.m_cr(l_lt=self.ll_t)

    @property
    def a_lt(self) -> float:
        return self.name.a_lt

    @property
    def web_buckling(self) -> bool:
        return self.name.web_buckling_susceptible(c=self.c)

    @property
    def shear_lag(self) -> bool:
        return self.name.shear_lag_effect(Lo=self.ll_t)

    @property
    def shear_area(self) -> float:
        return self.name.shear_area

    @property
    def fyw(self) -> float:
        return self.name.fyw

    @property
    def kv(self) -> float:
        return self.name.shear_buckling_coefficient_kv(c=self.c)

    @property
    def t_cre(self) -> float:
        return self.name.t_cre(kv=self.kv)


if __name__ == "__main__":
    section_name = ISectionRolled(name='ismb_100', country='indian', fy_Mpa=250)
    member_design_prop = DesignProperty(name=section_name, ll_t=7, lat=1, cant=0, c=0.0)
    print(section_name.__repr__())
    print(member_design_prop.__repr__())
