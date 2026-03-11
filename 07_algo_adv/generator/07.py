def wrapper_without_yield_from(xs):
    for x in xs:
        yield x

def wrapper_with_yield_from(xs):
    yield from xs

data = [1, 2, 3]
print(list(wrapper_without_yield_from(data)))
print(list(wrapper_with_yield_from(data)))