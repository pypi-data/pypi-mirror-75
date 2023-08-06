# Except as otherwise commented in this code, ascid is licensed under the GNU GPL v2
# and is Copyright 2014, Evan A. Sultanik, Ph.D.
# See the accompanying LICENSE file for the full text of the license.


import sys

from .pyrstrmax import Rstr_max


def find_repeating_strings(string):
    rstr = Rstr_max()
    rstr.add_str(string)
    r = rstr.go()
    longest = -1
    offsets = []
    s = ''
    if sys.version_info.major < 3:
        items = r.iteritems()
    else:
        items = r.items()
    for (offset_end, nb), (l, start_plage) in items:
        if l > longest:
            longest = l
            s = rstr.global_suffix[offset_end - l:offset_end]
            offsets = [rstr.idxPos[rstr.res[o]] for o in range(start_plage, start_plage + nb)]
    return s, offsets
