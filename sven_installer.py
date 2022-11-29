"""
Sven Co-op add-on installer - a command line tool for installing add-ons to the video game Sven Co-op
Copyright (C) 2020-2022 PatTheHyruler

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

To see more detailed licensing information, view the LICENSE file that
you should have received along with this program.
"""

import argparse
import distutils.dir_util
import os
import platform
import tempfile
from pathlib import Path
from typing import List, Optional

import patoolib
import vdf


def get_home_dir() -> Path:
    login = os.getlogin()
    if platform.system() == "Windows":
        return Path(f"C:/Users/{login}")
    elif platform.system() == "Linux":
        return Path(f"/home/{login}")
    else:
        raise Exception("Unsupported OS for getting used home directory")


def get_local_app_data_directory_path() -> Path:
    appname = "SvenCoopAddonInstaller"
    if platform.system() == "Windows":
        return get_home_dir() / Path(f"AppData/Local/{appname}")
    elif platform.system() == "Linux":
        return get_home_dir() / Path(f".local/share/{appname}")
    else:
        raise Exception("Unsupported OS for app data")


def get_saved_sven_path_file_path() -> Path:
    try:
        return get_local_app_data_directory_path() / "sven_path.txt"
    except Exception as e:
        raise Exception(e, "Failed to get path to file where Sven path (is/would be) saved")


def prompt_for_bool_input(message: str) -> bool:
    re_prompt_message = ""
    while True:
        user_input = input(f"{re_prompt_message}{message} (y/n)").lower().strip()
        if user_input == "y":
            return True
        elif user_input == "n":
            return False
        re_prompt_message = "Invalid input! Please type y for yes or n for no."


def is_path_suspicious(path: str | os.PathLike[str]):
    return len(path.strip()) == 0


def save_sven_path(args: argparse.Namespace):
    if not args.svenpath:
        raise Exception("--svenpath option must be set when --save option is used.")
    if args.delete:
        raise Exception("Conflicting options: --save and --delete must not be used together.")
    if is_path_suspicious(args.svenpath):
        raise Exception(f"Provided Sven path '{args.svenpath}' is sus.")

    try:
        appdata_path = get_local_app_data_directory_path()
        os.makedirs(appdata_path, exist_ok=True)
        saved_sven_path_file_path = get_saved_sven_path_file_path()
        if os.path.exists(saved_sven_path_file_path):
            if not prompt_for_bool_input(f"Saved Sven path '{get_saved_sven_path()}' already exists!\n"
                                         f"Do you want to overwrite it?"):
                return
            with open(saved_sven_path_file_path, "w") as f:
                f.write(args.svenpath)
    except Exception as e:
        raise Exception(e, "Unable to save Sven path.")


def only_expected_args_set(parsed_args: argparse.Namespace, *expected_args) -> bool:
    for parsed_arg_name, parsed_arg_value in parsed_args.__dict__.items():
        if parsed_arg_name not in expected_args:
            if parsed_arg_value is not None:
                try:
                    if parsed_arg_value:
                        return False
                except:
                    return False
    return True


def delete_saved_sven_path(args: argparse.Namespace):
    if not only_expected_args_set(args, "delete"):
        raise Exception("--delete option must be used without any other arguments.")
    saved_sven_path_file_path = get_saved_sven_path_file_path()
    if not os.path.isfile(saved_sven_path_file_path):
        raise Exception("Can't delete saved Sven path - no such path found!")
    os.remove(saved_sven_path_file_path)


def get_saved_sven_path() -> Path:
    saved_sven_path_file_path = get_saved_sven_path_file_path()
    try:
        with open(saved_sven_path_file_path, "r") as f:
            path_string = f.readline()
    except Exception as e:
        raise Exception(e, f"Failed to read saved Sven path from {saved_sven_path_file_path}")

    if is_path_suspicious(path_string):
        raise Exception(f"Saved Sven path is suspiciously short: '{path_string}'")

    return Path(path_string)


