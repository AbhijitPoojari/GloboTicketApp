const $ = sel => document.querySelector(sel);
const cityInput = $('#cityInput');
const searchBtn = $('#searchBtn');
const statusEl = $('#status');
const resultsEl = $('#results');

function setStatus(text, isError = false) {
  statusEl.textContent = text;
  statusEl.className = isError ? 'status error' : 'status';
}

function renderEvents(events) {
  resultsEl.innerHTML = '';
  if (!events || events.length === 0) {
    resultsEl.innerHTML = '<p>No events found.</p>';
    return;
  }

  const frag = document.createDocumentFragment();
  events.forEach(ev => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <img src="${ev.image || ''}" alt="" />
      <div class="card-body">
        <h3><a href="${ev.url}" target="_blank" rel="noopener noreferrer">${ev.name}</a></h3>
        <p class="meta">${ev.date || ''} — ${ev.venue || ''}</p>
      </div>
    `;
    frag.appendChild(card);
  });
  resultsEl.appendChild(frag);
}

const BACKEND_BASE = window.BACKEND_BASE || '';

async function searchCity() {
  const city = cityInput.value.trim();
  if (!city) {
    setStatus('Please enter a city', true);
    return;
  }
  setStatus('Loading...');
  resultsEl.innerHTML = '';

  try {
    const url = `${BACKEND_BASE}/events?city=${encodeURIComponent(city)}`;
    const res = await fetch(url);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      setStatus(err.error || 'Server error', true);
      return;
    }
    const data = await res.json();
    setStatus(`Found ${data.count} events`);
    renderEvents(data.events);
  } catch (e) {
    setStatus('Network error', true);
  }
}

searchBtn.addEventListener('click', searchCity);
cityInput.addEventListener('keydown', e => { if (e.key === 'Enter') searchCity(); });
