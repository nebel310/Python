import sounddevice as sd
import wavio

def record(filename, duration=5, samplerate=44100):
    print(f"Recording audio for {duration} seconds...")
    
    # Запись аудио
    audio_data = sd.rec(int(duration * samplerate), samplerate, channels=1, dtype='int16')
    sd.wait()
    
    # Сохранение записанного аудио в файл
    wavio.write(filename, audio_data, samplerate, sampwidth=2)
    
    print(f"Audio recorded and saved as {filename}")

# Пример использования функции
