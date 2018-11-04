distance = 3.7
delta = 1.2


def triangle(position, x0, x1, x2, clip):
    value = 0.0
    if position >= x0 and position <= x1:
        value = (position - x0)/(x1 - x0)
    elif position >= x1 and position <= x2:
        value = (x2-position)/(x1-x0)
    if value > clip:
        value = clip
    return value


def grade(position, x0, x1, clip):
    value = 0.0
    if position >= x1:
        value = 1.0
    elif position <= x0:
        value = 0.0
    else:
        value = (position - x0)/(x1 - x0)
    if value > clip:
        value = clip
    return value


def reverse_grade(position, x0, x1, clip):
    value = 0.0
    if position <= x0:
        value = 1.0
    elif position >= x1:
        value = 0.0
    else:
        value = (x1 - position)/(x1 - x0)
    if value > clip:
        value = clip
    return value


def main():
    verysmall = reverse_grade(distance, 0, 2.5, 1)
    small = triangle(distance, 1.5, 3, 4.5, 1)
    perfect = triangle(distance, 3.5, 5, 6.5, 1)
    big = triangle(distance, 5.5, 7, 8.5, 1)
    verybig = grade(distance, 7.5, 10, 1)

    shrinkingfast = reverse_grade(delta, -5, -2.5, 1)
    shrinking = triangle(delta, -3.5, -2, -0.5, 1)
    stable = triangle(delta, -1.5, 0, 1.5, 1)
    growing = triangle(delta, 0.5, 2, 3.5, 1)
    growingfast = grade(delta, 2.5, 5, 1)

    none = min(small, growing)
    slowdown = min(small, stable)
    speedup = min(perfect, growing)
    floorit = min(verybig, max(1-growing, 1-growingfast))
    breakhard = verysmall

    cog = ((-1 + 0 + 1) * none + (-6-5-4-3-2) * slowdown + (3+4+5+6) *
           speedup + (-10 - 8) * breakhard + (8 + 10) * floorit) / \
        (3*none + slowdown * 5 + speedup * 4 + 2 * breakhard + 2 * floorit)

    print(cog)


if __name__ == '__main__':
    main()
