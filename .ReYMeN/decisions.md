## Karar #36: TUI Hermes Seviyesine Yükseltme

**Ne yapıldı:** `tui.py` sade metin → prompt_toolkit + Rich tabanlı etkileşimli TUI

**Neden:** Mevcut tui.py (314 satır) sadece statik renkli çıktı fonksiyonlarıydı. Gerçek bir Terminal UI (komut girişi, geçmiş, otomatik tamamlama, panel sistemi) yoktu.

**Alternatifler:**
1. Sadece Rich fonksiyonları bırakmak → etkileşimsiz
2. Ayrı cli_tui.py modülü → dağınıklık
3. Mevcut tui.py'yi komple yeniden yazmak → Seçilen yol

**Eklenenler:**
- ReYMeNTUI class: prompt_toolkit tabanlı REPL (otomatik tamamlama, geçmiş, klavye kısayolları)
- Rich çıktı fonksiyonları korundu (info, success, warning, error, panel, table)
- Motor tool'u: TUI_BASLAT
- Fallback: prompt_toolkit yoksa basit input() REPL
## Karar #31 — Bot Çince cevap fix + Ensemble akışı

**Ne yapıldı?**
1. Hermes reymen profili SOUL.md'sine Türkçe talimatı eklendi (başa)
2. telegram_bot/__init__.py AIAgentOrchestrator → ConversationLoop ensemble akışına çevrildi
3. conversation_loop.py'ye .env yükleme eklendi (API key okunamıyordu)
4. OnceHafiza'daki eski Çince kayıt (dunyada guncel haberler) temizlendi
5. Gateway restart yapıldı

**Neden?**
- SOUL.md'de Türkçe talimatı yoktu → DeepSeek Çince cevap veriyordu
- Bot main.py'deki ağır ReAct döngüsü yerine ensemble akışı kullanmalı (DeepSeek önce toolsuz cevaplasın, sonra puanla karşılaştır)
- conversation_loop.py'de load_dotenv yoktu → API key bulunamıyordu

**Alternatif?**
- conversation_loop.py'deki ensemble zaten yazılıydı, sadece bot yönlendirilmedi
- SOUL.md'yi proje köküne koymak da çözümdü ama profil override ediyor

## Karar #42 — Auth: Hermes Pattern JWT + Role Bazli

**Ne yapildi:** Mevcut auth.py + web_ui/__init__.py auth sistemi Hermes dashboard_auth pattern'ine donusturuldu.

**Neden:** Kullanici "Jwt var role bazli hermes de olan sekili ile yap" dedi — Hermes'teki AuthProvider ABC + Session dataclass + provider registry + cookie yonetimi birebir uygulandi.

**Detay:**
- AuthProvider ABC (Hermes DashboardAuthProvider pattern)
- Session dataclass (user_id, display_name, role, provider, expires_at, access_token, refresh_token)
- Provider registry: register_provider(), get_provider(), list_providers()
- PasswordAuthProvider: complete_password_login(), verify_session(), refresh_session(), revoke_session()
- Cookie: hermes_session_at (access token) + hermes_session_rt (refresh token)
- Transparent refresh: access token expiredsa refresh token ile otomatik rotate
- /api/auth/me — mevcut Session bilgisi
- /api/auth/providers — kayitli provider listesi
- Audit logging (AuditEvent.LOGIN_SUCCESS/FAILURE/LOGOUT)
- Role bazli izin (admin/operator/viewer) middleware'de
- Eski _get_user/_require_auth/_izin_kontrol helper'lari temizlendi
- Commit: 61846927

**Karar:** Kabul. Hermes'teki ile birebir ayni desen.
