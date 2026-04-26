---
name: etkm-seo
version: 1.0
updated: 2026-03-09
description: >
  Use this skill whenever writing, reviewing, or publishing any content for ETKM
  websites — blog posts, page copy, page rewrites, landing pages, or any content
  that will live on etxkravmaga.com, fightbacketx.com, or etkmstudent.com. Covers
  on-page SEO (title tags, meta descriptions, headings, internal links), E-E-A-T
  signals (author attribution, experience markers, trust signals), schema markup
  generation (LocalBusiness, Person, Article, Event, Course), content quality gates
  (word counts, uniqueness, readability), local SEO for Tyler TX, and AI search
  optimization (GEO). Trigger on "SEO", "meta description", "title tag", "schema",
  "search ranking", "page optimization", "blog post", "page rewrite", "publish",
  or any time content is being prepared for a website. Also trigger when auditing
  existing pages. Load etkm-brand-foundation for voice alignment on all copy.
---

# ETKM SEO Skill

**Version:** 1.0
**Last Updated:** 2026-03-09
**Source reference:** claude-seo by AgriciDaniel (MIT), adapted for ETKM

---

## ETKM Domain Map

| Domain | Purpose | Primary Schema Type |
|--------|---------|-------------------|
| etxkravmaga.com | Main site — training, programs, events, blog | LocalBusiness + Course + Event |
| fightbacketx.com | Women's self-defense (Fight Back ETX) | LocalBusiness + Course |
| etkmstudent.com | Student portal — onboarding, resources, levels | WebPage + Course |

All three domains serve the same physical business:
- East Texas Krav Maga
- 2918 E. Grande Blvd., Tyler TX 75707
- (903) 590-0085

---

## SEO Checklist — Run on Every Page

Before any page goes live or any rewrite is delivered, verify all items.

### Title Tag

- 30-60 characters (Google truncates at ~60)
- Primary keyword near the beginning
- Brand name at the end: "| East Texas Krav Maga" or "| ETKM"
- Unique per page — no two pages share a title
- No keyword stuffing

**ETKM examples:**
- "Krav Maga Classes in Tyler TX | East Texas Krav Maga" (service page)
- "What Is Mindset in Self-Defense Training | ETKM" (student resource)
- "Free Trial Lesson — Start Your Training | East Texas Krav Maga" (landing page)

### Meta Description

- 120-160 characters (Google truncates at ~155-160)
- Includes primary keyword naturally
- Contains a compelling CTA or value statement
- Unique per page
- Speaks to the reader's internal problem, not just features

**ETKM examples:**
- "Learn practical self-defense in Tyler TX. ETKM builds confidence, awareness, and real-world capability. Schedule your free trial lesson today."
- "Your first 90 days at ETKM — what to expect, how to train, and what you're building. Start with mindset. Everything else follows."

### Heading Structure

- Exactly one H1 per page — matches page intent and includes primary keyword
- H2s for major sections — logical hierarchy, no skipped levels
- H3-H6 for subsections — descriptive, not generic
- No heading used purely for visual styling

### Internal Links

| Page Type | Target Link Count |
|-----------|------------------|
| Blog post (1,500+ words) | 5-10 internal links |
| Service/program page | 3-5 internal links |
| Student resource page | 3-5 internal links |
| Landing page | 2-3 internal links (focused) |

- Use descriptive anchor text — never "click here"
- Vary anchor text across pages
- Every page should be linked from at least one other page (no orphans)
- Link to relevant content: student pages link to related level pages, blog posts link to programs

### Images

- Alt text on every non-decorative image (10-125 characters)
- Alt text describes the image content, includes keyword where natural
- File size under 200KB (warning), under 500KB (critical)
- WebP or AVIF preferred over JPEG/PNG
- Width and height attributes set (prevents CLS)
- Lazy loading on below-fold images

### URL Structure

- Short, descriptive, hyphenated
- No parameters or query strings
- Includes primary keyword where natural
- Lowercase only

---

## Content Quality Gates

### Minimum Word Counts

| Page Type | Minimum Words | ETKM Context |
|-----------|--------------|---------------|
| Homepage | 500 | etxkravmaga.com main page |
| Service/program page | 800 | Self Defense, Fight Back, ACT, Youth, LE pages |
| Blog post | 1,500 | All blog content including "Aware & Able" series |
| Student resource page | 600 | Mindset, Tactics, Goals, Class Structure pages |
| Landing page | 600 | Free trial, event registration pages |
| About page | 400 | About Us |

