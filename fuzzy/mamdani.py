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
    verySmall = reverse_grade(distance, 1, 2.5, 1)
    small = triangle(distance, 1.5, 3, 4.5, 1)
    perfect = triangle(distance, 3.5, 5, 6.5, 1)
    big = triangle(distance, 5.5, 7, 8.5, 1)
    veryBig = grade(distance, 7.5, 9, 1)

    shrinkingFast = reverse_grade(delta, -4, -2.5, 1)
    shrinking = triangle(delta, -3.5, -2, -0.5, 1)
    stable = triangle(delta, -1.5, 0, 1.5, 1)
    growing = triangle(delta, 0.5, 2, 3.5, 1)
    growingFast = grade(delta, 2.5, 4, 1)


if __name__ == '__main__':
    main()
