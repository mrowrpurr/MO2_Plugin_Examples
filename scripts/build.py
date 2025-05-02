import os
import sys

def main():
    cpp_examples_path = os.path.join(os.getcwd(), 'cpp_examples')

    # If no arguments are passed, get all immediate child folders in ./cpp_examples/
    if len(sys.argv) == 1:
        subfolders = [
            name for name in os.listdir(cpp_examples_path)
            if os.path.isdir(os.path.join(cpp_examples_path, name))
        ]
    else:
        # Validate each argument
        subfolders: list[str] = []
        for arg in sys.argv[1:]:
            folder_path = os.path.join(cpp_examples_path, arg)
            if not os.path.exists(folder_path):
                print(f"Error: Folder '{arg}' does not exist in 'cpp_examples/'.")
                return
            subfolders.append(arg)

    # Run the shell command with the collected subfolders
    command = ['python', 'scripts/mob.py', "build"] + subfolders
    print(f"Running command: {' '.join(command)}")
    os.system(' '.join(command))

if __name__ == "__main__":
    main()