import threading
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr

recognizer = sr.Recognizer()


def write_info(text: str) -> None:
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, text)
    output_text.config(state=tk.DISABLED)


def convert_audio():
    def recognize():
        with sr.Microphone() as source:
            write_info("Адаптируем шумы микрофона...\n")
            recognizer.adjust_for_ambient_noise(source)

            write_info("Говорите...\n")

            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="ru-RU")
                write_info(f"\n{text} \n\n")
            except sr.UnknownValueError:
                write_info("Не удалось разобрать аудиозапись.\n\n")
            except sr.RequestError as e:
                write_info(f"Ошибка при запросе к сервису Google Speech Recognition API; {e}\n\n")
            except sr.WaitTimeoutError:
                write_info("Распознавание речи завершилось по таймеру. В течение тайм-аута звук не получен.\n\n")

    # Запуск слушания и вывода информации на экран в отдельном потоке позволяет не блокировать основное окно и, тем
    # самым, позволяет выводить её своевременно.
    thread = threading.Thread(target=recognize)
    thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title("Николай Литвин ИКБО-__-__")

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=30, state=tk.DISABLED)
    output_text.pack(pady=10)

    convert_button = tk.Button(root, text="Запись", command=convert_audio)
    convert_button.pack(pady=5)

    root.mainloop()
