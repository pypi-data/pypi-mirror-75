import sys
from source.backend.analyzer import *
from source.backend.file_to_fingerprint import filetofingerprint


# Algorithm taken from 'Winnowing: Local Algorithms for Document Fingerprinting'
def winnow(file_string, k, w):
    hashes = compute_hash(file_string, k)
    recorded = {}
    h2 = hashes.copy()
    # create the window of size 4
    h = [sys.maxsize for i in range(0, w)]
    r = 0
    minimum = 0
    global_pos = 0
    # loop through the hashes to find the minimum hash in every window
    for i in range(0, len(hashes)):
        r = (r + 1) % w
        h[r] = h2.pop(0)
        # if the minimum is the current index, check entire window for the minimum
        if minimum == r:
            for ind in scan_left_ind(r, w):
                if h[ind] < h[minimum]:
                    minimum = ind
            recorded = record(recorded, h[minimum], global_pos, w)
        else:  # check if the current index is the new minimum
            if h[r] < h[minimum]:
                minimum = r
                recorded = record(recorded, h[minimum], global_pos, w)
        global_pos += 1
    return recorded


# record the current hash and the its positioning
def record(recorded, minimum, global_pos, w):
    # determine if there is another hash in the same window already
    if global_pos < w and len(recorded) > 0:
        for rec in recorded.copy():
            # if there is, determine the true minimum and record it
            if minimum < rec:
                recorded.pop(rec)
                recorded[minimum] = [global_pos]
    else:
        if minimum in recorded:
            recorded[minimum] = recorded[minimum] + [global_pos]
        else:
            recorded[minimum] = [global_pos]
    return recorded


# create an array starting at the rightmost index of the current window
# continue until you hit the current index, r
def scan_left_ind(r, w):
    inds = []
    step = (r - 1) % w
    for i in range(0,4):
        inds.append(step)
        step = (step - 1 + w) % w
    return inds


# get all hashes from the file
# depricated: we now use winnow with a k value of 2 for getting all substrings
def compute_all(file_string, k):
    hashes = compute_hash(file_string, k)
    recorded = {}
    global_pos = 0
    # loop through the hashes to find the minimum hash in every window
    for fp_hash in hashes:
        if global_pos % 2 == 0:
            if fp_hash in recorded.keys():
                recorded[fp_hash] = recorded[fp_hash] + [global_pos]
            else:
                recorded[fp_hash] = [global_pos]
        global_pos += 1
    return recorded


# compute the k-gram hashes through a rolling hash function
def compute_hash(s, k):
    # setup the compute hash function
    ints = compute_ints(s)
    p = 31
    m = 10 ** 9 + 9
    # compute the p_pow values
    p_pow = compute_p_pow(k, p, m)
    final_pow = p_pow[k - 1]
    # compute the initial hash value
    hashes = [sum([num * power % m for num, power in zip(ints[0:k], p_pow)])]
    for i in range(0, len(s) - k):
        # compute the next hash value through the previous one
        hashes.append(int((hashes[i] - ints[i]) / p % m + (ints[k + i] * final_pow) % m))
    return hashes


# return the modified int value for the characters in the text
def compute_ints(s):
    ints = []
    for ch in s:
        ints.append(ord(ch) - ord('a') + 1)
    return ints


# compute the p_pow values
def compute_p_pow(k, p, m):
    p_pow = [1]
    for i in range(1, k):
        p_pow.append((p_pow[i-1] * p) % m)
    return p_pow


# Setup the winnowing function by removing all common characters and retrieving the k-gram hashes
def text_winnow_setup(text, k, w):
    # text to lowercase and remove all non-alphanumerics for text
    text = re.sub(r'\s+', '', text.lower())
    # return the output of the winnow function
    return winnow(text, k, w)


def text_compute_all_setup(text, k):
    # text to lowercase and remove all non-alphanumerics for text
    text = re.sub(r'\s+', '', text.lower())
    # return the output of the winnow function
    return compute_all(text, k)

# Wraps a list of filenames into filetofingerprint objects
def wrap_filenames(filenames):
    files = []
    filecount = 0
    for fnames in filenames:
        file = filetofingerprint(fnames, filecount, None, -1, {}, {}, {})
        files.append(file)
        filecount += 1
    return files

