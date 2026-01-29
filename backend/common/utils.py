import math


def calculate_emi(principal, annual_rate, tenure):

    r = annual_rate / (12 * 100)

    emi = (principal * r * pow(1 + r, tenure)) / (pow(1 + r, tenure) - 1)

    return round(emi, 2)
