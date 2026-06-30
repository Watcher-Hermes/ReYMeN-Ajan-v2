---
name: ReYMeN-kurulacak-repolar
title: "ReYMeN Kurulacak Repolar"
tags: [automation, devops, system]
description: >-
  ReYMeN Agent kurulumu için gerekli GitHub repolarının listesi ve
  sıralı kurulum talimatları. Watcher-ReYMeN/ReYMeN-full-backup
  reposundaki KURULACAK_REPOLAR.md dosyasını referans alır.
version: 1.0.0
author: ReYMeN-agent
license: MIT
metadata:
  ReYMeN:
    tags: [kurulum, github, repo, setup, migration]
audience: maintainer
related_skills:
      - ReYMeN-migration-restore
      - github-repo-management
---


> **Kategori:** devops

---

## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Tüm ajanlar |
| **Ne?** | >- |
| **Nerede?** | devops/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

---

# ReYMeN Kurulacak GitHub Repoları

## Amaç

ReYMeN Agent yeni bir bilgisayara kurulurken hangi GitHub repolarının
banklone edilmesi gerektiğini ve hangi sırayla kurulacağını tanımlar.

## Repo Listesi

| Sıra | Repo | URL | Durum |
|------|------|-----|:----:|
| 1 | ReYMeN-full-backup | https://github.com/Watcher-ReYMeN/ReYMeN-full-backup | ❌ Bulunamadı |
| 2 | ReYMeN-gemini-copilot | https://github.com/Izleyici-ReYMeN/ReYMeN-gemini-copilot | ✅ |
| 3 | ai-engineering-from-scratch-zh | https://github.com/fancyboi999/ai-engineering-from-scratch-zh | ✅ 489 skill |
| 4 | kali-pentest | https://github.com/x-glacier/kali-pentest | ✅ 269 araç |
| 5 | wifi-ag-tarayici | https://github.com/Izleyici-ReYMeN/wifi-ag-tarayici | ✅ |
| 6 | runners-journey | https://github.com/Izleyici-ReYMeN/runners-journey | ✅ |
| 7 | ReYMeN-studio | https://github.com/EKKOLearnAI/ReYMeN-studio | ✅ npm global |
| 8 | ReYMeN-share-skill | https://github.com/Noshkoto/ReYMeN-share-skill | ✅ skill |
| 9 | paper-deep-reader | https://github.com/kingmt123/paper-deep-reader | ✅ skill |
| 10 | hersona | https://github.com/shiro-0x/hersona | ✅ 6 skill |
| 7 | ReYMeN-studio | https://github.com/EKKOLearnAI/ReYMeN-studio | ✅ 7.890★ Web dashboard |
| 8 | share-skill | https://github.com/Noshkoto/ReYMeN-share-skill | ✅ Session export skill |
| 9 | paper-deep-reader | https://github.com/kingmt123/paper-deep-reader | ✅ Akademik makale okuma |
| 10 | hersona | https://github.com/shiro-0x/hersona | ✅ 6 adet kişilik şablonu |

## Kaynak Dosya

Detaylı açıklamalar ve kurulum komutları:

```
C:\Users\marko\ReYMeN-backup\KURULACAK_REPOLAR.md
```

Bu dosya `Watcher-ReYMeN/ReYMeN-full-backup` reposunda version
control altındadır. Güncellemek için:

```bash
cd /c/Users/marko/ReYMeN-backup
# KURULACAK_REPOLAR.md düzenle
git add KURULACAK_REPOLAR.md
git commit -m "Repo listesi güncellendi"
git push origin main
```

## Toplu Klonlama

Tüm repoları tek seferde indirmek için:

```bash
mkdir -p ~/ReYMeN-repos && cd ~/ReYMeN-repos
git clone https://github.com/Watcher-ReYMeN/ReYMeN-full-backup.git || echo "NOT: repo bulunamadi, manuel olustur"
git clone https://github.com/asdafgf/ReYMeN-gemini-copilot.git
git clone https://github.com/fancyboi999/ai-engineering-from-scratch-zh.git
git clone https://github.com/x-glacier/kali-pentest.git
git clone https://github.com/asdafgf/wifi-ag-tarayici.git
git clone https://github.com/asdafgf/runners-journey.git
echo "Tüm repolar indirildi."
```

## ReYMeN Studio Kurulumu

```bash
npm install -g ReYMeN-web-ui
ReYMeN-web-ui start
# → http://localhost:8648
```

Kurulum sonrası:
1. Tarayıcıda http://localhost:8648 aç
2. Kullanıcı kaydı oluştur
3. Giriş yap → otomatik ReYMeN profiline bağlanır
4. Skills, memory, sessions, cron hepsi aynı ReYMeN instance'ı üzerinden çalışır

**Uninstall:**
```bash
npm uninstall -g ReYMeN-web-ui
```

## ReYMeN Studio Yeni Skill Ekleme (GitHub'dan)

```bash
# 1. Clone
git clone https://github.com/OWNER/REPO.git

# 2. SKILL.md varsa skills klasörüne kopyala
cp -r REPO/skills/* ~/.hermes/skills/KATEGORI/

# 3. Yoksa direkt SKILL.md'i kopyala
cp REPO/SKILL.md ~/.hermes/skills/KATEGORI/REPO-ADI/

# 4. sync (Obsidian'a kaydet)
python C:\Users\marko\AppData\Local\hermes\hooks\sync_skills_to_obsidian.py
```

## Kurulum Notları

### ReYMeN Studio (ReYMeN-web-ui)
```bash
npm install -g ReYMeN-web-ui      # 59 package, ~10sn
ReYMeN-web-ui start               # localhost:8648
```
- Port: 8648
- Log: ~/.hermes-web-ui/server.log
- MCP server otomatik eklenir (72 MCP tool)
- Uninstall: `npm uninstall -g ReYMeN-web-ui`

## Pitfall

- `Watcher-ReYMeN/ReYMeN-full-backup` repo'su GitHub'da bulunamadi (404). Ya silinmis ya da hic olusturulmamis. Yedekleme icin `C:\Users\marko\ReYMeN-skills-backup\` klasoru lokal yedek olarak kullaniliyor. GitHub'a push icin yeni repo olusturulmasi gerekiyor (PAT fine-grained oldugu icin REST API ile olusturulamadi).

## Skill Güncelleme/Deployment Akışı

Bir dış repodan (örn. ReYMeN-mouse) skill alındığında veya güncellendiğinde **3 adım**:

```
1. Lokal ReYMeN skill kütüphanesine yükle/güncelle
   → C:\Users\marko\AppData\Local\hermes\skills\KATEGORI\SKILL-ADI\

2. ReYMeN-skills reposuna push et
   → Watcher-ReYMeN/ReYMeN-skills
   → cd /c/Users/marko/ReYMeN-skills
   → git add -A && git commit -m "update: ..." && git push

3. Obsidian'a sync et
   → python ...\sync_skills_to_obsidian.py
```

**KRITIK:** Adım 2 atlanmamalı. Lokale yüklemek yetmez — GitHub reposu güncel değilse başka bir cihaza migration'da skill kaybolur.

## Yeni Repo Ekleme

Yeni bir GitHub reposu ReYMeN kurulumuna eklendiğinde:

1. `KURULACAK_REPOLAR.md` dosyasına ekle (sıraya uygun)
2. Bu skill'i güncelle: `skill_manage(action='patch')`
3. Obsidian notunu güncelle: `ReYMeN/ReYMeN-Kurulacak-Repolar.md`
4. GitHub'a push et
