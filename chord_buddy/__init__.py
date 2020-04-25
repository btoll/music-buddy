import argparse
import music_buddy.scale_buddy

parser = argparse.ArgumentParser()
parser.add_argument("tonic", help="The tonic note of the chord", type=str)
parser.add_argument("-f", "--flat", help="Flat", action="store_true")
parser.add_argument("-s", "--sharp", help="Sharp", action="store_true")
parser.add_argument("-d", "--delimiter", help="The symbol that separates the notes", type=str, default="  ")
#parser.add_argument("-v", "--verbose", help="Add extra information", type=str, default=False)
args = parser.parse_args()


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


def get_chord(intervals):
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
    print("hi")
except ValueError as err:
    print("[ERROR] The tonic note must be in the range A..G")

