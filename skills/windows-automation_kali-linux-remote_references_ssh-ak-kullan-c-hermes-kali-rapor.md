
> **Kategori:** Windows

---

## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Kali ajanı |
| **Ne?** | Windows Automation_Kali Linux Remote_References_Ssh Ak Kullan C ReYMeN Kali Rapor |
| **Nerede?** | Windows/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

---

## SSH Akışı (Kullanıcı → ReYMeN → Kali → Rapor)

```
Kullanıcı → komutu yazar (örn: "sudo arp-scan -l")
    ↓
ReYMeN → terminal tool ile SSH yapar: ssh kali "<komut>"
    ↓
Kali → komutu çalıştırır, çıktı SSH üzerinden döner
    ↓
ReYMeN → kendi terminalinde çıktıyı alır
    ↓
ReYMeN → kullanıcıya sonucu raporlar (sadece çıktı, yorum yok)
```

**Akış kuralları:**
- ReYMeN kendi terminalinde sonucu görür → kullanıcıya raporlar
- Yorum yapma, adım adım açıklama yok — sadece çıktı
- "Sorma sonucun raporla bitti" modu