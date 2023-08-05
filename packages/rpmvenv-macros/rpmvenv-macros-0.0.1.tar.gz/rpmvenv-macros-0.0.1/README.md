# rpmvenv-macros

Extension for [RPMvenv](https://github.com/kevinconway/rpmvenv) for adding macros to the top of the spec file.

## Basic Usage:

A config such as:

```
{
     "extensions": {
        "enabled": [
            "macros",
        ]
    },
    "macros": {
        "macros": [
            "__os_install_post %{nil}",
            "_build_id_links none"
        ]
    }
}
```

Will produce the following lines in the spec file:

```
%define __os_install_post %{nil}
%define _build_id_links none
```