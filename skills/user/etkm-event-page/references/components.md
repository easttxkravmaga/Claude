# ETKM Event Page — Component Reference

Full CSS and HTML for every section. Replace `#W` with your wrapper ID throughout.

---

## UTILITY CLASSES

```css
#W .cp { max-width:1080px; margin:0 auto; padding:0 28px; }
#W .eyebrow { font-family:'Inter',sans-serif; font-size:10.5px; font-weight:600; letter-spacing:.2em; text-transform:uppercase; color:#BBBBBB; }
#W .rule { width:40px; height:3px; background:#CC0000; margin:18px 0 24px; }
#W .btn-p { background:#CC0000; color:#fff; font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:16px; letter-spacing:.12em; text-transform:uppercase; text-decoration:none; padding:18px 40px; transition:background .2s; display:inline-block; }
#W .btn-p:hover { background:#aa0000; }
#W .btn-g { color:#BBBBBB; font-family:'Barlow Condensed',sans-serif; font-weight:600; font-size:14px; letter-spacing:.1em; text-transform:uppercase; text-decoration:none; border-bottom:1px solid #575757; padding-bottom:2px; transition:color .2s,border-color .2s; }
#W .btn-g:hover { color:#fff; border-color:#fff; }
```

---

## 1. TOP BAR

Red announcement strip — always first.

```css
#W .topbar { background:#CC0000; padding:10px 0; text-align:center; font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:14px; letter-spacing:.12em; text-transform:uppercase; color:#fff; }
```

```html
<div class="topbar">
  [EVENT NAME] — [DATE RANGE] — Tyler, Texas — <strong>Seats Are Limited</strong>
</div>
```

---

## 2. DISCOUNT BANNER (Optional)

Only for first responder or special pricing variants.

```css
#W .disc-banner { background:#111; border-bottom:1px solid #1e1e1e; padding:20px 0; }
#W .disc-inner { display:flex; align-items:center; justify-content:center; gap:24px; flex-wrap:wrap; }
#W .disc-badge { background:#CC0000; color:#fff; font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:32px; letter-spacing:.04em; padding:10px 24px; line-height:1; }
#W .disc-text { font-size:15px; color:#BBBBBB; line-height:1.6; }
#W .disc-text strong { color:#fff; }
#W .disc-roles { display:flex; gap:10px; flex-wrap:wrap; margin-top:8px; }
#W .disc-role { background:#000; border:1px solid #2a2a2a; padding:5px 12px; font-size:10px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:#BBBBBB; }
```

```html
<div class="disc-banner">
  <div class="cp">
    <div class="disc-inner">
      <div class="disc-badge">50% OFF</div>
      <div class="disc-text">
        <strong>[Discount Name] — [Short reason].</strong><br>
        [Who qualifies] receive [X]% off all sessions. No code needed — discount applied at checkout.
        <div class="disc-roles">
          <div class="disc-role">&#128737; [Role 1]</div>
          <div class="disc-role">&#128293; [Role 2]</div>
        </div>
      </div>
    </div>
  </div>
</div>
```

---

## 3. HERO

```css
#W .hero { padding:80px 0 64px; border-bottom:1px solid #1e1e1e; position:relative; overflow:hidden; background:#000; }
#W .hero::after { content:''; position:absolute; top:0; right:0; width:35%; height:100%; background:linear-gradient(to left,rgba(204,0,0,.06),transparent); pointer-events:none; }
#W .hero-ey { display:flex; align-items:center; gap:10px; margin-bottom:28px; }
#W .hero-ey-line { width:28px; height:2px; background:#CC0000; flex-shrink:0; }
#W .hero h1 { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:clamp(46px,7vw,96px); line-height:.91; text-transform:uppercase; letter-spacing:-.01em; max-width:860px; margin-bottom:32px; color:#fff; }
#W .hero h1 em { font-style:normal; color:#CC0000; display:block; }
#W .hero-sub { font-size:18px; font-weight:400; color:#BBBBBB; max-width:580px; line-height:1.75; margin-bottom:48px; }
#W .cta-grp { display:flex; align-items:center; gap:20px; flex-wrap:wrap; }
```

