ascid
=====

Ascid is the Self-referential Cycle IDentifier.  It is capable of quickly (in linear time) detecting the maximum length repeated substrings in text files.

This is often useful, *e.g.*, when debugging a program that loops infinitely, *vi&.*, ascid can determine the point at which the log output loops back on itself.

## Usage

```
$ python ascid.py FILE_TO_PROCESS
```