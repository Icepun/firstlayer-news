# First Layer: ana menü duyuruları

Ana menünün sağındaki **Workshop News** sütunu, sunucudaki tek bir dosyadan beslenir. Duyuru eklemek, değiştirmek ya da kaldırmak için **oyun güncellemesi gerekmez**: dosyayı değiştirmek yeter.

```
https://news.vitrumgames.com/first-layer/announcements.json
```

## Nasıl çalışır

- Ana menü açılınca oyun önce **cihazdaki son kopyayı** anında gösterir; kopya yoksa oyunla gelen yedeği (`Assets/6_SO/UI/Announcements_Default.json`) gösterir. Ardından sunucudaki dosyayı indirir. Dosya geçerliyse menü yumuşak bir geçişle yenilenir ve yeni kopya saklanır.
- İnternet yoksa, sunucu kapalıysa ya da dosya bozuksa oyuncu **son geçerli kopyayı** görür. Ekranda hata çıkmaz.
- Bir değişiklik en geç **5–10 dakika** içinde oyunculara ulaşır (sunucu önbelleği). Oyuncu o sırada menüdeyse menüyü bir sonraki açışında görür.
- Sıralama: **sabitlenen** (`pinned`) duyuru ilk sıradadır, ardından en yeni tarihli olanlar gelir. İlk duyuru görselli büyük kartta, sonraki ikisi kısa satırlarda çıkar.
- Oyuncunun açmadığı duyurularda turuncu **NEW** rozeti görünür. Oyunu ilk kez açan oyuncuda hiçbir şey "yeni" sayılmaz.

## Kurulum

Dosya bu depodan GitHub Pages ile yayınlanır, adres ise bizim alan adımızdır:

- Ücretsizdir. Değişiklik geçmişi tutulur, dosya tarayıcıdan düzenlenir.
- **Hatalı dosya yayına çıkmaz.** Her kayıtta dosya otomatik denetlenir; hata varsa eski doğru sürüm yayında kalır.
- Oyunun içindeki adres bizim alan adımız olduğu için ileride barındırmayı değiştirmek yalnızca DNS ayarı gerektirir, oyun güncellemesi gerektirmez.

Ayarlar (yeniden kurmak gerekirse):

1. **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. **Settings → Pages → Custom domain:** `news.vitrumgames.com`, **Enforce HTTPS** açık.
3. Hostinger DNS'te `news` için bir **CNAME** kaydı → `icepun.github.io`.
4. Unity'de **Tools → Printing Sim → Main Menu → Check Live Announcements** çalıştır. Console'da `Announcements OK` görünmeli.

## Duyuru eklemek ya da değiştirmek

1. GitHub'da `site/first-layer/announcements.json` dosyasını aç ve kalem simgesine bas (Edit).
2. Düzenle, ardından **Commit changes** de.
3. **Actions** sekmesine bak:
   - **Yeşil tik:** 1–2 dakika içinde yayında.
   - **Kırmızı çarpı:** dosyada hata var, eski sürüm yayında kalır. Kaydı açınca hatanın ne olduğu yazar.
4. İstersen Unity'den **Check Live Announcements** ile şu an neyin göründüğüne bak.

Yerelde denemek için: `python tools/validate.py site/first-layer/announcements.json`

## Alanlar

| Alan | Gerekli | Açıklama |
| --- | --- | --- |
| `id` | evet | Benzersiz ve **değişmeyen** kimlik. NEW rozeti buna bağlıdır. Yeni duyuru için yeni `id` kullan; düzeltme yaparken `id` aynı kalsın. |
| `title` | evet | Başlık. Kartta en fazla 2 satır görünür (yaklaşık 45 karakter). |
| `summary` | | Kartta ve satırda görünen kısa metin (yaklaşık 120 karakter). |
| `body` | | "Read" ile açılan tam metin. Paragraf için `\n\n`, madde için `• `. |
| `category` | | Küçük turuncu etiket, örneğin `Update`, `Event`, `Roadmap`. |
| `date` | | `2026-10-04` biçiminde. Kartta `OCT 4, 2026` olarak görünür. Sıralama buna göre yapılır. |
| `pinned` | | `true` ise her zaman ilk sırada, büyük kartta durur. |
| `image` | | `https://` ile başlayan görsel. Önerilen 16:9 oran ve 1280×720 boyut, en fazla 4 MB. İndirilip cihazda saklanır. Yoksa oyunun varsayılan görseli kullanılır. |
| `link` | | `https://` ile başlayan bağlantı. Duyuru açılınca bir düğme olarak görünür. |
| `linkLabel` | | Bağlantı düğmesinin yazısı, örneğin `Join our Discord`. |
| `start` / `end` | | Yayın aralığı (UTC), örneğin `2026-10-10` ya da `2026-10-10T18:00:00Z`. Yalnızca gün yazılırsa `end` o günün sonuna kadar geçerlidir. Tarihi gelince duyuru kendiliğinden görünür, süresi bitince kaybolur. |
| `minVersion` / `maxVersion` | | Duyurunun görüneceği oyun sürümleri, örneğin eski sürümdekilere güncelleme duyurusu için `"maxVersion": "0.1.9"`. |
| `tr` / `pl` | | Çeviriler: `category`, `title`, `summary`, `body`, `linkLabel`. Boş bırakılan alan İngilizceye düşer. Oyun, oyuncunun diline göre bunları kullanır. |

Biçimlendirme etiketleri (`<b>` vb.) işlenmez, düz yazı olarak görünür. Bilinmeyen alanlar yok sayılır. Oyun en fazla 12 duyuru okur.

## Örnek

```json
{
  "schema": 1,
  "announcements": [
    {
      "id": "printathon-2026-10",
      "pinned": true,
      "date": "2026-10-10",
      "start": "2026-10-10",
      "end": "2026-10-12",
      "category": "Event",
      "title": "Print-a-thon weekend",
      "summary": "Share your best print on Discord this weekend. The community picks a favourite.",
      "body": "Post a screenshot of your best print in #showcase.\n\nWe will feature the winner here next week.",
      "image": "https://news.vitrumgames.com/first-layer/images/printathon.jpg",
      "link": "https://discord.gg/ANR3mNuerB",
      "linkLabel": "Join our Discord",
      "tr": {
        "category": "Etkinlik",
        "title": "Baskı maratonu hafta sonu",
        "summary": "En iyi baskını bu hafta sonu Discord'da paylaş, topluluk favorisini seçsin."
      }
    }
  ]
}
```

Görselleri de aynı depoya koyabilirsin: `site/first-layer/images/` → `https://news.vitrumgames.com/first-layer/images/...`

## İpuçları

- **Kaldırmak:** duyuruyu listeden sil ya da ona bir `end` tarihi ver.
- **Planlamak:** `start` ile ileri bir tarih ver. O gün geldiğinde kendiliğinden görünür.
- **Oyunla gelen yedek:** yeni bir build almadan önce oyun projesindeki `Assets/6_SO/UI/Announcements_Default.json` dosyasını buradakiyle eşitlemek iyi olur. **Tools → Printing Sim → Main Menu → Check Bundled Announcements** onu denetler.