```html
<section class="hero">
  <div class="cp">
    <div class="hero-ey fd">
      <div class="hero-ey-line"></div>
      <span class="eyebrow">[EYEBROW TEXT] &mdash; Tyler, TX</span>
    </div>
    <h1 class="fd">
      [LINE 1]
      <em>[ACCENT LINE IN RED]</em>
      [LINE 3 — optional]
    </h1>
    <p class="hero-sub fd">[Subheadline — 2 sentences max]</p>
    <div class="hero-btns fd">
      <a href="#register" class="btn-p">Register Now</a>
      <a href="#courses" class="btn-g">View Courses</a>
    </div>
    <!-- EVENT BAR goes here -->
  </div>
</section>
```

---

## 4. EVENT BAR

Inside the hero, below CTAs.

```css
#W .evbar { margin-top:56px; border:1px solid #2a2a2a; background:#111; padding:24px 28px; display:flex; flex-wrap:wrap; gap:12px 36px; align-items:center; }
#W .ebi-lbl { font-size:10px; font-weight:600; letter-spacing:.18em; text-transform:uppercase; color:#575757; }
#W .ebi-val { font-size:14.5px; font-weight:500; color:#fff; }
/* For discounted pricing, add: */
#W .ebi-strike { text-decoration:line-through; color:#575757; font-size:12px; margin-left:6px; }
```

```html
<div class="evbar fd">
  <div>
    <div class="ebi-lbl">Location</div>
    <div class="ebi-val">[VENUE] &mdash; Tyler, TX</div>
  </div>
  <div>
    <div class="ebi-lbl">Course 1 &mdash; [TITLE]</div>
    <div class="ebi-val">[DAY], [DATE] &middot; [TIME] &middot; $[PRICE]</div>
  </div>
  <div>
    <div class="ebi-lbl">Course 2 &mdash; [TITLE]</div>
    <div class="ebi-val">[DAY], [DATE] &middot; [TIME] &middot; $[PRICE]</div>
  </div>
  <div>
    <div class="ebi-lbl">Best Value</div>
    <div class="ebi-val">Both Sessions &middot; $[PRICE]</div>
  </div>
</div>
```

---

## 5. WHO THIS IS FOR

```css
#W .sec { padding:80px 0; border-bottom:1px solid #1a1a1a; background:#000; }
#W .sec-dark { padding:80px 0; border-bottom:1px solid #1a1a1a; background:#111; }
#W .sec-hd { margin-bottom:44px; }
#W .sec-hd h2 { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:clamp(36px,5vw,60px); line-height:.95; text-transform:uppercase; letter-spacing:-.01em; color:#fff; }
#W .who-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1px; background:#1e1e1e; border:1px solid #1e1e1e; }
#W .wc { background:#111; padding:26px 22px; transition:background .2s; }
#W .wc:hover { background:#1a1a1a; }
#W .wc-ico { font-size:22px; margin-bottom:10px; }
#W .wc-ttl { font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:17px; letter-spacing:.04em; text-transform:uppercase; color:#fff; margin-bottom:7px; }
#W .wc-txt { font-size:13px; color:#BBBBBB; line-height:1.55; }
```

```html
<section class="sec">
  <div class="cp">
    <div class="fd">
      <span class="eyebrow">Who This Is For</span>
      <div class="rule"></div>
      <div class="sec-hd"><h2>[AUDIENCE HEADLINE]</h2></div>
    </div>
    <div class="who-grid fd">
      <div class="wc">
        <div class="wc-ico">&#128737;</div>
        <div class="wc-ttl">[Audience Segment]</div>
        <div class="wc-txt">[1-2 sentences — their specific pain point and why this training matters to them]</div>
      </div>
      <!-- Repeat for 6–8 segments -->
    </div>
  </div>
</section>
```

---

## 6. CLASSROOM / PROOF PHOTO (Optional)

