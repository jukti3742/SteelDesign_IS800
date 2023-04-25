E = 2 * 10 ** (5 + 6)  # unit: N/m2

poisson_ratio_for_steel = 0.3  # poisson's ratio for steel


def steel_yield_tensile_stress(grade_in_Mpa, plate_tk_mm=12):
    if grade_in_Mpa == 250 and plate_tk_mm < 20:
        return [410 * (10 ** 6), 250 * (10 ** 6)]
    elif grade_in_Mpa == 250 and 20 <= plate_tk_mm <= 40:
        return [410 * (10 ** 6), 240 * (10 ** 6)]
    elif grade_in_Mpa == 250 and plate_tk_mm > 40:
        return [410 * (10 ** 6), 230 * (10 ** 6)]

    elif grade_in_Mpa == 275 and plate_tk_mm < 20:
        return [430 * (10 ** 6), 275 * (10 ** 6)]
    elif grade_in_Mpa == 275 and 20 <= plate_tk_mm <= 40:
        return [430 * (10 ** 6), 265 * (10 ** 6)]
    elif grade_in_Mpa == 275 and plate_tk_mm > 40:
        return [430 * (10 ** 6), 255 * (10 ** 6)]

    elif grade_in_Mpa == 300 and plate_tk_mm < 20:
        return [440 * (10 ** 6), 300 * (10 ** 6)]
    elif grade_in_Mpa == 300 and 20 <= plate_tk_mm <= 40:
        return [440 * (10 ** 6), 290 * (10 ** 6)]
    elif grade_in_Mpa == 300 and plate_tk_mm > 40:
        return [440 * (10 ** 6), 280 * (10 ** 6)]

    elif grade_in_Mpa == 350 and plate_tk_mm < 20:
        return [490 * (10 ** 6), 350 * (10 ** 6)]
    elif grade_in_Mpa == 350 and 20 <= plate_tk_mm <= 40:
        return [490 * (10 ** 6), 330 * (10 ** 6)]
    elif grade_in_Mpa == 350 and plate_tk_mm > 40:
        return [490 * (10 ** 6), 320 * (10 ** 6)]

    elif grade_in_Mpa == 410 and plate_tk_mm < 20:
        return [540 * (10 ** 6), 410 * (10 ** 6)]
    elif grade_in_Mpa == 410 and 20 <= plate_tk_mm <= 40:
        return [540 * (10 ** 6), 390 * (10 ** 6)]
    elif grade_in_Mpa == 410 and plate_tk_mm > 40:
        return [540 * (10 ** 6), 380 * (10 ** 6)]

    elif grade_in_Mpa == 450 and plate_tk_mm < 20:
        return [570 * (10 ** 6), 450 * (10 ** 6)]
    elif grade_in_Mpa == 450 and 20 <= plate_tk_mm <= 40:
        return [570 * (10 ** 6), 430 * (10 ** 6)]
    elif grade_in_Mpa == 450 and plate_tk_mm > 40:
        return [570 * (10 ** 6), 420 * (10 ** 6)]

    elif grade_in_Mpa == 550 and plate_tk_mm < 20:
        return [650 * (10 ** 6), 550 * (10 ** 6)]
    elif grade_in_Mpa == 550 and 20 <= plate_tk_mm <= 40:
        return [650 * (10 ** 6), 530 * (10 ** 6)]
    elif grade_in_Mpa == 550 and plate_tk_mm > 40:
        return [650 * (10 ** 6), 520 * (10 ** 6)]

    elif grade_in_Mpa == 600 and plate_tk_mm < 20:
        return [730 * (10 ** 6), 600 * (10 ** 6)]
    elif grade_in_Mpa == 600 and 20 <= plate_tk_mm <= 40:
        return [730 * (10 ** 6), 580 * (10 ** 6)]
    elif grade_in_Mpa == 600 and plate_tk_mm > 40:
        return [730 * (10 ** 6), 570 * (10 ** 6)]

    elif grade_in_Mpa == 650 and plate_tk_mm < 20:
        return [780 * (10 ** 6), 650 * (10 ** 6)]
    elif grade_in_Mpa == 650 and 20 <= plate_tk_mm <= 40:
        return [780 * (10 ** 6), 630 * (10 ** 6)]
    elif grade_in_Mpa == 650 and plate_tk_mm > 40:
        return [780 * (10 ** 6), 620 * (10 ** 6)]

    else:
        raise ValueError(f"Grade is not valid: {grade_in_Mpa}. Available grades: [250, 275, 300, 350, 410, 450, 550, "
                         f"600, 650]")


if __name__ == "__main__":
    print(steel_yield_tensile_stress(grade_in_Mpa=350, plate_tk_mm=45))
