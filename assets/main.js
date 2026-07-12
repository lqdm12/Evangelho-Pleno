/* ==========================================================================
   IGREJA EVANGELHO PLENO — Script principal
   ========================================================================== */

/* --------------------------------------------------------------------------
   FONTE ÚNICA DA VERDADE
   Mexer nos horários e endereços aqui atualiza o site inteiro.
   dia: 0=domingo, 1=segunda ... 6=sábado
   -------------------------------------------------------------------------- */
const CONGREGACOES = [
  {
    id: 'santa-teresa',
    nome: 'Santa Teresa',
    sede: true,
    endereco: 'Av. Luís Müller, 144 — Centro',
    cidade: 'Santa Teresa, ES',
    mapa: 'https://www.google.com/maps/search/?api=1&query=Av.+Luis+Muller,+144,+Centro,+Santa+Teresa+-+ES',
    whatsapp: '5527000000000',
    cultos: [
      { dia: 0, hora: 19, minuto: 0,  nome: 'Culto de Celebração' },
      { dia: 2, hora: 19, minuto: 30, nome: 'Culto de Ensino' }
    ]
  },
  {
    id: 'sao-roque',
    nome: 'São Roque do Canaã',
    sede: false,
    endereco: 'Av. Antônio Gil Veloso, 420',
    cidade: 'São Roque do Canaã, ES',
    mapa: 'https://www.google.com/maps/search/?api=1&query=Av.+Antonio+Gil+Veloso,+420,+Sao+Roque+do+Canaa+-+ES',
    whatsapp: '5527000000000',
    cultos: [
      { dia: 0, hora: 19, minuto: 30, nome: 'Culto de Celebração' },
      { dia: 4, hora: 19, minuto: 30, nome: 'Culto de Ensino' }
    ]
  },
  {
    id: 'varzea-alegre',
    nome: 'Várzea Alegre',
    sede: false,
    endereco: 'Centro — anexo ao posto de combustível',
    cidade: 'Várzea Alegre, ES',
    mapa: 'https://www.google.com/maps/search/?api=1&query=Varzea+Alegre+Centro+ES',
    whatsapp: '5527000000000',
    cultos: [
      { dia: 0, hora: 19, minuto: 30, nome: 'Culto de Celebração' },
      { dia: 3, hora: 19, minuto: 30, nome: 'Culto de Ensino' }
    ]
  }
];

const DIAS = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];

/* --------------------------------------------------------------------------
   Próximo culto de uma congregação
   -------------------------------------------------------------------------- */
function proximoCulto(congregacao, agora = new Date()) {
  let melhor = null;

  congregacao.cultos.forEach(culto => {
    const data = new Date(agora);
    const diferencaDias = (culto.dia - agora.getDay() + 7) % 7;

    data.setDate(agora.getDate() + diferencaDias);
    data.setHours(culto.hora, culto.minuto, 0, 0);

    // Se já passou hoje, joga para a semana que vem
    if (data <= agora) data.setDate(data.getDate() + 7);

    if (!melhor || data < melhor.data) melhor = { ...culto, data };
  });

  return melhor;
}

function formatarContagem(alvo, agora = new Date()) {
  const ms = alvo - agora;
  if (ms <= 0) return 'Acontecendo agora';

  const minutosTotais = Math.floor(ms / 60000);
  const dias  = Math.floor(minutosTotais / 1440);
  const horas = Math.floor((minutosTotais % 1440) / 60);
  const min   = minutosTotais % 60;

  if (dias > 0)  return `Faltam ${dias}d ${horas}h`;
  if (horas > 0) return `Faltam ${horas}h ${min}min`;
  return `Faltam ${min}min`;
}

const doisDigitos = n => String(n).padStart(2, '0');

/* --------------------------------------------------------------------------
   Seletor de congregação
   Estado em memória. Ao hospedar, dá para persistir com localStorage.
   -------------------------------------------------------------------------- */
let congregacaoAtiva = CONGREGACOES[0].id;

