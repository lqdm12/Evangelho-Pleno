# Igreja Evangelho Pleno — site

Fase atual: **estrutura**. Todo texto que ainda vai mudar está marcado com
`data-ph` no HTML. Abra qualquer página e clique no botão **"Ver placeholders"**
no canto inferior direito: tudo que precisa de conteúdo real acende em laranja.

---

## Como rodar

Não tem build nem dependência. É HTML, CSS e JS puros.

```bash
python3 -m http.server 8000
# abre http://localhost:8000
```

Hospedagem: qualquer serviço estático serve (Netlify, Vercel, GitHub Pages,
Cloudflare Pages). Basta subir a pasta.

---

## Arquivos

```
index.html            Home
primeira-visita.html  A página mais importante do site
quem-somos.html       História, doutrina, liderança
unidade.html          Campanha 2K26
ministerios.html      Grupos e como participar
agenda.html           Horários e eventos
contato.html          Formulário e pedido de oração
contribua.html        Dízimos e ofertas

assets/css/styles.css Folha única, comentada por seção
assets/js/main.js     Seletor de congregação, contagem, menu, revelação
assets/img/logo/      Logos recortados + ícone + cartaz 2K26
assets/img/fotos/     Fotos da igreja, otimizadas para web

build.py              Gera as páginas internas com header/rodapé compartilhados
```

**Importante:** as páginas internas são geradas pelo `build.py`. Se você mudar o
menu ou o rodapé, mude no `build.py` e rode `python3 build.py` de novo, senão as
páginas saem do ar umas com as outras. A `index.html` é escrita à mão e precisa
ser atualizada em paralelo.

---

## Identidade visual

Extraída da própria igreja, não inventada. As paredes do salão são cor de cal, o
letreiro é âmbar quente, e a campanha 2K26 é noite com brasa. O site usa os três.

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

O azul neon do kit antigo foi **descartado**. Ele briga com o laranja da campanha
e não existe em lugar nenhum do espaço físico.

### Tipografia

| Papel | Fonte | Uso |
|---|---|---|
| Display | **Bodoni Moda** | Só títulos. É o que mais se aproxima da serifa do cartaz "Unidade". |
| Utilitária | **Oswald** | Sobrescritos, rótulos, botões. Replica a condensada da tagline. |
| Corpo | **Inter** | Texto corrido. Neutra de propósito. |

Todas do Google Fonts, sem licença a pagar.

### Elemento assinatura

O **asterisco** do selo "Uma só Missão". Não é enfeite: são três congregações
convergindo em uma igreja. Ele aparece como selo giratório na faixa da Unidade e
pode virar divisor de seção conforme o site crescer.

---

## O seletor de congregação

É a peça central da home e a razão de o site funcionar para visitante novo.

A pessoa escolhe onde mora e o site responde: **qual é o próximo culto, que dia,
que horas, quanto falta e como chegar.** A contagem regressiva é ao vivo e se
atualiza a cada 30 segundos.

Todos os horários e endereços vivem em **um único lugar**: a constante
`CONGREGACOES` no topo de `assets/js/main.js`. Mudou horário? Mexe ali e o site
inteiro se atualiza — home, agenda, contato, primeira visita.

```js
{
  id: 'santa-teresa',
  nome: 'Santa Teresa',
  sede: true,
  endereco: 'Av. Luís Müller, 144 — Centro',
  cidade: 'Santa Teresa, ES',
  mapa: 'https://...',
  cultos: [
    { dia: 0, hora: 19, minuto: 0,  nome: 'Culto de Celebração' },
    { dia: 2, hora: 19, minuto: 30, nome: 'Culto de Ensino' }
  ]
}
```

`dia`: 0 = domingo, 1 = segunda, ... 6 = sábado.

---

## Pendências para o site ir ao ar

### Bloqueiam o lançamento

1. **Nome dos cultos de semana.** Usei "Culto de Ensino" como palpite. Como a
   igreja chama de verdade o culto de terça, quarta e quinta?
2. **Santa Teresa é a sede?** Marquei como sede porque foi a primeira que você
   listou. Confirmar.
3. **Endereço completo de Várzea Alegre.** "Centro, anexo ao posto de
   combustível" não gera pin no Google Maps. Precisa de rua e número, ou pelo
   menos o nome do posto.
4. **WhatsApp e Instagram** da igreja (estão como placeholder no rodapé e no
   `main.js`).
5. **Formulário de contato.** O HTML está pronto mas não envia nada. Precisa de
   um back-end. O mais barato: [Formspree](https://formspree.io) ou
   [Web3Forms](https://web3forms.com), que funcionam em site estático e são de
   graça no volume de uma igreja.
6. **Chave PIX e dados bancários** para a página Contribua.
7. **Domínio.** Sugestão: `evangelhopleno.com.br` ou `.org.br`.

### Melhoram muito, mas dá pra lançar sem

8. **Missão, visão e paixão** — as três frases oficiais. Hoje estão como
   `[TEXTO A DEFINIR]` e são um buraco visível na home.
9. **História da igreja** e **confissão de fé** resumida.
10. **Fotos da liderança.** Idealmente todas no mesmo lugar, com a mesma luz.
11. **Lista real de ministérios.** Coloquei seis genéricos como estrutura.
    Confirmar quais existem de fato e em quais congregações.
12. **Fotos das outras duas congregações.** Todas as fotos atuais parecem ser da
    mesma casa. Um visitante de São Roque ou Várzea Alegre vai querer ver a dele.

---

## Acessibilidade e desempenho

- Responsivo até 390px.
- Foco de teclado visível em tudo que é clicável.
- `prefers-reduced-motion` respeitado: o selo para de girar e as revelações somem.
- Fotos com `loading="lazy"` fora da primeira dobra.
- Zero dependência de JS para ler o conteúdo. Se o script falhar, o texto continua lá.

---

## Antes de entregar ao cliente

Remover as ferramentas da fase de estrutura:

1. O botão `<button class="barra-ph">` no fim de cada HTML.
2. A seção 18 do `styles.css` (modo placeholder).
3. Todos os atributos `data-ph` do HTML.
4. O `build.py` (ou mantenha, se for continuar editando pelo template).
