# generation
import math
import os
print("Setting current working directory to:", os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__))) 

def timestampify(seconds:float) -> str:
    """Convert seconds to timestamp format `00:00:00,000`"""
    milli = seconds % 1
    second = seconds % 60
    minutes = (seconds / 60) % 60
    hours = (seconds / (60 * 60))
    timestamp = f"{
        str(math.floor(hours)).zfill(2)
        }:{
            str(math.floor(minutes)).zfill(2)
            }:{
                str(math.floor(second)).zfill(2)
                },{
                    str(round(milli * 1000)).zfill(3)
                    }"
    return timestamp

def create_srt_format(subtitles:str, bpm:float, beats_per_line:float, beat_offset:float, millisecond_offset:float) -> list[str]:
    srt_format_lines = []
    starting_seconds = beat_offset * (60 / bpm) + millisecond_offset / 1000
    previous_seconds = starting_seconds

    for i, line in enumerate(str.split(subtitles, "\n")):
        print(f"Syncing #{i+1}/{len(str.split(subtitles, "\n"))} lines.\n{line}") # comment this if you hate it lol
        
        beat = beat_offset + beats_per_line * (i + 1) 
        seconds = beat * (60 / bpm) + millisecond_offset / 1000

        # srt formatting
        srt_format_lines.append(f"{i + 1}\n")
        srt_format_lines.append(f"{timestampify(previous_seconds)} --> {timestampify(seconds)}\n")
        srt_format_lines.append(line + "\n")
        srt_format_lines.append("\n")

        previous_seconds = seconds

    return srt_format_lines, timestampify(starting_seconds), timestampify(previous_seconds) # ending time

def write_to_file(file_location:str, content:list):
    with open(file_location, "a") as srt_file:
        srt_file.writelines(content)

def init_generation(source_location:str, destination_location:str, bpm:float, beats_per_line:float, beat_offset:float, millisecond_offset:float):
    # you can maybe generate multiple files using this function, if you need to.
    with open(source_location, "r") as text_file:
        subtitles = text_file.read()

    srt_format_lines, starting_timestamp, ending_timestamp = create_srt_format(subtitles, bpm, beats_per_line, beat_offset, millisecond_offset)

    write_to_file(destination_location, srt_format_lines)

    print(f"Finished synchronizing {len(str.split(subtitles, "\n"))} lines, starts at {starting_timestamp} , ends at {ending_timestamp}")

def interface():
    """Creates interface for user to type in configurations."""

    prompt_source_location = lambda : input("Raw text file directory (default = ./raw_texts.txt or drag your file in):\n") or "./raw_texts.txt"
    source_location = prompt_source_location()
    while True:
        if not os.path.exists(source_location):
            print("Source doesn't exist, make sure no other marks like '', " + '""' +", & are kept")
            source_location = prompt_source_location()
        else: break

    prompt_destination_location = lambda : input("Srt file directory (default = ./synchronized_captions.srt or drag your file in): ") or "./synchronized_captions.srt"
    destination_location = prompt_destination_location()
    while True:
        if os.path.splitext(destination_location)[1] != ".srt":
            print(f"Destination's extension is {os.path.splitext(destination_location)[1]}, it is required to be .srt")
            destination_location = prompt_destination_location()
        else: break

    if not os.path.exists(destination_location): print("Destination file will be created.")
    
    bpm = None
    while bpm == None:
        try:
            bpm = float(input("Beats per minute (required): "))
            if bpm <=0:
                bpm = None
                raise Exception("Less than or equal to 0")
        except:
            print("Please specify a valid beats per minute.")
    
    try: beats_per_line = float(input("Beats per line of text (default = 8): "))
    except: beats_per_line = 8
    try: beat_offset = float(input("Offset by how many beats (default = 0): "))
    except: beat_offset = 0
    try: millisecond_offset = float(input("Offset by how many milliseconds (default = 0): "))
    except: millisecond_offset = 0

    print(f"\nBpm = {bpm}\nBeats per line = {beats_per_line}\nOffset = {beat_offset} beat, {millisecond_offset}ms\nSource: {source_location}\nDestination: {destination_location}")

    def confirmation():
        match input("Proceed? (Y/n): ").lower():
            case "y":
                init_generation(source_location, destination_location, bpm, beats_per_line, beat_offset, millisecond_offset)
                print(f"Finished successfully, destination file at: {destination_location}")
                input("Press enter to exit")
            case "n":
                print("Restarting configuration prompts.")
                interface()
            case _:
                confirmation()
    confirmation()

interface()