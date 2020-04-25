import argparse

parser = argparse.ArgumentParser()
parser.add_argument("tonic", help="The tonic note of the scale", type=str)
parser.add_argument("-f", "--flat", help="Flat", action="store_true")
parser.add_argument("-s", "--sharp", help="Sharp", action="store_true")
parser.add_argument("-d", "--delimiter", help="The symbol that separates the notes", type=str, default="  ")
#parser.add_argument("-v", "--verbose", help="Add extra information", type=str, default=False)
args = parser.parse_args()

accidentals = {
    "": "",
    "flat": b"\xe2\x99\xad".decode(),
    "sharp": b"\xe2\x99\xaf".decode(),
    "natural": b"\xe2\x99\xae".decode(),
    "doubleflat": b"\xe2\x99\xad\xe2\x99\xad".decode(),
    "doublesharp": b"\xe2\x99\xaf\xe2\x99\xaf".decode(),
    #doublesharp = b"\xf0\x9d\x84\xaa"
}

intervals = {
    "major": ( 1, 1, 0, 1, 1, 1, 0 ),
    #    "harmonic_minor": (1, 0, 1, 1, 0, 1.5, 0 ),
    "melodic_minor": ( 1, 0, 1, 1, 1, 1, 0 ),
    "natural_minor": ( 1, 0, 1, 1, 0, 1, 1 ),
}


def display_key_string():
    if not args.flat and not args.sharp:
        return ""
    else:
        return get_accidental()


def get_accidental():
    if args.flat:
        return accidentals["flat"]
    else:
        return accidentals["sharp"]


def get_major_pentatonic_scale(major_scale):
    # 1, 2, 3, 5, 6
    return major_scale[0], major_scale[:3] + major_scale[4:6]


def get_relative_minor_pentatonic_scale(major_scale):
    # 1, 3, 4, 5, 7
    minor_tonic, minor_scale = get_relative_minor_scale(major_scale)
    return minor_tonic, minor_scale[:1] + minor_scale[2:5] + minor_scale[6:7]


def get_relative_minor_scale(major_scale):
    front = major_scale[-3:]
    back = major_scale[1:-3]
    return front[0], front + back + front[:1]


def get_scale(intervals):
    notes = ( "A", "B", "C", "D", "E", "F", "G" )
    half_steps = ( "C", "F" )

    i = notes.index(args.tonic.upper())
    interval = intervals[0]
    partial_scale = notes[i+1:] + notes[:i]

    # Note that `get_accidental()` can't be called here because we don't
    # want the empty string (the default) to return a "sharp".
    # Else, the key of E would have its tonic changed to E♯.
    tonic = args.tonic.upper() + display_key_string()
    carried = bool(display_key_string())

    scale = [tonic]
    acc = get_accidental()

    # C natural and all sharps.
    if not args.flat and not args.sharp or args.sharp:
        for idx, note in enumerate(partial_scale):
            i = intervals[idx]
            if i is 1 and note in half_steps or \
                i is 1 and note not in half_steps and carried or \
                note in half_steps and carried:
                    carried = True
                    scale.append(note + acc)
            else:
                carried = False
                scale.append(note)

    # All flats.
    if args.flat:
        for idx, note in enumerate(partial_scale):
            i = intervals[idx]
            if i is 1 and carried and note not in half_steps or \
                i is 0 and not carried and note not in half_steps or \
                i is 0 and carried and note in half_steps:
                    carried = True
                    scale.append(note + acc)
#            elif i is 1 and carried and note in half_steps or \
#                i is 1 and not carried and note not in half_steps:
            else:
                carried = False
                scale.append(note)

    scale.append(tonic)
    return tonic, scale


try:
    tonic, major_scale = get_scale(intervals["major"])

    print(args.tonic.upper() + display_key_string() + " major:")
    print(args.delimiter.join(major_scale))

    _, major_pentatonic_scale = get_major_pentatonic_scale(major_scale)
    print("\n" + tonic + " major pentatonic:")
    print("    ".join(major_pentatonic_scale))

    relative_minor_tonic, minor_scale = get_relative_minor_scale(major_scale)
    print("\n" + "".join(relative_minor_tonic) + " relative minor:")
    print("    ".join(minor_scale))

    _, minor_pentatonic_scale = get_relative_minor_pentatonic_scale(major_scale)
    print("\n" + "".join(relative_minor_tonic) + " minor pentatonic scale:")
    print("    ".join(minor_pentatonic_scale))
except ValueError as err:
    print("[ERROR] The tonic note must be in the range A..G")

