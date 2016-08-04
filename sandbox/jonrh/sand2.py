list1 = [
    {"a": 1, "b": [1, 2, 3]},
    {"a": 1, "b": [4, 5, 6]},
    {"a": 1, "b": [7, 8, 9]},
    {"a": 1, "b": [10, 11, 12]}
]

list2 = [
    {"a": 1, "b": [1, 2, 3]},
    {"a": 1, "b": [10, 11, 12]}
]

for removal in list2:
    list1.remove(removal)

print list1
