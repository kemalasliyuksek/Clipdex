# Clipdex

Clipdex is a simple text expander application developed with Python that increases your writing efficiency by replacing frequently used text snippets with shortcuts. When you type a defined shortcut, the application automatically replaces it with the long text you specified.

## ✨ Features

- **System-Wide Operation:** Works in any text input field across the OS.
    
- **User-Friendly Interface:** Easily add, edit, and delete shortcuts through the user-friendly interface built with PyQt6.
    
- **Instant Updates:** Changes made to your snippet list are applied instantly without needing to restart the application.
    
- **Simple Trigger Mechanism:** Uses a simple trigger: start with a `:` character and end with a `Space` or `Enter`.
    

## 🚀 Installation

Follow the steps below to run the project on your local machine.

1. **Clone the Repository:**
    
    ```
    git clone https://github.com/kemalasliyuksek/clipdex.git
    cd clipdex
    ```
    
2. **Install Requirements:** All the necessary libraries for the project are listed in the `requirements.txt` file.
    
    ```
    pip install -r requirements.txt
    ```
    

## 🏃‍♀️ How to Run

After completing the installation, run the `main.py` file to start the application:

```
python main.py
```

When the application starts, the keyboard listener will begin running in the background, and the GUI window for managing your snippets will open.

## 📝 Usage

### Snippet Management

- **Add:** Click the "Add" button to create a new shortcut and its corresponding expansion text.
    
- **Edit:** Select a snippet from the list and click the "Edit" button to update an existing entry.
    
- **Delete:** Select the snippet you want to remove and click the "Delete" button.
    

### Text Expansion

In any text editor or input field, type the shortcut you've defined for the text you want to expand using the following format:

**`:` + `your_shortcut_name` + `Space` or `Enter`**

**Example:** Let's say you have defined the shortcut `"mail"` to expand to `"user@email.com"` in your `snippets.json` file.

The moment you type `:mail` into any text field, it will be automatically replaced with `user@email.com`.

## 📦 Project Structure

```
.
├── clipdex_core/
│   ├── listener.py         # The core engine that listens for keyboard events and performs text replacement.
│   └── snippet_manager.py  # Manages reading/writing snippets from/to the snippets.json file.
├── clipdex_gui/
│   ├── main_window.py      # The main application window and UI elements.
│   └── dialogs.py          # The dialog window for adding/editing new snippets.
├── main.py                 # The entry point of the application. Starts the GUI and the background listener.
├── requirements.txt        # Required Python libraries.
└── snippets.json           # The JSON file where snippets and their expansions are stored.
```

## 🛠️ Technologies Used

- [Python](https://www.python.org/ "null")
    
- [PyQt6](https://riverbankcomputing.com/software/pyqt/intro "null") - For the graphical user interface.
    
- [pynput](https://pynput.readthedocs.io/en/latest/ "null") - For system-wide keyboard listening.
    
- [keyboard](https://github.com/boppreh/keyboard "null") - For writing and deleting text.
    

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

# Clipdex (Türkçe)

Clipdex, sık kullandığınız metin parçacıklarını (snippet) kısayollarla değiştirerek yazma verimliliğinizi artıran, Python ile geliştirilmiş basit bir metin genişletme (text expander) uygulamasıdır. Tanımladığınız bir kısayolu yazdığınızda, uygulama bunu otomatik olarak belirlediğiniz uzun metinle değiştirir.

## ✨ Özellikler

- **Sistem Genelinde Çalışma:** Herhangi bir metin giriş alanında çalışır.
    
- **Kullanıcı Dostu Arayüz:** PyQt6 ile oluşturulmuş arayüzü sayesinde kısayolları kolayca ekleyin, düzenleyin ve silin.
    
- **Anlık Güncelleme:** Kısayol listenizde yaptığınız değişiklikler, uygulamayı yeniden başlatmaya gerek kalmadan anında aktif olur.
    
- **Basit Tetikleme Mekanizması:** `:` karakteri ile başlayan ve `Boşluk` veya `Enter` ile biten basit bir kullanım sunar.
    

## 🚀 Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

1. **Depoyu Klonlayın:**
    
    ```
    git clone https://github.com/kemalasliyuksek/clipdex.git
    cd clipdex
    ```
    
2. **Gerekli Kütüphaneleri Yükleyin:** Projenin ihtiyaç duyduğu tüm kütüphaneler `requirements.txt` dosyasında listelenmiştir.
    
    ```
    pip install -r requirements.txt
    ```
    

## 🏃‍♀️ Nasıl Çalıştırılır?

Kurulum adımlarını tamamladıktan sonra, uygulamayı başlatmak için `main.py` dosyasını çalıştırın:

```
python main.py
```

Uygulama başlatıldığında, arka planda klavye dinleyicisi çalışmaya başlayacak ve kısayol yönetimi için arayüz penceresi açılacaktır.

## 📝 Kullanım

### Kısayol Yönetimi

- **Ekleme:** "Add" butonuna tıklayarak yeni bir kısayol ve genişletilecek metni ekleyebilirsiniz.
    
- **Düzenleme:** Listeden bir kısayol seçip "Edit" butonuna tıklayarak mevcut girdiyi güncelleyebilirsiniz.
    
- **Silme:** Düzenlemek istediğiniz kısayolu seçip "Delete" butonuna tıklayarak silebilirsiniz.
    

### Metin Genişletme

Herhangi bir metin editöründe veya giriş alanında, genişletmek istediğiniz metin için tanımladığınız kısayolu aşağıdaki formatla yazın:

**`:` + `kısayol_adınız` + `Boşluk` veya `Enter`**

**Örnek:** `snippets.json` dosyasında `"mail"` kısayolu için `"kullanici@eposta.com"` metnini tanımladığınızı varsayalım.

Metin alanına `:mail` yazdığınız anda, bu ifade otomatik olarak `kullanici@eposta.com` ile değiştirilecektir.

## 📦 Proje Yapısı

```
.
├── clipdex_core/
│   ├── listener.py         # Klavye olaylarını dinleyen ve metin değişimini yapan ana motor.
│   └── snippet_manager.py  # snippets.json dosyasından kısayolları okuyan/yazan yönetici.
├── clipdex_gui/
│   ├── main_window.py      # Ana uygulama penceresini ve arayüz elemanlarını oluşturan sınıf.
│   └── dialogs.py          # Yeni kısayol ekleme/düzenleme diyalog penceresi.
├── main.py                 # Uygulamanın giriş noktası. Arayüzü ve arka plan dinleyicisini başlatır.
├── requirements.txt        # Gerekli Python kütüphaneleri.
└── snippets.json           # Kısayol ve metinlerin saklandığı JSON dosyası.
```

## 🛠️ Kullanılan Teknolojiler

- [Python](https://www.python.org/ "null")
    
- [PyQt6](https://riverbankcomputing.com/software/pyqt/intro "null") - Kullanıcı arayüzü için.
    
- [pynput](https://pynput.readthedocs.io/en/latest/ "null") - Sistem genelinde klavye dinlemesi için.
    
- [keyboard](https://github.com/boppreh/keyboard "null") - Metin yazma ve silme işlemleri için.
    

## 📄 Lisans

	Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atın.
