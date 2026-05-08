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

    // ── Media upload (image direct, video signed URL) ──────────────────────
    const drop = document.getElementById('media-drop');
    const fileInput = document.getElementById('media-file');
    const prompt = document.getElementById('media-prompt');
    const progress = document.getElementById('media-progress');
    const progressBar = document.getElementById('media-progress-bar');
    const progressLabel = document.getElementById('media-progress-label');
    const preview = document.getElementById('media-preview');
    const warning = document.getElementById('media-warning');

    let mediaState = {
      gcs_path: null,
      mime: null,
      size: null,
      media_type: 'none',
      duration_sec: null,
      aspect_ratio: null,
    };

    function setProgress(pct, label) {
      progress.classList.remove('etkm-hidden');
      prompt.classList.add('etkm-hidden');
      progressBar.style.width = pct + '%';
      if (label) progressLabel.textContent = label;
    }
    function clearProgress() { progress.classList.add('etkm-hidden'); }

    function showPreview(html) {
      prompt.classList.add('etkm-hidden');
      progress.classList.add('etkm-hidden');
      preview.classList.remove('etkm-hidden');
      preview.innerHTML = html + ' <button type="button" id="media-remove" class="etkm-btn etkm-btn--small" style="margin-left:8px;">Remove</button>';
      document.getElementById('media-remove').addEventListener('click', resetMedia);
    }

    function resetMedia() {
      mediaState = {gcs_path: null, mime: null, size: null, media_type: 'none', duration_sec: null, aspect_ratio: null};
      preview.classList.add('etkm-hidden');
      prompt.classList.remove('etkm-hidden');
      progress.classList.add('etkm-hidden');
      warning.classList.add('etkm-hidden');
      warning.innerHTML = '';
      fileInput.value = '';
    }

    function checkAspectWarning() {
      const sel = selectedPlatforms();
      if (
        mediaState.media_type === 'video' &&
        sel.includes('instagram') &&
        mediaState.aspect_ratio &&
        mediaState.aspect_ratio !== '9:16'
      ) {
        warning.classList.remove('etkm-hidden');
        warning.innerHTML = '<div class="etkm-banner etkm-banner--error">⚠ Instagram Reels expect 9:16 vertical video. This video is ' + mediaState.aspect_ratio + ' — Instagram will publish it with black bars on the sides. Re-export at 1080×1920 to fix.</div>';
      } else {
        warning.classList.add('etkm-hidden');
        warning.innerHTML = '';
      }
    }

    drop.addEventListener('click', (e) => {
      if (e.target === drop || e.target.closest('#media-prompt')) {
        fileInput.click();
      }
    });

    fileInput.addEventListener('change', async () => {
      const file = fileInput.files && fileInput.files[0];
      if (!file) return;
      const isVideo = file.type === 'video/mp4';
      const isImage = file.type.startsWith('image/');
      if (!isVideo && !isImage) {
        showBanner('error', 'Unsupported file type. Use PNG, JPG, GIF, WebP, or MP4.');
        resetMedia();
        return;
      }

      try {
        if (isImage) await uploadImage(file);
        else await uploadVideo(file);
        checkAspectWarning();
      } catch (e) {
        showBanner('error', `Upload failed: ${e.message}`);
        resetMedia();
      }
    });

    async function uploadImage(file) {
      if (file.size > 20 * 1024 * 1024) throw new Error('Image exceeds 20 MB');
      setProgress(10, 'Uploading image...');
      const fd = new FormData();
      fd.append('file', file);
      fd.append('slug', file.name);
      const r = await fetch('/api/media/upload-image', {method: 'POST', body: fd});
      const data = await r.json();
      if (!r.ok || !data.ok) throw new Error(data.error || 'upload failed');
      mediaState = {
        gcs_path: data.gcs_path,
        mime: data.mime,
        size: data.size,
        media_type: 'image',
        duration_sec: null,
        aspect_ratio: null,
      };
      const reader = new FileReader();
      reader.onload = () => showPreview(`<img src="${reader.result}" style="max-width:320px;max-height:240px;border-radius:6px;" />`);
      reader.readAsDataURL(file);
    }

    async function uploadVideo(file) {
      if (file.size > 200 * 1024 * 1024) throw new Error('Video exceeds 200 MB');
      setProgress(0, 'Requesting upload URL...');
      const signResp = await fetch('/api/media/sign-upload-url', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filename: file.name, content_type: file.type, size: file.size}),
      });
      const signData = await signResp.json();
      if (!signResp.ok || !signData.ok) throw new Error(signData.error || 'signing failed');

      // Read browser-side metadata before upload (HTML5 video element exposes
      // duration + dimensions once metadata loads)
      const clientMeta = await readVideoMetadata(file);

      // Upload directly to GCS via XHR for progress events
      await new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('PUT', signData.upload_url);
        xhr.setRequestHeader('Content-Type', file.type);
        xhr.upload.addEventListener('progress', (ev) => {
          if (ev.lengthComputable) {
            const pct = Math.round((ev.loaded / ev.total) * 90);  // reserve last 10% for finalize
            setProgress(pct, `Uploading… ${Math.round(ev.loaded / 1024 / 1024)} / ${Math.round(file.size / 1024 / 1024)} MB`);
          }
        });
        xhr.onload = () => xhr.status >= 200 && xhr.status < 300 ? resolve() : reject(new Error('GCS upload failed status ' + xhr.status));
        xhr.onerror = () => reject(new Error('Network error during upload'));
        xhr.send(file);
      });

      setProgress(95, 'Reading metadata...');
      const finResp = await fetch('/api/media/finalize', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({gcs_path: signData.gcs_path, client_meta: clientMeta}),
      });
      const finData = await finResp.json();
      if (!finResp.ok || !finData.ok) throw new Error(finData.error || 'finalize failed');

      mediaState = {
        gcs_path: finData.gcs_path,
        mime: finData.mime,
        size: finData.size,
        media_type: 'video',
        duration_sec: finData.duration_sec,
        aspect_ratio: finData.aspect_ratio,
      };

      const objectUrl = URL.createObjectURL(file);
      showPreview(
        `<video src="${objectUrl}" controls muted style="max-width:320px;max-height:240px;border-radius:6px;background:#000;"></video>` +
        `<div class="etkm-text-faded" style="font-size:12px;margin-top:6px;">` +
          `${finData.duration_sec || '?'} sec · ${finData.aspect_ratio || '?'} · ${Math.round((finData.size || 0) / 1024 / 1024)} MB` +
        `</div>`
      );
    }

    function readVideoMetadata(file) {
      return new Promise((resolve) => {
        const v = document.createElement('video');
        v.preload = 'metadata';
        v.onloadedmetadata = () => {
          resolve({
            duration_sec: Math.round(v.duration),
            width: v.videoWidth,
            height: v.videoHeight,
          });
          URL.revokeObjectURL(v.src);
        };
        v.onerror = () => resolve({});
        v.src = URL.createObjectURL(file);
      });
    }

    // Re-check warning whenever platform selection changes
    platformBoxes.forEach(b => b.addEventListener('change', checkAspectWarning));

    // ── Form submit ────────────────────────────────────────────────────────
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
        media: {
          media_type: mediaState.media_type,
          gcs_path: mediaState.gcs_path,
          mime: mediaState.mime,
          size: mediaState.size,
          duration_sec: mediaState.duration_sec,
          aspect_ratio: mediaState.aspect_ratio,
        },
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
          } else if (action === 'publish') {
            if (!confirm('Publish this post immediately? It will be queued for the next 60-second worker cycle.')) return;
            r = await fetch(`/api/posts/${id}/publish`, {method: 'POST'});
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
