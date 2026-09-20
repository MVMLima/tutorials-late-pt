#!/usr/bin/env python3
"""Gera os prompts e os scripts de execução dos agentes tradutores (agy / Antigravity CLI)."""
import pathlib

ROOT = pathlib.Path("/home/marc/Documentos/Projetos/tutorials-late-pt")
AG = ROOT / "_work" / "agents"
AG.mkdir(parents=True, exist_ok=True)

AGENTES = [
    ("01", "episodios/01-matrizes-de-contato.qmd",
     "Episódio 1 — Matrizes de contato (Contact matrices): o que é uma matriz de contato, como as "
     "matrizes são estimadas a partir de inquéritos (POLYMOD), uso de {socialmixr} e {contactsurveys} "
     "para baixar e carregar inquéritos do Zenodo, {wpp2024} para a estrutura populacional, "
     "normalização, matrizes simétricas, idades, e como usar a matriz em análises epidemiológicas."),
    ("02", "episodios/02-simular-transmissao.qmd",
     "Episódio 2 — Simular a transmissão (Simulating transmission): simular a propagação de uma "
     "doença com o pacote {epidemics}, modelos compartimentais (SIR/SEIR), condições iniciais, "
     "estrutura populacional, matriz de contato, conjunto de parâmetros, incerteza, e leitura das "
     "saídas do modelo."),
    ("03", "episodios/03-escolher-modelo.qmd",
     "Episódio 3 — Escolher um modelo adequado (Choosing an appropriate model): critérios para "
     "escolher entre modelos determinísticos e estocásticos, com e sem estrutura etária, e o que "
     "cada escolha implica para a pergunta de saúde pública."),
    ("04", "episodios/04-modelar-intervencoes.qmd",
     "Episódio 4 — Modelar intervenções (Modelling interventions): como representar intervenções "
     "não farmacológicas no {epidemics} (máscaras, distanciamento, fechamento de escolas, "
     "distanciamento no local de trabalho), taxas de transmissão reduzidas, adesão, e comparação "
     "de trajetórias com e sem intervenção."),
    ("05", "episodios/05-comparar-intervencoes.qmd",
     "Episódio 5 — Comparar desfechos de saúde pública das intervenções (Comparing public health "
     "outcomes of interventions): baixar inquéritos de contato de outros países com "
     "{contactsurveys}/{socialmixr}, {wpp2024} para demografia, comparar cenários de intervenção, "
     "infecções evitadas e outras métricas de desfecho."),
    ("06", "episodios/06-comparar-vacinacao.qmd",
     "Episódio 6 — Comparar estratégias de vacinação (Comparing vaccination strategies): efeitos "
     "diretos e indiretos da vacinação, imunidade de rebanho, priorização por idade, cenários de "
     "vacinação com {epidemics}, combinação de vacinação com intervenções não farmacológicas, "
     "cobertura vacinal e esquemas de doses."),
    ("07", "episodios/07-carga-de-doenca.qmd",
     "Episódio 7 — Modelar a carga de doença (Modelling disease burden): estimar demanda por "
     "serviços de saúde a partir das saídas do modelo, internações e leitos, DALYs, anos de vida "
     "perdidos e uso dessas métricas para orientar decisões."),
    ("08", "setup.qmd + glossario.qmd",
     "Página de Setup (instalação de R e do ambiente, ferramentas de compilação, pacotes do "
     "Epiverse, projeto do R) e o Glossário de Termos. São DOIS arquivos de saída. No glossário, "
     "mantenha as seções de letra (`## A`, `## B`, ...) e reordene as entradas de cada seção na "
     "ordem alfabética do português; preserve integralmente as âncoras `{#algumacoisa}` e os links "
     "internos `(#algumacoisa)`, porque os episódios apontam para elas."),
]

PROMPT = """Você é um tradutor técnico-científico de epidemiologia. Trabalhe no diretório
{root}

## Passo 1 — Leia as regras
Leia o arquivo `scripts/BRIEF-traducao.md` (caminho absoluto: {root}/scripts/BRIEF-traducao.md)
e siga TODAS as regras invioláveis e o termbase. Ele é a fonte de verdade.

## Passo 2 — Tarefa
{descricao}

ENTRADA (leia o arquivo inteiro antes de começar):
{entradas}

SAÍDA (crie/sobrescreva):
{saidas}

O texto de entrada é uma aula de modelagem de cenários para análise de surtos em R, já convertida
do formato Carpentries/The Carpentries Workbench para o formato Quarto (callouts
`::: {{.callout-...}}`). Os títulos dos callouts já estão em português: não os altere.

## Regras extras para este trabalho
- No cabeçalho YAML (entre `---`), mantenha APENAS a linha `title:` traduzida. Remova
  `teaching:`, `exercises:`, `fig_caption:`, `code_folding:`, `editor_options:` e qualquer outra linha.
- O arquivo de saída deve conter SOMENTE o conteúdo da aula traduzido. Não acrescente
  comentários seus, nem relatórios, nem blocos de código novos.
- Preserve exatamente a quantidade, a ordem e a indentação dos blocos de código e dos
  `::: {{.callout-...}}` do original. Mantenha uma linha em branco antes e depois de cada `:::`.
- NÃO traduza o conteúdo dentro dos blocos de código, exceto comentários que começam com `#`.
- Se o original tiver um bloco `::: {{.panel-tabset}}`, preserve-o como está.

## Como escrever o arquivo
Use a ferramenta de escrita de arquivo para criar o arquivo de saída completo, com caminho absoluto.
Se o arquivo for grande, escreva em partes (primeira parte criando o arquivo, o restante com
`cat >> arquivo << 'EOF'` no shell), sempre com caminho absoluto e fechando o heredoc corretamente.

## Checklist antes de terminar
1. Nenhum token de código R alterado (exceto comentários `#`).
2. Todos os blocos `::: {{.callout-...}}` preservados, com os mesmos títulos.
3. Saídas de console/erros do R preservados em inglês.
4. Nenhum número, link, referência ou dado inventado.
5. `wc -l` do arquivo de saída conferido e comparável ao da entrada.
6. Marcações `<!-- [verificar] -->` e `<!-- CONTEXTO-BR: ... -->` deixadas onde couber.

## Relatório final (texto curto)
- Caminhos absolutos dos arquivos escritos + número de linhas de cada um
- Lista das marcações `[verificar]` (linha e motivo)
- Lista das sugestões `CONTEXTO-BR` (linha e sugestão)
"""

for num, saida_rel, desc in AGENTES:
    partes = [s.strip() for s in saida_rel.split(" + ")]
    entradas = "\n".join(f"  - {ROOT}/_source/en-quarto/{s}" for s in partes)
    saidas = "\n".join(f"  - {ROOT}/{s}" for s in partes)
    txt = PROMPT.format(root=ROOT, descricao=desc, entradas=entradas, saidas=saidas)
    (AG / f"prompt-{num}.md").write_text(txt, encoding="utf-8")

    sh = f"""#!/usr/bin/env bash
# Agente tradutor {num}
cd "{ROOT}" || exit 1
LOG="{AG}/log-{num}.txt"
agy --dangerously-skip-permissions --print-timeout 40m --print="$(cat '{AG}/prompt-{num}.md')" > "$LOG" 2>&1
echo "EXIT_AGENTE{num}=$?" >> "$LOG"
"""
    p = AG / f"run-{num}.sh"
    p.write_text(sh, encoding="utf-8")
    p.chmod(0o755)

print("Prompts e scripts gerados em", AG)
for f in sorted(AG.iterdir()):
    print(" ", f.name, f.stat().st_size, "bytes")