class SteamLibraryFolder:
    path = Path

    def __init__(self, path: Path):
        self.path = path

    def __repr__(self) -> str:
        return f"SteamLibraryFolder at '{self.path}'"

    def __eq__(self, other):
        if type(other) != SteamLibraryFolder:
            return False
        other: SteamLibraryFolder
        return self.path == other.path

    @property
    def steamapps(self) -> Path:
        return self.path / Path("steamapps")

    def app_manifest_path(self, app_id: str) -> Path:
        return self.steamapps / Path(f"appmanifest_{app_id}.acf")

    def app_install_path(self, app_id: str) -> Optional[Path]:
        if self.has_app(app_id):
            with open(self.app_manifest_path(app_id)) as f:
                data = vdf.parse(f)
            return self.steamapps / Path("common") / Path(data["AppState"]["installdir"])
        return None

    def has_app(self, app_id: str) -> bool:
        return os.path.isfile(self.app_manifest_path(app_id))


class Steam:
    @staticmethod
    def get_library_folders_file_path(steam_path: Path):
        return steam_path / Path("steamapps/libraryfolders.vdf")

    @staticmethod
    def get_library_folders(steam_path: Path) -> List[SteamLibraryFolder]:
        fp = Steam.get_library_folders_file_path(steam_path)
        library_folders = []
        if os.path.isfile(fp):
            with open(fp) as f:
                data = vdf.parse(f)
            for library_folder_data in data["libraryfolders"].values():
                library_folders.append(SteamLibraryFolder(library_folder_data["path"]))
        return library_folders

    @staticmethod
    def get_all_library_folders() -> List[SteamLibraryFolder]:
        library_folders = []
        for steam_path in Steam.get_steam_paths():
            library_folders += [lf for lf in Steam.get_library_folders(steam_path) if lf not in library_folders]
        return library_folders

    @staticmethod
    def is_valid_steam_path(steam_path: Path):
        return os.path.isfile(Steam.get_library_folders_file_path(steam_path))

    @staticmethod
    def get_steam_paths() -> List[Path]:
        if platform.system() == "Windows":
            # Get Steam install location from the Windows registry
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                     "SOFTWARE\\WOW6432Node\\Valve\\Steam")
                value = winreg.QueryValueEx(key, "InstallPath")[0]
                return [value]
            except:
                raise Exception("Couldn't locate Steam")
        elif platform.system() == "Linux":
            potential_paths = [
                get_home_dir() / Path(".steam/steam"),
                get_home_dir() / Path(".var/app/com.valvesoftware.Steam/data/Steam")
            ]

            return [steam_path for steam_path in potential_paths if Steam.is_valid_steam_path(steam_path)]

    @staticmethod
    def get_app_install_paths(app_id: str) -> List[Path]:
        result = []
        for library_folder in Steam.get_all_library_folders():
            if library_folder.has_app(app_id):
                result.append(library_folder.app_install_path(app_id))
        return result


def get_temp_dir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(None, "SvenCoopAddonInstaller", tempfile.gettempdir(),
                                       ignore_cleanup_errors=True)


def extract_file(file: Path, target_dir: Path):
    print(f"Extracting file '{file}' to '{target_dir}'")
    base_exception_message = f"Failed to extract file '{file}'."
    if not os.path.isdir(target_dir):
        raise Exception(f"{base_exception_message} Target '{target_dir}' isn't a directory.")

    try:
        patoolib.extract_archive(str(file), outdir=str(target_dir))
        print("Successfully extracted")
    except Exception as e:
        raise Exception(e, f"{base_exception_message}: {e}")


def install_extracted(source_dir: Path, target_dir: Path, depth: int = 0):
    exception_base_message = f"Failed to install from '{source_dir}' to '{target_dir}'"

    expected_directories = (
        source_dir / Path("maps"),
        source_dir / Path("models"),
        source_dir / Path("gfx"),
        source_dir / Path("scripts"),
        source_dir / Path("sound"),
        source_dir / Path("sprites"),
    )

    def is_valid_addon_dir() -> bool:
        for directory in expected_directories:
            if directory.is_dir():
                return True
        for file_name in os.listdir(source_dir):
            if file_name.endswith(".wad"):
                return True
        return False

    if is_valid_addon_dir():
        print(f"Copying from '{source_dir}' to '{target_dir}'")
        distutils.dir_util.copy_tree(str(source_dir), str(target_dir))
        return
    elif depth < 3:
        succeeded = False
        encountered_exceptions = []
        for file_name in os.listdir(source_dir):
            if os.path.isdir(source_dir / Path(file_name)):
                try:
                    install_extracted(source_dir / Path(file_name), target_dir, depth=depth + 1)
                    succeeded = True
                    return
                except Exception as e:
                    encountered_exceptions.append(e)
        if not succeeded:
            raise Exception(f"{exception_base_message}\n" +
                            ("" if not encountered_exceptions else
                             ("Encountered errors:\n" + "\n".join([str(e) for e in encountered_exceptions]))))
    else:
        raise Exception(f"{exception_base_message} - didn't find suitable directory structure")