```css
#W .cls-photo { background:#000; padding:0; overflow:hidden; border-bottom:1px solid #1a1a1a; }
#W .cls-photo-inner { position:relative; max-height:520px; overflow:hidden; }
#W .cls-photo img { width:100%; display:block; filter:grayscale(100%) contrast(1.08); object-fit:cover; }
#W .cls-overlay { position:absolute; inset:0; background:linear-gradient(to right,rgba(0,0,0,.7) 0%,rgba(0,0,0,.1) 60%); }
#W .cls-text { position:absolute; top:50%; left:0; transform:translateY(-50%); padding:0 52px; max-width:600px; }
#W .cls-headline { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:clamp(28px,3.5vw,46px); text-transform:uppercase; line-height:.97; color:#fff; }
#W .cls-headline span { color:#CC0000; }
#W .cls-badge { position:absolute; bottom:20px; right:24px; background:rgba(0,0,0,.75); border:1px solid #2a2a2a; padding:8px 14px; }
```

```html
<div class="cls-photo">
  <div class="cls-photo-inner">
    <img src="data:image/jpeg;base64,[B64]" alt="[ALT TEXT]">
    <div class="cls-overlay"></div>
    <div class="cls-text">
      <div class="cls-headline">This Is What<br><span>Real Training</span><br>Looks Like.</div>
    </div>
    <div class="cls-badge">
      <div style="font-size:10px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#CC0000;font-family:'Inter',sans-serif;">CBL Training &amp; Consulting</div>
      <div style="font-size:12px;color:#BBBBBB;font-family:'Inter',sans-serif;margin-top:2px;">East Texas &mdash; Previous Session</div>
    </div>
  </div>
</div>
```

---

## 7. CORE INSIGHT BLOCK

The "bad decisions" statement. Always present. Copy adapts slightly per variant.

```css
#W .insight { background:#111; border-left:4px solid #CC0000; padding:72px 0; }
#W .iq { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:clamp(28px,4vw,50px); line-height:1.08; text-transform:uppercase; color:#fff; margin-bottom:24px; }
#W .iq strong { color:#CC0000; }
#W .ib { font-size:16.5px; color:#BBBBBB; line-height:1.75; max-width:640px; }
```

```html
<div class="insight">
  <div class="cp">
    <div class="fd" style="max-width:760px;">
      <span class="eyebrow" style="display:block;margin-bottom:18px;">[Eyebrow]</span>
      <p class="iq">Bad decisions don&#39;t come from<br><strong>lack of [skill/training].</strong><br>They come from unmanaged stress.</p>
      <p class="ib">[2–3 sentences connecting the core truth to this specific audience's reality.]</p>
    </div>
  </div>
</div>
```

---

## 8. FORMAT BLOCK (Optional — "How This Works")

Use when the training format needs explanation (interactive, hands-on optional, etc.)

```css
#W .format-block { background:#111; border:1px solid #222; border-left:4px solid #CC0000; padding:48px 52px; margin-top:48px; }
#W .format-block h3 { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:clamp(26px,3vw,40px); text-transform:uppercase; color:#fff; line-height:1.0; margin-bottom:20px; }
#W .format-block h3 em { font-style:normal; color:#CC0000; }
#W .format-block p { font-size:16px; color:#BBBBBB; line-height:1.75; margin-bottom:16px; }
#W .format-block p strong { color:#fff; }
#W .ftags { display:flex; flex-wrap:wrap; gap:10px; margin-top:28px; }
#W .ftag { background:#000; border:1px solid #2a2a2a; padding:8px 16px; font-size:11px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:#BBBBBB; }
```

---

## 9. COURSE BLOCKS

Two-column layout. Course 1: meta left, content right. Course 2: content left, meta right.

