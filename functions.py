# PYTHON 2.7 SANDBOX

# google foobar level 3 challenge 1
# https://brilliant.org/wiki/absorbing-markov-chains/
# https://github.com/mkutny/absorbing-markov-chains/blob/master/amc.py

# matrix rules
# row-axis: from
# col-axis: to

# use absorbing markov chains and fraction library
# to return denominator and numberator

from fractions import Fraction, gcd

# def print_matrix(m):
#     print("== Matix Start ==")
#     for row in m:
#         print(row)
#     print("== Matrix End ==")


def print_matrix(m):
    print("== Matix Start ==")
    for row in m:
        print "[",
        for num in row:
            print num,
        print("]")
    print("== Matrix End ==")


def swap(m, i, j):
    # col swap
    for k in xrange(len(m)):
        m[k][i], m[k][j] = m[k][j], m[k][i]
        # temp = m[k][i]
        # m[k][i] = m[k][j]
        # m[k][j] = temp
    # row swap
    for k in xrange(len(m)):
        m[i][k], m[j][k] = m[j][k], m[i][k]
        # temp = m[i][k]
        # m[i][k] = m[j][k]
        # m[j][k] = temp
    return m


def sort(m):
    for i, row in enumerate(m):
        if not any(row):
            # search for none zero row and swap until i
            # else end swapping if no non zero row exists
            swap_num = 0
            for j in range(i+1, len(m)):
                if any(m[j]):
                    swap_num = j
                    break
            while swap_num > i:
                m = swap(m, swap_num-1, swap_num)
                swap_num -= 1
    return m


def normalize(m):
    n = []
    for row in m:
        if any(row):
            n.append([Fraction(x, sum(row)) if x != 0 else 0 for x in row])
        else:
            n.append(row)
    return n


def num_transients(m):
    for i, row in enumerate(m):
        if not any(row):
            return i
    return 0


def find_q_r(m):
    t = num_transients(m)
    q = []
    r = []
    for i in xrange(t):
        q.append(m[i][:t])
        r.append(m[i][t:])
    return q, r


def identity(t):
    I = [[0 for i in xrange(t)] for j in xrange(t)]
    for i, j in zip(range(t), range(t)):
        I[i][j] = 1
    return I


def subtract(a, b):
    c = [[0 for j in xrange(len(a))] for i in xrange(len(a[0]))]
    for i in xrange(len(a)):
        for j in xrange(len(a[i])):
            c[i][j] = a[i][j] - b[i][j]
    return c

# def transpose(m):
#     n = [[] for i in xrange(len(m))]
#     for i in xrange(len(m)):
#         for j in xrange(len(m[i])):
#             n[j].append(m[i][j])
#     return n


def minor(m, i, j):
    return [row[:j] + row[j+1:] for row in m[:i]+m[i+1:]]


def determinant(m):
    if len(m) == 2:
        return m[0][0]*m[1][1] - m[0][1]*m[1][0]
    d = 0
    for c in xrange(len(m)):
        d += ((-1)**c)*m[0][c]*determinant(minor(m, 0, c))
    return d


def inverse(m):
    d = determinant(m)
    # if len(m) == 1: return [[Fraction(m[0][0].denominator, m[0][0].numerator if m[0][0].numerator != 0 else 1)]]
    if len(m) == 2:
        return [[Fraction(m[1][1], d), Fraction(-1*m[0][1], d)],
                [Fraction(-1*m[1][0], d), Fraction(m[0][0], d)]]
    n = [[None for i in xrange(len(m))] for i in xrange(len(m))]
    for i in xrange(len(m)):
        for j in xrange(len(m[i])):
            cofactor = ((-1)**(i+j))*determinant(minor(m, j, i))
            n[i][j] = Fraction(cofactor, d) if cofactor != 0 else 0
    return n


def multiply(a, b):
    c = [[None for i in xrange(len(b[0]))] for j in xrange(len(a))]
    for i in xrange(len(a)):
        for j in xrange(len(b[0])):
            row = a[i]
            col = []
            for k in xrange(len(b)):
                col.append(b[k][j])
            c[i][j] = sum([x*y for x, y in zip(row, col)])
    return c


def lcm(ls):
    return reduce(lambda a, b: (a*b)//gcd(a, b), ls)


def solution(m):
    if len(m) == 1 and len(m[0]) == 1 and m[0][0] == 0:
        return [1, 1]
    m = sort(m)
    m = normalize(m)
    Q, R = find_q_r(m)
    I = identity(len(Q))
    N = inverse(subtract(I, Q))
    M = multiply(N, R)

    prob_dist = M[0]
    denominator = lcm([x.denominator for x in prob_dist])
    answer = [int(x*denominator) for x in prob_dist] + [denominator]
    return answer


# m = [[0,1,0,0,0,1,0,0,0,0],
#      [4,0,0,3,2,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0]]

# m = [[0,1,0,0,0,1],
#      [4,0,0,3,2,0],
#      [0,0,0,0,0,0],
#      [0,0,0,0,0,0],
#      [0,0,0,0,0,0],
#      [0,0,0,0,0,0]]

# m = [[0,2,1,0,0],
#      [0,0,0,3,4],
#      [0,0,0,0,0],
#      [0,0,0,0,0],
#      [0,0,0,0,0]]

# m = [[1,1,1,1],
#      [0,0,0,0],
#      [0,0,0,0],
#      [1,2,3,4]]

# m = [[1,2,3],
#      [0,0,0],
#      [3,2,1]]

# m = [[3,4],
#      [0,0]]

m = [[0]]

# m = [[1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# m = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
#      [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
#      [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
#      [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
#      [1, 1, 1, 0, 1, 0, 1, 0, 1, 0]]

print(solution(m))
# print_matrix(normalize(m))
# print_matrix(sort(m))
# print(num_transients(m))
# Q, R = find_q_r(normalize(sort(m)))
# print_matrix(Q)
# print_matrix(R)
# I = identity(1)
# print_matrix(I)
# N = inverse(subtract(I, Q))
# print_matrix(N)
# print_matrix(multiply(N, R))
