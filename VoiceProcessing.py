import speech_recognition as sr
from difflib import SequenceMatcher


def extract_command(file):
    control_commands = {
        "forward":  ["forward",  "front",      "move forward",  "go ahead", "advance",      "proceed",      "head forward"],
        "backward": ["backward", "back",       "move backward", "go back",  "retreat",      "recede",       "head backward"],
        "left":     ["left",     "turn left",  "move left",     "go left",  "rotate left",  "swerve left",  "steer left"],
        "right":    ["right",    "turn right", "move right",    "go right", "rotate right", "swerve right", "steer right"]}

    init_rec = sr.Recognizer()
    print("Let's speak!!")

    # with sr.Microphone() as source:
    with sr.AudioFile(file) as source:
        print(source)
        audio_data = init_rec.record(source)
        # audio_data = init_rec.record(source, duration=5)
        print("Recognizing your text.............")
        try:
            text = init_rec.recognize_google(audio_data)
            print(f"I think you said '{text}'")
            max_score = 0
            command = ""
            for key, values in control_commands.items():
                for value in values:
                    score = SequenceMatcher(None, text, value).ratio()
                    if score > max_score:
                        max_score = score
                        command = key
            print(
                f"The best matching command is '{command}' with a score of {max_score:.2f}")
            if max_score >= 0.4:
                return command
            return None
        except:
            print("error")
            return None

if __name__ == "__main__":
    extract_command("voice_save/voice.wav")