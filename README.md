# Sven Co-op Add-on installer

This is a small program for installing custom addons (like maps and models) for Sven Co-op.

Of course, if the archive is not a Sven Co-op map or model, that can cause problems (most likely just nothing will happen, but best be careful anyway), so I recommend not using random archives that are not meant to be Sven Co-op maps or models.

The program will attempt to find your Sven Co-op install location on its own, but if it can't find it, you can specify the location yourself.

## Usage (for Windows users, simplified)
You can get the latest executable version of the program by going to the [latest release page](https://github.com/PatTheHyruler/sven-coop-installer/releases/latest) and downloading the `sven_installer.exe` file listed there.  
Then you should be able to drag+drop one or more Sven Co-op add-on archive files (probably `*.zip`) onto the executable.

If that doesn't work, you can try using the executable via the command line to customize its behaviour.

## Usage (command line)
You can run the program
* as a .py file using `python ./sven_installer.py` (or `python3 ./sven_installer.py`). The packages from requirements.txt must be installed before this.
* as an executable (on Windows) using `.\sven_installer.exe`

The above commands assume that they're being run in the same directory as the sven_installer program being used.
If that is not the case, the commands will need to be customized to point towards the sven_installer program's actual location.

Run the program with the `--help` command line argument for more detailed information on how to use the program and provide arguments to it.

## Requirements:

**Python 3**

**Python packages from requirements.txt**

(Optional) A supported tool for extracting .rar files on your Path

### Installing required Python packages
#### Windows
    python -m pip install -r requirements.txt
#### Linux
    python3 -m pip install -r requirements.txt

### More about .rar files
It appears that due to license issues, it's not possible (or at least not easy?) to build in .rar file support into a Python program or package.  
Thus, the program will instead attempt to find a tool on your system that already supports .rar files (rar, unrar, 7z).  
In my case (on Pop OS), I had to install unrar (`sudo apt install unrar`), despite already having 7z installed.