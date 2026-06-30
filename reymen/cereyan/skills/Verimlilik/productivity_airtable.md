---
name: productivity_airtable
title: Productivity Airtable
description: ''
tags:
- verimlilik
category: Verimlilik
audience: agent
---
## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Tüm ajanlar |
| **Ne?** | Airtable REST API via curl. Records CRUD, filters, upserts. |
| **Nerede?** | productivity/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

# Airtable

Bu skill modüler bir yönlendiricidir. İhtiyacınız olan bölümü seçin ve ilgili reference dosyasını yükleyin.

## 📂 Bölümler

| Bölüm | Reference Dosyası |
|-------|------------------|
| Airtable — Bases, Tables & Records | `references/airtable-bases-tables-records.md` |
| Prerequisites | `references/prerequisites.md` |
| API Basics | `references/api-basics.md` |
| Field Types (request body shapes) | `references/field-types-request-body-shapes.md` |
| Common Queries | `references/common-queries.md` |
| Common Mutations | `references/common-mutations.md` |
| Pagination | `references/pagination.md` |
| Typical ReYMeN Workflow | `references/typical-ReYMeN-workflow.md` |
| Pitfalls | `references/pitfalls.md` |
| Important Notes for ReYMeN | `references/important-notes-for-ReYMeN.md` |

## Kullanım

1. İhtiyacın olan bölümü belirle
2. `skill_view(name="...", file_path="references/...")` ile yükle