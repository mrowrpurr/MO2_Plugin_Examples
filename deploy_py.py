import os
import shutil
import sys

def deploy_plugin(plugin_name):
    source_folder = os.path.join('python_examples', plugin_name)
    source_file = f"python_examples/{plugin_name}.py"
    target_folder = os.path.join('C:\\Modding\\MO2\\plugins', plugin_name)
    target_file = os.path.join('C:\\Modding\\MO2\\plugins', f"{plugin_name}.py")

    # Check if it's a folder or a file
    if os.path.isdir(source_folder):
        # Remove the target folder if it exists
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        # Remove the target file if it exists
        if os.path.exists(target_file):
            os.remove(target_file)
        # Copy the source folder to the target location
        shutil.copytree(source_folder, target_folder)
        print(f"Deployed folder {plugin_name} to {target_folder}")
    elif os.path.isfile(source_file):
        # Remove the target folder if it exists
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        # Remove the target file if it exists
        if os.path.exists(target_file):
            os.remove(target_file)
        # Copy the source file to the target location
        shutil.copy2(source_file, target_file)
        print(f"Deployed file {plugin_name}.py to {target_file}")
    else:
        print(f"Error: {plugin_name} is not a valid subfolder or .py file in python_examples.")
        sys.exit(1)

def main():
    args = sys.argv[1:]

    if args:
        for plugin_name in args:
            deploy_plugin(plugin_name)
    else:
        # No arguments, deploy all subfolders and .py files in python_examples
        python_examples_path = 'python_examples'
        if not os.path.isdir(python_examples_path):
            print("Error: python_examples folder does not exist.")
            sys.exit(1)

        for item in os.listdir(python_examples_path):
            item_path = os.path.join(python_examples_path, item)
            if os.path.isdir(item_path):
                deploy_plugin(item)
            elif os.path.isfile(item_path) and item.endswith('.py'):
                deploy_plugin(item[:-3])  # Remove .py extension

if __name__ == "__main__":
    main()