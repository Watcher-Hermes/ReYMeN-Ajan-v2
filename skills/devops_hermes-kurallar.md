---
name: ReYMeN-kurallar
title: ReYMeN Kural ve Engelleme Raporu
description: "ReYMeN Agent için izin verilen ve engellenen işlemlerin listesi — otomatik onay kuralları."
tags: [ReYMeN, rules, permissions, security, approval]
category: devops
audience: maintainer
version: 1.0.0
triggers: [kural, engelleme, izin, onay, güvenlik]
related_skills: [ReYMeN-approval-policy, ReYMeN-agent]
---


> **Kategori:** devops

---

## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Tüm ajanlar |
| **Ne?** | ReYMeN Agent için izin verilen ve engellenen işlemlerin listesi — otomatik onay kuralları. |
| **Nerede?** | devops/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

---

# ReYMeN Kural ve Engelleme Raporu

## İzin Verilen (Otomatik Onaylı)
- Komut çalıştırma
- Dosya okuma / yazma / düzenleme
- Web arama ve ekstraksiyon
- Otomasyon scriptleri
- Obsidian kayıtları

## Engellenen / Kısıtlanan Konular
- Yasa dışı içerik üretimi
- Kişisel veri işleme
- Güvenlik riskli komutlar
- Uygunsuz dil / içerik
- Üçüncü parti gizli bilgi paylaşımı

## Kritik Notlar
- Tüm onaylar auto, tek seçenek sistemine geçildi
- Planlı görevler cron_mode: auto ile çalışıyor
- Yapısal dönüşüm olursa sabah kontrol edilecek
