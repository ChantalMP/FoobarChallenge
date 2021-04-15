
'''
Don't Get Volunteered!
======================

As a henchman on Commander Lambda's space station, you're expected to be resourceful, smart, and a quick thinker.
It's not easy building a doomsday device and ordering the bunnies around at the same time, after all! In order to make sure that everyone is sufficiently
quick-witted, Commander Lambda has installed new flooring outside the henchman dormitories. It looks like a chessboard, and every morning and evening
you have to solve a new movement puzzle in order to cross the floor. That would be fine if you got to be the rook or the queen, but instead,
you have to be the knight. Worse, if you take too much time solving the puzzle, you get "volunteered" as a test subject for the LAMBCHOP doomsday device!

To help yourself get to and from your bunk every day, write a function called solution(src, dest) which takes in two parameters: the source square,
on which you start, and the destination square, which is where you need to land to solve the puzzle.  The function should return an integer representing
the smallest number of moves it will take for you to travel from the source square to the destination square using a chess knight's moves
(that is, two squares in any direction immediately followed by one square perpendicular to that direction, or vice versa, in an "L" shape).
Both the source and destination squares will be an integer between 0 and 63, inclusive, and are numbered like the example chessboard below:

-------------------------
| 0| 1| 2| 3| 4| 5| 6| 7|
-------------------------
| 8| 9|10|11|12|13|14|15|
-------------------------
|16|17|18|19|20|21|22|23|
-------------------------
|24|25|26|27|28|29|30|31|
-------------------------
|32|33|34|35|36|37|38|39|
-------------------------
|40|41|42|43|44|45|46|47|
-------------------------
|48|49|50|51|52|53|54|55|
-------------------------
|56|57|58|59|60|61|62|63|
-------------------------

-- Python cases --
Input:
solution.solution(0, 1)
Output:
    3

Input:
solution.solution(19, 36)
Output:
    1
'''

def nr_to_idx(nr):
    return (nr//8,nr%8)

def idx_to_nr(idx):
    return idx[0]*8 + idx[1]

def can_visit(src_idx, possible_moves):
    targets = []
    for move in possible_moves:
        target = (src_idx[0]+move[0], src_idx[1]+move[1])
        if target[0] > -1 and target[0] < 8 and target[1] > -1 and target[1] < 8:
            targets.append(target)

    return targets


def solution(src, dest):
    if src == dest:
        return 0
    possible_moves = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
    goal_idx = nr_to_idx(dest)

    visited = {}
    queue = [nr_to_idx(src)]
    visited[nr_to_idx(src)] = 0

    while len(queue) > 0:
        next = queue.pop(0)
        can_visit_moves = can_visit(next, possible_moves)
        for move in can_visit_moves:
            if move not in visited.keys():
                queue.append(move)
                visited[move] = visited[next]+1
                if move == goal_idx: #reached dest, give back used steps
                    return visited[move]

if __name__ == '__main__':
    print(solution(0, 0))