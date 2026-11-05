"""install_lucas_engines.py

Add Remus1, Remus2, Remus3, and Remus4 to the External engines list of Lucas Chess.

The workshop designer runs this file on each class laptop, with Lucas Chess closed,
using the Run button in VS Code. Lucas Chess keeps its list in the file ExtEngines.pk.
This program opens that file, keeps every engine already in it, and adds each Remus
that is missing. An engine that already runs the right remus.bat stays as it is, so a
second run adds no duplicates. An engine with the right name and the wrong remus.bat
gets the right one, which repairs the list after the Remus folder moves.
"""

# cspell:ignore autor

import os
import pickle
import shutil
from pathlib import Path

REMUS_NAMES = ["Remus1", "Remus2", "Remus3", "Remus4"]


def read_engines(file_path: Path) -> list[dict]:
    """Return the engines in ExtEngines.pk, or an empty list if it does not exist."""
    engines = []
    if not file_path.is_file():
        return engines
    # The file holds a list of byte strings, and each one holds one engine's settings
    for engine_bytes in pickle.loads(file_path.read_bytes()):
        engines.append(pickle.loads(engine_bytes))
    return engines


def write_engines(engines: list[dict], file_path: Path) -> None:
    """Save a list of engines in the format of ExtEngines.pk."""
    engine_list = []
    for engine in engines:
        engine_list.append(pickle.dumps(engine, protocol=4))
    file_path.write_bytes(pickle.dumps(engine_list, protocol=4))


def new_engine(name: str, bat_path: Path) -> dict:
    """Return the settings Lucas Chess saves when a person adds this engine by hand."""
    return {
        "_li_changed_options": [],
        "_li_uci_options": [],
        "_name": name,
        "args": [],
        "autor": "-",
        "book": None,
        "book_max_plies": 0,
        "book_rr": "mp",
        "elo": 0,
        "emulate_movetime": False,
        "id_author": "-",
        "id_info": "",
        "id_name": name,
        "key": name,
        "maxMultiPV": 0,
        "max_depth": 0,
        "max_time": 0.0,
        "menu": name,
        "min_fixed_depth": 0,
        "multiPV": 0,
        "nodes": 0,
        "nodes_compatible": None,
        "nomDebug": None,
        "parent_external": None,
        "path_exe": str(bat_path),
        "siDebug": False,
        "type": 1,
        "url": "",
        "version": "",
    }


def register_engine(
    engines: list[dict], name: str, bat_path: Path, bin_folder: Path
) -> bool:
    """
    Make sure one Remus is in the list, and report whether the list changed.

    Parameters
    ----------
    engines : list[dict]
        The engines from ExtEngines.pk, changed in place.
    name : str
        The name of the engine, such as "Remus1".
    bat_path : Path
        The full path of the remus.bat this engine must run.
    bin_folder : Path
        The folder of LucasR.exe. Lucas Chess saves many paths relative to it.

    Returns
    -------
    bool
        True if the list changed.
    """
    # The same remus.bat under any name counts as registered
    for engine in engines:
        if (bin_folder / engine["path_exe"]).resolve() == bat_path:
            print(f"{name} is already registered as {engine['key']}")
            return False

    for engine in engines:
        if engine["key"] == name:
            print(f"{name} moved from {engine['path_exe']} to {bat_path}")
            engine["path_exe"] = str(bat_path)
            return True

    print(f"{name} added, and it runs {bat_path}")
    engines.append(new_engine(name, bat_path))
    return True


def main():
    remus_folder = Path(__file__).resolve().parent.parent.parent
    lucas_folder = Path(os.environ["LOCALAPPDATA"], "Programs", "LucasChessR")
    config_folder = lucas_folder / "UserData" / "__Config__"
    if not config_folder.is_dir():
        print(f"Lucas Chess is not installed: {config_folder} does not exist")
        return

    bat_paths = {}
    for name in REMUS_NAMES:
        bat_paths[name] = remus_folder / "engines" / name / "remus.bat"
        if not bat_paths[name].is_file():
            print(f"Nothing changed: {bat_paths[name]} does not exist")
            return

    file_path = config_folder / "ExtEngines.pk"
    engines = read_engines(file_path)
    print(f"Read {len(engines)} engines from {file_path}")

    list_changed = False
    for name in REMUS_NAMES:
        if register_engine(engines, name, bat_paths[name], lucas_folder / "bin"):
            list_changed = True

    if not list_changed:
        print("Nothing changed: every Remus is already registered")
        return

    # Keep the first list found on this laptop, so the designer can put it back
    backup_path = config_folder / "ExtEngines_before_remus.pk"
    if file_path.is_file() and not backup_path.is_file():
        shutil.copy2(file_path, backup_path)
        print(f"Saved the old list as {backup_path}")

    write_engines(engines, file_path)
    print(f"Saved {len(engines)} engines in {file_path}")


if __name__ == "__main__":
    main()