### Content Must Include

- Publication date visible on blog posts
- Last updated date on resource pages that get revised
- Author attribution where applicable (see E-E-A-T below)
- At least one CTA per page
- No duplicate content across pages — 100% unique for all non-location pages

---

## E-E-A-T Framework — ETKM Application

E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) now
applies to ALL competitive queries as of the December 2025 core update.
Self-defense training is inherently YMYL-adjacent (personal safety).
ETKM must score high on all four signals.

### Experience (Weight: 20%)

Nathan has 42 years of martial arts experience. This is ETKM's single
strongest E-E-A-T signal and it should be visible on every page.

**Signals to include:**
- First-hand training experience referenced in content
- Original descriptions of real scenarios and training methods
- Specific details that can't be fabricated (class structure, drill descriptions)
- Student transformation stories with real outcomes
- Before/after descriptions grounded in actual training progression

**What to add to pages:**
- Author byline: "By Nathan Lundstrom, Self Protection Specialist — 42 years of martial arts experience"
- Personal teaching perspective woven into resource pages
- Real class descriptions, not generic martial arts language

### Expertise (Weight: 25%)

**Signals to include:**
- Nathan's credentials and background visible on every authored page
- Technical accuracy in all training descriptions (use etkm-definitions)
- Specialized vocabulary used correctly (ETKM terminology, not generic)
- Content current with modern self-defense methodology
- Author bio on blog posts with credentials

### Authoritativeness (Weight: 25%)

**Signals to build over time:**
- Student testimonials on key pages (free trial, programs)
- Links from local Tyler TX organizations, churches, law enforcement
- CBLTAC partnership and guest instructor relationships
- Consistent publication history (blog, social, email)
- Community involvement documentation

### Trustworthiness (Weight: 30%)

**ETKM already has most of these — verify they're visible:**
- Physical address on every page footer
- Phone number on every page
- HTTPS with valid certificate
- Privacy policy and terms accessible
- Real student reviews/testimonials
- Clear pricing or path to pricing
- Professional, consistent branding (etkm-brand-kit)
- Copyright year current (2026)

---

## Schema Markup — ETKM Templates

Use JSON-LD format. Place in the page `<head>` or before closing `</body>`.

### LocalBusiness (Every Page on etxkravmaga.com)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "East Texas Krav Maga",
  "url": "https://etxkravmaga.com",
  "telephone": "(903) 590-0085",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "2918 E. Grande Blvd.",
    "addressLocality": "Tyler",
    "addressRegion": "TX",
    "postalCode": "75707",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 32.3246,
    "longitude": -95.2616
  },
  "openingHours": "Mo-Sa",
  "priceRange": "$$",
  "description": "Reality-based self-defense training in Tyler, Texas. Krav Maga classes for adults, women, youth, law enforcement, and armed citizens.",
  "sameAs": [
    "https://www.facebook.com/easttexaskravmaga",
    "https://www.instagram.com/easttexaskravmaga"
  ]
}
```

### Person — Nathan (Author Pages, About Page)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Nathan Lundstrom",
  "jobTitle": "Self Protection Specialist",
  "description": "Owner and lead instructor at East Texas Krav Maga with 42 years of martial arts experience.",
  "worksFor": {
    "@type": "LocalBusiness",
    "name": "East Texas Krav Maga"
  },
  "url": "https://etxkravmaga.com/about-us/"
}
```

