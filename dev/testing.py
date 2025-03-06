
# Nested for loops
nested_items = [
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
]
for item in nested_items:
    for number in item:
        print(number)