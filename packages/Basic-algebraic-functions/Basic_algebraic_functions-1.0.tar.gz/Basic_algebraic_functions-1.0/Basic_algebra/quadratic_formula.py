def quadratic_formula():
    from math import sqrt

    try:
        a = int(input("a =  "))
        b = int(input("b =  "))
        c = int(input("c =  "))
    except ValueError or NameError:
        print("Please enter a number")

    D = b ** 2 - 4 * a * c

    if D < 0:
        print("The root is negative. There are no real solutions.")
    elif D == 0:
        x = (-b) / (2 * a)
        print(x)
    else:
        x1 = (-b + sqrt(D)) / (2 * a)
        x2 = (-b - sqrt(D)) / (2 * a)
        print(f"x = {x1} V x = {x2}")
