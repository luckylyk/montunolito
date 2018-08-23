from montunolito.converters.midi import encoder


def convert_to_midi(keyboard_sequence, tempo=None):
    track = 0
    channel = 8
    time = 0    # In beats
    duration = 1    # In beats
    volume = 100  # 0-127, as per the MIDI standard
    tempo *= 4

    midi = encoder.MIDIFile(2)
    midi.addTempo(track, time, tempo)
    for i, eighth in enumerate(keyboard_sequence):
        for pitch in eighth:
            midi.addNote(track, channel, pitch, time + i, duration, volume)

    return midi