```css
#W .courses-sec { padding:80px 0; border-bottom:1px solid #1a1a1a; background:#000; }
#W .cb { display:grid; grid-template-columns:1fr 1fr; gap:0; border:1px solid #222; margin-bottom:36px; background:#111; }
#W .cm { padding:44px 40px; border-right:1px solid #222; display:flex; flex-direction:column; }
#W .cm-r { padding:44px 40px; border-left:1px solid #222; display:flex; flex-direction:column; }
#W .ctag { font-size:10px; font-weight:600; letter-spacing:.2em; text-transform:uppercase; color:#CC0000; margin-bottom:18px; }
#W .ctitle { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:34px; line-height:1.0; text-transform:uppercase; color:#fff; margin-bottom:18px; }
#W .cdpill { display:inline-flex; align-items:center; gap:6px; background:#000; border:1px solid #2a2a2a; padding:7px 14px; font-size:11.5px; font-weight:600; letter-spacing:.1em; text-transform:uppercase; color:#BBBBBB; margin-bottom:22px; width:fit-content; }
#W .cdpill span { color:#fff; }
#W .cdesc { font-size:14.5px; color:#BBBBBB; line-height:1.7; margin-bottom:24px; flex-grow:1; }
#W .cprice { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:40px; color:#fff; letter-spacing:-.02em; }
#W .cprice sup { font-size:20px; vertical-align:super; }
#W .cpnote { font-size:11px; color:#575757; letter-spacing:.1em; text-transform:uppercase; margin-top:3px; }
#W .ccta { background:#CC0000; color:#fff; font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:14px; letter-spacing:.12em; text-transform:uppercase; text-decoration:none; padding:13px 26px; margin-top:22px; display:inline-block; transition:background .2s; width:fit-content; }
#W .ccta:hover { background:#aa0000; }
#W .cc { padding:44px 40px; }
#W .cc-lbl { font-size:10px; font-weight:600; letter-spacing:.2em; text-transform:uppercase; color:#575757; margin-bottom:14px; margin-top:24px; }
#W .cc-lbl:first-child { margin-top:0; }
#W .ll { list-style:none; margin-bottom:20px; }
#W .ll li { font-size:14px; color:#BBBBBB; padding:8px 0 8px 18px; border-bottom:1px solid #1e1e1e; position:relative; line-height:1.5; }
#W .ll li::before { content:'—'; position:absolute; left:0; color:#CC0000; font-weight:700; }
#W .ai { background:#000; border:1px solid #1e1e1e; border-left:3px solid #1e1e1e; padding:13px 15px; margin-bottom:7px; transition:border-color .2s; }
#W .ai:hover { border-left-color:#CC0000; }
#W .ar { font-size:10px; font-weight:700; letter-spacing:.18em; text-transform:uppercase; color:#CC0000; margin-bottom:3px; }
#W .at { font-size:13px; color:#BBBBBB; line-height:1.5; }
```

**Course 1 HTML structure:**
```html
<div class="cb fd">
  <div class="cm">  <!-- META: left column -->
    <div class="ctag">Course 1 of 2</div>
    <div class="ctitle">[COURSE TITLE]</div>
    <div class="cdpill">&#128197; [DAY], [DATE] &nbsp;|&nbsp; <span>[TIME]</span></div>
    <p class="cdesc">[2-3 sentence overview]</p>
    <div class="cprice"><sup>$</sup>[PRICE]</div>
    <div class="cpnote">Per Person &middot; Single Session</div>
    <!-- Ecwid embed (Course 1 product) -->
    <div class="ccta-wrap">
      [ECWID_EMBED_C1]
    </div>
  </div>
  <div class="cc">  <!-- CONTENT: right column -->
    <div class="cc-lbl">What You'll Learn</div>
    <ul class="ll">
      <li>[Learning point]</li>
    </ul>
    <div class="cc-lbl">How This Applies in Real Life</div>
    <div class="ai"><div class="ar">[AUDIENCE]</div><div class="at">[Application]</div></div>
  </div>
</div>
```

**Course 2 HTML structure** (reversed — content left, meta right):
```html
<div class="cb fd">
  <div class="cc">  <!-- CONTENT: left -->
    ...
  </div>
  <div class="cm-r">  <!-- META: right -->
    ...
    <!-- Ecwid embed (Course 2 product) -->
    <div class="ccta-wrap">
      [ECWID_EMBED_C2]
    </div>
  </div>
</div>
```

