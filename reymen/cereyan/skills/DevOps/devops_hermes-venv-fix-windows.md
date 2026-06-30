---
name: ReYMeN-venv-fix-windows
title: ReYMeN Venv Fix - Windows .pyd Kilit Hatasi
description: Use when ReYMeN guncellenemiyor, venv icindeki .pyd dosyalari kilitli
  hatasi aliniyor. Windows'ta process kill + venv silme cozumu.
tags:
- devops
- ReYMeN
- venv
- windows
- update
category: DevOps
audience: user
---
## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Windows ajanı |
| **Ne?** | Use when ReYMeN guncellenemiyor, venv icindeki .pyd dosyalari kilitli hatasi aliniyor. Windows'ta process kill + venv silme cozumu. |
| **Nerede?** | devops/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

# ReYMeN Venv Fix - Windows

## Sorun
ReYMeN güncellenemiyor: venv içindeki `.pyd` dosyaları Windows tarafından kilitlenmiş.

## Kök Neden
ReYMeN çalışırken installer venv'i silmeye çalışır ama Windows, belleğe yüklenmiş `.pyd` dosyalarını kilitler. ReYMeN arka planda otomatik yeniden başladığı için kill + delete döngüsü başarısız olur.

## Çözüm Adımları

### 1. package-lock.json local değişikliğini temizle
```bash
git -C "$LOCALAPPDATA/hermes/hermes-agent" checkout -- package-lock.json
```

### 2. Hangi process venv'i kilitlediğini bul
PowerShell ile:
```powershell
# psutil benzeri: process modüllerini tara
Get-Process | Where-Object { $_.Modules.FileName -like "*.pyd" } | Select-Object Id, ProcessName
```
Elle PID tespit et (genelde `python.exe` veya `ReYMeN.exe`).

### 3. O PID'i öldür
```powershell
Stop-Process -Id <PID> -Force
```

### 4. Hemen venv'i sil (bekleme yapma!)
```powershell
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\hermes\hermes-agent\venv"
```

### 5. Installer'ı çalıştır
```cmd
%LOCALAPPDATA%\hermes\hermes-agent\scripts\install.cmd
```
`[y/N]` sorusuna `n` yaz.

## Kritik Uyarı
Kill ile Delete arasında **2-3 saniyeden fazla beklenmez**. ReYMeN otomatik yeniden başlarsa kilit geri gelir ve işlem başarısız olur.

Hızlı tek satır PowerShell (tüm adımlar):
```powershell
# package-lock temizle + kilidi bul + öldür + venv sil
git -C "$env:LOCALAPPDATA\hermes\hermes-agent" checkout -- package-lock.json
$p = Get-Process | Where-Object { $_.Modules.FileName -like "*ReYMeN*venv*" } | Select-Object -First 1
if ($p) { Stop-Process -Id $p.Id -Force }
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\hermes\hermes-agent\venv"
```
Sonra `install.cmd` çalıştır.