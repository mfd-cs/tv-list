import requests

SOURCE_URL = "https://streams.uzunmuhalefet.com/lists/tr.m3u"

# CNN Türk için kullandığımız çalışan özel link
CNN_TURK_STATIC = """#EXTINF:-1 tvg-id="" tvg-name="CNN Türk" tvg-logo="https://raw.githubusercontent.com/fshmstr/Logos/master/Haber/CNN%20Turk.png" group-title="Haber",CNN Türk
https://live.dogantv.com.tr/cnn_turk/cnn_turk.m3u8"""

WANTED_CHANNELS = [
    "TRT 1", "TRT Haber", "TRT 2", "TRT Belgesel", "TRT Türk", "TRT Müzik",
    "TRT Çocuk", "TRT Diyanet Çocuk", "TRT 3 Spor", "TRT Spor Yıldız",
    "CNN Türk",
    "Habertürk", "NTV", "A Haber", "A Spor", "ATV", "TV8",
    "Show TV", "Kanal D", "Star TV", "24 TV", "360 TV", "Kanal 7", "Beyaz TV",
    "TV 100", "Ülke TV", "TGRT Haber", "Bloomberg HT", "Halk TV", "NOW TV",
    "TELE1", "teve2", "TLC", "DMAX", "TV 8.5", "CNBC-e", "Minika Çocuk", "Minika Go"
]

def generate_custom_m3u():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        lines = response.text.splitlines()
        custom_playlist = ["#EXTM3U"]
        for wanted in WANTED_CHANNELS:
            if wanted == "CNN Türk":
                custom_playlist.append(CNN_TURK_STATIC)
                continue
            i = 0
            while i < len(lines):
                if lines[i].startswith("#EXTINF") and f',{wanted}' in lines[i]:
                    custom_playlist.append(lines[i])
                    if i + 1 < len(lines):
                        custom_playlist.append(lines[i+1])
                    break
                i += 1
        with open("custom_playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(custom_playlist))
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    generate_custom_m3u()
