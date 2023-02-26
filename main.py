import time
from chatgpt_wrapper import ChatGPT
import speech_recognition as sr
from gtts import gTTS
from tempfile import NamedTemporaryFile
from vlc import MediaPlayer


def get_prompt(lang: str):
    r = sr.Recognizer()
    with sr.Microphone() as src:
        audio = r.listen(src)
    prompt = r.recognize_google(audio, language=lang)
    if __debug__:
        print("google thinks you said: ", prompt)
    return prompt


def get_response(prompt: str):
    bot = ChatGPT()
    response = bot.ask(prompt)
    if __debug__:
        print("chatgpt responds with: ", response)
    return response


def output_audio(response: str, lang: str):
    tts = gTTS(response, lang=lang)
    with NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        print(f.name)
        tts.write_to_fp(f)
    player = MediaPlayer(f.name)
    player.play()
    time.sleep(1)
    if __debug__:
        print(f"audio length: {player.get_length()}ms")
    time.sleep(player.get_length() / 1000)


def main():
    lang = input("which language will you use (en-US, zh-CN, etc.):")
    loop = True
    while loop:
        prompt = get_prompt(lang)
        if prompt in ("exit", "退出"):
            loop = False
        response = get_response(prompt)
        output_audio(response, lang.split('-')[0])


if __name__ == '__main__':
    main()
