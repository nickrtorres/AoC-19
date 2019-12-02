def total_fuel_required(mass):
    m = int(mass) // 3 - 2
    if m <= 0:
        return 0
    return m + total_fuel_required(m)

assert 2 == total_fuel_required(14)
assert 966 == total_fuel_required(1969)
assert 50346 == total_fuel_required(100756)


with open('input') as f:
    input = f.read()


print(sum(total_fuel_required(m) for m in input.splitlines()))
