# Wommit

**W**rite c**ommit** **t**ool

---

[![PyCalVer 20.08.0031-dev][version_img]][version_ref]
[![PyPI Releases][pypi_img]][pypi_ref]

#### A package for intuitively formatting appealing commmit messages with emojis, using an assortment of different methods.

![CHECK ME OUT](https://i.imgur.com/VIXvQXY.png)

---

### Example usage:

![EXAMPLE](https://i.imgur.com/EORqAkh.gif)

---

### Commands

`wommit ...`:

- `c`: Commit all staged files using an intuitive drop-down menu or a fast autocompletion prompt.

  *Options:*
  
  - `-m`: Use menu mode, overriding default.

  - `-e`: Use autocompletion mode, overriding default.
  
  - `-m [MESSAGE]`: Write a manual commit message, and commits if it's in the accepted format, as well as converting known types to emojis. 
  
  - `-g`: Use global settings and data instead of local.

  - `--test`:  Test either of the modes without commiting.
  
  
- `check`: Manually check previously added commit. 

  *Options:*

  - `-id [HASH]`: Check a commit message with the specified ID.
  
  - `-ids [HASH1] [HASH2]`: Check all commit messages between two IDs (newest ID first).

  - `-m [MESSAGE]`:  Check if the given string passes the check.
  
  - `-l`:  Check all local commits that have not been pushed.

- `configure ...`: Opens a prompt for adding/removing types and scopes.

    - `e`: Edit current types and scopes.
    
    - `p`: Prints all types and scopes.
    
    - `s`: Edit settings.

    *Options:*

  - `-g`: Edit global settings.
  
  - `-t`: Manually test the functionality.
  
 - `format`: Pastes the format a message needs to meet in order to pass the check.
 
 ---
 
 ## Info
 
 Use the [wommit-changelog-action](https://github.com/bkkp/wommit-changelog-action) in your wommit project to automatically release your project with appropriate changelogs.

[version_img]: https://img.shields.io/static/v1.svg?label=Wommit&message=20.08.0031-dev&color=blue
[version_ref]: https://pypi.org/project/wommit/
[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg
[pypi_ref]: https://pypi.org/project/wommit/

