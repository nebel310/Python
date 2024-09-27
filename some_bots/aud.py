import pyaudio
import wave

# Установите параметры для записи аудио
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5  # Длительность записи в секундах
OUTPUT_FILENAME = "запись.wav"

# Создайте объект PyAudio
audio = pyaudio.PyAudio()

# Откройте поток для записи
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Запись...")

frames = []

# Запись аудио
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Запись завершена.")

# Закройте поток
stream.stop_stream()
stream.close()
audio.terminate()

# Сохраните запись в файл
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Запись сохранена в {OUTPUT_FILENAME}")