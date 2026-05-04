---
name: etkm-ecwid-intelligence
version: 1.0
updated: 2026-05-03
description: >
  The single authority on Ecwid (by Lightspeed) for the ETKM stack. Load this
  skill for ANY task involving the ETKM pro shop, Ecwid storefront, product
  catalog, order management, payment processing (Square), Printful dropshipping,
  digital product delivery, abandoned cart recovery, Ecwid API operations,
  Ecwid-Pipedrive sync, Ecwid-n8n automation, WordPress embedding,
  storefront customization, or any ecommerce decision for ETKM. This skill
  contains complete platform knowledge: plan tiers, feature gates, API
  endpoints, webhook events, rate limits, authentication, integration paths,
  known limitations, and ETKM-specific configuration. Do NOT operate on the
  ETKM pro shop or make ecommerce decisions without this skill loaded.
triggers:
  - "pro shop"
  - "Ecwid"
  - "ecommerce"
  - "online store"
  - "product catalog"
  - "Printful"
  - "print on demand"
  - "POD"
  - "apparel"
  - "merch"
  - "merchandise"
  - "digital products"
  - "downloadable"
  - "payment processing"
  - "Square payment"
  - "abandoned cart"
  - "order management"
  - "shipping"
  - "storefront"
  - "product variations"
  - "inventory"
  - "Ecwid API"
  - "store webhook"
  - "ecommerce automation"
  - "Campus Ready purchase"
  - "sell courses"
  - "sell PDFs"
  - "payment plan"
  - "installment"
  - "pro shop redesign"
  - "store reorganization"
---

# ETKM Ecwid Intelligence Hub

**Version:** 1.0  |  **Updated:** 2026-05-03  |  **Next Review:** 2026-08-03

## SECTION 1 — PLATFORM OVERVIEW

Ecwid (by Lightspeed) is a hosted SaaS ecommerce platform designed to embed into existing websites. Not self-hostable. All data lives on Ecwid AWS infrastructure. Accessed via my.ecwid.com admin, REST API, or mobile app. Ecwid was built as an embeddable widget first — the strongest WordPress-embedded ecommerce option. ETKM pro shop lives at /store/ via the official Ecwid plugin.

### Ecwid in the ETKM Stack

| Layer | System | What It Owns |
|---|---|---|
| Ecommerce | **Ecwid** | Products, orders, customers, digital downloads, storefront |
| Payment Processing | **Square** | Card processing, transactions, settlement |
| CRM | Pipedrive | Deals, contacts, pipeline stages |
| Operations | Notion | Projects, tasks, content, SOPs |
| Automation | n8n | Bidirectional sync between systems |
| AI | Claude API + MCP | Intelligence, content, store management |
| Website | WordPress + GeneratePress | Public site; Ecwid embeds inside |
| Messaging | Telegram | Sheriff Agent, ops notifications |
| Dropshipping | Printful | Apparel fulfillment, POD production |

Division of truth: Ecwid = product catalog, orders, ecommerce customers. Pipedrive = sales pipeline, CRM contacts. Square = payment transactions, settlement. Never duplicate without n8n sync logic.

Lightspeed acquired Ecwid Oct 1, 2021. Free plan killed Nov 20, 2025. Pricing trending up. Support quality declined. Admin/API/App Market remain independent for now.

## SECTION 2 — PLAN TIERS AND FEATURE GATES

| Tier | Price (annual) | Products | Key Gates |
|---|---|---|---|
| Starter | ~$5 | 5 | No API, no App Market. Not viable. |
| Venture | ~$15/mo | 100 | Digital products, Printful partial, social selling. No variations, no abandoned cart, no staff. Current ETKM plan. |
| Business | ~$45/mo | 2,500 | Variations, abandoned cart, subscriptions, reviews, 2 staff, phone support. Recommended upgrade. |
| Unlimited | ~$105/mo | Unlimited | Unlimited staff, POS, priority support. Future scale tier. |

**ETKM Decision (May 2026): Upgrade Venture to Business.** Abandoned cart recovery ($100-300/mo) pays for the $30/mo delta in month one. Planned promotions enable seasonal drops. Reviews add social proof. 2 staff accounts enable team growth.

## SECTION 3 — PAYMENT PROCESSING

Primary processor: **Square.** Configured as Ecwid payment gateway. 2.9% + $0.30 per transaction. On-site checkout (no redirect). Orders appear in both Ecwid admin and Square Dashboard.

Square capabilities: one-time payments (yes), on-site form (yes), Apple/Google Pay (yes), refunds from Ecwid (no — use Square Dashboard), recurring subscriptions (NO — locked to Stripe/Lightspeed Payments), dispute management (no — Square Dashboard only).

