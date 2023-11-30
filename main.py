from openai import OpenAI
from config import *
import json
from io import BytesIO
from pydub import AudioSegment
from recorder import record
from pydub.playback import _play_with_simpleaudio as play_audio
import time


client = OpenAI(
    # # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
)

file_path = "data.json"

while True:

    with open(file_path, 'r') as file:
        loaded_data = json.load(file)

    chat_completion = client.chat.completions.create(
        messages=loaded_data,
        model="gpt-4",
    )

    answer = chat_completion.choices[0].message.content
    new_line = {"role": "assistant", "content": answer}
    loaded_data.append(new_line)
    
    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=answer,
    )


    audio_stream = BytesIO(response.read())

    # Create an AudioSegment from the binary data
    audio = AudioSegment.from_file(audio_stream)

    x = play_audio(audio)
    print("Nick --> ", end = "")
    for i in answer:
        print(i, end="", flush=True)
        time.sleep(0.05)

    while x.is_playing():
        pass


    record()

    audio_file= open("output.mp3", "rb")


    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print("\nYou--> " + transcript.text)
    
    new_line = {"role": "assistant", "content": transcript.text}

    loaded_data.append(new_line)

    with open(file_path, 'w') as file:
        json.dump(loaded_data, file, indent=4)



