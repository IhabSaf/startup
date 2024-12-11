import pyaudio
import wave
import requests
import os

# API-sleutel voor Audd.io
API_KEY = '6ac3c8cb6a25baeb0f56da8e313bc633'  # Vergeet niet je eigen API-sleutel in te vullen

# Functie om audio op te nemen van de microfoon
def record_audio(filename="C:\\Users\\Ihab\\Documents\\mijn_opnames\\output.wav", duration=30):
    try:
        # Verbeterde opnameparameters voor de hoogste kwaliteit
        sample_rate = 20000  # Verhoogde samplefrequentie (96000 Hz voor hoge kwaliteit)
        chunk_size = 1024    # Grotere chunk_size voor meer gedetailleerde opname
        channels = 2         # Stereo-audio (2 kanalen)
        format = pyaudio.paFloat32  # 32-bit float audio voor maximale kwaliteit

        # Initialiseer pyaudio
        p = pyaudio.PyAudio()

        # Controleer of microfoon beschikbaar is
        device_count = p.get_device_count()
        if device_count == 0:
            print("Geen audioapparaten gevonden. Controleer je microfooninstellingen.")
            return None

        # Start de opname
        stream = p.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

        print("Opname gestart...")

        frames = []

        # Neem audio op voor de opgegeven duur
        for _ in range(0, int(sample_rate / chunk_size * duration)):
            data = stream.read(chunk_size)
            frames.append(data)

        print("Opname gestopt.")

        # Stop de stream en sluit pyaudio
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Zorg ervoor dat de opslagmap bestaat
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Sla de opname op als een WAV-bestand op de gewenste locatie
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

        print(f"Audio opgeslagen als {filename}")
        return filename

    except Exception as e:
        print(f"Er is een fout opgetreden bij de opname: {e}")
        return None

# Functie om muziek te herkennen via Audd.io API
def recognize_music(file_path):
    if file_path is None:
        print("Geen bestand gevonden om te herkennen.")
        return

    url = "https://api.audd.io/"
    
    # Open het audiobestand dat je wilt herkennen
    try:
        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()

        # Form-data voor de API-aanroep
        data = {
            'api_token': API_KEY,
            'return': 'apple_music,spotify',  # Extra gegevens die je wilt ontvangen (bijv. Apple Music, Spotify-link)
        }

        # Bestanden om te uploaden
        files = {
            'file': audio_data
        }

        # Verzenden van het bestand naar de Audd.io API
        response = requests.post(url, data=data, files=files)

        if response.status_code == 200:
            result = response.json()
            
            if result.get('status') == 'success' and result.get('result'):
                song = result['result']
                print(f"Muziek herkend!")
                print(f"Artiest: {song['artist']}")
                print(f"Nummer: {song['title']}")
                print(f"Album: {song.get('album', 'Onbekend')}")
                print(f"Apple Music Link: {song.get('apple_music', 'Niet beschikbaar')}")
                print(f"Spotify Link: {song.get('spotify', 'Niet beschikbaar')}")
            else:
                print("Geen muziek herkend.")
        else:
            print(f"Fout bij muziekherkenning: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Er is een fout opgetreden bij de muziekherkenning: {e}")

# Functie om opnames te maken en te herkennen
def record_and_recognize(duration=30):
    # Specificeer het pad naar de gewenste opslaglocatie
    filename = "C:\\Users\\Ihab\\Documents\\mijn_opnames\\output.wav"  # Verander dit naar jouw gewenste locatie
    file_path = record_audio(filename, duration)
    recognize_music(file_path)

# Voer de opname en herkenning uit
record_and_recognize(duration=30)
