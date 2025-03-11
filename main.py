import os
import subprocess

def list_python_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".py") and f != "main.py"]

def execute_python_file(filepath):
    print(f"Executing {filepath}")
    subprocess.run(["python", filepath])

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    python_files = list_python_files(directory)
    
    print("Select a Python file to execute:")
    for idx, filename in enumerate(python_files):
        print(f"{idx + 1}. {filename}")
    
    choice = int(input("Enter the number of the file to execute: ")) - 1
    if 0 <= choice < len(python_files):
        execute_python_file(os.path.join(directory, python_files[choice]))
    else:
        print("Invalid choice.")
