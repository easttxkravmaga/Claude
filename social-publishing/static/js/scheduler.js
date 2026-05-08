/* ETKM Social Publishing — Scheduler tab JS
 * Vanilla JS, no framework. Powers Compose, All Posts, AI Generator forms.
 */

(function () {
  // ── Compose: master caption + per-platform sections ──────────────────────
  const composeCard = document.getElementById('compose-card');
  if (composeCard) {
    const limits = JSON.parse(composeCard.dataset.platformLimits || '{}');
    const platformBoxes = composeCard.querySelectorAll('input[name="platforms"]');
    const masterCaption = document.getElementById('master-caption');
    const masterCounter = document.getElementById('master-counter');
    const platformSections = document.getElementById('per-platform-sections');
    const statusSelect = document.getElementById('status-select');
    const scheduledAt = document.getElementById('scheduled-at');
    const banner = document.getElementById('compose-banner');
    const form = document.getElementById('compose-form');

    const platformLabels = {
      facebook: 'Facebook',
      instagram: 'Instagram',
      linkedin: 'LinkedIn',
    };
    const platformHints = {
      facebook: 'Facebook posts get 2-4 hashtags max.',
      instagram: 'Instagram posts get 8-15 hashtags. NEVER include URLs in the caption.',
      linkedin: 'LinkedIn posts get 3-5 hashtags. URLs are allowed.',
    };

    const perPlatformOverrides = {};

    function selectedPlatforms() {
      return Array.from(platformBoxes).filter(b => b.checked).map(b => b.value);
    }

    function updateMasterCounter() {
      const sel = selectedPlatforms();
      const limit = sel.length ? Math.min(...sel.map(p => limits[p])) : 0;
      const used = masterCaption.value.length;
      const remaining = limit - used;
      const platformNote = sel.length
        ? `${remaining} chars left for ${sel.length === 1 ? platformLabels[sel[0]] : 'tightest platform'} (${limit} max)`
        : 'pick at least one platform above';
      masterCounter.textContent = platformNote;
      masterCounter.classList.toggle('etkm-counter--warn', remaining < limit * 0.1 && remaining >= 0);
      masterCounter.classList.toggle('etkm-counter--danger', remaining < 0);
    }

    function renderPerPlatformSections() {
      const sel = selectedPlatforms();
      if (sel.length < 2) {
        platformSections.innerHTML = '';
        return;
      }

      platformSections.innerHTML = sel.map(p => {
        const captionVal = perPlatformOverrides[p] !== undefined
          ? perPlatformOverrides[p]
          : masterCaption.value;
        const cls = p === 'facebook' ? 'etkm-pill--platform-fb'
                  : p === 'instagram' ? 'etkm-pill--platform-ig'
                  : 'etkm-pill--platform-li';
        return `
          <div class="etkm-platform-section" data-platform="${p}">
            <div class="etkm-platform-section__head">
              <span class="etkm-platform-section__title">
                <span class="etkm-pill ${cls}">${platformLabels[p]}</span>
                ${platformLabels[p]} caption
              </span>
              <button type="button" class="etkm-btn etkm-btn--small" data-tailor="${p}">
                ✨ Tailor for ${platformLabels[p]}
              </button>
            </div>
            <div class="etkm-counter" data-counter-for="${p}">— chars left of ${limits[p]}</div>
            <textarea class="etkm-textarea" data-platform-caption="${p}"
                      placeholder="${platformLabels[p]} caption">${captionVal}</textarea>
            <div class="etkm-field__hint">${platformHints[p]}</div>
          </div>`;
      }).join('');

      platformSections.querySelectorAll('[data-platform-caption]').forEach(ta => {
        const p = ta.dataset.platformCaption;
        ta.addEventListener('input', () => {
          perPlatformOverrides[p] = ta.value;
          updatePlatformCounter(p);
        });
        updatePlatformCounter(p);
      });

      platformSections.querySelectorAll('[data-tailor]').forEach(btn => {
        btn.addEventListener('click', async () => {
          const p = btn.dataset.tailor;
          if (!masterCaption.value.trim()) {
            showBanner('error', 'Write a master caption first, then click Tailor.');
            return;
          }
          btn.disabled = true;
          const orig = btn.textContent;
          btn.textContent = '... tailoring';
          try {
            const r = await fetch('/api/ai/tailor-caption', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({
                master_caption: masterCaption.value,
                target_platform: p,
              }),
            });
            const data = await r.json();
            if (!r.ok || !data.ok) throw new Error(data.error || 'Tailor failed');
            const ta = platformSections.querySelector(`[data-platform-caption="${p}"]`);
            ta.value = data.tailored_caption;
            perPlatformOverrides[p] = data.tailored_caption;
            updatePlatformCounter(p);
            showBanner('success', `Tailored for ${platformLabels[p]}.`);
          } catch (e) {
            showBanner('error', `Tailor failed: ${e.message}`);
          } finally {
            btn.disabled = false;
            btn.textContent = orig;
          }
        });
      });
    }

    function updatePlatformCounter(p) {
      const el = platformSections.querySelector(`[data-counter-for="${p}"]`);
      const ta = platformSections.querySelector(`[data-platform-caption="${p}"]`);
      if (!el || !ta) return;
      const remaining = limits[p] - ta.value.length;
      el.textContent = `${remaining} chars left of ${limits[p]}`;
      el.classList.toggle('etkm-counter--warn', remaining < limits[p] * 0.1 && remaining >= 0);
      el.classList.toggle('etkm-counter--danger', remaining < 0);
    }

    function showBanner(kind, msg) {
      banner.innerHTML = `<div class="etkm-banner etkm-banner--${kind}">${msg}</div>`;
    }

    platformBoxes.forEach(b => b.addEventListener('change', () => {
      renderPerPlatformSections();
      updateMasterCounter();
    }));
    masterCaption.addEventListener('input', () => {
      updateMasterCounter();
      // Re-fill any per-platform sections that haven't been overridden
      const sel = selectedPlatforms();
      sel.forEach(p => {
        if (perPlatformOverrides[p] === undefined) {
          const ta = platformSections.querySelector(`[data-platform-caption="${p}"]`);
          if (ta) {
            ta.value = masterCaption.value;
            updatePlatformCounter(p);
          }
        }
      });
    });

    statusSelect.addEventListener('change', () => {
      scheduledAt.disabled = statusSelect.value !== 'scheduled';
    });
    scheduledAt.disabled = statusSelect.value !== 'scheduled';

    form.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const fd = new FormData(form);
      const platforms = fd.getAll('platforms');
      if (platforms.length === 0) {
        showBanner('error', 'Tick at least one platform.');
        return;
      }
      const payload = {
        title: fd.get('title'),
        master_caption: masterCaption.value,
        per_platform_captions: perPlatformOverrides,
        platforms: platforms,
        campaign_tag: fd.get('campaign_tag') || null,
        status: fd.get('status'),
        scheduled_at: fd.get('scheduled_at') || null,
        approved: fd.get('approved') === 'on',
      };
      try {
        const r = await fetch('/api/posts', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload),
        });
        const data = await r.json();
        if (!r.ok || !data.ok) throw new Error(data.error || 'Save failed');
        showBanner('success', `Saved ${data.post_ids.length} post${data.post_ids.length>1?'s':''}. Redirecting...`);
        setTimeout(() => { window.location = data.redirect; }, 800);
      } catch (e) {
        showBanner('error', `Save failed: ${e.message}`);
      }
    });

    updateMasterCounter();
  }

  // ── All Posts: row actions ───────────────────────────────────────────────
  document.querySelectorAll('.etkm-table tbody tr[data-post-id]').forEach(row => {
    const id = row.dataset.postId;
    row.querySelectorAll('button[data-action]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const action = btn.dataset.action;
        try {
          let r;
          if (action === 'delete') {
            if (!confirm('Delete this post?')) return;
            r = await fetch(`/api/posts/${id}`, {method: 'DELETE'});
          } else if (action === 'approve') {
            r = await fetch(`/api/posts/${id}/approve`, {method: 'POST'});
          } else if (action === 'retry') {
            r = await fetch(`/api/posts/${id}/retry`, {method: 'POST'});
          }
          const data = await r.json();
          if (!r.ok || !data.ok) throw new Error(data.error || 'Action failed');
          window.location.reload();
        } catch (e) {
          alert(`Failed: ${e.message}`);
        }
      });
    });
  });

  // ── AI Generator: form submit (calls /api/ai/generate-campaign) ──────────
  const aiForm = document.getElementById('ai-form');
  if (aiForm) {
    document.querySelectorAll('.etkm-quickfill button[data-fill]').forEach(b => {
      b.addEventListener('click', () => {
        const input = document.getElementById('ai-program');
        input.value = b.dataset.fill;
        input.focus();
      });
    });

    aiForm.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const fd = new FormData(aiForm);
      const banner = document.getElementById('ai-banner');
      banner.innerHTML = '<div class="etkm-banner etkm-banner--info">Generating, this takes 8-25 seconds...</div>';
      const payload = {
        program: fd.get('program'),
        tone: fd.get('tone'),
        goal: fd.get('goal'),
        platforms: fd.getAll('platforms'),
        start_date: fd.get('start_date'),
        end_date: fd.get('end_date'),
        posts_per_platform: parseInt(fd.get('posts_per_platform'), 10),
        campaign_tag: fd.get('campaign_tag'),
      };
      try {
        const r = await fetch('/api/ai/generate-campaign', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload),
        });
        const data = await r.json();
        if (!r.ok || !data.ok) throw new Error(data.error || 'Generation failed');
        banner.innerHTML = `<div class="etkm-banner etkm-banner--success">Generated ${data.posts_created} drafts.</div>`;
        setTimeout(() => { window.location = data.redirect || '/scheduler?tab=all'; }, 800);
      } catch (e) {
        banner.innerHTML = `<div class="etkm-banner etkm-banner--error">${e.message}</div>`;
      }
    });
  }
})();
