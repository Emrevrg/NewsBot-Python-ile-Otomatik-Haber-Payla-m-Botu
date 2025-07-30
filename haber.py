import tkinter as tk
from tkinter import ttk, messagebox
import feedparser
import webbrowser
import random
import time
import platform
import os

# Kategoriye göre RSS kaynakları
RSS_CATEGORIES = {
    "Gündem": [
        "https://www.cnnturk.com/feed/rss/news",
        "https://rss.haberler.com/rss.asp?kategori=guncel",
        "https://www.hurriyet.com.tr/rss/gundem",
        "https://www.milliyet.com.tr/rss/rssNew/gundemRss.xml",
        "https://www.aa.com.tr/tr/rss/default?cat=guncel",
        "https://feeds.bbci.co.uk/turkce/rss.xml",
    ],
    "Ekonomi": [
        "https://www.hurriyet.com.tr/rss/ekonomi",
        "https://www.milliyet.com.tr/rss/rssNew/ekonomiRss.xml",
        "https://www.sondakika.com/rss/ekonomi.xml",
    ],
    "Spor": [
        "https://www.hurriyet.com.tr/rss/spor",
        "https://www.milliyet.com.tr/rss/rssNew/sporRss.xml",
        "https://www.fanatik.com.tr/rss",
    ]
}

class NewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📰 Python Haber Botu")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.current_index = 0
        self.mode = "guncel"
        self.guncel_haberler = []
        self.eski_haberler = []
        self.selected_category = tk.StringVar(value="Gündem")
        self.theme = "dark"

        self.create_widgets()
        self.apply_theme()
        self.load_news(initial=True)
        self.auto_refresh()

    def play_sound(self):
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 250)
        else:
            os.system('printf "\\a"')

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=5)

        ttk.Label(top_frame, text="Kategori: ").pack(side=tk.LEFT)
        cat_menu = ttk.OptionMenu(top_frame, self.selected_category, self.selected_category.get(),
                                  *RSS_CATEGORIES.keys(), command=lambda _: self.load_news(initial=True))
        cat_menu.pack(side=tk.LEFT, padx=5)

        self.theme_btn = ttk.Button(top_frame, text="🎨 Tema Değiştir", command=self.toggle_theme)
        self.theme_btn.pack(side=tk.LEFT, padx=10)

        self.title_label = ttk.Label(self.root, text="Yükleniyor...", font=("Arial", 16, "bold"), wraplength=760)
        self.title_label.pack(pady=10)

        self.summary_text = tk.Text(self.root, wrap=tk.WORD, height=18, font=("Arial", 12))
        self.summary_text.pack(padx=10, pady=5)
        self.summary_text.config(state=tk.DISABLED)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.prev_btn = ttk.Button(self.button_frame, text="⬅️ Önceki", command=self.prev_news)
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.open_btn = ttk.Button(self.button_frame, text="🌐 Haberi Aç", command=self.open_link)
        self.open_btn.grid(row=0, column=1, padx=10)

        self.next_btn = ttk.Button(self.button_frame, text="➡️ Sonraki", command=self.next_news)
        self.next_btn.grid(row=0, column=2, padx=10)

        self.mode_btn = ttk.Button(self.root, text="📚 Eski Haberlere Geç", command=self.toggle_mode)
        self.mode_btn.pack(pady=5)

    def apply_theme(self):
        if self.theme == "dark":
            self.root.configure(bg="#1e1e1e")
            self.summary_text.configure(bg="#252526", fg="#d4d4d4", insertbackground="white")
            self.style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
            self.style.configure("TButton", background="#333333", foreground="#ffffff")
        else:
            self.root.configure(bg="#f0f0f0")
            self.summary_text.configure(bg="#ffffff", fg="#000000", insertbackground="black")
            self.style.configure("TLabel", background="#f0f0f0", foreground="#000000")
            self.style.configure("TButton", background="#e0e0e0", foreground="#000000")

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()

    def load_news(self, initial=False):
        try:
            rss_urls = RSS_CATEGORIES[self.selected_category.get()]
            yeni_haberler = []
            for url in rss_urls:
                feed = feedparser.parse(url)
                yeni_haberler.extend(feed.entries[:10])  # En güncel 10 haber
            yeni_haberler = sorted(yeni_haberler, key=lambda x: x.published_parsed if 'published_parsed' in x else time.gmtime(), reverse=True)

            if not yeni_haberler:
                raise Exception("Haber bulunamadı.")

            if initial or not self.guncel_haberler:
                self.guncel_haberler = yeni_haberler
                self.current_index = 0
                self.show_news(self.guncel_haberler, 0)
            else:
                if yeni_haberler[0].link != self.guncel_haberler[0].link:
                    self.eski_haberler = self.guncel_haberler
                    self.guncel_haberler = yeni_haberler
                    self.current_index = 0
                    self.mode = "guncel"
                    self.mode_btn.config(text="📚 Eski Haberlere Geç")
                    self.play_sound()
                    messagebox.showinfo("Yeni Haber!", "🆕 Yeni haber geldi! Gösteriliyor...")
                    self.show_news(self.guncel_haberler, 0)
        except Exception as e:
            messagebox.showerror("Hata", f"Haberler yüklenemedi: {e}")

    def show_news(self, news_list, index):
        if index < 0 or index >= len(news_list):
            return
        entry = news_list[index]
        self.title_label.config(text=entry.title)
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, entry.get("summary", "Açıklama bulunamadı."))
        self.summary_text.config(state=tk.DISABLED)

        if self.mode == "guncel" and index == len(news_list) - 1:
            self.title_label.config(text="📰 Güncel haberler bunlardı. İsterseniz eski haberlere geçin.")

    def prev_news(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_news()

    def next_news(self):
        current_list = self.guncel_haberler if self.mode == "guncel" else self.eski_haberler
        if self.current_index < len(current_list) - 1:
            self.current_index += 1
            self.show_current_news()

    def open_link(self):
        current_list = self.guncel_haberler if self.mode == "guncel" else self.eski_haberler
        webbrowser.open(current_list[self.current_index].link)

    def toggle_mode(self):
        if self.mode == "guncel":
            if not self.eski_haberler:
                messagebox.showinfo("Bilgi", "Henüz eski haber bulunamadı.")
                return
            self.mode = "eski"
            self.mode_btn.config(text="📰 Güncel Haberlere Dön")
            self.current_index = 0
            self.show_news(self.eski_haberler, 0)
        else:
            self.mode = "guncel"
            self.mode_btn.config(text="📚 Eski Haberlere Geç")
            self.current_index = 0
            self.show_news(self.guncel_haberler, 0)

    def show_current_news(self):
        current_list = self.guncel_haberler if self.mode == "guncel" else self.eski_haberler
        self.show_news(current_list, self.current_index)

    def auto_refresh(self):
        self.root.after(300000, self.refresh_news)  # 5 dakikada bir yenile

    def refresh_news(self):
        self.load_news()
        self.auto_refresh()

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsApp(root)
    root.mainloop()
