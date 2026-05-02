import requests
import re

SOURCE_URL = "https://streams.uzunmuhalefet.com/lists/tr.m3u"

# CNN Türk - Manuel eklenen çalışan link
CNN_TURK_STATIC = """#EXTINF:-1 tvg-id="" tvg-name="CNN Türk" tvg-logo="https://raw.githubusercontent.com/fshmstr/Logos/master/Haber/CNN%20Turk.png" group-title="TV KANALLARI",CNN Türk
https://live.dogantv.com.tr/cnn_turk/cnn_turk.m3u8"""

# SS'lerinden çıkarılan tam kanal listesi
WANTED_CHANNELS = [
    "TRT 1", "TRT Haber", "TRT 2", "TRT Belgesel", "TRT Türk", "TRT Müzik", "Diyanet TV", 
    "TRT Çocuk", "TRT Diyanet Çocuk", "TRT 3 Spor", "TRT Spor Yıldız",
    "CNN Türk", "Habertürk", "NTV", "A Haber", "A Spor", "ATV", "TV8", "Show TV", 
    "Kanal D", "Star TV", "24 TV", "360 TV", "Kanal 7", "Beyaz TV", "TV 100", 
    "Ülke TV", "TGRT Haber", "Bloomberg HT", "TV 8.5", "DMAX", "Kardelen TV", 
    "Kocaeli TV", "Balkan Türk",
    "Halk TV", "Çiftçi TV", "Köy TV", "Erzurum Web TV", "TBMM TV", "Toprak TV", "TRT Avaz", 
    "DHA 1", "DHA 2", "İHA 1", "İHA 2", "Kanal 7 Avrupa", "Kanal Avrupa",
    "A Para", "A2", "ATV Avrupa", "Çay TV", "CGTN Belgesel", "CNBC-e", "Minika Çocuk",
    "Show Max", "Show Türk"
]

def generate_custom_m3u():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        lines = response.text.replace('\r', '').split('\n')
        
        source_channels = {}
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#EXTINF"):
                name = line.split(',')[-1].strip()
                if i + 1 < len(lines):
                    source_channels[name.lower()] = (line, lines[i+1].strip())
                i += 2
            else: i += 1
        
        custom_playlist = ["#EXTM3U"]
        for wanted in WANTED_CHANNELS:
            if wanted == "CNN Türk":
                custom_playlist.append(CNN_TURK_STATIC)
                continue
            
            w_low = wanted.lower()
            found_key = None
            # Esnek eşleşme: İsim tam tutmasa bile "HD" veya "[TR]" eklerini tolere eder
            for k in source_channels.keys():
                if w_low == k or f" {w_low} " in f" {k} " or k.startswith(f"{w_low} "):
                    found_key = k
                    break
            
            if found_key:
                info, url = source_channels[found_key]
                # Kategorileri SİL ve tek bir başlığa zorla
                new_info = re.sub(r'group-title="[^"]*"', '', info)
                new_info = new_info.replace('#EXTINF:-1', '#EXTINF:-1 group-title="TV KANALLARI"')
                custom_playlist.append(f"{new_info.strip()}\n{url}")

        with open("custom_playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(custom_playlist))
    except Exception as e: print(f"Hata: {e}")

if __name__ == "__main__":
    generate_custom_m3u()
