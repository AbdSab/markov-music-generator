import mido

m = mido.MidiFile("new_song.mid")

for track in m.tracks:
        for msg in track:
            print msg