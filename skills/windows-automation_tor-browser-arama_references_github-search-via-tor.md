
> **Kategori:** Windows

---

## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Windows ajanı |
| **Ne?** | Windows Automation_Tor Browser Arama_References_Github Search Via Tor |
| **Nerede?** | Windows/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

---

# GitHub Search via Tor — Best Practices

## Why Tor for GitHub
- GitHub API rate limit: 60 req/hr (unauthenticated), 5000 req/hr (authenticated)
- Tor curl bypasses GitHub's IP-based rate limiting for read-only API calls
- Use `curl --socks5-hostname 127.0.0.1:9150` for ALL GitHub API queries

## Search Patterns

### Find ReYMeN-related repos
```
curl --socks5-hostname 127.0.0.1:9150 \
  "https://api.github.com/search/repositories?q=ReYMeN+agent+KEYWORD&sort=stars&per_page=10"
```

### Find ReYMeN issues
```
curl --socks5-hostname 127.0.0.1:9150 \
  "https://api.github.com/search/issues?q=repo:NousResearch/ReYMeN-agent+KEYWORD"
```

### Keywords to try
- `ReYMeN+agent+skill` → skill repos
- `ReYMeN+agent+mcp` → MCP servers
- `ReYMeN+memory+agent` → memory systems
- `ReYMeN+gui+OR+dashboard` → GUI projects
- `ReYMeN+gateway+telegram` → messaging integrations
- `ReYMeN+security+OR+injection` → security topics

## Navigation Flow (User Watching)

1. First, search API with curl → get list
2. Tell user what you found: "X reposu buldum, en iyisi Y"
3. Focus Tor: `focus_tor.ps1`
4. Navigate to best repo: `hermestor.py navigate "https://github.com/OWNER/REPO"`
5. Wait 4-5s
6. Screenshot + OCR to verify

## Repos Found (14 June 2026)

| Repo | Stars | Category |
|------|-------|----------|
| EKKOLearnAI/ReYMeN-studio | 7.890 | Web dashboard (TypeScript) |
| awizemann/scarf | 623 | macOS/iOS app (Swift) |
| xaspx/ReYMeN-control-interface | 762 | Web dashboard (JS) |
| JPeetz/ReYMeN-Studio | 195 | Multi-agent UI (TypeScript) |
| yoloshii/ClawMem | 182 | Memory layer |
| 410979729/scope-recall-ReYMeN | 96 | Memory provider |
| mudrii/hermesd | 92 | TUI dashboard (Python) |
| Sibyl-Labs/Sibyl-Memory | 83 | Memory plugin |
| sanchomuzax/ReYMeN-webui | 106 | Process monitoring |
| Noshkoto/ReYMeN-share-skill | 0 | Session export skill |
| kingmt123/paper-deep-reader | 0 | Academic paper skill |
| shiro-0x/hersona | 0 | Personality templates |
| djairjr/ReYMeN-agent-onboarding | 4 | Setup meta-skill |
