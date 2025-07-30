# NewsBot-Python-ile-Otomatik-Haber-Payla-m-Botu
# NewsBot

NewsBot, Python diliyle geliştirilmiş bir otomatik haber çekme ve dağıtım botudur. Belirli haber kaynaklarından içerikleri alır ve istenilen platforma (örneğin Telegram) iletir. Gerçek zamanlı ya da belirlenen zaman aralıklarıyla çalışacak şekilde yapılandırılabilir.

## 📰 Özellikler

- 🔍 Haber kaynaklarından otomatik veri çekme (API, RSS veya web kazıyıcı)
- 📤 Telegram bot üzerinden kullanıcıya haber gönderme
- ⏰ Belirli zaman aralıklarında otomatik gönderim (örn. 30 dakikada bir)
- 🧾 Kullanıcının komutlarıyla güncel haberleri alma (`/haber`, `/teknoloji`, vs.)
- 🧠 Gelişmiş içerik özeti veya filtreleme (isteğe bağlı)
- 📈 Türkçe haberlerle uyumlu çalışma desteği

## 🛠️ Kullanılan Teknolojiler

- Python 3.x
- `python-telegram-bot` (veya `telebot`)
- `requests`
- `BeautifulSoup4`
- `schedule` (veya `apscheduler`)
- İsteğe bağlı olarak SerpAPI, OpenAI, NewsAPI gibi servisler

## ⚙️ Kurulum ve Kullanım

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/kullaniciadi/newsbot.git
   cd newsbot