function montarSeletor() {
  const raiz = document.querySelector('[data-seletor]');
  if (!raiz) return;

  const abas       = raiz.querySelector('[data-abas]');
  const nomeCulto  = raiz.querySelector('[data-culto-nome]');
  const quandoTxt  = raiz.querySelector('[data-culto-quando]');
  const contagem   = raiz.querySelector('[data-contagem]');
  const endereco   = raiz.querySelector('[data-endereco]');
  const linkMapa   = raiz.querySelector('[data-mapa]');

  CONGREGACOES.forEach(cong => {
    const botao = document.createElement('button');
    botao.className = 'aba';
    botao.type = 'button';
    botao.role = 'tab';
    botao.textContent = cong.nome;
    botao.setAttribute('aria-selected', cong.id === congregacaoAtiva);
    botao.addEventListener('click', () => {
      congregacaoAtiva = cong.id;
      abas.querySelectorAll('.aba').forEach(b => b.setAttribute('aria-selected', 'false'));
      botao.setAttribute('aria-selected', 'true');
      atualizar();
    });
    abas.appendChild(botao);
  });

  function atualizar() {
    const cong  = CONGREGACOES.find(c => c.id === congregacaoAtiva);
    const culto = proximoCulto(cong);

    nomeCulto.textContent = culto.nome;
    quandoTxt.textContent = `${DIAS[culto.dia]}, ${culto.hora}h${culto.minuto ? doisDigitos(culto.minuto) : ''}`;
    contagem.textContent  = formatarContagem(culto.data);
    endereco.textContent  = `${cong.endereco} — ${cong.cidade}`;
    linkMapa.href         = cong.mapa;
  }

  atualizar();
  setInterval(atualizar, 30000);
}

/* --------------------------------------------------------------------------
   Tabela de horários (página Agenda / Contato)
   -------------------------------------------------------------------------- */
function montarHorarios() {
  const raiz = document.querySelector('[data-horarios]');
  if (!raiz) return;

  CONGREGACOES.forEach(cong => {
    const linha = document.createElement('div');
    linha.className = 'horario';

    const cultos = cong.cultos
      .slice()
      .sort((a, b) => a.dia - b.dia)
      .map(c => `<strong>${DIAS[c.dia]}</strong> ${c.hora}h${c.minuto ? doisDigitos(c.minuto) : ''} · ${c.nome}`)
      .join('<br>');

    linha.innerHTML = `
      <div class="horario__local">${cong.nome}${cong.sede ? ' <span style="font-family:var(--util);font-size:.6rem;letter-spacing:.14em;color:var(--brasa);vertical-align:middle;">SEDE</span>' : ''}</div>
      <div class="horario__dia">${cultos}</div>
      <div class="horario__endereco">${cong.endereco}<br>${cong.cidade}</div>
      <a class="btn btn--contorno" href="${cong.mapa}" target="_blank" rel="noopener">Como chegar</a>
    `;
    raiz.appendChild(linha);
  });
}

/* --------------------------------------------------------------------------
   Cabeçalho, menu, revelação e modo placeholder
   -------------------------------------------------------------------------- */
function ligarCabecalho() {
  const cabecalho = document.querySelector('.cabecalho');
  const botao     = document.querySelector('.hamburguer');
  const nav       = document.querySelector('.nav');
  if (!cabecalho) return;

  const aoRolar = () => {
    cabecalho.classList.toggle('cabecalho--fixo', window.scrollY > 40);
  };
  aoRolar();
  window.addEventListener('scroll', aoRolar, { passive: true });

  if (botao && nav) {
    botao.addEventListener('click', () => {
      const aberto = botao.getAttribute('aria-expanded') === 'true';
      botao.setAttribute('aria-expanded', String(!aberto));
      nav.dataset.aberto = String(!aberto);
      document.body.style.overflow = !aberto ? 'hidden' : '';
    });
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        botao.setAttribute('aria-expanded', 'false');
        nav.dataset.aberto = 'false';
        document.body.style.overflow = '';
      });
    });
  }
}

function ligarRevelacao() {
  const alvos = document.querySelectorAll('[data-revelar]');
  if (!alvos.length) return;

  const observador = new IntersectionObserver(entradas => {
    entradas.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visivel');
        observador.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

  alvos.forEach(alvo => observador.observe(alvo));
}

function ligarModoPlaceholder() {
  const botao = document.querySelector('.barra-ph');
  if (!botao) return;

  botao.addEventListener('click', () => {
    const ativo = document.body.dataset.modoPh === 'true';
    document.body.dataset.modoPh = String(!ativo);
    botao.querySelector('[data-ph-texto]').textContent =
      !ativo ? 'Placeholders visíveis' : 'Ver placeholders';
  });
}

document.addEventListener('DOMContentLoaded', () => {
  ligarCabecalho();
  montarSeletor();
  montarHorarios();
  ligarRevelacao();
  ligarModoPlaceholder();
});
