# coding: utf-8

"""
This file is a part of asexecutor
https://github.com/efiminem/asexecutor
"""

B = 1

KiB = 1024 * B
MiB = 1024 * KiB
GiB = 1024 * MiB
TiB = 1024 * GiB
PiB = 1024 * TiB
EiB = 1024 * PiB
ZiB = 1024 * EiB
YiB = 1024 * ZiB

KB = 1000 * B
MB = 1000 * KB
GB = 1000 * MB
TB = 1000 * GB
PB = 1000 * TB
EB = 1000 * PB
ZB = 1000 * EB
YB = 1000 * ZB

memory_short_names_IEC = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
memory_short_names = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
memory_names_IEC = [
    "byte",
    "kibibyte",
    "mebibyte",
    "gibibyte",
    "tebibyte",
    "pebibyte",
    "exbibyte",
    "zebibyte",
    "yobibyte",
]
memory_names = [
    "byte",
    "kilobyte",
    "megabyte",
    "gigabyte",
    "terabyte",
    "petabyte",
    "exabyte",
    "zettabyte",
    "yottabyte",
]

memory_values_IEC = [B, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB]
memory_values = [B, KB, MB, GB, TB, PB, EB, ZB, YB]
