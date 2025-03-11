def triangleLeft():
    for i in range(5):
        for j in range(i+1):
            print("*", end="")
        print()

def triangleCenter():
    for i in range(5):
        for j in range(5-i):
            print(" ", end="")
        for j in range(2*i+1):
            print("*", end="")
        print()
triangleCenter()