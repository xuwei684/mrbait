#!/usr/bin/python

import time
from itertools import islice
import re

"""
Conclusions:
- No real difference across methods. countSlidingWindowSubstring2 seems a bit
  faster but probably just because of not having the function calls. I like
  countSlidingWindowSubstring the best because I understand the code of the
  generator function for that one better, plus its one less package dependency
  Islice is maybe a little bit faster than the substring picking method but
  I get more flexibility with my substring method
- Converting to a simplified consensus seems to be the fastest overall
- The additional overhead of the regex substitution in the 'Simplest'
  version doesn't affect it much and this ends up being by far the fastest
  option (less than half the average runtime)
"""

def time_me(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))

        print(endTime - startTime,'ms')
        return result

    return wrapper

def seqCounterLoop(seq):
	d = {}
	d = {
		'A':0,
		'N':0,
		'-':0,
		'C':0,
		'G':0,
		'T':0,
		"R"	: 0,
		"Y"	: 0,
		"S"	: 0,
		"W"	: 0,
		"K"	: 0,
		"M"	: 0,
		"B"	: 0,
		"D"	: 0,
		"H"	: 0,
		"V"	: 0
	}
	for c in seq:
		if c in d:
			d[c] += 1
	d['VAR'] = d['R'] + d['Y'] + d['S'] + d['W'] \
	+ d['K'] + d['M'] + d['B'] + d['D'] + d['H'] + d['V']

def seqCounterLoopSimplified(seq):
	d = {}
	d = {
		'.':0,
		'N':0,
		'-':0,
		'*':0
	}
	for c in seq:
		if c in d:
			d[c] += 1


#Options: Count for each sliding window, or first convert string to simplified chars
#This generator slices substrings using the islice function from itertools
def windowSlice(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

@time_me
def countSlidingWindow(seq, num):
	"""This option calls seqCounterLoop per sliding window on unaltered sequence"""
	print("Using islice:")
	for j in range(num):
		seq_norm = seq.upper()
		for i in windowSlice(seq_norm, 10):
			window_seq = "".join(i)
			seqCounterLoop(window_seq)

#generator to create sliding windows by slicing out substrings
def windowSub(seq, shift, width=2):
	seqlen = len(seq)
	for i in range(0,seqlen,shift):
		if i+width > seqlen:
			j = seqlen
		else:
			j = i + width
		yield seq[i:j]
		if j==seqlen: break

@time_me
def countSlidingWindowSubstring(seq, num, shift, width):
	"""This option does a sliding window manually by caalculating start/stop of substrings"""
	print("Using substrings:")
	for j in range(num):
		seq_norm = seq.upper()
		for i in windowSub(seq_norm, shift, width):
			#print(i)
			window_seq = "".join(i)
			seqCounterLoop(window_seq)

@time_me
def countSlidingWindowSubstring2(seq, num, shift, width):
	"""This option does a sliding window manually by caalculating start/stop of substrings"""
	print("Using substrings, no generator function:")
	for j in range(num):
		seq_norm = seq.upper()
		seqlen = len(seq_norm)
		for i in range(0,seqlen,shift):
			if i+width > seqlen:
				j = seqlen
			else:
				j = i + width
			window_seq = "".join(seq_norm[i:j])
			seqCounterLoop(window_seq)
			if j==seqlen: break

@time_me
def countSlidingWindowSubstringSimple(seq, num, shift, width):
	"""This option does a sliding window manually by caalculating start/stop of substrings"""
	print("Using substrings, simplified consensus:")
	for j in range(num):
		seq_norm = (seq.upper()).translate(str.maketrans("ATGCRYSWKMBDHV", "....**********"))
		for i in windowSub(seq_norm, shift, width):
			#print(i)
			window_seq = "".join(i)
			seqCounterLoopSimplified(window_seq)

@time_me
def countSlidingWindowSubstringSimplest(seq, num, shift, width):
	"""This option does a sliding window manually by caalculating start/stop of substrings"""
	print("Using substrings, more simplified consensus:")
	for j in range(num):
		seq_temp = re.sub('[ACGT]', '', seq.upper())
		seq_norm = seq_temp.translate(str.maketrans("RYSWKMBDHV", "**********"))
		for i in windowSub(seq_norm, shift, width):
			#print(i)
			window_seq = "".join(i)
			seqCounterLoopSimplified(window_seq)




seq = "ATGTGTAA-NRATTYRR-NNNAtattgygygwrttsgstttyn--agagg--gwtrrcacacccncacncgcc-ay-accdhaaca-vhVaaccannNNN"

reps = 10000
countSlidingWindow(seq, reps)
countSlidingWindowSubstring(seq, reps, 1, 10)
countSlidingWindowSubstring2(seq, reps, 1, 10)
#Now trying by converting all chars to simplified version:
countSlidingWindowSubstringSimple(seq, reps, 1, 10)
countSlidingWindowSubstringSimplest(seq, reps, 1, 10)
