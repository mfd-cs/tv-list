import requests
import re

SOURCE_URL = "https://streams.uzunmuhalefet.com/lists/tr.m3u"

# CNN Türk sabit bloğu - Kategori sıfırlandı
CNN_TURK_STATIC = """#EXTINF:-1 tvg-id="" tvg-name="CNN Türk" tvg-logo="https://raw.githubusercontent.com/fshmstr/Logos/master/Haber/CNN%20Turk.png" group-title="TV KANALLARI",CNN Türk
https://live.dogantv.com.tr/cnn_turk/cnn_turk.m3u8"""

# SS'lerden çekilen tam kanal listesi (Sıralı)
WANTED_CHANNELS = [
    "TRT 1", "TRT Haber", "TRT 2", "TRT Belgesel", "TRT Türk", "TRT Müzik", "Diyanet TV", 
    "TRT Çocuk", "TRT Diyanet Çocuk", "TRT 3 Spor", "TRT Spor Yıldız",
    "CNN Türk", "Habertürk", "NTV", "A Haber", "A Spor", "ATV", "TV8", "Show TV", 
    "Kanal D", "Star TV", "24 TV", "360 TV", "Kanal 7", "Beyaz TV", "TV 100", 
    "Ülke TV", "TGRT Haber", "Bloomberg HT", "TV 8.5", "DMAX", "Kardelen TV", 
    "Kocaeli TV", "Ekol TV", "TLC", "TVNET", "NOW TV", "TELE1", "teve2", "Balkan Türk",
    "Halk TV", "Çiftçi TV", "Köy TV", "Çocuklara Özel TV", "Erzurum Web TV", "Euro D", 
    "Finans Türk", "TBMM TV", "Toprak TV", "TRT Avaz", "TRT EBA", "Yaban TV", 
    "Çizgi Film TV", "DHA 1", "DHA 2", "İHA 1", "İHA 2", "Kanal 7 Avrupa", "Kanal Avrupa",
    "A Para", "A2", "ATV Avrupa", "Çay TV", "CGTN Belgesel", "CNBC-e", "Minika Çocuk",
    "ABN Turkey", "Aile TV", "Al Zahra Turkic", "ASF TV", "Asr-ı Saadet TV", "Aşr-ı Şerif TV",
    "Belgesel TV", "Dost TV", "İkra TV", "İlahi TV", "İlmihal TV",
    "Show Max", "Show Türk" # Sona eklenenler
]

def generate_custom_m3u():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        content = response.text
        
        entries = re.findall(r'(#EXTINF:.*?\n(http.*?))', content, re.DOTALL)
        custom_playlist = ["#EXTM3U"]
        
        for wanted in WANTED_CHANNELS:
            if wanted == "CNN Türk":
                custom_playlist.append(CNN_TURK_STATIC)
                continue
                
            found = False
            for info, url in entries:
                channel_name_match = re.search(r',([^,]+)$', info)
                if channel_name_match:
                    actual_name = channel_name_match.group(1).strip()
                    # İsim eşleşmesi (HD veya normal hali)
                    if wanted.lower() == actual_name.lower() or f"{wanted} HD".lower() == actual_name.lower():
                        # Kategoriyi SİL ve "TV KANALLARI" yap (Kesin Çözüm)
                        new_info = re.sub(r'group-title="[^"]*"', '', info)
                        new_info = new_info.replace('#EXTINF:-1', '#EXTINF:-1 group-title="TV KANALLARI"')
                        
                        custom_playlist.append(f"{new_info.strip()}\n{url.strip()}")
                        found = True
                        break
        
        with open("custom_playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(custom_playlist))
        print("Liste SS'lere göre eksiksiz güncellendi!")
            
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    generate_custom_m3u()
