import numpy as np
def create_four_equidistant_points(p1, p2):
    t_values = np.linspace(0, 1, 4)
    return [(p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])) for t in t_values]

print(create_four_equidistant_points([0, 0], [100, 100]))
