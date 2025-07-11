# Clipdex - MacOS Kurulum ve Kullanım

## Kurulum

### 1. Python Bağımlılıklarını Yükleyin

```bash
pip3 install -r requirements.txt
```

### 2. Accessibility İzni Verin

Clipdex'in klavye kısayollarını çalıştırabilmesi için Accessibility izni vermeniz gerekiyor:

1. **System Preferences** > **Security & Privacy** > **Privacy** sekmesine gidin
2. Sol panelden **Accessibility**'yi seçin
3. **Lock** simgesine tıklayın ve şifrenizi girin
4. **+** butonuna tıklayın ve Clipdex uygulamasını ekleyin
5. Clipdex'i seçin ve **Allow** butonuna tıklayın

### 3. Uygulamayı Çalıştırın

```bash
python3 main.py
```

## Kullanım

### Temel Kullanım

1. **Kısayol Oluşturma**: Herhangi bir metin editöründe `:` karakteri ile başlayan bir kısayol yazın
2. **Genişletme**: Space veya Enter tuşuna basarak metni genişletin
3. **Geri Alma**: Genişletme sonrası Backspace tuşuna basarak işlemi geri alabilirsiniz

### Örnek Kullanım

```
:merhaba [Space] → Merhaba dünya!
:email [Space] → kemal@kemalasliyuksek.com
```

### Ayarlar

- **Auto-start**: Uygulamanın sistem başlangıcında otomatik çalışmasını sağlar
- **Trigger Key**: Space veya Enter tuşunu tetikleyici olarak seçebilirsiniz

## MacOS Özellikleri

### Menü Bar Entegrasyonu

- Uygulama kapatıldığında menü barında ikon olarak kalır
- Menü bar ikonuna tıklayarak uygulamayı tekrar açabilirsiniz
- "Quit" seçeneği ile uygulamayı tamamen kapatabilirsiniz

### LaunchAgent Desteği

- Auto-start özelliği MacOS LaunchAgent sistemi kullanır
- `~/Library/LaunchAgents/com.clipdex.plist` dosyası oluşturulur

### Veri Konumu

- Snippets: `~/Library/Application Support/Clipdex/snippets.json`
- Config: `~/Library/Application Support/Clipdex/config.json`

## Sorun Giderme

### Accessibility İzni Sorunu

Eğer "This process is not trusted!" hatası alıyorsanız:

1. System Preferences > Security & Privacy > Privacy > Accessibility
2. Clipdex'i listeden kaldırın
3. Uygulamayı yeniden başlatın
4. İzin isteğini kabul edin

### Klavye Kısayolları Çalışmıyor

1. Accessibility izninin verildiğinden emin olun
2. Uygulamayı yeniden başlatın
3. Test için basit bir kısayol deneyin: `:test [Space]`

### Menü Bar İkonu Görünmüyor

1. Uygulamayı kapatın (X butonuna tıklayın)
2. Menü barında ikon görünmelidir
3. İkon görünmüyorsa uygulamayı yeniden başlatın

## Teknik Detaylar

### Platform Spesifik Özellikler

- **Auto-start**: LaunchAgent plist dosyası kullanır
- **System Tray**: MacOS menü bar entegrasyonu
- **File Paths**: `~/Library/Application Support/Clipdex/` dizini
- **Icons**: `.icns` formatında ikonlar kullanır

### Güvenlik

- Accessibility izni sadece klavye dinleme için kullanılır
- Kişisel veriler yerel olarak saklanır
- Ağ bağlantısı gerektirmez

## Destek

Sorunlarınız için:
- GitHub Issues: https://github.com/kemalasliyuksek/Clipdex
- Email: kemal@kemalasliyuksek.com 