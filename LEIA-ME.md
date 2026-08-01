# Igreja Evangelho Pleno — site

Site estático das três congregações no Espírito Santo (Santa Teresa, São Roque
do Canaã e Várzea Alegre). Sem framework, sem build pesado: **Python + HTML,
CSS e JS puros**.

---

## Como rodar

```bash
# 1. Gerar as páginas a partir dos templates
python3 build.py

# 2. Servir localmente
python3 -m http.server 8000
# abre http://localhost:8000
```

Hospedagem: qualquer serviço estático (Netlify, Vercel, GitHub Pages, Cloudflare
Pages). Basta subir a pasta — as páginas já saem prontas na raiz.

---

## Arquitetura

```
build.py               Constrói as 9 páginas + robots.txt + sitemap.xml
src/
  base.html            Esqueleto: <head>, header, footer, skip-link
  partials/
    cabecalho.html     Header compartilhado (logo + menu)
    rodape.html        Footer compartilhado
  paginas/             Conteúdo de cada página (só a parte do <main>)
    index.html         Home
    primeira-visita.html  A página mais importante do site
    quem-somos.html       História, doutrina, liderança
    unidade.html          Campanha 2K26
    ministerios.html      Grupos e como participar
    agenda.html           Horários e eventos
    contato.html          Formulário e pedido de oração
    contribua.html        Dízimos e ofertas
    404.html              Página não encontrada
assets/css/styles.css  Folha única, comentada por seção
assets/js/main.js      Seletor de congregação, contagem, menu, formulário
assets/img/logo/       Logos otimizados + favicon.svg
assets/img/fotos/      Fotos da igreja, otimizadas para web
```

**Regra de ouro:** menu, rodapé, contatos e textos do rodapé vivem no `build.py`
e em `src/partials/`. Nunca edite o HTML da raiz à mão — mude a fonte e rode
`python3 build.py` de novo.

### Configuração central (`build.py`)

| Constante | O que controla |
|---|---|
| `SITE_URL` | URL pública (sitemap, robots, compartilhamento) |
| `NAV` / `CTA` | Menu principal e botão Contribua |
| `PAGINAS` | Títulos e descrições de cada página |
| `CONTATO` | WhatsApp, Instagram e e-mail do PIX |
| `FORMS` | Chave do formulário (Web3Forms) |

O build **valida** todos os links internos e aborta se achar um quebrado.

---

## Conteúdo que ainda falta (antes de ir ao ar)

Textos que ainda precisam de resposta real, marcados como `[A DEFINIR]`:

1. **Nome dos cultos de semana.** Hoje "Culto de Ensino" é palpite.
2. **Santa Teresa é a sede?** Confirmar (hoje marcada como sede).
3. **Endereço completo de Várzea Alegre.** "Centro, anexo ao posto" não gera
   pin no Google Maps.
4. **Instagram** da igreja (`CONTATO` no `build.py`).
5. **Chave PIX / dados bancários** completos na página Contribua.
6. **Domínio.** Hoje `SITE_URL` usa `evangelhopleno.com.br` como sugestão.
7. **Onde estacionar em cada congregação** (primeira visita).
8. **Fotos das outras duas congregações** — as atuais parecem ser da mesma casa.

---

## O seletor de congregação

É a peça central da home: a pessoa escolhe onde mora e o site responde com o
**próximo culto, que dia, que horas, quanto falta e como chegar**. A contagem é
ao vivo e atualiza a cada 30 segundos.

Todos os horários e endereços vivem num único lugar: a constante `CONGREGACOES`
no topo de `assets/js/main.js`. Mudou horário? Mexe ali e atualiza home, agenda,
contato e primeira visita.

`dia`: 0 = domingo, 1 = segunda, ... 6 = sábado.

---

## Formulário de contato

A página `contato.html` envia por **Web3Forms** (grátis no volume de uma igreja).
Para ativar:

1. Crie uma chave em https://web3forms.com.
2. Cole em `FORMS["chave_web3forms"]` no `build.py`.
3. Rode `python3 build.py`.

O envio é feito via `fetch` com confirmação na tela — sem recarregar a página.

---

## Identidade visual

Extraída da própria igreja, não inventada. As paredes do salão são cor de cal, o
letreiro é âmbar quente, e a campanha 2K26 é noite com brasa.

### Cor

| Token | Hex | Onde |
|---|---|---|
| `--noite` | `#0C0B0A` | Herói, capas, rodapé, faixa Unidade |
| `--carvao` | `#1A1613` | Cartões sobre fundo escuro |
| `--grafite` | `#23201C` | Texto sobre fundo claro |
| `--cal` | `#F4F0E9` | Superfície principal — é a parede da igreja |
| `--areia` | `#E6DFD3` | Seções alternadas |
| `--brasa` | `#F1592A` | Cor primária: botões, destaques, itálicos |
| `--ambar` | `#E9A23B` | Detalhes quentes — vem do letreiro neon |
| `--neutro` | `#7C7268` | Texto secundário |

### Tipografia

| Papel | Fonte | Uso |
|---|---|---|
| Display | **Bodoni Moda** | Só títulos. |
| Utilitária | **Oswald** | Sobrescritos, rótulos, botões. |
| Corpo | **Inter** | Texto corrido. Neutra de propósito. |

Todas do Google Fonts, sem licença a pagar.

### Elemento assinatura

O **asterisco** do selo "Uma só Missão": três congregações convergindo em uma
igreja. Aparece girando na faixa da Unidade e no favicon.

---

## Acessibilidade e desempenho

- Responsivo até 390px.
- Skip-link para pular direto ao conteúdo.
- Foco de teclado visível em tudo que é clicável.
- `prefers-reduced-motion` respeitado (selo para, revelações somem).
- Formulário com `required`, labels e status de envio por voz.
- Fotografias com `loading="lazy"` fora da primeira dobra.
- Logos e favicon otimizados (o favicon é um SVG de ~500 bytes).
- Open Graph configurado para compartilhamento bonito no WhatsApp.
- Zero dependência de JS para ler o conteúdo: se o script falhar, o texto continua lá.
