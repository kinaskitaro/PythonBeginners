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

if __name__ == "__main__":
    print("Select a function to execute:")
    print("1. triangleLeft")
    print("2. triangleCenter")
    
    choice = int(input("Enter the number of the function to execute: "))
    if choice == 1:
        triangleLeft()
    elif choice == 2:
        triangleCenter()
    else:
        print("Invalid choice.")