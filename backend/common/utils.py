def calculate_emi(principal, annual_rate, tenure):
    principal = float(principal)
    annual_rate = float(annual_rate)
    tenure = int(tenure)
    if principal <= 0:
        raise ValueError("principal must be greater than zero")
    if tenure <= 0:
        raise ValueError("tenure must be greater than zero")
    if annual_rate < 0:
        raise ValueError("annual_rate must not be negative")

    r = annual_rate / (12 * 100)
    if r == 0:
        return round(principal / tenure, 2)

    emi = (principal * r * pow(1 + r, tenure)) / (pow(1 + r, tenure) - 1)

    return round(emi, 2)