def install_file(file: Path, sven_path: Path, temp_dir: tempfile.TemporaryDirectory = None):
    print(f"Installing '{file}' to {sven_path}" + (
        "" if not temp_dir else f" using temporary directory '{temp_dir.name}'"))
    if not os.path.exists(sven_path):
        raise Exception(f"Sven path '{sven_path}' doesn't exist")
    elif not os.path.isdir(sven_path):
        raise Exception(f"Sven path '{sven_path}' is not a directory")

    sven_addons = sven_path / Path("svencoop_addon")
    if not os.path.isdir(sven_addons):
        try:
            os.mkdir(sven_addons)
        except Exception as e:
            raise Exception(e, f"Failed to create svencoop_addon directory in Sven path '{sven_path}'")

    external_temp_dir = temp_dir
    if temp_dir is None:
        temp_dir = get_temp_dir()

        extract_file(file, Path(temp_dir.name))

    install_extracted(Path(temp_dir.name), sven_addons)

    if external_temp_dir is None:
        temp_dir.cleanup()


def install_file_multiple_targets(file: Path, sven_paths: List[Path]):
    print(f"Installing '{file}' to {[sp.as_posix() for sp in sven_paths]}")
    temp_dir = get_temp_dir()
    extract_file(file, Path(temp_dir.name))
    for sven_path in sven_paths:
        try:
            install_file(file, sven_path, temp_dir)
        except Exception as e:
            print(e)
    temp_dir.cleanup()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("file", help="path to the archive (probably .zip) file(s) that you want to install.", type=str,
                        nargs='*')
    parser.add_argument("-sp", "--svenpath",
                        help="Path to the directory where Sven Co-op is installed.\n"
                             f"Should end with something like ...{os.path.normpath(f'steamapps/common/Sven Co-op')}.",
                        type=str)
    parser.add_argument("-s", "--save", help="Save the Sven Co-op installation path.\nRequires --svenpath option.",
                        default=False, action="store_true")
    parser.add_argument("-d", "--delete", help="Forget the saved Sven Co-op installation path.",
                        default=False, action="store_true")
    parser.add_argument("-l", "--license", help="Show licensing information for this program and exit",
                        default=False, action="store_true")

    args = parser.parse_args()

    if args.license:
        print("""
Sven Co-op add-on installer - a command line tool for installing add-ons to the video game Sven Co-op
Copyright (C) 2022 PatTheHyruler

This program is licensed under GNU General Public License version 3.
Among other things, that means:
1) This program comes with ABSOLUTELY NO WARRANTY.
2) This is free software, and you are welcome to redistribute it under certain conditions.

To see more detailed licensing information, please view the LICENSE file
that you should have received along with this program.
        """)
        return

    if args.delete:
        delete_saved_sven_path(args)

    if args.save:
        try:
            save_sven_path(args)
        except Exception as e:
            if args.file:
                print(e)
                print("Continuing with installation despite error")
            else:
                raise e

    if not args.file:
        if args.delete or args.save:
            return
        else:
            raise Exception("Expected files to install, but found none")

    sven_paths = []
    if args.svenpath:
        sven_paths.append(Path(args.svenpath))
    else:
        try:
            sven_paths.append(get_saved_sven_path())
        except:
            sven_paths += Steam.get_app_install_paths("225840")

    if len(sven_paths) == 0:
        raise Exception("Failed to find any Sven installation paths")

    for file in args.file:
        try:
            install_file_multiple_targets(Path(file), sven_paths)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        parse_args()
    except Exception as e:
        print(e)
