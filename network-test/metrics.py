def calculate_rate(nbytes, seconds):
    nbits = nbytes * 8
    if nbits >= 1000000000:
        return nbits / 1000000000, 'G'
    elif nbits >= 1000000:
        return nbits / 1000000, 'M'
    else:
        return nbits / 1000, 'K'
    