**Critical:** Ecwid subscriptions do not work with Square. ETKM uses one-time purchases only.

Split payments for Campus Ready ($297 or 3x$99): Option A (recommended) — two separate SKUs. Option B — third-party installment app (Sezzle/Klarna/Afterpay, 2-6% fee). Option C — manual invoices via n8n.

Ecwid charges **0% transaction fees** on all plans. Only Square takes its cut.

## SECTION 4 — PRODUCTS AND CATALOG

Product types: Physical (apparel, gear), Digital (PDFs up to 25GB, auto-download on purchase), Service (lessons), Subscription (NOT for ETKM — Square limitation).

Digital delivery: checkout completes, Ecwid sends confirmation email with unique download link. No manual delivery needed.

Printful dropshipping: connect free app, design in mockup generator, push to Ecwid, customer orders, Printful prints/ships, tracking auto-syncs. Margins: t-shirt ~48%, hoodie ~30%, embroidered ~32%. ETKM strategy: limited-time seasonal drops, hero SKUs only, brand design system applied.

Recommended categories: Apparel (T-Shirts, Hoodies, Hats), Training Gear, Programs (Campus Ready, Field Manuals, Assessment Guides), Limited Editions (seasonal collections).

## SECTION 5 — REST API

Base URL: `https://app.ecwid.com/api/v3/{storeId}/`  
Auth: `Authorization: Bearer secret_*` (OAuth 2.0, tokens never expire)  
Rate: 600 req/min per token (429 + Retry-After on exceed)  
Format: JSON. Compression: gzip. Field selection: responseFields param.  
Plans: Venture+ only (not Starter). No GraphQL.

Key endpoints: /products, /products/{id}/variations, /categories, /orders, /customers, /discount_coupons, /batch (up to 500 bundled requests), /profile (settings, shipping, payment options).

Scopes to grant: read_store_profile, update_store_profile, read_catalog, update_catalog, create_catalog, read_orders, update_orders, create_orders, read_customers, update_customers, create_customers, read_discount_coupons, update_discount_coupons, customize_storefront, read_staff, update_staff, read_store_stats.

Claude can read: full catalog, orders, customers, coupons, reports, settings, staff. Claude can write: products, categories, inventory, prices, orders, statuses, tracking, coupons, customers, shipping, custom CSS/JS. Claude cannot: process Square refunds, modify checkout flow, rotate app keys, cancel plan.

Errors: 400 bad request, 401 unauthorized, 403 forbidden, 404 not found, 409 conflict, 422 unprocessable, 429 rate limited, 500 server error.

## SECTION 6 — WEBHOOKS

Single HTTPS endpoint per app. Payload: storeId, entityId, eventType, data. Signature: X-Ecwid-Webhook-Signature header. Setup requires contacting Ecwid support.

Events: order.created/updated/deleted, unfinished_order.created/updated/deleted, product.created/updated/deleted, category.created/updated/deleted, customer.created/updated/deleted, customer_group.created/updated/deleted, discount_coupon.created/updated/deleted, promotion.created/updated/deleted, profile.updated, profile.subscriptionStatusChanged, application.installed/uninstalled/subscriptionStatusChanged.

Retry: 4 attempts at 15-min intervals, then hourly for 24 hours, then dropped. Build daily reconciliation cron in n8n.

Critical: webhooks are notifications only. Always re-query API for current state. Events can arrive out of order.

## SECTION 7 — INTEGRATIONS

Zapier: native app with triggers (New Customer, New Paid Order, New Product, New Abandoned Cart) and actions (Create Customer/Order/Product, Update Product). Primary Ecwid-Pipedrive middleware.

n8n: no dedicated node. Use HTTP Request with Bearer token. Most flexible for custom automation.

Make.com: no official module. Not recommended.

Pipedrive: no native integration. Connect via Zapier (recommended) or n8n (most flexible). Reference flow: order.created webhook to n8n, fetch full order via API, search/create Pipedrive person, create deal, notify via Telegram.

WordPress: official plugin ecwid-shopping-cart. Auto-creates /store/ page. SSO, embedded admin, shortcodes. Limitations: one storefront per page, some SEO indexing issues.

Analytics: GA4, GTM, Meta Pixel, TikTok Pixel, Pinterest Tag, Snap Pixel — all native fields.

Accounting: QuickBooks via Synder ($20+/mo), Xero via Synder/Zapier.

Email: Mailchimp deep native (Business+), Omnisend/Marsello via App Market, others via Zapier.

Shipping: USPS/UPS/FedEx native live rates, ShipStation/ShippingEasy/Easyship via App Market.

## SECTION 8 — STOREFRONT CUSTOMIZATION

