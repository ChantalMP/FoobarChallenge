import fractions
from fractions import Fraction

'''
Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing,
begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach,
not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample.
You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random,
the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state
(which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the
ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and
return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state,
then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the
ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state.
The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

'''

'''
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
'''

def compute_prob_matrix_parts(m, terminal_states, non_terminal_states):
    #transform to probs
    last_transient_state = 0
    for i in range(len(m)):
        row = m[i]
        row_sum = sum(row)
        if row_sum != 0:
            for j in range(len(row)):
                m[i][j] = Fraction(row[j],row_sum)
            last_transient_state +=1
        else:
            m[i][i] = Fraction(1,1)

    # get Q and R
    Q = []
    R = []
    for row in non_terminal_states:
        new_row_Q = []
        new_row_R = []
        for column_Q in non_terminal_states:
            new_row_Q.append(m[row][column_Q])

        for column_R in terminal_states:
            new_row_R.append(m[row][column_R])

        Q.append(new_row_Q)
        R.append(new_row_R)

    return m, Q, R

def identity_matrix(n):
    IdM = [([0]*n) for _ in range(n)]
    for idx in range(n):
        IdM[idx][idx] = Fraction(1,1)
    return IdM

def matrix_diff(m1, m2):
    for i in range(len(m1)):
        for j in range(len(m1[0])):
            m1[i][j] = m1[i][j] - m2[i][j]
    return m1

def zeros_matrix(rows, cols):
    A = []
    for i in range(rows):
        A.append([])
        for j in range(cols):
            A[-1].append(Fraction(0,1))

    return A

def matrix_multiply(A,B):
    rowsA = len(A)
    colsA = len(A[0])

    rowsB = len(B)
    colsB = len(B[0])

    if colsA != rowsB:
        print('Number of A columns must equal number of B rows.')

    C = zeros_matrix(rowsA, colsB)

    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total

    return C

def copy_matrix(M):
    rows = len(M)
    cols = len(M[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(rows):
            MC[i][j] = M[i][j]

    return MC

def invert_matrix(A):

    n = len(A)
    AM = copy_matrix(A)
    I = identity_matrix(n)
    IM = copy_matrix(I)

    # Section 3: Perform row operations
    indices = list(range(n))  # to allow flexible row referencing ***
    for fd in range(n):  # fd stands for focus diagonal
        fdScaler = Fraction(1,1) / AM[fd][fd]
        # FIRST: scale fd row with fd inverse.
        for j in range(n):  # Use j to indicate column looping.
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler
        # SECOND: operate on all rows except fd row as follows:
        for i in indices[0:fd] + indices[fd + 1:]:
            # *** skip row with fd in it.
            crScaler = AM[i][fd]  # cr stands for "current row".
            for j in range(n):
                # cr - crScaler * fdRow, but one element at a time.
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]

    return IM

def compute_fundamental_matrix(Q):
    id_matrix = identity_matrix(len(Q))
    diff = matrix_diff(id_matrix, Q)
    N = invert_matrix(diff)
    return N

def reduce_fractions(numerators, denominators):
    numerators_new = []
    denominators_new = []
    for numerator, denominator in zip(numerators, denominators):
        a = numerator
        b = denominator
        while a!=b and a!=1 and b!=1:
            a, b = min(a, b), abs(a-b)
        if a==b:
            numerator = numerator//a
            denominator = denominator//a
        numerators_new.append(numerator)
        denominators_new.append(denominator)
    return numerators_new, denominators_new

def get_lcm_fractions(rationals):
    numerators = [r.numerator for r in rationals]
    denominators = [r.denominator for r in rationals]
    numerators, denominators = reduce_fractions(numerators, denominators)

    lcm = denominators[0]
    for d in denominators[1:]:
        lcm = lcm // fractions.gcd(lcm, d) * d

    result = []
    for i in range(len(denominators)):
        ratio = lcm / denominators[i]
        numerator = numerators[i]*ratio
        result.append(int(numerator))

    result.append(lcm)

    return result

def solution(m):
    terminal_states = []
    non_terminal_states = []
    for idx, row in enumerate(m):
        if sum(row) == 0:
            terminal_states.append(idx)
        else:
            non_terminal_states.append(idx)

    if len(terminal_states) == 1:
        return [1, 1]

    m,Q,R = compute_prob_matrix_parts(m, terminal_states, non_terminal_states)
    #(I -q)-1
    N = compute_fundamental_matrix(Q)
    B = matrix_multiply(N, R)


    result_probs = [B[0][end] for end in range(len(B[0]))]
    result = get_lcm_fractions(result_probs)
    return result

if __name__ == '__main__':
    print(solution([
        [0, 0, 0],
        [1, 0, 1],
        [0, 0, 0]
        ]))

    print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
