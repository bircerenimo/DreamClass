🌟 DreamClass - Grup 27 Hackathon Projesi

Bu proje, [Hackathon Adı] kapsamında Grup 27 tarafından geliştirilmiştir. DreamClass, öğrenciler için hayal gücüne dayalı, kişiselleştirilmiş ve etkileşimli ders deneyimleri sunan yapay zeka destekli bir eğitim platformudur. Uygulama, Google Gemini API ile çalışmakta olup hikâyeleştirme, içerik üretimi ve quiz gibi eğitim materyalleri üretmektedir.
->Proje master branch kısmında mevcut. 
---

## 📁 .env Dosyası Kurulumu

Projenin kök dizinine `.env` adında bir dosya oluşturun ve aşağıdaki formatı kullanarak gerekli bilgileri girin:

```env
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
API_RESTRICTIONS=true
ALLOWED_DOMAINS=localhost:5000,127.0.0.1:5000,localhost,127.0.0.1
ALLOWED_API=Generative Language API
ALLOWED_IPS=127.0.0.1,localhost
DEBUG=True
PORT=5000
HOST=0.0.0.0
