import collections

(min, max) = (234208, 765869)


def meets_criteria(nums):
    seen = collections.defaultdict(int)
    cur, prev = 0, 0
    for num in nums:
        cur = int(num)
        seen[cur] = seen[cur] + 1
        if prev > cur:
            return False
        prev = cur

    return len([key for (key, val) in seen.items() if val == 2]) > 0

assert True == meets_criteria(str(112233))
assert True == meets_criteria(str(111122))
assert False == meets_criteria(str(12345))
assert False == meets_criteria(str(11111))
assert False == meets_criteria(str(123444))


def count_passwords(min, max):
    return len([pw for pw in range(min, max) if meets_criteria(str(pw))])


print(count_passwords(min, max))
