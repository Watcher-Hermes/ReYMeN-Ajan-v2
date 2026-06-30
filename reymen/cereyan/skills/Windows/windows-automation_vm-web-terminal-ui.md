---
name: windows-automation_vm-web-terminal-ui
title: Windows Automation Vm Web Terminal Ui
description: ''
tags:
- windows
category: Windows
audience: agent
---
## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Tüm ajanlar |
| **Ne?** | > |
| **Nerede?** | automation/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

# Vm Web Terminal Ui

Bu skill modüler bir yönlendiricidir. İhtiyacınız olan bölümü seçin ve ilgili reference dosyasını yükleyin.

## 📂 Bölümler

| Bölüm | Reference Dosyası |
|-------|------------------|
| Kullanım Amacı | `references/kullan-m-amac.md` |
| Mimari | `references/mimari.md` |
| Kurulum Adımları | `references/kurulum-ad-mlar.md` |
| HTML template with dark terminal theme | `references/html-template-with-dark-terminal-theme.md` |
| Expected: {"connected": true/false} | `references/expected-connected-true-false.md` |
| Expected: {"output": "kali\n", "error": ""} | `references/expected-output-kali-n-error.md` |
| Önemli Kod Desenleri | `references/nemli-kod-desenleri.md` |
| Kullanıcı Format Tercihi | `references/kullan-c-format-tercihi.md` |
| Telegram ReYMeN → Kali Komut Gönderme Akışı | `references/telegram-ReYMeN-kali-komut-g-nderme-ak.md` |
| Kali'de komut çalıştır — Telegram ReYMeN'ten | `references/kali-de-komut-al-t-r-telegram-ReYMeN-ten.md` |
| Çıktı: {"output": "kali\n192.168.0.19\n", "error": ""} | `references/kt-output-kali-n192-168-0-19-n-error.md` |
| YANLIŞ: echo "=== $BASLIK ===" && ... (zsh bozulur) | `references/yanli-echo-baslik-zsh-bozulur.md` |
| {"connected": false} ise Flask'ı yeniden başlat (.bat dosyasına çift tıkla) | `references/connected-false-ise-flask-yeniden-ba-lat-bat-dosyas-na-ift-t.md` |
| Pitfall'lar | `references/pitfall-lar.md` |
| Başarı Kriterleri | `references/ba-ar-kriterleri.md` |
| Template Reference | `references/template-reference.md` |
| Referans Dosyaları | `references/referans-dosyalar.md` |

## Kullanım

1. İhtiyacın olan bölümü belirle
2. `skill_view(name="...", file_path="references/...")` ile yükle