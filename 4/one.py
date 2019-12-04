(min, max) = (234208, 765869)

def meets_criteria(nums):
    seen = set()
    prev, repeated = 0, False
    for num in nums:
        cur = int(num)
        if prev > cur:
            return False
        prev = cur

        if cur in seen:
            repeated = True
        else:
            seen.add(cur)

    return repeated

assert True == meets_criteria(str(11111))
assert False == meets_criteria(str(223450))
assert False == meets_criteria(str(123789))


def count_passwords(min, max):
    return len([pw for pw in range(min, max) if meets_criteria(str(pw))])


print(count_passwords(min, max))
