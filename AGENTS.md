<!-- BEGIN hal-contract: generato da a-agentzero 1.13.15 · tpl 2 — NON EDITARE TRA I FENCE -->
## HAL — contratto consumer

- HAL canonico: `/var/www/hal_gateway` (repo `hal_gateway`). **Da questo progetto**: mai modificare
  `agents/` del canonico, mai eseguire `link-workspace-skills.sh` / `deploy-all.sh` /
  `publish-global-commands.sh` (guardie: «Guardia HAL» e path assoluto), mai ricreare
  symlink HAL verso `.agents`/`agents`/`.zed`/`product` — i mount sono rimossi (de-racing).
- Script L0: invocarli con path assoluto, es. `bash /var/www/hal_gateway/agents/a-agentzero/scripts/<script>.sh`.
- Comandi L0 `/version`, `/document`, `/review`, `/improve`, `/commit`, `/todo`, `/slice`, `/cycle`, `/graph`, `/sync`, `/learn`, `/laya`: pubblicati come skill globali (`~/.agents/skills/`,
  rigenerate solo da hal_gateway via `publish-global-commands.sh`); una skill locale
  omonima ha priorità. Lettura del canone: `read`
  `/var/www/hal_gateway/agents/a-agentzero/commands/<cmd>.md`.
- **Delega MCP (scelta voce per voce)**: agenti L1 e skill embedded (jtbd, gherkin,
  enrichment, uiux, charts, illustrator, personas, laya…) NON sono globali né montati:
  il progetto le usa solo se servono, caricandole on-demand dai tool MCP del server
  hal_gateway (`skills_list` per il catalogo, `skill_read` per il SKILL.md integrale o
  un reference con `file`); fallback senza MCP: `read` del path in catalogo.
- Le skill `.agents/skills/` presenti in questo repo sono L2 di questo progetto.

### Catalogo HAL (generato — non editare a mano)

- **a-agentzero** — Agente radice HAL: ereditarietà a 3 livelli, competenze modulari, avvio multiprogetto, workflow generici, checklist e scaffold L2. Istruzioni: `read /var/www/hal_gateway/agents/a-agentzero/SKILL.md`
- **a-b2b** — Agente L1 per piloti B2B e contact/account research: orchestra il profilo B2B e include la skill enrichment per ricerca ICP, CRM cascade e lead valid…. Istruzioni: `read /var/www/hal_gateway/agents/a-b2b/SKILL.md`
- **a-copywriter** — Scrive e revisiona copy web generico (prodotti, categorie, blog, landing, meta, FAQ). Istruzioni: `read /var/www/hal_gateway/agents/a-copywriter/SKILL.md`
- **a-design** — Agente L1 Design & Visual Experience: unifica layout e accessibilità (uiux), grafici e data visualization (charts) e asset illustrativi (illustrator). Istruzioni: `read /var/www/hal_gateway/agents/a-design/SKILL.md`
- **a-harness** — Meta-Harness: TDD XP, Steward, DDD, Makefile gates, session progress, when-stuck, Plan→Act, L3. Istruzioni: `read /var/www/hal_gateway/agents/a-harness/SKILL.md`
- **a-knowledge** — Agente L1 Knowledge / Context Engineering: trasforma libri e documentazione tecnica (PDF, EPUB, DOCX, HTML, Markdown) in skill interrogabili on-demand. Istruzioni: `read /var/www/hal_gateway/agents/a-knowledge/SKILL.md`
- **a-product** — Agente L1 Product Management: discovery, PO (PRD, Lean Canvas, priorità, validazione), JTBD, Personas e BDD Spec. Istruzioni: `read /var/www/hal_gateway/agents/a-product/SKILL.md`
- **a-seozoom** — Agente SEO/GEO multi-progetto: orchestra import dati, analisi metriche, on-page, GEO/AEO, audit, schema, pSEO, IA, hreflang, topic-cluster e Google A…. Istruzioni: `read /var/www/hal_gateway/agents/a-seozoom/SKILL.md`
- **a-wordpress** — Analizza installazioni WordPress specifiche e sviluppa, mantiene e revisiona plugin (stabili e migrate). Istruzioni: `read /var/www/hal_gateway/agents/a-wordpress/SKILL.md`
- **charts** (in a-design) — Data Visualization integrata in a-design: scelta del tipo, encoding visuale, implementazione (SVG/D3/canvas/HTML) e QA. `read /var/www/hal_gateway/agents/a-design/charts/SKILL.md`
- **enrichment** (in a-b2b) — Contact/account enrichment B2B: dual entry (CRM cohort + domain-first), ICP/fit gates, HubSpot → Apollo → LeadMagic → SQLite master, lead-research ou…. `read /var/www/hal_gateway/agents/a-b2b/enrichment/SKILL.md`
- **gherkin** (in a-product) — QA Lead / BDD Spec integrato in a-product: suite Gherkin da jtbd seeds, inventory UI/IO, journey E2E, expand edge, /cover, add-scenario da NL, /secur…. `read /var/www/hal_gateway/agents/a-product/gherkin/SKILL.md`
- **illustrator** (in a-design) — Genera illustrazioni coerenti orchestrando stile-visivo, prompt-composizione, preview-render e qa-artefatti. `read /var/www/hal_gateway/agents/a-design/illustrator/SKILL.md`
- **jtbd** (in a-product) — Job Analyst / JTBD integrato in a-product: Jobs-To-Be-Done job-first, ODI needs/unmet, continuity di flusso, job stories e scenario seeds per BDD;. `read /var/www/hal_gateway/agents/a-product/jtbd/SKILL.md`
- **learn** (in a-agentzero) — Slash /learn con tripla modalità: /learn ? illustra gli apprendimenti dalla conversazione o sessione corrente;. `read /var/www/hal_gateway/agents/a-agentzero/learn/SKILL.md`
- **personas** (in a-product) — User Researcher integrato in a-product: definisce personas da PRD/mockup con intervista PO, verifica journey coherence vs mockup/PRD, aggiunge person…. `read /var/www/hal_gateway/agents/a-product/personas/SKILL.md`
- **sync** (in a-agentzero) — Sincronizza agenti HAL L0/L1 (deploy) e comandi Cursor L0 ereditabili;. `read /var/www/hal_gateway/agents/a-agentzero/sync/SKILL.md`
- **uiux** (in a-design) — UI/UX per siti statici e shell pagina integrato in a-design: stack M3/vanilla CSS, accessibilità WCAG, layout editoriale, pattern guida/chrome comuni…. `read /var/www/hal_gateway/agents/a-design/uiux/SKILL.md`
- **gdrive-sync-safe** — Guide to safely manage local Google Drive mirrors and prevent IDE freezes or recursive index locking. `read /var/www/hal_gateway/agents/gdrive-sync-safe/SKILL.md`
- **laya** — Interfaccia per Laya System 1: routing di categorie, choice tra opzioni, score euristico di rischio o aderenza, confidence 0-100%, context 0-100%, no…. `read /var/www/hal_gateway/agents/project-skills/laya/SKILL.md`
- **harness-hal** (solo gateway) — Delta harness per HAL Gateway: Platform API root (Makefile specchio CI), path artefatti, profile bootstrap standard, N/A documentati (int/e2e/parity)…. `read /var/www/hal_gateway/agents/project-skills/harness-hal/SKILL.md`
<!-- END hal-contract -->
