# PYTHON 2.7 SANDBOX

# google foobar level 3 challenge 1
# https://brilliant.org/wiki/absorbing-markov-chains/

# matrix rules
# row-axis: from
# col-axis: to

# use absorbing markov chains and fraction library
# to return denominator and numberator

from fractions import Fraction

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


def normalize(m):
    n = []
    for i, row in enumerate(m):
        if any(row):
            n.append([Fraction(x, sum(row)) if x != 0 else 0 for x in row])
        else:
            n.append([0 for i in xrange(len(row))])
    return n


def num_transients(m):
    for i, row in enumerate(m):
        if any(row):
            continue
        else:
            return i


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
    c = []
    for i in xrange(len(a)):
        row = []
        for j in xrange(len(a[i])):
            row.append(a[i][j] - b[i][j])
        c.append(row)
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


def solution(m):
    m = normalize(m)
    Q, R = find_q_r(m)
    N = inverse(subtract(identity(len(Q)), Q))
    M = multiply(N, R)

    prob_distribution = M[0]
    denominator = max([x.denominator for x in prob_distribution])
    answer = [int(x*denominator) for x in prob_distribution]
    answer.append(denominator)
    return answer


m = [[0, 1, 0, 0, 0, 1],
     [4, 0, 0, 3, 2, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0]]

print(solution(m))
