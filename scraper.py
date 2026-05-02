import requests
import re

SOURCE_URL = "https://streams.uzunmuhalefet.com/lists/tr.m3u"

# CNN Türk sabit bloğu - Tek kategori yaptık
CNN_TURK_STATIC = """#EXTINF:-1 tvg-id="" tvg-name="CNN Türk" tvg-logo="https://raw.githubusercontent.com/fshmstr/Logos/master/Haber/CNN%20Turk.png" group-title="Kendi Listem",CNN Türk
https://live.dogantv.com.tr/cnn_turk/cnn_turk.m3u8"""

# Kanalları tam olarak bu sırayla dizeceğiz
WANTED_CHANNELS = [
    "TRT 1", "TRT Haber", "TRT 2", "TRT Belgesel", "TRT Türk", "TRT Müzik",
    "TRT Çocuk", "TRT Diyanet Çocuk", "TRT 3 Spor", "TRT Spor Yıldız",
    "CNN Türk", "Habertürk", "NTV", "A Haber", "A Spor", "ATV", "TV8",
    "Show TV", "Kanal D", "Star TV", "24 TV", "360 TV", "Kanal 7", "Beyaz TV",
    "TV 100", "Ülke TV", "TGRT Haber", "Bloomberg HT", "Halk TV", "NOW TV",
    "TELE1", "teve2", "TLC", "DMAX", "TV 8.5", "CNBC-e", "Minika Çocuk", "Minika Go"
]

def generate_custom_m3u():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        content = response.text
        
        # Tüm kanalları ve linklerini regex ile yakalayalım
        entries = re.findall(r'(#EXTINF:.*?\n(http.*?))', content, re.DOTALL)
        
        custom_playlist = ["#EXTM3U"]
        
        for wanted in WANTED_CHANNELS:
            if wanted == "CNN Türk":
                custom_playlist.append(CNN_TURK_STATIC)
                continue
                
            for info, url in entries:
                # Kanal ismini virgülden sonra yakala
                channel_name_match = re.search(r',([^,]+)$', info)
                if channel_name_match:
                    actual_name = channel_name_match.group(1).strip()
                    # İsim tam tutuyorsa veya HD versiyonuysa
                    if wanted.lower() in actual_name.lower():
                        # Mevcut group-title ne olursa olsun SİL ve "Kendi Listem" YAP
                        new_info = re.sub(r'group-title="[^"]*"', 'group-title="Kendi Listem"', info)
                        # Eğer group-title hiç yoksa ekle
                        if 'group-title="' not in new_info:
                            new_info = new_info.replace('#EXTINF:-1', '#EXTINF:-1 group-title="Kendi Listem"')
                        
                        custom_playlist.append(f"{new_info.strip()}\n{url.strip()}")
                        break
            
        with open("custom_playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(custom_playlist))
            
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    generate_custom_m3u()
