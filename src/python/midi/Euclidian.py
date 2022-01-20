import math


precomputed_euclidian_patterns = []


# (private) compute full set of eclidian patterns for given length, represent these as bit patterns
def _compute_euclidian_patterns(length):
    patterns = [0] * (length+1)
    for count in range(0,length+1):
        pat = 0
        for i in range(0,count):
            pos = math.floor(i*length/count)
            pos = pos if pos<length else length-1
            pat = pat | (1 << pos)
        patterns[count] = pat
    return patterns

# return a collection of patterns of varying density starting from the given pattern
# the returned patterns with start with 0 triggers, increase in number until it matches
# the start_pattern, then continue until every step is a trigger.


# return full set of eclidian patterns for given length
def get_euclidian_patterns(length):
    while len(precomputed_euclidian_patterns) <= length:
        precomputed_euclidian_patterns.append(None)
    if precomputed_euclidian_patterns[length]:
        return precomputed_euclidian_patterns[length]
    precomputed_euclidian_patterns[length] = _compute_euclidian_patterns(length)
    return precomputed_euclidian_patterns[length]


def number_to_pattern(x,length):
    s = [' '] * length
    for i in range(0,length):
        if x&1:
            s[i] = 'x'
        x = x>>1
    return ''.join(s)


def pattern_to_number(s):
    x = 0
    for i in range(len(s)-1,-1,-1):
        x = x<<1
        if s[i] != ' ' and s[i] != '.':
            x = x | 1
    return x


def count_triggers(x):
    count = 0
    while x:
        count = count + (x & 1)
        x = x>>1
    return count


def _densifier(start_pattern_num, pattern_length):
    patterns = get_euclidian_patterns(pattern_length)
    patterns_rev = patterns.copy()
    patterns_rev.reverse()
    start_trigger_count = 0
    start_trigger_count = count_triggers(start_pattern_num)

    # empty pattern
    new_patterns = [0] * (pattern_length+1)
    # first build from 1 to start_pattern
    for target in range(1, start_trigger_count):
        for pattern in patterns_rev:
            new_pattern = pattern & start_pattern_num
            if count_triggers(new_pattern) <= target:
                new_patterns[target] = new_pattern
                break
    # original
    new_patterns[start_trigger_count] = start_pattern_num
    # build up to all triggers
    for target in range(start_trigger_count+1, pattern_length+1):
        for pattern in patterns:
            new_pattern = pattern | start_pattern_num
            if count_triggers(new_pattern) >= target:
                new_patterns[target] = new_pattern
                break
    # TODO deal with places where we add/subtract 2 instead of 1
    # TODO preserve accents
    return new_patterns


def densifier(pat):
    num_patterns = _densifier(pattern_to_number(pat), len(pat))
    ret = []
    for np in num_patterns:
        ret.append(number_to_pattern(np,len(pat)))
    return ret


if __name__ == "__main__":
    for p in get_euclidian_patterns(15):
        print(number_to_pattern(p,15))
    print()
    for i in range(0,16):
        print(number_to_pattern(i,16), pattern_to_number(number_to_pattern(i,16)))
    print()
    pat = "X xx      xx    X xx      xx    "
    print(pat.upper())
    print('\n'.join(densifier(pat)))