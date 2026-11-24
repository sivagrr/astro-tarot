(() => {
  const deck = JSON.parse(document.getElementById('deck-data').textContent);
  const spreads = JSON.parse(document.getElementById('spreads-data').textContent);
  const cardsEl = document.getElementById('drawn-cards');
  const status = document.getElementById('reading-status');
  const drawButton = document.getElementById('draw-button');
  const resetButton = document.getElementById('reset-button');
  const combined = document.getElementById('combined-reading');
  const combinedText = document.getElementById('combined-text');
  const title = document.getElementById('stage-title');
  const description = document.getElementById('stage-description');
  const spreadOptions = document.getElementById('spread-options');
  const yesnoOptions = document.getElementById('yesno-options');
  const staticPrefix = '/static/';
  const state = {
    cards: [],
    busy: false,
    focus: 'general',
    spread: 'three',
    yesno: 'general'
  };
  const selected = name => document.querySelector(`input[name="${name}"]:checked`)?.value;
  const announce = message => {
    status.textContent = message;
  };
  const choice = max => {
    const buffer = new Uint32Array(1);
    if (window.crypto?.getRandomValues) {
      window.crypto.getRandomValues(buffer);
      return buffer[0] % max;
    }
    return Math.floor(Math.random() * max);
  };

  function sync() {
    state.focus = selected('focus') || 'general';
    state.spread = selected('spread') || 'three';
    state.yesno = selected('yesno-focus') || 'general';
    const yesno = state.focus === 'yesno';
    spreadOptions.hidden = yesno;
    yesnoOptions.hidden = !yesno;
    if (!state.cards.length) announce(yesno ? 'Yes / No uses one upright card.' : 'Choose a spread, then shuffle and draw.');
  }
  document.querySelectorAll('input[name="focus"],input[name="spread"],input[name="yesno-focus"]').forEach(el => el.addEventListener('change', () => {
    if (state.busy) return;
    if (state.cards.length) {
      state.cards = [];
      cardsEl.innerHTML = '<div class="placeholder-card" aria-hidden="true">✳</div>';
      combined.hidden = true;
      drawButton.hidden = false;
      resetButton.hidden = true;
      title.textContent = 'A little space for insight.';
      description.textContent = 'Take a breath. Bring a question to mind.';
    }
    sync();
  }));
  const querySpread = new URLSearchParams(location.search).get('spread');
  if (spreads.some(item => item.id === querySpread)) document.querySelector(`input[name="spread"][value="${querySpread}"]`).checked = true;
  sync();

  function meaning(item) {
    return item.orientation === 'Reversed' ? item.card.reversed_meaning : item.card.upright_meaning;
  }

  function focusNote(item) {
    return state.focus === 'love' ? item.card.love_note : state.focus === 'career' ? item.card.career_note : '';
  }

  function answer(item) {
    const raw = (state.yesno === 'love' ? item.card.yes_no_love : state.yesno === 'spiritual' ? item.card.yes_no_spiritual : '') || item.card.yes_no_upright;
    const labels = {
      yes: 'Leaning yes',
      no: 'Leaning no',
      maybe: 'Unclear / maybe',
      delayed: 'Delayed',
      maybe_delayed: 'Maybe / delayed',
      'maybe/delayed': 'Maybe / delayed'
    };
    return labels[String(raw).toLowerCase().trim().replace(/\s+/g, '_')] || 'Unclear / maybe';
  }

  function perspective(item) {
    return item.card.group === 'Major Arcana' ? 'a broader theme' : 'an everyday concern';
  }

  function combinedReading() {
    if (!state.cards.length || state.cards.some(item => !item.revealed)) {
      combined.hidden = true;
      return;
    }
    const rows = state.cards;
    if (state.focus === 'yesno') {
      combined.querySelector('h3').textContent = 'Your one-card answer';
      combinedText.textContent = `${answer(rows[0])}. ${rows[0].card.name} invites a closer look at ${rows[0].card.daily_keywords.toLowerCase()}. Treat this as a prompt to consider your choices, timing, and what you can learn, rather than a certain outcome.`;
    } else if (rows.length === 1) {
      combined.querySelector('h3').textContent = 'Your spread, together';
      combinedText.textContent = `${rows[0].card.name} brings ${perspective(rows[0])} into your present focus. ${meaning(rows[0])} What small step feels useful now?`;
    } else {
      combined.querySelector('h3').textContent = 'Your spread, together';
      const situation = rows[0],
        challenge = rows.length === 3 ? rows[1] : rows[2],
        next = rows.at(-1);
      let text = `Your opening situation, ${situation.card.name} (${situation.orientation.toLowerCase()}), points toward ${situation.card.daily_keywords.toLowerCase()} as ${perspective(situation)}. ${meaning(situation)} The challenge, ${challenge.card.name} (${challenge.orientation.toLowerCase()}), asks you to notice ${challenge.card.daily_keywords.toLowerCase()} without treating it as a fixed obstacle. ${meaning(challenge)} `;
      if (rows.length === 5) text += `The underlying influence, ${rows[1].card.name} (${rows[1].orientation.toLowerCase()}), may add context: ${meaning(rows[1])} ${rows[3].card.name} (${rows[3].orientation.toLowerCase()}) in Support suggests a resource you can draw on: ${meaning(rows[3])} `;
      text += `${next.card.name} (${next.orientation.toLowerCase()}) in Next step invites one grounded action. ${meaning(next)} Reversed cards invite another angle, not an automatically negative result.`;
      combinedText.textContent = text;
    }
    combined.hidden = false;
    announce('All cards revealed. Your combined interpretation is available.');
  }

  function render() {
    cardsEl.replaceChildren();
    const positions = state.focus === 'yesno' ? ['Your one-card answer'] : spreads.find(s => s.id === state.spread).positions;
    state.cards.forEach((item, index) => {
      const article = document.createElement('article');
      article.className = 'drawn-card';
      const position = document.createElement('span');
      position.className = 'position';
      position.textContent = positions[index];
      article.append(position);
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'flip-card' + (item.revealed ? ' is-revealed' : '');
      button.disabled = item.revealed;
      button.setAttribute('aria-label', item.revealed ? `${item.card.name}, ${item.orientation}` : `Reveal ${positions[index]} card`);
      const inner = document.createElement('span');
      inner.className = 'flip-inner';
      const back = document.createElement('span');
      back.className = 'flip-back';
      back.setAttribute('aria-hidden', 'true');
      back.textContent = '✳';
      const face = document.createElement('span');
      face.className = 'flip-face';
      face.setAttribute('aria-hidden', 'true');
      const image = document.createElement('img');
      image.src = staticPrefix + item.card.image;
      image.alt = '';
      image.loading = 'lazy';
      face.append(image);
      inner.append(back, face);
      button.append(inner);
      button.addEventListener('click', () => {
        if (item.revealed || state.busy) return;
        item.revealed = true;
        button.classList.add('is-revealed');
        button.disabled = true;
        const detail = document.createElement('div');
        detail.className = 'drawn-meaning';
        const heading = document.createElement('h3');
        heading.textContent = `${item.card.name} · ${item.orientation}`;
        const para = document.createElement('p');
        para.textContent = meaning(item);
        detail.append(heading, para);
        const note = focusNote(item);
        if (note) {
          const extra = document.createElement('p');
          extra.textContent = note;
          detail.append(extra);
        }
        article.append(detail);
        announce(`${positions[index]}: ${item.card.name}, ${item.orientation}.`);
        combinedReading();
      });
      article.append(button);
      cardsEl.append(article);
    });
    combinedReading();
  }

  function draw() {
    if (state.busy) return;
    sync();
    state.busy = true;
    drawButton.disabled = true;
    resetButton.disabled = true;
    document.querySelectorAll('.tarot-draw-page input[type="radio"]').forEach(el => el.disabled = true);
    combined.hidden = true;
    const count = state.focus === 'yesno' ? 1 : spreads.find(s => s.id === state.spread).positions.length;
    const pool = [...deck];
    state.cards = [];
    for (let i = 0; i < count; i++) {
      const card = pool.splice(choice(pool.length), 1)[0];
      state.cards.push({
        card,
        orientation: state.focus === 'yesno' ? 'Upright' : (choice(2) ? 'Upright' : 'Reversed'),
        revealed: false
      });
    }
    title.textContent = 'Your cards are ready.';
    description.textContent = 'Turn each card over when you feel ready.';
    render();
    announce(`Drawing ${count} ${count === 1 ? 'card' : 'cards'}. Cards are face down.`);
    const delay = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 400;
    window.setTimeout(() => {
      state.busy = false;
      drawButton.disabled = false;
      resetButton.disabled = false;
      document.querySelectorAll('.tarot-draw-page input[type="radio"]').forEach(el => el.disabled = false);
      drawButton.hidden = true;
      resetButton.hidden = false;
      cardsEl.querySelector('button')?.focus();
      announce(`${count} ${count === 1 ? 'card is' : 'cards are'} ready to reveal.`);
    }, delay);
  }
  drawButton.addEventListener('click', draw);
  resetButton.addEventListener('click', () => {
    if (state.busy) return;
    draw();
  });
})();