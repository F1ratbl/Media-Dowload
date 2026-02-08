# 🎬 Medya İndirici (Media Downloader)

[🇹🇷 Türkçe](#-türkçe) | [🇬🇧 English](#-english)

---

# 🇹🇷 Türkçe

Bu proje, YouTube videolarını hızlı ve kolay bir şekilde indirmeni sağlayan, modern ve şık arayüze sahip bir web uygulamasıdır. Arka planda güçlü Python kütüphaneleri çalışırken, ön yüzde kullanıcı dostu bir deneyim sunar.

## Özellikler

Bu uygulama ile şunları yapabilirsin:
- **Video Analizi:** Herhangi bir YouTube bağlantısını yapıştırıp videonun başlığını, kapağını, süresini ve izlenme sayısını anında görebilirsin.
- **Kalite Seçenekleri:** Videoyu farklı çözünürlüklerde (1080p, 720p vb.) indirebilirsin.
- **Sadece Ses İndirme:** Videoyu izlemek yerine sadece dinlemek istersen, ses dosyası olarak da indirebilirsin.
- **İndirme Geçmişi:** Daha önce indirdiğin dosyaların listesini ve detaylarını "Geçmiş" sekmesinde tutar.
- **Canlı İlerleme Takibi:** İndirme işleminin ne durumda olduğunu (yüzde kaç indiğini) anlık olarak takip edebilirsin.

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi çalıştırmanın iki yolu vardır:
1. **Docker ile (Önerilen)** - Hiçbir şey kurmadan tek komutla çalıştırın.
2. **Manuel Kurulum** - Python ve kütüphaneleri kendiniz kurarak çalıştırın.

### Yöntem 1: Docker ile Çalıştırma 🐳 (En Kolayı)

Bilgisayarınızda **Docker Desktop** yüklü olması yeterlidir. Python veya FFmpeg kurmanıza gerek kalmaz. Veritabanı (PostgreSQL) otomatik olarak kurulur.

1. Proje klasörüne gelin.
2. Terminale şu komutu yazın:

```bash
docker compose up --build
```

3. Kurulum bitince tarayıcıdan **`http://localhost:8000`** adresine gidin.
4. İndirdiğiniz dosyalar otomatik olarak bilgisayarınızdaki `downloads/` klasörüne düşecektir.

---

### Yöntem 2: Manuel Kurulum ⚙️

#### 1. Gereksinimler
Bilgisayarında **Python** yüklü olmalı. Ayrıca video işlemleri için **FFmpeg** gerekebilir (çoğu sistemde `yt-dlp` bunu halleder ama aklında olsun).

#### 2. Kütüphaneleri Yükle
Terminalini aç ve proje klasörüne gelip şu komutu çalıştır:

```bash
pip install -r requirements.txt
```

#### 3. Uygulamayı Başlat

```bash
uvicorn main:app --reload
```

Bu komutu yazdıktan sonra tarayıcını açıp `http://127.0.0.1:8000` adresine gidersen uygulamanın açıldığını göreceksin!

---

## 🗄️ Veritabanı ve Ayarlar

Bu proje, verilerini saklamak için güçlü ve güvenilir **PostgreSQL** veritabanını kullanır.
Tüm gizli ayarlar (şifreler, portlar) **`.env`** dosyasında saklanır.

---

## 🤔 "Neden URL Değişmiyor (Tek Sayfa)?"

Uygulamayı kullanırken fark etmiş olabilirsin; menüden "İndirilenler" veya "Geçmiş" sayfasına geçtiğinde tarayıcının adres çubuğundaki link (URL) değişmiyor. Hep ana sayfadasın gibi görünüyor. **Bunun sebebi uygulamanın "Single Page Application (SPA)" mantığına benzer, ancak çok daha basit bir yapıda çalışmasıdır.**

Bunu şöyle düşünebilirsin:
Elinin altında bir **kitap** yerine tek bir **büyük poster** var. Farklı sayfalara gitmek için sayfa çevirmiyorsun, sadece posterin o an bakmak istediğin kısmına ışık tutuyoruz, diğer kısımları karanlıkta (görünmez) bırakıyoruz.

**Teknik olarak:**
- Tüm "sayfalar" (Arama ekranı, Sonuçlar, Geçmiş vb.) aslında `index.html` dosyasının içinde en baştan beri yüklü duruyor.
- Sen bir butona bastığında, JavaScript kodları devreye girip "Şu kutuyu gizle (`hidden`), diğer kutuyu göster" diyor.
- Bu sayede sayfa yenilenmesine gerek kalmıyor, geçişler çok daha hızlı ve akıcı oluyor. Buna "Client-Side Navigation" (İstemci Taraflı Gezinme) diyoruz.

---

## 📂 Proje Yapısı (Hangi Dosya Ne İşe Yarıyor?)

Merak edenler için projede neler olduğunu da özetleyeyim:

- **`main.py`**: Web sunucusunu (FastAPI) başlatan, gelen istekleri karşılayan ve doğru yere yönlendiren ana dosya.
- **`worker.py`**: Videoları indiren, YouTube'dan bilgileri çeken ve tüm ağır işleri yapan kodlar burada.
- **`history.py` & `history.json`**: İndirdiğin dosyaların kaydını `json` formatında tutar ve yönetir.
- **`templates/index.html`**: Gördüğün o şık tasarım, butonlar ve animasyonlar burada. İçinde hem HTML (yapı), hem Tailwind (stil), hem de JavaScript (mantık) kodları var.
- **`downloads/`**: İndirilen dosyaların kaydedildiği klasör.
- **`docker-compose.yml` & `Dockerfile`**: Projenin Docker ile çalışmasını sağlayan dosyalar.
- **`.env`**: Gizli ayarların (veritabanı şifresi vb.) tutulduğu dosya.

---
Bu yazılım yalnızca eğitim ve kişisel araştırma amaçlı geliştirilmiştir. Yazılımın kullanımı sırasında YouTube Hizmet Şartları'na ve yerel telif hakkı yasalarına uyulması kullanıcının sorumluluğundadır.
---

# 🇬🇧 English

This project is a modern and stylish web application that allows you to download YouTube videos quickly and easily. While powerful Python libraries run in the background, it enables a user-friendly experience on the frontend.

## Features

With this application, you can:
- **Analyze Videos:** Paste any YouTube link to instantly view the video's title, thumbnail, duration, and view count.
- **Quality Options:** Download videos in various resolutions (1080p, 720p, etc.).
- **Audio Only Download:** If you prefer listening over watching, you can download just the audio file.
- **Download History:** Keep track of your previously downloaded files and their details in the "History" tab.
- **Live Progress Tracking:** Monitor the status of your downloads (percentage complete) in real-time.

---

## 🛠️ Installation and Usage

There are two ways to run the project:
1. **Using Docker (Recommended)** - Run with a single command without installing dependencies.
2. **Manual Installation** - Install Python and libraries manually.

### Method 1: Using Docker 🐳 (Easiest)

You only need **Docker Desktop** installed on your computer. No need to install Python or FFmpeg manually. Database (PostgreSQL) is installed automatically.

1. Navigate to the project folder.
2. Run the following command in terminal:

```bash
docker compose up --build
```

3. Once built, open **`http://localhost:8000`** in your browser.
4. Downloaded files will automatically appear in your local `downloads/` folder.

---

### Method 2: Manual Installation ⚙️

#### 1. Requirements
You must have **Python** installed on your computer. Additionally, **FFmpeg** might be required for video processing (in most cases `yt-dlp` handles this, but keep it in mind).

#### 2. Install Libraries
Open your terminal, navigate to the project folder, and run the following command:

```bash
pip install -r requirements.txt
```

#### 3. Start the Application

```bash
uvicorn main:app --reload
```

After running this command, open your browser and go to `http://127.0.0.1:8000` to see the application running!

---

## 🗄️ Database and Configuration

This project uses the robust **PostgreSQL** database to store your data.
All sensitive settings (passwords, ports) are stored in the **`.env`** file.

---

## 🤔 "Why Doesn't the URL Change? (Single Page)"

You might have noticed that when you switch to the "Downloads" or "History" pages from the menu, the link (URL) in the browser's address bar doesn't change. It looks like you're always on the home page. **This is because the application works on a logic similar to a "Single Page Application (SPA)", but in a much simpler structure.**

Think of it this way:
Instead of a **book** with multiple pages, you have a single **large poster**. To see different sections, you don't turn a page; we just shine a light on the part of the poster you want to see at that moment, leaving the other parts in the dark (hidden).

**Technically:**
- All "pages" (Search screen, Results, History, etc.) are actually loaded inside the `index.html` file from the start.
- When you click a button, JavaScript codes kick in and say "Hide this box (`hidden`), show that box".
- This eliminates the need for page refreshes, making transitions much faster and smoother. This is called "Client-Side Navigation".

---

## 📂 Project Structure (What Does Each File Do?)

Here is a summary of what's inside the project for those curious:

- **`main.py`**: The main file that starts the web server (FastAPI), handles incoming requests, and routes them to the right place.
- **`worker.py`**: Codes that download videos, fetch information from YouTube, and handle all the heavy lifting are here.
- **`history.py` & `history.json`**: It keeps and manages the record of your downloaded files in `json` format.
- **`templates/index.html`**: The face of the application. The stylish design, buttons, and animations you see are here. It contains HTML (structure), Tailwind (style), and JavaScript (logic) codes.
- **`downloads/`**: The folder where downloaded files are saved.
- **`docker-compose.yml` & `Dockerfile`**: Configuration files to run the project with Docker.
- **`.env`**: File where sensitive settings (like database password) are kept.

---
This software is developed solely for educational and personal research purposes. Compliance with YouTube's Terms of Service and local copyright laws is the sole responsibility of the user.
---
