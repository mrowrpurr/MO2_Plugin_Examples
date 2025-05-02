from pathlib import Path

def copy_files() -> None:
    source_files: list[Path] = [
        Path(r"cpp_examples\hello_world_plugin\vsbuild\src\RelWithDebInfo\hello_world_plugin.dll"),
        Path(r"cpp_examples\hello_world_plugin\vsbuild\src\RelWithDebInfo\hello_world_plugin.pdb"),
    ]
    destination_dir: Path = Path(r"C:\Modding\MO2\plugins")

    for source_file in source_files:
        destination_file: Path = destination_dir / source_file.name
        destination_file.write_bytes(source_file.read_bytes())
        print(f"Copied {source_file} -> {destination_file}")

if __name__ == "__main__":
    copy_files()
