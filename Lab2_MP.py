from random import randint
from math import sqrt

y_max = (30 - 4) * 10
y_min = (20 - 4) * 10
x1_min = 15
x1_max = 45
x2_min = 30
x2_max = 80
m = 5


def get_r_kr(m):
    table_values = {2: 1.69, 6: 2, 8: 2.17, 10: 2.29, 12: 2.39, 15: 2.49, 20: 2.62}
    for i in range(len(table_values.keys())):
        if m == list(table_values.keys())[i]:
            return list(table_values.values())[i]
        if m > list(table_values.keys())[i]:
            less_than_m_key = list(table_values.keys())[i]
            less_than_m = list(table_values.values())[i]
            more_than_m_key = list(table_values.keys())[i + 1]
            more_than_m = list(table_values.values())[i + 1]
            return less_than_m + (more_than_m - less_than_m) * (m - less_than_m_key) / (
                    more_than_m_key - less_than_m_key)


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] * matrix[2][2] + matrix[0][1] * matrix[1][2] * matrix[2][0] + matrix[0][2] * \
           matrix[1][0] * matrix[2][1] - matrix[0][2] * matrix[1][1] * matrix[2][0] - matrix[0][1] * matrix[1][0] * \
           matrix[2][2] - matrix[0][0] * matrix[1][2] * matrix[2][1]

def main():
    global m
    list1 = [randint(y_min, y_max) for i in range(m)]
    list2 = [randint(y_min, y_max) for i in range(m)]
    list3 = [randint(y_min, y_max) for i in range(m)]

    average1 = sum(list1) / len(list1)
    average2 = sum(list2) / len(list2)
    average3 = sum(list3) / len(list3)

    disp1 = sum((i - average1) ** 2 for i in list1) / len(list1)
    disp2 = sum((i - average2) ** 2 for i in list2) / len(list2)
    disp3 = sum((i - average3) ** 2 for i in list3) / len(list3)

    osn_vidh = sqrt(2 * (2 * m - 2) / (m * (m - 4)))

    Fuv1 = disp1 / disp2 if disp1 >= disp2 else disp2 / disp1
    Fuv2 = disp2 / disp3 if disp2 >= disp3 else disp3 / disp2
    Fuv3 = disp1 / disp3 if disp1 >= disp3 else disp3 / disp1

    Quv1 = (m - 2) / m * Fuv1
    Quv2 = (m - 2)  / m * Fuv2
    Quv3 = (m - 2) / m * Fuv3

    Ruv1 = abs(Quv1 - 1) / osn_vidh
    Ruv2 = abs(Quv2 - 1) / osn_vidh
    Ruv3 = abs(Quv3 - 1) / osn_vidh

    Rkr = get_r_kr(m)

    print(" Y min = ", y_min, "\n", "Y max = ", y_max)

    print("\nЗначення факторів:")
    print(*list1, sep=' ')
    print(*list2, sep=' ')
    print(*list3, sep=' ')
    print('\nСереднє значення відгуку:')
    print(average1)
    print(average2)
    print(average3)
    print('\nДисперсії:')
    print(f'{disp1:.3f}')
    print(f'{disp2:.3f}')
    print(f'{disp3:.3f}')
    print('\nОсновне відхилення:')
    print(f'{osn_vidh:.3f}')
    print('\nПеревірка на однорідність:')
    print(f"\n{Ruv1:.3f}", '<' if Ruv1 < Rkr else '>', f'{Rkr:.3f}')
    print(f'\n{Ruv2:.3f}', '<' if Ruv2 < Rkr else '>', f'{Rkr:.3f}')
    print(f'\n{Ruv3:.3f}', '<' if Ruv3 < Rkr else '>', f'{Rkr:.3f}')

    if Ruv1 < Rkr and Ruv2 < Rkr and Ruv3 < Rkr:
        print('\nОднорідність підтверджується з ймовірністю 0.90\n')

        norm = [
            [-1, -1],
            [1, -1],
            [-1, 1]
        ]

        mx1 = sum(i[0] for i in norm) / 3
        mx2 = sum(i[1] for i in norm) / 3
        my = (average1 + average2 + average3) / 3
        a1 = sum(i[0] ** 2 for i in norm) / 3
        a2 = sum(i[0] * i[1] for i in norm) / 3
        a3 = sum(i[1] ** 2 for i in norm) / 3
        aa1 = sum(norm[i][0] * [average1, average2, average3][i] for i in range(len(norm))) / 3
        a22 = sum(norm[i][1] * [average1, average2, average3][i] for i in range(len(norm))) / 3
        matrix_b = [
            [1, mx1, mx2],
            [mx1, a1, a2],
            [mx2, a2, a3]
        ]
        matrix_b0 = [
            [my, mx1, mx2],
            [aa1, a1, a2],
            [a22, a2, a3]
        ]
        matrix_b1 = [
            [1, my, mx2],
            [mx1, aa1, a2],
            [mx2, a22, a3]
        ]
        matrix_b2 = [
            [1, mx1, my],
            [mx1, a1, aa1],
            [mx2, a2, a22]
        ]
        b0 = determinant(matrix_b0) / determinant(matrix_b)
        b1 = determinant(matrix_b1) / determinant(matrix_b)
        b2 = determinant(matrix_b2) / determinant(matrix_b)

        print('\nНормоване рівняння регресії:')

        for i in norm:
            print(
                f'y = b0 + b1 * x1 + b2 * x2 = {b0:.3f} + {b1:.3f} * {i[0]:2} + {b2:.3f} * {i[1]:2}'
                f' = {b0 + b1 * i[0] + b2 * i[1]:.3f}')

        x1 = (x1_max - x1_min) / 2
        x2 = (x2_max - x2_min) / 2
        x10 = (x1_max + x1_min) / 2
        x20 = (x2_max + x2_min) / 2

        a_0 = b0 - b1 * (x10 / x1) - b2 * (x20 / x2)
        aa1 = b1 / x1
        aa2 = b2 / x2

        print('\nНатуралізоване рівняння регресії:')
        print(
            f'y = a0 + a1 * x1 + a2 * x2 = {a_0:.3f} + {aa1:.3f} * {x1_min:3} + {aa2:.3f} * {x2_min:3}'
            f' = {a_0 + aa1 * x1_min + aa2 * x2_min:.3f}')
        print(
            f'y = a0 + a1 * x1 + a2 * x2 = {a_0:.3f} + {aa1:.3f} * {x1_max:3} + {aa2:.3f} * {x2_min:3}'
            f' = {a_0 + aa1 * x1_max + aa2 * x2_min:.3f}')
        print(
            f'y = a0 + a1 * x1 + a2 * x2 = {a_0:.3f} + {aa1:.3f} * {x1_min:3} + {aa2:.3f} * {x2_max:3}'
            f' = {a_0 + aa1 * x1_min + aa2 * x2_max:.3f}')

    else:
        print('\nОднорідність не підтвердилася, підвищуємо m на 1\n')
        m += 1
        main()


main()
