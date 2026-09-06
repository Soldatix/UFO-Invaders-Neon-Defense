from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="ufo-standard-info"' in s:
    print('Info already upgraded')
    raise SystemExit(0)

css = r'''

    /* Apps & Games standard Info / Donations */
    #modal-info .modal-box { max-width: 760px !important; }
    .ufo-info-charity { padding:14px 16px; background:rgba(16,185,129,.08); border:1px solid rgba(16,185,129,.24); border-radius:13px; }
    .ufo-info-kicker { color:#34d399; font-size:11px; font-weight:900; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:8px; }
    .ufo-info-charity p + p { margin-top:8px; }
    .ufo-info-section-title { color:#9ca3af; font-size:11px; font-weight:900; letter-spacing:1.1px; text-transform:uppercase; }
    .ufo-payment-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }
    .ufo-payment-card { min-width:0; padding:15px; border-radius:14px; border:1px solid #263553; background:linear-gradient(150deg,#0d1730,#070c1c); display:flex; flex-direction:column; gap:10px; }
    .ufo-payment-brand { display:flex; align-items:center; gap:9px; }
    .ufo-payment-symbol { width:38px; height:38px; display:grid; place-items:center; border-radius:11px; border:1px solid rgba(60,245,255,.32); background:rgba(60,245,255,.09); color:#3cf5ff; font-weight:900; font-size:16px; }
    .ufo-payment-brand strong { color:#f8fafc; font-size:15px; }
    .ufo-payment-desc { color:#cbd5e1; font-size:12px; line-height:1.55; flex:1; }
    .ufo-payment-badges { display:flex; flex-wrap:wrap; gap:6px; }
    .ufo-payment-badge { padding:4px 8px; border:1px solid #2c3b59; border-radius:999px; background:#101a32; color:#cbd5e1; font-size:10px; font-weight:800; }
    .ufo-payment-action { min-height:43px; display:flex; align-items:center; justify-content:center; text-decoration:none; border-radius:11px; font-weight:900; color:#031018; text-align:center; padding:9px 12px; background:linear-gradient(90deg,#4dd7e7,#51a8ff); }
    .ufo-payment-card.stripe .ufo-payment-action { background:linear-gradient(90deg,#ffe45c,#ffb84d); }
    .ufo-payment-note { color:#94a3b8; font-size:11px; }
    .ufo-crypto-list { display:flex; flex-direction:column; gap:8px; }
    .ufo-crypto-row { display:grid; grid-template-columns:72px minmax(0,1fr) auto; align-items:center; gap:10px; padding:11px 12px; border-radius:12px; border:1px solid #23324e; background:#050a18; }
    .ufo-crypto-code { color:#3cf5ff; font-weight:900; font-family:monospace; }
    .ufo-crypto-address { min-width:0; color:#dbeafe; font-size:11px; line-height:1.45; font-family:ui-monospace,SFMono-Regular,Consolas,monospace; overflow-wrap:anywhere; user-select:text; -webkit-user-select:text; }
    .ufo-copy-btn { min-width:76px; padding:7px 9px; border-radius:9px; border:1px solid #334565; background:#111b35; color:#dbeafe; font-size:11px; font-weight:800; cursor:pointer; }
    .ufo-copy-btn.copied { border-color:rgba(52,211,153,.55); background:rgba(16,185,129,.14); color:#6ee7b7; }
    @media (max-width:640px) { .ufo-payment-grid{grid-template-columns:1fr}.ufo-crypto-row{grid-template-columns:58px minmax(0,1fr)}.ufo-copy-btn{grid-column:2;justify-self:end}#modal-info .modal-body{padding:15px} }
'''

pos = s.rfind('</style>')
if pos < 0:
    raise SystemExit('No style block found')
s = s[:pos] + css + '\n  ' + s[pos:]

