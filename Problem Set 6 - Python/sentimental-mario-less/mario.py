while True:
    try:
        height = int(input("Height: "))
        if 1 <= height <= 8:
            break

    except ValueError:
        continue

for j in range(1, height + 1):
    print(" " * (height - j) + "#" * j)
