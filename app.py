
import mido
import json
import random

song = mido.MidiFile("music.mid")

N = 3
pattern = {}

def train():
    #Converting notes to list of bytes
    notes_bytes = []
    for track in song.tracks:
        for msg in track:
            with open("data.txt", "a") as out:
                out.write(str(msg) + "\n")
            if type(msg) is mido.messages.messages.Message:
                notes_bytes.append(msg.bytes())


    #Trainig
    l = len(notes_bytes)
    for i in range(l- N-1):

        #Convert to string
        to_string = ""
        for j in range(i, i+N):
            to_string += "".join([str(x) for x in notes_bytes[j]])
        
        #Check if current gram exist
        if to_string not in pattern:
            pattern[to_string] = []
        
        #Add occurance
        pattern[to_string].append(notes_bytes[i +N+1])

    #Save Training
    with open("data.json", "w") as out:
        json.dump(pattern, out)
    print notes_bytes

def generate():
    with open("data.json", "r") as out:
        pattern = json.load(out)

    MAX = 100
    new_song = mido.MidiFile()
    new_notes = [[192, 1], [176, 7, 127], [176, 10, 64]]

    for i in range(N, MAX):

        #Get last N notes as string
        to_string = ""
        for j in range(i-N, i):
            to_string += "".join([str(x) for x in new_notes[j]])

        #Save the new note
        if to_string in pattern:
            new_notes.append(random.choice(pattern[to_string]))
        else:
            new_notes.append(random.choice(pattern[random.choice(pattern.keys())]))

    new_track = mido.MidiTrack()
    new_song.tracks.append(new_track)
    for i in range(MAX):
        new_track.append(mido.Message.from_bytes(new_notes[i]))
        with open("data_gen.txt", "a") as out:
            out.write(str(mido.Message.from_bytes(new_notes[i])) + "\n")
    new_song.save("new_song.mid")
train()
generate()