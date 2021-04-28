import fractions
from collections import defaultdict

'''
Distract the Trainers
=====================

The time for the mass escape has come, and you need to distract the bunny trainers so that the workers can make it out! Unfortunately for you,
they're watching the bunnies closely. Fortunately, this means they haven't realized yet that the space station is about to explode due to the
destruction of the LAMBCHOP doomsday device. Also fortunately, all that time you spent working as first a minion and then a henchman means that
you know the trainers are fond of bananas. And gambling. And thumb wrestling.

The bunny trainers, being bored, readily accept your suggestion to play the Banana Games.

You will set up simultaneous thumb wrestling matches. In each match, two trainers will pair off to thumb wrestle. The trainer with fewer bananas will
bet all their bananas, and the other trainer will match the bet. The winner will receive all of the bet bananas. You don't pair off trainers with the
same number of bananas (you will see why, shortly). You know enough trainer psychology to know that the one who has more bananas always gets
over-confident and loses. Once a match begins, the pair of trainers will continue to thumb wrestle and exchange bananas, until both of them have the
same number of bananas. Once that happens, both of them will lose interest and go back to supervising the bunny workers, and you don't want THAT to happen!

For example, if the two trainers that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2
(the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas).
At that point they stop and get back to training bunnies.

How is all this useful to distract the bunny trainers? Notice that if the trainers had started with 1 and 4 bananas, then they keep thumb wrestling!
1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each trainer starts with,
returns the fewest possible number of bunny trainers that will be left to watch the workers. Element i of the list will be the number of bananas t
hat trainer i (counting from 0) starts with.

The number of trainers will be at least 1 and not more than 100, and the number of bananas each trainer starts with will be a positive integer
no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.

'''
# trainer 1: N bananas, trainer 2: M bananas -> N < M -> trainer 2 looses -> trainer one gets N of M bananas -> repeat until N = M
# goal: max num of trainers in infinite loop

'''
-- Python cases --
Input:
solution.solution(1,1)
Output:
    2

Input:
solution.solution([1, 7, 3, 21, 13, 19])
Output:
    0
'''

#uneven sum -> has to be infinit
#one number half of other -> infinit
def infinit(b1, b2):
    #reduce
    gcd = fractions.gcd(b1,b2)
    b1 = b1 / gcd
    b2 = b2 / gcd
    if b1 == b2:
        return False
    elif ((b1 + b2) & (b1 + b2 - 1)) == 0:
        return False
    else:
        return True

def solution(banana_list):
    guard_matches = defaultdict(list)
    guard_match_count = defaultdict(int)
    for idx, b1 in enumerate(banana_list):
        for idx2, b2 in enumerate(banana_list):
            if b1 < b2:
                if infinit(b1,b2):
                    guard_matches[idx].append(idx2)
                    guard_matches[idx2].append(idx)
                    guard_match_count[idx] += 1
                    guard_match_count[idx2] += 1

    guards_ordered = sorted(guard_match_count, key=guard_match_count.get)
    guards_selected = []

    while len(guards_ordered) > 0:
        current_guard = guards_ordered[0]
        found = False
        for guard in guards_ordered[1:]:
            if guard in guard_matches[current_guard]:
                guards_ordered.pop(0)
                guards_ordered.remove(guard)
                guards_selected.append(current_guard)
                guards_selected.append(guard)
                for rest_guard in guards_ordered:
                    if guard_matches[rest_guard]:
                        if guard in guard_matches[rest_guard]:
                            guard_matches[rest_guard].remove(guard)
                            guard_match_count[rest_guard] -= 1
                        if current_guard in guard_matches[rest_guard]:
                            guard_matches[rest_guard].remove(current_guard)
                            guard_match_count[rest_guard] -= 1

                guards_ordered = sorted(guards_ordered, key=guard_match_count.get)
                found = True
                break

        if not found:
            guards_ordered.pop(0)

    return len(banana_list) - len(guards_selected)


if __name__ == '__main__':
    print(solution([1, 7, 3, 21, 13, 19]))