---

## 10. COMBINED / BEST VALUE BLOCK

```css
#W .combo-blk { background:#111; border:1px solid #222; border-top:4px solid #CC0000; padding:52px 48px; }
#W .combo-hdr { display:grid; grid-template-columns:1fr auto; gap:28px; align-items:start; margin-bottom:44px; }
#W .combo-ttl { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:clamp(26px,3.5vw,42px); line-height:1.0; text-transform:uppercase; color:#fff; }
#W .combo-pr { text-align:right; }
#W .combo-prn { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:52px; color:#fff; line-height:1; }
#W .combo-prn sup { font-size:24px; vertical-align:super; }
#W .combo-save { font-size:11px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:#CC0000; margin-top:4px; }
#W .combo-inc { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:36px; }
#W .ci { background:#000; border:1px solid #1e1e1e; padding:22px; }
#W .ci-n { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:44px; color:#1e1e1e; line-height:1; margin-bottom:7px; }
#W .ci-t { font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:16px; text-transform:uppercase; color:#fff; margin-bottom:7px; }
#W .ci-d { font-size:13px; color:#575757; line-height:1.5; }
#W .combo-why { background:#000; border:1px solid #1e1e1e; border-left:3px solid #CC0000; padding:26px 30px; margin-bottom:32px; }
#W .combo-why p { font-size:15.5px; color:#BBBBBB; line-height:1.7; }
#W .combo-why p strong { color:#fff; }
/* Ecwid handles the button styling now, but we keep the wrapper clean */
#W .combo-cta-wrap { margin-top: 20px; }
```

---

## 11. INSTRUCTOR BLOCK

```css
#W .inst-grid { display:grid; grid-template-columns:280px 1fr; gap:56px; align-items:start; }
#W .inst-card { background:#111; border:1px solid #222; padding:0; overflow:hidden; }
#W .inst-photo { width:100%; aspect-ratio:4/5; object-fit:cover; object-position:center top; display:block; filter:grayscale(100%) contrast(1.05); }
#W .inst-card-body { padding:24px; }
#W .inst-name { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:22px; text-transform:uppercase; color:#fff; margin-bottom:5px; }
#W .inst-tag { font-size:11px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:#CC0000; margin-bottom:14px; }
#W .inst-creds { display:flex; flex-direction:column; gap:6px; margin-top:14px; }
#W .inst-cred { display:flex; align-items:center; gap:8px; font-size:11.5px; color:#575757; }
#W .inst-cred::before { content:''; width:3px; height:3px; background:#CC0000; border-radius:50%; flex-shrink:0; }
#W .inst-bio h3 { font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:clamp(24px,3vw,38px); text-transform:uppercase; color:#fff; margin-bottom:14px; line-height:1.05; }
#W .inst-bio p { font-size:15px; color:#BBBBBB; line-height:1.75; margin-bottom:18px; }
```

---

## 12. LOCATION BLOCK

```css
#W .loc-blk { background:#111; border:1px solid #222; padding:40px 44px; display:grid; grid-template-columns:1fr 1fr; gap:44px; align-items:center; }
#W .loc-lbl { font-size:10px; font-weight:600; letter-spacing:.18em; text-transform:uppercase; color:#575757; margin-bottom:7px; }
#W .loc-name { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:26px; text-transform:uppercase; color:#fff; margin-bottom:7px; }
#W .loc-addr { font-size:15px; color:#BBBBBB; line-height:1.6; }
#W .loc-note { font-size:13px; color:#575757; border-top:1px solid #222; padding-top:18px; margin-top:20px; line-height:1.6; }
```

---

## 13. FINAL CTA

