def fuel_required(mass):
    return int(mass) // 3 - 2

assert 2 == fuel_required(12)
assert 2 == fuel_required(14)
assert 654 == fuel_required(1969)
assert 33583 == fuel_required(100756)


with open('input') as f:
    input = f.read()


print(sum(fuel_required(m) for m in input.splitlines()))
