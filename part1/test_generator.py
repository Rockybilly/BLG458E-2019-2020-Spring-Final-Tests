import random
import part1

init_string = """- init:
    run: rm -f part1 part1.o part1.hi
    visible: false
- compile:
    run: ghc part1.hs -o part1
    blocker: true
"""

close_string = """- cleanup:
    run: rm -f part1 part1.o part1.hi
    visible: false
"""

functions_tested = ["sundays1", "sundays1tr", "sundays2"]

test_count = 10
test_file = open("part1.yaml", "w+")

test_file.write(init_string)

for i in range(test_count):
    case_number = i * 3 + 1
    start = random.randrange(0, 1001)
    end = random.randrange(1001, 2021)

    result = part1.sundays1(start, end)
    result2 = part1.sundays2(start, end)
    result3 = part1.sundays3(start, end)

    if not (result == result2 == result3):
        raise Exception("The supplied part1 python code is unreliable.")

    for j, func in enumerate(functions_tested):
        test_file.write(f"- case_{case_number + j}:\n")
        test_file.write("    run: ./part1\n")
        test_file.write("    script:\n")
        test_file.write(f'      - send: "{func} {start} {end}"\n')
        test_file.write(f'      - expect: "{result}"\n')
        test_file.write("      - expect: _EOF_\n")


test_file.write(close_string)
test_file.close()