```css
#W .fcta { padding:96px 0; background:#111; border-top:1px solid #1e1e1e; text-align:center; }
#W .fcta h2 { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:clamp(34px,5vw,64px); text-transform:uppercase; line-height:.95; color:#fff; margin-bottom:18px; }
#W .fcta h2 em { font-style:normal; color:#CC0000; }
#W .fcta p { font-size:16.5px; color:#BBBBBB; max-width:520px; margin:0 auto 36px; line-height:1.7; }
#W .fopts { display:flex; justify-content:center; flex-wrap:wrap; gap:14px; }
#W .fopt { background:#000; border:1px solid #2a2a2a; padding:22px 28px; text-align:center; transition:border-color .2s,background .2s; min-width:185px; }
#W .fopt:hover { border-color:#CC0000; background:#1a1a1a; }
#W .fopt-p { font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:32px; color:#fff; }
#W .fopt-l { font-size:11px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:#BBBBBB; margin-top:4px; margin-bottom:16px; }
#W .fcta-main-wrap { margin:36px auto 0; width:fit-content; }
```

```html
<section class="fcta">
  <div class="cp">
    <h2 class="fd">[LINE 1]<br><em>[RED LINE]</em></h2>
    <p class="fd">Seats are limited. Reserve your seat now.</p>
    <div class="fopts fd">
      <div class="fopt">
        <div class="fopt-p">$[C1_PRICE]</div>
        <div class="fopt-l">Course 1 Only<br>[DAY], [MONTH DATE]</div>
        <div class="ccta-wrap">[ECWID_EMBED_C1]</div>
      </div>
      <div class="fopt">
        <div class="fopt-p">$[C2_PRICE]</div>
        <div class="fopt-l">Course 2 Only<br>[DAY], [MONTH DATE]</div>
        <div class="ccta-wrap">[ECWID_EMBED_C2]</div>
      </div>
      <div class="fopt" style="border-color:#CC0000;">
        <div class="fopt-p" style="color:#CC0000;">$[BOTH_PRICE]</div>
        <div class="fopt-l">Both Sessions<br>Best Value &mdash; Save $[SAVINGS]</div>
        <div class="ccta-wrap">[ECWID_EMBED_BOTH]</div>
      </div>
    </div>
    <div class="fcta-main-wrap fd">
      [ECWID_EMBED_BOTH]
    </div>
  </div>
</section>
```

---

## 14. FOOTER

```css
#W .etkm-foot { background:#000; border-top:1px solid #1a1a1a; padding:28px 0; text-align:center; }
#W .etkm-foot p { font-size:12px; color:#575757; line-height:1.7; }
#W .etkm-foot a { color:#BBBBBB; text-decoration:none; }
```

```html
<div class="etkm-foot">
  <div class="cp">
    <p>East Texas Krav Maga &middot; 2918 E. Grande Blvd., Tyler TX 75707 &middot; <a href="tel:9035900085">(903) 590-0085</a> &middot; <a href="https://etxkravmaga.com" target="_blank">etxkravmaga.com</a></p>
    <p style="margin-top:7px;">[EVENT NAME] with [INSTRUCTOR] &mdash; [DATES] &mdash; Tyler, Texas</p>
  </div>
</div>
```

---

## RESPONSIVE BREAKPOINT (Always Include)

```css
@media(max-width:860px){
  #W .cb { grid-template-columns:1fr; }
  #W .cm { border-right:none!important; border-bottom:1px solid #222; }
  #W .cm-r { border-left:none!important; border-bottom:1px solid #222; order:-1; }
  #W .combo-inc { grid-template-columns:1fr; }
  #W .combo-hdr { grid-template-columns:1fr; }
  #W .combo-pr { text-align:left; }
  #W .combo-blk { padding:32px 24px; }
  #W .inst-grid { grid-template-columns:1fr; }
  #W .inst-card { max-width:320px; }
  #W .loc-blk { grid-template-columns:1fr; }
  #W .evbar { flex-direction:column; gap:14px; }
  #W .format-block { padding:32px 28px; }
  #W .cls-text { padding:0 24px; }
  #W .disc-inner { flex-direction:column; text-align:center; }
}
```
