# Clipdex - MacOS Kurulum Rehberi

## MacOS'ta Kısayol Sorunları ve Çözümleri

MacOS'ta Clipdex'in kısayollarını kullanabilmek için sistem izinlerini ayarlamanız gerekmektedir.

### 1. Accessibility İzinlerini Ayarlama

1. **System Preferences**'ı açın
2. **Security & Privacy** sekmesine gidin
3. **Privacy** sekmesini seçin
4. Sol panelden **Accessibility**'yi seçin
5. Kilit simgesine tıklayın ve şifrenizi girin
6. **+** butonuna tıklayın
7. **Clipdex** uygulamasını bulun ve ekleyin
8. Clipdex'in yanındaki kutucuğu işaretleyin

### 2. Uygulamayı Yeniden Başlatma

İzinleri verdikten sonra:
1. Clipdex uygulamasını tamamen kapatın
2. `main.py` dosyasını tekrar çalıştırın
3. Terminal çıktısında "✓ MacOS klavye izinleri kontrol edildi - Tamam" mesajını görmelisiniz

### 3. Test Etme

İzinler doğru ayarlandıktan sonra:
1. Herhangi bir metin editöründe `:test` yazın
2. Space tuşuna basın
3. Eğer snippets.json dosyanızda "test" kısayolu varsa, genişletilmiş metni görmelisiniz

### 4. Sorun Giderme

#### Kısayollar çalışmıyor mu?
- Terminal çıktısını kontrol edin
- "⚠️ MacOS izin sorunu tespit edildi!" mesajı varsa izinleri tekrar kontrol edin
- System Preferences > Security & Privacy > Privacy > Accessibility'de Clipdex'in işaretli olduğundan emin olun

#### Uygulama çöküyor mu?
- Terminal'de hata mesajlarını kontrol edin
- Gerekirse uygulamayı yeniden başlatın

### 5. Güvenlik Notu

Clipdex, klavye olaylarını dinlemek için sistem genelinde çalışır. Bu, güvenlik açısından normal bir durumdur ve sadece metin genişletme işlevi için kullanılır.

### 6. Ek Bilgiler

- MacOS Catalina ve üzeri sürümlerde ek güvenlik önlemleri olabilir
- İlk çalıştırmada sistem uyarısı alabilirsiniz - "Allow" seçeneğini seçin
- Uygulama güncellemelerinden sonra izinleri tekrar kontrol etmeniz gerekebilir 