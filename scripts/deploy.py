import sys
from pathlib import Path

def copy_files(plugin_name: str) -> None:
    source_dll = Path(f"cpp_examples/{plugin_name}/vsbuild/src/RelWithDebInfo/{plugin_name}.dll")
    source_pdb = Path(f"cpp_examples/{plugin_name}/vsbuild/src/RelWithDebInfo/{plugin_name}.pdb")
    destination_dir = Path(r"C:\Modding\MO2\plugins")

    if not source_dll.exists():
        print(f"{plugin_name} has not been built")
        return

    print(f"Copying {plugin_name}.dll")
    destination_dll = destination_dir / source_dll.name
    destination_dll.write_bytes(source_dll.read_bytes())

    if source_pdb.exists():
        destination_pdb = destination_dir / source_pdb.name
        destination_pdb.write_bytes(source_pdb.read_bytes())


def main():
    cpp_examples_path = Path("cpp_examples")

    if len(sys.argv) == 1:
        # No arguments, deploy all plugins
        subfolders = [
            folder.name for folder in cpp_examples_path.iterdir()
            if folder.is_dir()
        ]
    else:
        # Validate each argument
        subfolders: list[str] = []
        for arg in sys.argv[1:]:
            folder_path = cpp_examples_path / arg
            if not folder_path.exists() or not folder_path.is_dir():
                print(f"Error: Folder '{arg}' does not exist in 'cpp_examples/'.")
                return
            subfolders.append(arg)

    for plugin_name in subfolders:
        copy_files(plugin_name)


if __name__ == "__main__":
    main()