### Article/BlogPosting (All Blog Content)

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "[TITLE — under 60 chars]",
  "author": {
    "@type": "Person",
    "name": "Nathan Lundstrom",
    "url": "https://etxkravmaga.com/about-us/"
  },
  "publisher": {
    "@type": "LocalBusiness",
    "name": "East Texas Krav Maga",
    "url": "https://etxkravmaga.com"
  },
  "datePublished": "[ISO 8601]",
  "dateModified": "[ISO 8601]",
  "description": "[META DESCRIPTION]",
  "mainEntityOfPage": "[PAGE URL]"
}
```

### Event (CBLTAC and Future Events)

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "[EVENT NAME]",
  "startDate": "[ISO 8601]",
  "endDate": "[ISO 8601]",
  "location": {
    "@type": "Place",
    "name": "[VENUE NAME]",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "[ADDRESS]",
      "addressLocality": "Tyler",
      "addressRegion": "TX"
    }
  },
  "organizer": {
    "@type": "LocalBusiness",
    "name": "East Texas Krav Maga",
    "url": "https://etxkravmaga.com"
  },
  "offers": {
    "@type": "Offer",
    "price": "[PRICE]",
    "priceCurrency": "USD",
    "url": "[REGISTRATION URL]",
    "availability": "https://schema.org/InStock"
  },
  "description": "[EVENT DESCRIPTION]"
}
```

### Course (Program Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "[PROGRAM NAME]",
  "description": "[PROGRAM DESCRIPTION]",
  "provider": {
    "@type": "LocalBusiness",
    "name": "East Texas Krav Maga",
    "url": "https://etxkravmaga.com"
  }
}
```

### Schema Never-Do List

- Never use HowTo schema (deprecated September 2023)
- Never use FAQPage schema (restricted to government/healthcare)
- Never use placeholder text in schema values
- Always use absolute URLs, not relative
- Always use ISO 8601 dates

---

## Local SEO — Tyler TX

ETKM is a local business. Every page should reinforce local relevance.

**On-page signals:**
- "Tyler TX" or "Tyler, Texas" appears naturally in title tags, H1s, and body content
- "East Texas" referenced where natural (it's in the business name)
- Service area mentioned: Tyler and surrounding East Texas communities
- NAP (Name, Address, Phone) consistent across all pages and all domains
- Google Business Profile should match website NAP exactly

**Local content strategy:**
- Blog posts referencing Tyler-specific scenarios (parking lots, local venues)
- Event pages with Tyler venue addresses in schema markup
- Community partnerships mentioned (LifePoint, local organizations)
- "Serving Tyler TX and East Texas" in service page descriptions

---

## AI Search Optimization (GEO)

Content optimized for AI Overviews, ChatGPT, and Perplexity citations.

**What makes content citable by AI:**
- Clear, direct answers to specific questions within the first 2-3 paragraphs
- Well-structured headings that match common search queries
- Factual, authoritative statements that AI can extract as passages
- Schema markup that helps AI understand content structure
- Author attribution that establishes credibility

**ETKM-specific GEO opportunities:**
- "What is Krav Maga" — ETKM's definition should be authoritative and structured
- "Self-defense classes in Tyler TX" — local answer with schema support
- "How to prepare for a Krav Maga class" — class structure page answers this directly
- "Krav Maga vs BJJ" — Nathan has pre-built analogies for this comparison
- "Women's self-defense Tyler TX" — fightbacketx.com content

**AI crawler access:**
- Verify robots.txt allows GPTBot, ClaudeBot, PerplexityBot
- No aggressive blocking that prevents AI indexing
- Consider adding llms.txt for AI-specific content guidance

---

## Page Rewrite / New Page Workflow

When writing or rewriting any ETKM web page:

1. Load etkm-brand-foundation — voice alignment
2. Load this skill — SEO requirements
3. Write the content in ETKM voice
4. Run the SEO checklist above against the draft
5. Generate title tag and meta description
6. Identify schema markup opportunities
7. Identify internal link targets (minimum per page type)
8. Verify word count meets quality gates
9. Add author attribution where appropriate
10. Deliver: page copy + title tag + meta description + schema JSON-LD + internal link suggestions

---

## Reference: Deprecated and Restricted Schema (Do Not Use)

| Type | Status | Since |
|------|--------|-------|
| HowTo | Deprecated | September 2023 |
| FAQPage | Restricted to government/healthcare | August 2023 |
| SpecialAnnouncement | Deprecated | July 2025 |
| ClaimReview | Retired | June 2025 |

---

## Reference: Core Web Vitals Thresholds (Current)

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | Under 2.5s | 2.5-4.0s | Over 4.0s |
| INP (Interaction to Next Paint) | Under 200ms | 200-500ms | Over 500ms |
| CLS (Cumulative Layout Shift) | Under 0.1 | 0.1-0.25 | Over 0.25 |

Note: INP replaced FID as of March 2024. Never reference FID.
