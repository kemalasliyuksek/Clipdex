# Clipdex – Text Expander and Snippet Manager

Clipdex is an **open-source text expander** that turns shortcuts starting with `:` into full text while you type.  
It ships with a modern PyQt6 interface and a background listener that works system-wide.

## Features

- `:` + *shortcut* + **Space** / **Enter** ⟶ *text expansion*  
- Undo last expansion with a single **Backspace**  
- Intuitive UI to add / edit / delete shortcuts  
- Instant search and live filtering  
- Snippets stored in a JSON file and auto-reloaded on change  
- Minimize to system tray and keep running in background  
- Cross-platform: Windows, macOS, Linux

## Quick Start

```bash
# 1. Clone repository
$ git clone https://github.com/kemalasliyuksek/clipdex.git
$ cd clipdex

# 2. (Optional) Create a virtual environment
$ python -m venv venv
$ source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
(venv) $ pip install -r requirements.txt

# 4. Run the application
(venv) $ python main.py
```

> **Note:** On Linux, you may need `sudo` or udev rules for the `keyboard` package to capture keystrokes.

## Usage

1. Click **Add** in the UI to create a new snippet.  
   Example: `mail` → `user@example.com`  
2. While typing anywhere, write `:mail` and press **Space** (or **Enter**) to expand.  
3. Made a mistake? Press **Backspace** once to undo the expansion and bring back `:mail`.

### System Tray

When you close the window, Clipdex minimizes to the system tray and keeps running.  
Right-click the tray icon and choose **Quit** to exit completely.

## Directory Structure

```text
Clipdex/
├─ clipdex_core/        # Background listener and snippet logic
│  ├─ listener.py       # Captures keyboard events & expands text
│  └─ snippet_manager.py# JSON read/write operations
├─ clipdex_gui/         # PyQt6-based GUI
│  ├─ main_window.py    # Main window and tabs
│  ├─ dialogs.py        # Add/Edit dialogs
│  └─ assets/           # App & tray icons
├─ snippets.json        # User snippets (comes with sample data)
├─ main.py              # Entry point that starts GUI + listener
└─ requirements.txt     # Project dependencies
```

## Developer Guide

- **Style:** Follow `black` & `flake8` conventions.  
- **Pull Requests:** Prefix titles with `[Feature]`, `[Fix]`, or `[Refactor]`.  
- **Tests:** Add unit tests for critical functions.

### Packaging (PyInstaller)

```bash
(venv) $ pyinstaller --onefile --noconsole --icon clipdex_gui/assets/app_icon.ico main.py
```

The resulting `dist/Clipdex.exe` can be distributed directly.

## Contributing

All **issues** and **pull requests** are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE).

---

# Clipdex – Metin Genişletici (Text Expander) ve Snippet Yöneticisi

Clipdex; klavyenizde `:` (iki nokta) karakteri ile başlayan kısayolları, yazarken otomatik olarak tam metne dönüştüren açık kaynaklı bir **metin genişletici** (text-expander) uygulamasıdır.  
PyQt6 ile geliştirilmiş modern bir grafik arayüzün yanı sıra, arka planda çalışan bir dinleyici (listener) sayesinde sistem genelinde kesintisiz çalışır.

## Özellikler

- `:` + *kısayol* + **Boşluk** / **Enter** ⟶ *metin genişler*  
- **Backspace** ile son yapılan genişletmeyi geri alma  
- Kısayol ekleme / düzenleme / silme işlemleri için sezgisel arayüz  
- Anında arama ve canlı filtreleme  
- Kısayolları JSON dosyasında saklama ve dosya değişikliklerini otomatik algılama  
- Sistem tepsisine küçülme (tray icon) ve arka planda çalışma  
- Çoklu platform desteği: Windows, macOS, Linux

## Hızlı Başlangıç

```bash
# 1. Depoyu klonlayın
$ git clone https://github.com/kemalasliyuksek/clipdex.git
$ cd clipdex

# 2. Sanal ortam oluşturun (önerilir)
$ python -m venv venv
$ source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Bağımlılıkları yükleyin
(venv) $ pip install -r requirements.txt

# 4. Uygulamayı çalıştırın
(venv) $ python main.py
```

> **Not:** Linux kullanıcılarının `keyboard` paketinin root olmadan dinleyici başlatabilmesi için `sudo` veya gerekli udev ayarlarını yapması gerekebilir.

## Kullanım

1. Arayüzde **Add** düğmesine tıklayarak yeni bir kısayol ekleyin.  
   Örnek: `mail` → `kullanici@eposta.com`  
2. Herhangi bir uygulamada yazarken `:mail` yazıp **boşluk** (veya **Enter**) tuşuna bastığınızda, metin otomatik olarak e-postaya dönüşür.  
3. Yanlışlıkla genişlettiniz mi? Bir kez **Backspace** tuşuna basın, Clipdex genişletmeyi geri alıp sizin için `:mail` kısayolunu tekrar yazar.

### Sistem Tepsisi

Pencereyi kapattığınızda Clipdex, sistem tepsisine küçülür ve arka planda çalışmaya devam eder.  
Tamamen çıkmak için tepsi simgesine sağ tıklayıp **Quit** seçeneğini kullanın.

## Dizin Yapısı

```text
Clipdex/
├─ clipdex_core/        # Arka plan dinleyici ve snippet mantığı
│  ├─ listener.py       # Klavye olaylarını yakalama & genişletme
│  └─ snippet_manager.py# JSON okuma / yazma işlemleri
├─ clipdex_gui/         # PyQt6 tabanlı grafik arayüz
│  ├─ main_window.py    # Ana pencere ve sekmeler
│  ├─ dialogs.py        # Ekle/Düzenle diyalogları
│  └─ assets/           # Uygulama ve tepsi ikonları
├─ snippets.json        # Kullanıcı kısayolları (örnek verilerle gelir)
├─ main.py              # GUI + dinleyiciyi başlatan giriş noktası
└─ requirements.txt     # Proje bağımlılıkları
```

## Geliştirici Rehberi

- **Stil:** `black` & `flake8` ile uyumlu kod yazın.  
- **Pull Request:** Konu başlığına `[Feature]`, `[Fix]` veya `[Refactor]` etiketi ekleyin.  
- **Test:** Kritik fonksiyonlar için birim testleri eklemeyi unutmayın.

### Paketleme (PyInstaller)

```bash
(venv) $ pyinstaller --onefile --noconsole --icon clipdex_gui/assets/app_icon.ico main.py
```

Oluşan `dist/Clipdex.exe` dosyasını doğrudan dağıtabilirsiniz.

## Katkıda Bulunun

Her türlü **issue** ve **pull request** memnuniyetle karşılanır!  
Büyük değişiklikler için önce konu açıp tartışmayı başlatmanız önerilir.

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---
