const source = document.querySelector('#source');
const target = document.querySelector('#target');
const text = document.querySelector('#sourceText');
const result = document.querySelector('#result');
const status = document.querySelector('#status');
const provider = document.querySelector('#provider');
const counter = document.querySelector('#counter');
const translateBtn = document.querySelector('#translate');

text.addEventListener('input', () => counter.textContent = `${text.value.length.toLocaleString()} / 5,000`);

document.querySelector('#clear').onclick = () => { text.value=''; result.textContent='Your translated text will appear here.'; result.classList.add('empty'); provider.textContent='Ready'; counter.textContent='0 / 5,000'; };

document.querySelector('#swap').onclick = () => {
  if (source.value === 'auto') return;
  const old = source.value; source.value = target.value; target.value = old;
  const oldText = text.value; text.value = result.classList.contains('empty') ? '' : result.textContent; result.textContent = oldText || 'Your translated text will appear here.'; result.classList.toggle('empty', !oldText);
};

document.querySelector('#copy').onclick = async () => {
  if (result.classList.contains('empty')) return;
  await navigator.clipboard.writeText(result.textContent);
  status.textContent='Translation copied to clipboard.'; status.classList.remove('hidden'); setTimeout(()=>status.classList.add('hidden'),1800);
};

document.querySelector('#speak').onclick = () => {
  if (result.classList.contains('empty')) return;
  const u = new SpeechSynthesisUtterance(result.textContent);
  u.lang = target.value;
  window.speechSynthesis.cancel(); window.speechSynthesis.speak(u);
};

translateBtn.onclick = async () => {
  if (!text.value.trim()) { status.textContent='Please enter some text first.'; status.classList.remove('hidden'); return; }
  status.classList.add('hidden'); translateBtn.classList.add('loading'); translateBtn.textContent='Translating…'; provider.textContent='Working';
  try {
    const response = await fetch('/api/translate', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:text.value,source:source.value,target:target.value})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Translation failed');
    result.textContent=data.translated_text; result.classList.remove('empty'); provider.textContent=data.provider;
  } catch (e) { status.textContent=e.message; status.classList.remove('hidden'); provider.textContent='Error'; }
  finally { translateBtn.classList.remove('loading'); translateBtn.innerHTML='Translate&nbsp; →'; }
};
