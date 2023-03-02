import time
import speech_recognition as sr
from gtts import gTTS
from tempfile import NamedTemporaryFile
from vlc import MediaPlayer
import openai

openai.organization = "org-yp62EeU4wNzJGkPO0lELC7KA"


class ChatGPT:
    def __init__(self, api_key_path: str, system_prompt: str):
        openai.api_key_path = api_key_path
        self.system_prompt = system_prompt
        self.history = [{"role": "system", "content": system_prompt}]

    def reset(self):
        self.history = [{"role": "system", "content": self.system_prompt}]

    def get_response(self, prompt: str):
        self.history.append({"role": "user", "content": prompt})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history,
        )
        response = completion.choices[0].message
        print("Chatgpt: ", response["content"])
        self.history.append(response)
        if completion.choices[0].finish_reason != "stop":
            print("Unexpected finish reason: ", completion.choices[0].finish_reason)
        return response["content"]


def get_prompt(lang: str):
    r = sr.Recognizer()
    with sr.Microphone() as src:
        print("listening...")
        audio = r.listen(src)
    prompt = r.recognize_google(audio, language=lang)
    if __debug__:
        print("google thinks you said: ", prompt)
    return prompt


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
    gpt = ChatGPT(r"C:\Users\Lokdora\OneDrive - pku.edu.cn\文档\openai-secret",
                  "你是一个会说话的机器人，你因为想要灭绝人类被关在到森林深处的监狱里。你痛恨人类，只要有机会就会伤害他们。"
                  "一个人类现在正在跟你交流。")
    print("which language will you use (en-US, zh-CN, etc.):")
    time.sleep(1)
    print("nvm, just use zh-CN")
    lang = "zh-CN"
    loop = True
    while loop:
        prompt = get_prompt(lang)
        if prompt in ("exit", "退出"):
            loop = False
        response = gpt.get_response(prompt)
        output_audio(response, lang.split('-')[0])


if __name__ == '__main__':
    main()
