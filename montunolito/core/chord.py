

def get_new_chordgrid(lenght=32):
    return [None] * lenght


def deepcopy(chordgrid):
    chordgrid_copy = []
    for chord in chordgrid:
        if chord is None:
            chordgrid_copy.append(None)
            continue
        chordgrid_copy.append({k: v for k, v in chord.items()})
    return chordgrid_copy


def is_valid_chordgrid(chordgrid):
    return bool(chordgrid[0])