wallets = [
    ('BTC','bc1qwlrxrh64peukga0fp59m9yg7gpf0yj8q7fxnsc'),
    ('ETH','0xA99A52085c6725854daa46bb302041569c8bA4E3'),
    ('XRP','rP43SsrkhPkxTsFohMAm32sAQg7vqwmDpr'),
    ('SOL','8xkdVTEaDGuWu4aE3HpEx8r9Aux98JZbdsMiDQvJWBWR'),
    ('DOGE','DGAT32ku8WmFaTDxCgVuRuVpUFmfdmD5Jb'),
    ('XLM','GCYH4OD4I2GNRKFFOYROE3N3S2HCT5RXIML3TZV5DP3TLTLXPXQXIJZ3'),
    ('LTC','LWtaFniqdYpv2xJtqo9WqDwCsQ2cW6PYWi'),
    ('RVN','RAtXzKZyB3awfq2u2cK8YppC9kJamU5tPQ'),
]
wallet_html = '\n'.join(
    f'            <div class="ufo-crypto-row"><div class="ufo-crypto-code">{coin}</div><div class="ufo-crypto-address">{addr}</div><button class="ufo-copy-btn" data-address="{addr}" onclick="copyInfoWallet(this)">Copy</button></div>'
    for coin, addr in wallets
)

modal = f'''    <!-- Info / Donations Modal -->
    <div id="modal-info" class="screen-overlay hidden">
      <div id="ufo-standard-info" class="modal-box">
        <div class="modal-header">
          <span class="modal-title" id="info-title">Information / Donations</span>
          <button id="info-close" class="icon-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="ufo-info-charity">
            <div class="ufo-info-kicker" id="info-charity-title">Charity purpose</div>
            <p id="info-free"><strong>The game is free to use, but voluntary donations are welcome.</strong></p>
            <p id="info-charity-text">A part of the received donations will be forwarded to various charitable organizations. The largest part will be donated to institutions caring for children without adequate parental care.</p>
          </div>
          <div class="ufo-info-section-title" id="info-direct-title">Direct online payments</div>
          <div class="ufo-payment-grid">
            <div class="ufo-payment-card">
              <div class="ufo-payment-brand"><span class="ufo-payment-symbol">P</span><strong>PayPal</strong></div>
              <div class="ufo-payment-desc" id="info-paypal-desc">Pay securely with PayPal or other payment options offered by PayPal Checkout.</div>
              <div class="ufo-payment-badges"><span class="ufo-payment-badge">PayPal</span><span class="ufo-payment-badge info-cards">Debit / Credit Card</span><span class="ufo-payment-badge">Apple Pay</span></div>
              <a class="ufo-payment-action" id="info-paypal-button" href="https://www.paypal.com/ncp/payment/RU2CWCNVQ7XD6" target="_blank" rel="noopener noreferrer">Donate with PayPal ↗</a>
            </div>
            <div class="ufo-payment-card stripe">
              <div class="ufo-payment-brand"><span class="ufo-payment-symbol">S</span><strong>Stripe</strong></div>
              <div class="ufo-payment-desc" id="info-stripe-desc">Pay securely by card or with payment methods available through Stripe Checkout.</div>
              <div class="ufo-payment-badges"><span class="ufo-payment-badge info-cards">Debit / Credit Card</span><span class="ufo-payment-badge">Link</span><span class="ufo-payment-badge" id="info-wallets-badge">Digital wallets</span></div>
              <a class="ufo-payment-action" id="info-stripe-button" href="https://buy.stripe.com/7sYeVd7Blfe89cm0k02kw00" target="_blank" rel="noopener noreferrer">Donate with Stripe ↗</a>
            </div>
          </div>
          <div class="ufo-payment-note" id="info-payment-note">Available payment methods can vary by country, device and payment provider.</div>
          <div class="ufo-info-section-title" id="info-crypto-title">Crypto Wallets</div>
          <div class="ufo-crypto-list">
{wallet_html}
          </div>
        </div>
        <div class="modal-footer"><button id="info-footer-close" class="icon-btn">Close</button></div>
      </div>
    </div>

    <!-- Read Me Modal -->'''

