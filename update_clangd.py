import os

# Get the current working directory
current_dir = os.getcwd().replace('\\', '/')

# Path to the .clangd file
clangd_file = os.path.join(current_dir, '.clangd')

# Read the .clangd file
with open(clangd_file, 'r') as file:
    content = file.read()

# Replace "build/build" with the current directory path
updated_content = content.replace('build/build', f'{current_dir}/build/build')

# Write the updated content back to the .clangd file
with open(clangd_file, 'w') as file:
    file.write(updated_content)

print(".clangd file updated successfully.")