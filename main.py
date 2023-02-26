from chatgpt_wrapper import ChatGPT
import speech_recognition as sr
from gtts import gTTS
from tempfile import NamedTemporaryFile
from playsound import playsound
import os


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
    tts.save("tmp.mp3")
    playsound(os.path.join(os.getcwd(), 'tmp.mp3'), True)


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
    print(f"__debug__ = {__debug__}")
    main()