pattern = re.compile(r'    <!-- Info / Donations Modal -->.*?    <!-- Read Me Modal -->', re.S)
s, n = pattern.subn(modal, s, count=1)
if n != 1:
    raise SystemExit(f'Info modal replacement count: {n}')

js = r'''

    const INFO_TRANSLATIONS = {
      en:{menu:'ℹ Info / Donations',title:'Information / Donations',charity:'Charity purpose',free:'The game is free to use, but voluntary donations are welcome.',charityText:'A part of the received donations will be forwarded to various charitable organizations. The largest part will be donated to institutions caring for children without adequate parental care.',direct:'Direct online payments',paypalDesc:'Pay securely with PayPal or other payment options offered by PayPal Checkout.',stripeDesc:'Pay securely by card or with payment methods available through Stripe Checkout.',cards:'Debit / Credit Card',wallets:'Digital wallets',paypalButton:'Donate with PayPal ↗',stripeButton:'Donate with Stripe ↗',note:'Available payment methods can vary by country, device and payment provider.',crypto:'Crypto Wallets',copy:'Copy',copied:'Copied!',close:'Close'},
      hr:{menu:'ℹ Info / Donacije',title:'Informacije / Donacije',charity:'Humanitarna svrha',free:'Igra je besplatna za korištenje, ali dobrovoljne donacije su dobrodošle.',charityText:'Dio primljenih donacija proslijedit će se različitim humanitarnim organizacijama. Najveći dio bit će doniran ustanovama koje skrbe o djeci bez odgovarajuće roditeljske skrbi.',direct:'Izravna online plaćanja',paypalDesc:'Platite sigurno putem PayPala ili drugim načinima plaćanja koje nudi PayPal Checkout.',stripeDesc:'Platite sigurno karticom ili načinima plaćanja dostupnima putem Stripe Checkouta.',cards:'Debitna / kreditna kartica',wallets:'Digitalni novčanici',paypalButton:'Doniraj putem PayPala ↗',stripeButton:'Doniraj putem Stripea ↗',note:'Dostupni načini plaćanja mogu se razlikovati ovisno o državi, uređaju i pružatelju plaćanja.',crypto:'Kripto novčanici',copy:'Kopiraj',copied:'Kopirano!',close:'Zatvori'},
      de:{menu:'ℹ Info / Spenden',title:'Informationen / Spenden',charity:'Wohltätiger Zweck',free:'Das Spiel kann kostenlos genutzt werden, freiwillige Spenden sind jedoch willkommen.',charityText:'Ein Teil der erhaltenen Spenden wird an verschiedene gemeinnützige Organisationen weitergeleitet. Der größte Teil wird an Einrichtungen gespendet, die Kinder ohne angemessene elterliche Fürsorge betreuen.',direct:'Direkte Online-Zahlungen',paypalDesc:'Sicher mit PayPal oder weiteren von PayPal Checkout angebotenen Zahlungsmethoden bezahlen.',stripeDesc:'Sicher per Karte oder mit den über Stripe Checkout verfügbaren Zahlungsmethoden bezahlen.',cards:'Debit- / Kreditkarte',wallets:'Digitale Wallets',paypalButton:'Mit PayPal spenden ↗',stripeButton:'Mit Stripe spenden ↗',note:'Verfügbare Zahlungsmethoden können je nach Land, Gerät und Zahlungsanbieter variieren.',crypto:'Krypto-Wallets',copy:'Kopieren',copied:'Kopiert!',close:'Schließen'},
      it:{menu:'ℹ Info / Donazioni',title:'Informazioni / Donazioni',charity:'Scopo benefico',free:'Il gioco è gratuito, ma le donazioni volontarie sono benvenute.',charityText:'Una parte delle donazioni ricevute sarà destinata a diverse organizzazioni benefiche. La parte maggiore sarà donata a istituti che si occupano di bambini privi di adeguate cure parentali.',direct:'Pagamenti online diretti',paypalDesc:'Paga in modo sicuro con PayPal o con gli altri metodi disponibili tramite PayPal Checkout.',stripeDesc:'Paga in modo sicuro con carta o con i metodi disponibili tramite Stripe Checkout.',cards:'Carta di debito / credito',wallets:'Portafogli digitali',paypalButton:'Dona con PayPal ↗',stripeButton:'Dona con Stripe ↗',note:'I metodi di pagamento disponibili possono variare in base al Paese, al dispositivo e al fornitore di pagamento.',crypto:'Portafogli crypto',copy:'Copia',copied:'Copiato!',close:'Chiudi'},
      es:{menu:'ℹ Info / Donaciones',title:'Información / Donaciones',charity:'Finalidad benéfica',free:'El juego es gratuito, pero las donaciones voluntarias son bienvenidas.',charityText:'Una parte de las donaciones recibidas se destinará a diversas organizaciones benéficas. La mayor parte se donará a instituciones que atienden a niños sin una atención parental adecuada.',direct:'Pagos directos en línea',paypalDesc:'Paga de forma segura con PayPal u otros métodos disponibles mediante PayPal Checkout.',stripeDesc:'Paga de forma segura con tarjeta o con los métodos disponibles mediante Stripe Checkout.',cards:'Tarjeta de débito / crédito',wallets:'Carteras digitales',paypalButton:'Donar con PayPal ↗',stripeButton:'Donar con Stripe ↗',note:'Los métodos de pago disponibles pueden variar según el país, el dispositivo y el proveedor de pago.',crypto:'Carteras de criptomonedas',copy:'Copiar',copied:'¡Copiado!',close:'Cerrar'}
    };

    function updateInfoLanguage(lang) {
      const i = INFO_TRANSLATIONS[lang] || INFO_TRANSLATIONS.en;
      const set = (id, value) => { const el = document.getElementById(id); if (el) el.textContent = value; };
      set('menu-info-btn', i.menu); set('info-title', i.title); set('info-charity-title', i.charity); set('info-free', i.free);
      set('info-charity-text', i.charityText); set('info-direct-title', i.direct); set('info-paypal-desc', i.paypalDesc); set('info-stripe-desc', i.stripeDesc);
      document.querySelectorAll('.info-cards').forEach(el => el.textContent = i.cards);
      set('info-wallets-badge', i.wallets); set('info-paypal-button', i.paypalButton); set('info-stripe-button', i.stripeButton);
      set('info-payment-note', i.note); set('info-crypto-title', i.crypto); set('info-footer-close', i.close);
      document.querySelectorAll('.ufo-copy-btn').forEach(btn => { if (!btn.classList.contains('copied')) btn.textContent = i.copy; });
    }

    function copyInfoWallet(button) {
      const i = INFO_TRANSLATIONS[language] || INFO_TRANSLATIONS.en;
      const address = button.dataset.address || '';
      const done = () => {
        button.classList.add('copied'); button.textContent = i.copied;
        setTimeout(() => { button.classList.remove('copied'); button.textContent = (INFO_TRANSLATIONS[language] || INFO_TRANSLATIONS.en).copy; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(address).then(done).catch(() => fallbackCopyInfoWallet(address, done));
      else fallbackCopyInfoWallet(address, done);
    }

    function fallbackCopyInfoWallet(address, done) {
      const ta = document.createElement('textarea'); ta.value = address; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); done(); } catch (_) {} ta.remove();
    }
'''

marker = '    // --- Event Listeners ---'
if marker not in s:
    raise SystemExit('Event listener marker not found')
s = s.replace(marker, js + '\n\n' + marker, 1)

needle = "      const t = TRANSLATIONS[lang] || TRANSLATIONS.en;"
if needle not in s:
    raise SystemExit('setLanguage translation line not found')
s = s.replace(needle, needle + "\n      updateInfoLanguage(lang);", 1)

p.write_text(s, encoding='utf-8')
print('UFO Info upgraded')
