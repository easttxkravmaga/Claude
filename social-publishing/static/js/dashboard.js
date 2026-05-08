/* ETKM Social Publishing — Dashboard JS
 * Polls scheduler status, handles credential refresh + delete actions.
 */

(function () {
  const pill = document.getElementById('scheduler-pill');

  async function pollStatus() {
    try {
      const r = await fetch('/api/scheduler/status');
      if (!r.ok) return;
      const data = await r.json();
      if (data.busy) {
        pill.className = 'etkm-pill etkm-pill--orange';
        pill.textContent = 'Scheduler busy';
      } else {
        pill.className = 'etkm-pill etkm-pill--neutral';
        pill.textContent = 'Scheduler idle';
      }
    } catch (e) { /* network blip; try again next tick */ }
  }
  if (pill) {
    pollStatus();
    setInterval(pollStatus, 30000);
  }

  document.querySelectorAll('.etkm-cred[data-cred-id]').forEach(card => {
    const id = card.dataset.credId;
    card.querySelectorAll('button[data-action]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const action = btn.dataset.action;
        const orig = btn.textContent;
        try {
          let r;
          if (action === 'refresh') {
            btn.disabled = true;
            btn.textContent = '... refreshing';
            r = await fetch(`/api/credentials/${id}/refresh`, {method: 'POST'});
          } else if (action === 'delete') {
            if (!confirm('Delete this credential? You will need to re-authorize.')) return;
            r = await fetch(`/api/credentials/${id}`, {method: 'DELETE'});
          }
          const data = await r.json();
          if (!r.ok || !data.ok) throw new Error(data.error || 'Action failed');
          window.location.reload();
        } catch (e) {
          alert(`Failed: ${e.message}`);
          btn.disabled = false;
          btn.textContent = orig;
        }
      });
    });
  });

  const refreshAll = document.getElementById('refresh-all');
  if (refreshAll) {
    refreshAll.addEventListener('click', async () => {
      refreshAll.disabled = true;
      refreshAll.textContent = '... refreshing';
      try {
        const r = await fetch('/api/credentials');
        const data = await r.json();
        if (!data.ok) throw new Error('list failed');
        const sevenDays = 7 * 24 * 60 * 60 * 1000;
        const now = Date.now();
        const expiring = data.credentials.filter(c => {
          if (!c.expires_at) return false;
          return new Date(c.expires_at).getTime() < now + sevenDays;
        });
        if (expiring.length === 0) {
          alert('No credentials expiring within 7 days.');
          refreshAll.disabled = false;
          refreshAll.textContent = 'Refresh All Expiring';
          return;
        }
        for (const c of expiring) {
          await fetch(`/api/credentials/${c.id}/refresh`, {method: 'POST'});
        }
        window.location.reload();
      } catch (e) {
        alert(`Failed: ${e.message}`);
        refreshAll.disabled = false;
        refreshAll.textContent = 'Refresh All Expiring';
      }
    });
  }
})();
