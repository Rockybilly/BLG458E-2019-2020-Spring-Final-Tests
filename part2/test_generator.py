import random
from collections import deque

SUITS = {
     "c":0,
     "d":1,
     "h":1,
     "s":0
         }

RANKS = {
    "1":11,
    "2":2,
    "3":3,
    "4":4,
    "5":5,
    "6":6,
    "7":7,
    "8":8,
    "9":9,
    "t":10,
    "j":10,
    "q":10,
    "k":10,
}

def all_same_color(lst):
    n = -1
    for i in lst:
        if n == SUITS[i[0]] or n == -1:
            n = SUITS[i[0]]
        else:
            return False
    return True

def score(lst, goal):
    s = sum(RANKS[x[1]] for x in lst)
    pre = 3*(s - goal) if s > goal else goal - s
    return pre // 2 if all_same_color(lst) else pre

init_string = """- init:
    run: rm -f part2 part2.o part2.hi
    visible: false
- compile:
    run: ghc part2.hs -o part2
    blocker: true
"""

close_string = """- cleanup:
    run: rm -f part2 part2.o part2.hi
    visible: false
"""

test_file = open("part2.yaml", "w+")
test_file.write(init_string)

test_count = 10

for test_number in range(1, test_count + 1):
    deck_size = random.randrange(2, 10)
    random_deck = deque()
    goal = random.randrange(10, 50)

    for _ in range(deck_size):
        s = random.choice(list(SUITS.keys()))
        r = random.choice(list(RANKS.keys()))
        random_deck.append(s + r)


    draw_count = random.randrange(1, deck_size)
    discard_count = random.randrange(0, deck_size // 2)

    move_probability_list = ["d", "d", "d", "d", "d", "d", "r"]

    hand = []
    error = False
    moves = []
    #print(random_deck)

    test_file.write(f"- case_{test_number}:\n")
    test_file.write("    run: ./part2\n")
    test_file.write("    script:\n")
    test_file.write('      - expect: "Enter cards:"\n')

    for card in random_deck:
        test_file.write(f'      - send: "{card}"\n')
    test_file.write('      - send: "."\n')
    test_file.write('      - expect: "Enter moves:"\n')

    while draw_count + discard_count > 0:
        if draw_count == 0: move = "r"
        elif discard_count == 0: move = "d"
        else: move = random.choice(move_probability_list)

        if move == "d":
            draw_count -= 1
            hand.append(random_deck.popleft())
            moves.append("d")
        elif move == "r":
            discard_count -= 1
            if hand:
                discarded = random.choice(hand)
                moves.append("r" + discarded)

                if discarded in hand:
                    hand.remove(discarded)
                else:
                    error = True
                    break
            else:
                moves.append("rc1")
                error = True
                break

    print(goal, error, moves, score(hand, goal))

    for move in moves:
        test_file.write(f'      - send: "{move}"\n')

    test_file.write('      - send: "."\n')
    test_file.write('      - expect: "Enter goal:"\n')
    test_file.write(f'      - send: "{goal}"\n')
    
    if error:
        test_file.write('      - expect: "part2: card not in list"\n')
        test_file.write('      - expect: _EOF_\n')
        test_file.write("    exit: 1\n")
    else:
        test_file.write(f'      - expect: "Score: {score(hand, goal)}"\n')
        test_file.write('      - expect: _EOF_\n')
    


test_file.write(close_string)
test_file.close()