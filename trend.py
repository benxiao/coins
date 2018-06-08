


def mark_peaks(seq, max_tolerance=10):
    states = []
    for



MAX_TOLERANCE = 20
tolerance = 0
seq0 = list(prior_open[:-1])
seq1 = list(prior_open[1:])
print(len(seq0), len(seq1))

states = []
for v0, v1 in zip(seq0, seq1):
    if v1 > v0:
        if tolerance < MAX_TOLERANCE:
            tolerance += 1
    else:
        if tolerance > -MAX_TOLERANCE:
            tolerance -= 1

    if tolerance > 0:
        states.append('G')

    elif tolerance == 0:
        states.append("I")

    else:
        states.append("R")