No-code: built-in design panel. Low-code: custom CSS injection (admin > Design > Themes). Full-code: Storefront JS API + custom app injection.

ETKM brand alignment: #000000 primary, #FFFFFF secondary, #CC0000 accent (NOT #FF0000), #575757 gray, #BBBBBB light gray, Montserrat 900 headlines, Inter 400 body, grayscale(100%) images, color:#fff !important on red buttons.

JS API: Ecwid.OnAPILoaded, Ecwid.OnPageLoaded, Ecwid.OnCartChanged, Ecwid.openPage, Ecwid.getStorefrontLang.

## SECTION 9 — ABANDONED CART RECOVERY (Business+)

Customer adds to cart, doesn't checkout. Ecwid captures email + cart. After configurable delay (1h/6h/24h), sends recovery email with cart contents and checkout link. Enable at admin > Marketing > Abandoned Cart Recovery.

Revenue impact at $10K/mo: ~$100-300/mo recovered = $1,200-3,600/year. Business plan cost: $360/year. ROI: 3.3x-10x.

Webhook: unfinished_order.created fires on abandonment. Use for custom n8n follow-ups, Pipedrive logging, Claude-generated recovery copy.

## SECTION 10 — DATA AND BACKUP

Export: products/customers/orders via admin CSV. All entities via REST API (JSON). Backup protocol: weekly CSV, nightly n8n cron to Google Drive, quarterly full export. Never store API tokens in Notion.

Migration: Cart2Cart and LitExtension support Ecwid. Built-in WooCommerce importer in Ecwid plugin.

## SECTION 11 — SECURITY

PCI DSS Level 1. AES-256. HTTPS enforced. Auto SSL. AWS hosted. GDPR: native cookie consent, customer export/delete, Ecwid = Data Processor, merchant = Data Controller. Best practices: 2FA, distinct admin email, secret tokens server-side only, store tokens in n8n credentials.

## SECTION 12 — LIMITATIONS AND GOTCHAS

No GraphQL. No native Pipedrive/n8n/Make integration. Square cannot do recurring billing. Limited audit logs. Webhook URL changes require support. 24-hour webhook retry cap. App key rotation is disruptive. Support quality degraded post-Lightspeed.

Known issues: Google indexing on some WP configs, tax-inclusive pricing bug, billing friction, Instant Site rigidity, 4+ second page loads on some configs.

What not to do: never use Square for subscriptions; never expose secret tokens in client JS; never rely on webhooks as sole data source; never assume delivery order; never store tokens in Notion; never use #FF0000 (use #CC0000).

## SECTION 13 — ETKM REFERENCE ARCHITECTURE

Order flow: Customer > Ecwid (Square) > webhook > n8n > fetch order > Pipedrive contact+deal > Telegram notify > digital auto-download or Printful auto-fulfill.

Daily reconciliation: n8n cron > Ecwid API orders last 24h > compare Pipedrive deals > flag mismatches > Telegram alert.

Notion location: Ecwid Deep Reference Page under ETKM Big Projects List. URL: https://www.notion.so/356924c8167381aab205de8d10e56db1

Cost model (Business): Ecwid $45/mo + Square fees ~$320/mo (at $10K) + Printful variable + Synder $20/mo + Zapier $20-50/mo = ~$405-435/mo total.

## SECTION 14 — COMPETITIVE CONTEXT

Ecwid wins for ETKM: best WP embed, 0% transaction fees, Square support, Printful native, clean REST API, $45/mo Business plan. Reconsider if: app gaps cost >$500/mo (Shopify), need self-hosted/multi-vendor (WooCommerce), exceed 2,500 products (BigCommerce), support blocks revenue bug >2 weeks (escalate).

## SECTION 15 — MAINTENANCE

Next review: 2026-08-03. Quarterly: verify plan/pricing, check API changelog, test token, review webhook success rate, audit catalog, verify Printful sync, check Square status, review App Market, update skill version, sync Notion page.

## SECTION 16 — RECOVERY

Token compromised: delete app, create new, update all workflows, re-register webhooks, test. Webhook failure: check n8n logs, verify endpoint, check SSL, reconcile if >24h down. Square failure: check Square Dashboard, verify Ecwid connection, reconnect, test small transaction. Printful failure: check Printful Dashboard, reconnect, re-sync, test order.

## SECTION 17 — HARD LIMITS

API: 600 req/min per token. Batch: 500 per request. Products: 100 (Venture), 2,500 (Business), unlimited (Unlimited). Digital files: 25GB. Staff: 0/2/unlimited. Webhook retry: 24 hours then dropped. Square regions: US, UK, CA, AU, JP, IE. Extra fields: 8KB per order.