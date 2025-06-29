
<div align="center">
  <img src="https://raw.githubusercontent.com/kemalasliyuksek/Clipdex/main/clipdex_gui/assets/icon_package/icon_256x256.png" alt="Clipdex Logo" width="150"/>
  <br/>
  <p>
    <strong>Sistem genelinde çalışan, modern ve açık kaynaklı bir metin genişletici (Text Expander).</strong>
  </p>
  <p>
    <em><strong>A modern, open-source, and system-wide text expander.</strong></em>
  </p>
  <p>
    <a href="https://github.com/kemalasliyuksek/clipdex/blob/main/LICENSE"><img src="https://img.shields.io/github/license/kemalasliyuksek/clipdex?style=for-the-badge" alt="License"></a>
    <a href="#"><img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python Version"></a>
    <a href="#"><img src="https://img.shields.io/badge/PyQt-6-orange?style=for-the-badge&logo=qt" alt="PyQt6"></a>
    <a href="https://github.com/kemalasliyuksek/clipdex/issues"><img src="https://img.shields.io/github/issues/kemalasliyuksek/clipdex?style=for-the-badge" alt="Issues"></a>
  </p>
</div>

---

> ### 📢 Windows Release (v1.0.0)
> The executable file for Windows is now available for download from the [**Releases**](https://github.com/kemalasliyuksek/clipdex/releases) section.
> 
> ### 📢 Windows Sürümü (v1.0.0)
> Windows için çalıştırılabilir dosya şimdi [**Releases**](https://github.com/kemalasliyuksek/clipdex/releases) bölümünden indirilebilir.


## 🇬🇧 English

Clipdex is an open-source text expander that turns your custom shortcuts into full text snippets as you type, system-wide. It comes with a modern PyQt6 interface and a background listener that works seamlessly across all applications.

### ✨ Features

-   **Smart Expansion**: Type a shortcut like `:mail` and press `Space` or `Enter` to expand it into your predefined text (e.g., `your.email@example.com`).
-   **Undo Functionality**: Made a mistake? A single `Backspace` right after an expansion will undo it and bring back your shortcut.
-   **Modern UI**: An intuitive interface built with PyQt6 to easily add, edit, and delete your snippets.
-   **Instant Search**: Live filtering to quickly find the shortcut you need.
-   **System Tray Integration**: Clipdex runs quietly in the system tray. Close the window, and it will keep running in the background.
-   **Cross-Platform**: Works on Windows, macOS, and Linux.
-   **Import/Export**: Easily backup and restore your snippets.

> **Note for Windows Users (v1.0.0):** The Windows executable for version 1.0.0 is now available. Some antivirus programs may flag the application as a potential threat (a "false positive"). This is due to the nature of system-wide keyboard listening packages (`pynput` and `keyboard`) used to expand text everywhere. Clipdex is completely safe to use. As an open-source project, you are welcome to review the entire codebase to verify its functionality.

### 🚀 Quick Start

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kemalasliyuksek/clipdex.git
    cd clipdex
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

> **Note:** On Linux, you might need to run the application with `sudo` for the keyboard listener to work correctly.

### 🛠️ How to Use

1.  Launch the application and click the **Add** button to create a new snippet.
2.  Assign a memorable shortcut (e.g., `github`) to a longer piece of text (e.g., `https://github.com/your-username`).
3.  Go to any text field in any application, type `:github`, and press `Space` or `Enter`.
4.  Watch the magic happen! The shortcut will be replaced by the full text.

### 🏗️ Technologies Used

-   **Backend**: Python
-   **GUI**: PyQt6
-   **Keyboard Listening**: `pynput` & `keyboard` packages

### 📁 Project Structure

```
Clipdex/
├── clipdex_core/          # Core logic for the listener and snippet management
│   ├── listener.py        # Captures keyboard events & expands text
│   ├── snippet_manager.py # Manages reading/writing snippets to JSON
│   └── config_manager.py  # Handles application configuration
├── clipdex_gui/           # PyQt6 GUI files
│   ├── main_window.py     # Main application window and tabs
│   ├── dialogs.py         # Add/Edit snippet dialogs
│   └── assets/            # Icons and other resources
├── snippets.json          # Your custom snippets
├── main.py                # Application entry point
└── requirements.txt       # Python dependencies
```

### 🤝 Contributing

I'm open to any contributions! You can open an **issue** or submit a **pull request** to contribute to the project. For major changes, please open an issue first to discuss what you want to change.

### 📜 License

This project is licensed under the [MIT License](https://github.com/kemalasliyuksek/clipdex/blob/main/LICENSE).

### 👤 Contact

-   **Kemal Aslıyüksek**
-   **GitHub**: [@kemalasliyuksek](https://github.com/kemalasliyuksek)
-   **Email**: [kemal@kemalasliyuksek.com](mailto:kemal@kemalasliyuksek.com)
-   **Web Site**: [kemalasliyuksek.com](https://kemalasliyuksek.com)

---

## 🇹🇷 Türkçe

Clipdex, sık kullandığınız metinleri sizin belirlediğiniz kısayollara dönüştüren, siz yazarken sistem genelinde çalışan, açık kaynaklı bir **metin genişletici** (text-expander) uygulamasıdır. PyQt6 ile geliştirilmiş modern bir arayüze ve tüm uygulamalarda sorunsuz çalışan bir arka plan dinleyiciye sahiptir.

### ✨ Özellikler

-   **Akıllı Genişletme**: `:mail` gibi bir kısayol yazıp `Boşluk` veya `Enter`'a basarak bunu önceden tanımlanmış metninize (ör. `mailadresiniz@ornek.com`) dönüştürün.
-   **Geri Alma Fonksiyonu**: Hata mı yaptınız? Genişletmeden hemen sonra tek bir `Backspace` tuşuna basmak, işlemi geri alır ve kısayolunuzu geri getirir.
-   **Modern Arayüz**: Kısayollarınızı kolayca eklemek, düzenlemek ve silmek için PyQt6 ile oluşturulmuş sezgisel bir arayüz.
-   **Anında Arama**: İhtiyacınız olan kısayolu hızla bulmak için canlı filtreleme.
-   **Sistem Tepsisi Entegrasyonu**: Clipdex, sistem tepsisinde sessizce çalışır. Pencereyi kapattığınızda arka planda çalışmaya devam eder.
-   **Çapraz Platform**: Windows, macOS ve Linux'ta çalışır.
-   **İçe/Dışa Aktarma**: Kısayollarınızı kolayca yedekleyin ve geri yükleyin.

> **Windows Kullanıcıları için Not (v1.0.0):** Windows için 1.0.0 sürümü yayınlandı. Bazı antivirüs programları, uygulamayı potansiyel bir tehdit olarak işaretleyebilir (hatalı pozitif bildirim). Bu durum, metin genişletme özelliğinin sistem genelinde çalışabilmesi için kullanılan klavye dinleme paketlerinden (`pynput` ve `keyboard`) kaynaklanmaktadır. Clipdex'in kullanımı tamamen güvenlidir. Açık kaynaklı bir proje olduğu için, işlevselliğini doğrulamak üzere tüm kod tabanını inceleyebilirsiniz.

### 🚀 Hızlı Başlangıç

1.  **Depoyu klonlayın:**
    ```bash
    git clone https://github.com/kemalasliyuksek/clipdex.git
    cd clipdex
    ```

2.  **Sanal ortam oluşturun ve aktif edin (önerilir):**
    ```bash
    # Windows için
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux için
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Bağımlılıkları yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uygulamayı çalıştırın:**
    ```bash
    python main.py
    ```

> **Not:** Linux'ta, klavye dinleyicisinin doğru çalışması için uygulamayı `sudo` ile çalıştırmanız gerekebilir.

### 🛠️ Nasıl Kullanılır?

1.  Uygulamayı başlatın ve yeni bir kısayol oluşturmak için **Ekle** düğmesine tıklayın.
2.  Uzun bir metin parçasına (ör. `https://github.com/kullanici-adiniz`) hatırlanabilir bir kısayol (ör. `github`) atayın.
3.  Herhangi bir uygulamadaki herhangi bir metin alanına gidin, `:github` yazın ve `Boşluk` veya `Enter`'a basın.
4.  Kısayolunuzun anında tam metne dönüştüğünü görün!

### 🏗️ Kullanılan Teknolojiler

-   **Backend**: Python
-   **GUI**: PyQt6
-   **Klavye Dinleme**: `pynput` & `keyboard` paketleri

### 📁 Proje Yapısı

```
Clipdex/
├── clipdex_core/          # Dinleyici ve snippet yönetimi için çekirdek mantık
│   ├── listener.py        # Klavye olaylarını yakalar ve metni genişletir
│   ├── snippet_manager.py # JSON'a snippet'leri okuma/yazma işlemlerini yönetir
│   └── config_manager.py  # Uygulama yapılandırmasını yönetir
├── clipdex_gui/           # PyQt6 GUI dosyaları
│   ├── main_window.py     # Ana uygulama penceresi ve sekmeler
│   ├── dialogs.py         # Kısayol ekle/düzenle iletişim kutuları
│   └── assets/            # Simgeler ve diğer kaynaklar
├── snippets.json          # Özel kısayollarınız
├── main.py                # Uygulama giriş noktası
└── requirements.txt       # Python bağımlılıkları
```

### 🤝 Katkıda Bulunma

Her türlü katkıya açığım! Projeyi geliştirmek için **issue** açabilir veya **pull request** gönderebilirsiniz. Büyük değişiklikler için lütfen önce bir issue açarak neyi değiştirmek istediğinizi tartışalım.

### 📜 Lisans

Bu proje [MIT Lisansı](https://github.com/kemalasliyuksek/clipdex/blob/main/LICENSE) ile lisanslanmıştır.

### 👤 İletişim

-   **Kemal Aslıyüksek**
-   **GitHub**: [@kemalasliyuksek](https://github.com/kemalasliyuksek)
-   **Email**: [kemal@kemalasliyuksek.com](mailto:kemal@kemalasliyuksek.com)
-   **Web Sitesi**: [kemalasliyuksek.com](https://kemalasliyuksek.com)