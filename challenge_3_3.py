'''
Bomb, Baby!
===========

You're so close to destroying the LAMBCHOP doomsday device you can taste it! But in order to do so, you need to deploy special self-replicating bombs
designed for you by the brightest scientists on Bunny Planet. There are two types: Mach bombs (M) and Facula bombs (F). The bombs, once released into
the LAMBCHOP's inner workings, will automatically deploy to all the strategic points you've identified and destroy them at the same time.

But there's a few catches. First, the bombs self-replicate via one of two distinct processes:
Every Mach bomb retrieves a sync unit from a Facula bomb; for every Mach bomb, a Facula bomb is created;
Every Facula bomb spontaneously creates a Mach bomb.

For example, if you had 3 Mach bombs and 2 Facula bombs, they could either produce 3 Mach bombs and 5 Facula bombs, or 5 Mach bombs and 2 Facula bombs.
The replication process can be changed each cycle.

Second, you need to ensure that you have exactly the right number of Mach and Facula bombs to destroy the LAMBCHOP device. Too few, and the device might survive.
Too many, and you might overload the mass capacitors and create a singularity at the heart of the space station - not good!

And finally, you were only able to smuggle one of each type of bomb - one Mach, one Facula - aboard the ship when you arrived, so that's all you have to start with.
(Thus it may be impossible to deploy the bombs to destroy the LAMBCHOP, but that's not going to stop you from trying!)

You need to know how many replication cycles (generations) it will take to generate the correct amount of bombs to destroy the LAMBCHOP.
Write a function solution(M, F) where M and F are the number of Mach and Facula bombs needed. Return the fewest number of generations (as a string)
that need to pass before you'll have the exact number of bombs necessary to destroy the LAMBCHOP, or the string "impossible" if this can't be done!
M and F will be string representations of positive integers no larger than 10^50. For example, if M = "2" and F = "1", one generation would need to pass,
so the solution would be "1". However, if M = "2" and F = "4", it would not be possible.
'''

'''
-- Python cases --
Input:
solution.solution('4', '7')
Output:
    4

Input:
solution.solution('2', '1')
Output:
    1
'''

def step_M(state):
    return (state[0], state[1]+state[0])

def step_F(state):
    return (state[0]+state[1], state[1])

def helper(state, cycles, x,y):
    # terminate
    if state[0] == x and state[1] == y:
        return cycles

    elif state[0] > x or state[1] > y:
        return 10^50 +1

    #else investigate both paths
    state_M = step_M(state)
    state_F = step_F(state)

    return min(helper(state_M, cycles+1, x, y),helper(state_F, cycles+1, x, y))

def solution_naive(x,y):
    start_state = (1,1)
    init_cycles = 0

    return str(helper(start_state, init_cycles, int(x), int(y)))

def solution(x,y):
    x = int(x)
    y = int(y)
    cycles = 0
    while True:
        if x == 1 and y == 1:
            return str(cycles)
        elif x < 1 or y < 1:
            return 'impossible'
        if x < y:
            steps = y//x
            if x == 1:
                steps-=1
            y = y - steps*x
            cycles += steps
        else:
            steps = x // y
            if y == 1:
                steps-=1
            x = x - steps * y
            cycles += steps

if __name__ == '__main__':
    print(solution('4', '7'))