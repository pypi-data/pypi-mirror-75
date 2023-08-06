# The following code, up until the END_MIT comment, is being redistributed from
# the py-rstr-max project: https://code.google.com/p/py-rstr-max/
# and is licensed under the MIT License:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# It was modified by Evan Sultanik to be forward compatible with Python 3

from array import array

import sys

if sys.version_info.major >= 3:
    xrange = range


def direct_kark_sort(s):
    alphabet = [None] + sorted(set(s))
    k = len(alphabet)
    n = len(s)
    t = dict((c, i) for i, c in enumerate(alphabet))
    SA = array('i', [0] * (n + 3))
    kark_sort(array('i', [t[c] for c in s] + [0] * 3), SA, n, k)
    return SA[:n]


def radixpass(a, b, r, s, n, k):
    c = array("i", [0] * (k + 1))
    for i in xrange(n):
        c[r[a[i] + s]] += 1

    somme = 0
    for i in xrange(k + 1):
        freq, c[i] = c[i], somme
        somme += freq

    for i in xrange(n):
        b[c[r[a[i] + s]]] = a[i]
        c[r[a[i] + s]] += 1


def kark_sort(s, SA, n, K):
    n0 = (n + 2) // 3
    n1 = (n + 1) // 3
    n2 = n // 3
    n02 = n0 + n2

    SA12 = array('i', [0] * (n02 + 3))
    SA0 = array('i', [0] * n0)

    s12 = [i for i in xrange(n + (n0 - n1)) if i % 3]
    s12.extend([0] * 3)
    s12 = array('i', s12)

    radixpass(s12, SA12, s, 2, n02, K)
    radixpass(SA12, s12, s, 1, n02, K)
    radixpass(s12, SA12, s, 0, n02, K)

    name = 0
    c0, c1, c2 = -1, -1, -1
    for i in xrange(n02):
        if s[SA12[i]] != c0 or s[SA12[i] + 1] != c1 or s[SA12[i] + 2] != c2:
            name += 1
            c0 = s[SA12[i]]
            c1 = s[SA12[i] + 1]
            c2 = s[SA12[i] + 2]
        if SA12[i] % 3 == 1:
            s12[SA12[i] // 3] = name
        else:
            s12[SA12[i] // 3 + n0] = name

    if name < n02:
        kark_sort(s12, SA12, n02, name + 1)
        for i in xrange(n02):
            s12[SA12[i]] = i + 1
    else:
        for i in xrange(n02):
            SA12[s12[i] - 1] = i

    s0 = array('i', [SA12[i] * 3 for i in xrange(n02) if SA12[i] < n0])
    radixpass(s0, SA0, s, 0, n0, K)

    p = j = k = 0
    t = n0 - n1
    while k < n:
        i = SA12[t] * 3 + 1 if SA12[t] < n0 else (SA12[t] - n0) * 3 + 2
        j = SA0[p] if p < n0 else 0

        if SA12[t] < n0:
            test = (s12[SA12[t] + n0] <= s12[j // 3]) if (s[i] == s[j]) else (s[i] < s[j])
        elif (s[i] == s[j]):
            test = s12[SA12[t] - n0 + 1] <= s12[j // 3 + n0] if (s[i + 1] == s[j + 1]) else s[i + 1] < s[j + 1]
        else:
            test = s[i] < s[j]

        if (test):
            SA[k] = i
            t += 1
            if t == n02:
                k += 1
                while p < n0:
                    SA[k] = SA0[p]
                    p += 1
                    k += 1

        else:
            SA[k] = j
            p += 1
            if p == n0:
                k += 1
                while t < n02:
                    SA[k] = (SA12[t] * 3) + 1 if SA12[t] < n0 else ((SA12[t] - n0) * 3) + 2
                    t += 1
                    k += 1
        k += 1


class Rstr_max:
    def __init__(self):
        self.array_str = []

    def add_str(self, str_unicode):
        self.array_str.append(str_unicode)

    def step1_sort_suffix(self):
        char_frontier = chr(2)

        self.global_suffix = char_frontier.join(self.array_str)

        nbChars = len(self.global_suffix)
        init = [-1] * nbChars
        self.idxString = array('i', init)
        self.idxPos = array('i', init)
        self.endAt = array('i', init)

        k = idx = 0
        for mot in self.array_str:
            last = k + len(mot)
            for p in xrange(len(mot)):
                self.idxString[k] = idx
                self.idxPos[k] = p
                self.endAt[k] = last
                k += 1
            idx += 1
            k += 1

        self.res = direct_kark_sort(self.global_suffix)

    def step2_lcp(self):
        n = len(self.res)
        init = [0] * n
        rank = array('i', init)
        LCP = array('i', init)

        s = self.global_suffix
        suffix_array = self.res
        endAt = self.endAt

        for i in xrange(len(self.array_str), n):
            v = self.res[i]
            rank[v] = i

        l = 0
        for j in xrange(n):
            if (l > 0):
                l -= 1
            i = rank[j]
            j2 = suffix_array[i - 1]
            if i:
                while l + j < endAt[j] and l + j2 < endAt[j2] and s[j + l] == s[j2 + l]:
                    l += 1
                LCP[i - 1] = l
            else:
                l = 0
        self.lcp = LCP

    def step3_rstr(self):
        prev_len = 0
        idx = 0
        results = {}
        len_lcp = len(self.lcp) - 1

        class Stack:
            pass

        stack = Stack()
        stack._top = 0
        stack.lst_max = []

        if len(self.res) == 0:
            return {}

        pos1 = self.res[0]
        for idx in xrange(len_lcp):
            current_len = self.lcp[idx]
            pos2 = self.res[idx + 1]
            end_ = max(pos1, pos2) + current_len  # max(pos1, pos2) + current_len
            n = prev_len - current_len
            if n < 0:
                stack.lst_max.append([-n, idx, end_])
                stack._top += -n
            elif n > 0:
                self.removeMany(stack, results, n, idx)
            elif stack._top > 0 and end_ > stack.lst_max[-1][-1]:
                stack.lst_max[-1][-1] = end_

            prev_len = current_len
            pos1 = pos2

        if (stack._top > 0):
            self.removeMany(stack, results, stack._top, idx + 1)

        return results

    def removeMany(self, stack, results, m, idxEnd):
        prevStart = -1
        while m > 0:
            n, idxStart, maxEnd = stack.lst_max.pop()
            if prevStart != idxStart:
                id_ = (maxEnd, idxEnd - idxStart + 1)
                if id_ not in results or results[id_][0] < stack._top:
                    results[id_] = (stack._top, idxStart)
                prevStart = idxStart
            m -= n
            stack._top -= n
        if m < 0:
            stack.lst_max.append([-m, idxStart, maxEnd - n - m])
            stack._top -= m

    def go(self):
        self.step1_sort_suffix()
        self.step2_lcp()
        r = self.step3_rstr()
        return r

# END_MIT