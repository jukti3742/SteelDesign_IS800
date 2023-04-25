class_of_section = ["plastic", "compact", "semi_compact", "slender"]


def most_critical_class(elements: list, high_value_critical=True):
    global class_of_section
    element_hierarchy = {
        1: class_of_section[0],
        2: class_of_section[1],
        3: class_of_section[2],
        4: class_of_section[3]
    }
    num_list = [num for num, words in filter(lambda item: item[1] in elements, element_hierarchy.items())]
    if high_value_critical:
        return element_hierarchy[max(num_list)]
    else:
        return element_hierarchy[min(num_list)]


def z_plastic_symmetrical_i_section(flange_width, tf, tot_height, tw):
    h = tot_height
    b = flange_width
    hw = h - 2 * tf
    zp_xx = (b * h ** 2 / 4) - (((b - tw) * hw ** 2) / 4)
    zp_yy = (tf * b ** 2 / 2) + (hw * tw ** 2 / 4)
    return zp_xx, zp_yy


def buckling_class_factor(value):
    if value == 'a':
        return 0.21
    elif value == 'b':
        return 0.34
    elif value == 'c':
        return 0.49
    elif value == 'd':
        return 0.76
    else:
        raise ValueError('buckling class shall be a, b, c, or d. Refer Table 7')


if __name__ == "__main__":
    print(most_critical_class(['plastic', 'compact']))
