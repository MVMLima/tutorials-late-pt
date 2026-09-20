# BRIEF — Tradução e adaptação PT-BR do tutorial Epiverse-TRACE "Late tasks"

## Fonte
- Original (EN): https://epiverse-trace.github.io/tutorials-late/ (Epiverse-TRACE, CC-BY 4.0)
- Repositório: https://github.com/epiverse-trace/tutorials-late
- Arquivos de trabalho (já convertidos de Carpentries → Quarto): `_source/en-quarto/`

## Objetivo
Produzir a versão em português brasileiro do curso *Scenario modelling for outbreak analytics with
R* (modelagem de cenários para análise de surtos com R), para uso em oficinas presenciais com
epidemiologistas de vigilância.

## Regras invioláveis

1. **Não alterar código.** Nenhum token de código R pode mudar: funções, argumentos, nomes de
   objetos, strings, números, caminhos de arquivo, nomes de colunas. Só é permitido traduzir
   **comentários R** (linhas cujo conteúdo, ignorando espaços, começa com `#`).
2. **Não alterar saídas pré-impressas.** Blocos de saída de console, mensagens de erro e avisos do
   R permanecem em inglês, exatamente como o R os emite.
3. **Não alterar estrutura Quarto.** Mantenha todas as linhas `::: {.callout-...}` / `:::` / `:::
   {.panel-tabset}` como estão (os títulos já estão em português). Não crie, funda ou remova
   callouts. Mantenha uma linha em branco antes e depois de cada cerca `:::`.
4. **Não inventar.** Não acrescente números, datas, referências, DOIs, links, nomes de portarias
   ou dados que não estejam no original. Se algo estiver ambíguo, traduza literalmente e marque
   com `<!-- [verificar] -->` logo depois.
5. **Manter em inglês** (nome técnico, não se traduz): nomes de pacotes (`{epidemics}`,
   `{socialmixr}`, `{contactsurveys}`, `{wpp2024}`, `{finalsize}`, `{epiparameter}`, `{tidyverse}`),
   nomes de funções (`epidemics::model_default()`, `socialmixr::contact_matrix()`, `wpp2024::`,
   `finalsize::final_size()`), nomes de argumentos e colunas, valores de colunas, URLs, caminhos
   de arquivo, e os termos **SEIR**, **SIR**, **ODE**, **R0**, **Rt**, **NPIs**, **POLYMOD**,
   **lockdown**, **DALYs**, **CFR**, **IFR**, **linelist**.
6. **Escrita matemática intacta**: não toque em nada entre `$...$`, `$$...$$`, `\\(...\\)` nem
   nos identificadores de âncora `{#algumacoisa}`.
7. **Tom.** Português brasileiro técnico, direto, como um epidemiologista explicando para outro.
   Sem floreio, sem "vamos mergulhar", sem "poderoso". Trate o leitor por "você".
8. **Links internos**: mantenha os destinos como estão (já apontam para os arquivos do site PT).

## Termbase (use consistentemente)

| Inglês | Português |
|---|---|
| scenario modelling | modelagem de cenários |
| outbreak | surto |
| outbreak analytics | análise de surtos |
| intervention | intervenção |
| non-pharmaceutical interventions (NPIs) | intervenções não farmacológicas (NPIs) |
| contact matrix | matriz de contato |
| contact survey | inquérito de contato |
| contact rate | taxa de contato |
| normalisation | normalização |
| age group / age category | faixa etária |
| population structure | estrutura populacional |
| demography | demografia |
| susceptibility / susceptible | suscetibilidade / suscetível |
| infectiousness / infectious | infecciosidade / infeccioso |
| transmissibility | transmissibilidade |
| transmission rate | taxa de transmissão |
| force of infection | força de infecção |
| compartmental model | modelo compartimental |
| ordinary differential equations (ODE) | equações diferenciais ordinárias (EDO) |
| stochastic / deterministic | estocástico / determinístico |
| initial conditions | condições iniciais |
| parameter set | conjunto de parâmetros |
| scenario | cenário |
| baseline | linha de base |
| counterfactual | contrafactual |
| to avert | evitar |
| infections averted | infecções evitadas |
| model output | saída do modelo |
| trajectory | trajetória |
| peak | pico |
| attack rate | taxa de ataque |
| disease burden | carga de doença |
| DALYs | DALYs |
| years of life lost | anos de vida perdidos |
| healthcare demand | demanda por serviços de saúde |
| hospitalisation | internação |
| hospital bed | leito hospitalar |
| ICU | UTI |
| vaccination | vacinação |
| vaccine | vacina |
| vaccine efficacy | eficácia vacinal |
| vaccine coverage | cobertura vacinal |
| booster dose | dose de reforço |
| dosing | esquema de doses |
| rollout | campanha de vacinação |
| vaccine prioritisation | priorização da vacinação |
| targeted vaccination | vacinação direcionada |
| direct effects | efeitos diretos |
| indirect effects | efeitos indiretos |
| herd immunity | imunidade de rebanho |
| waning immunity | queda da imunidade |
| adherence | adesão |
| school closure | fechamento de escolas |
| mask | máscara |
| social distancing | distanciamento social |
| survey | inquérito |
| to estimate | estimar |
| estimate (substantivo) | estimativa |
| uncertainty | incerteza |
| to account for | levar em conta |
| workshop | oficina |
| Challenge | Desafio |
| Solution | Solução |
| Hint | Dica |
| Key points | Pontos-chave |
| you can | você pode |

## Ambiente (adaptação ao contexto brasileiro)
- Onde o original diz **RStudio**, escreva **Positron (ou RStudio, se preferir)** na primeira
  menção de cada arquivo e apenas **Positron** nas seguintes. Não reescreva capturas de tela nem
  menus que só existem no RStudio — nesses casos mantenha RStudio e não invente equivalente.
- Onde o original ensina a instalar pacotes, você pode acrescentar a menção ao espelho brasileiro
  do CRAN — use **exatamente** esta linha, sem alterar o resto:
  `options(repos = c(CRAN = "https://cran-r.c3sl.ufpr.br/"))`.
- **Não** crie blocos de contexto brasileiro por conta própria. Quando perceber um ponto onde
  caberia uma ligação com a prática brasileira (SINAN, SIVEP-Gripe, DATASUS, e-SUS, PNI, semana
  epidemiológica, leitos de UTI no SUS, rotina de vigilância), deixe um comentário na linha exata,
  neste formato:
  `<!-- CONTEXTO-BR: sugestão curta do que caberia aqui -->`
  O revisor (agente pai) decide e escreve o texto final desses boxes.

## Entrega
- Arquivo de saída no caminho indicado no prompt do seu agente, em UTF-8.
- Ao terminar, informe: caminho absoluto, número de linhas (`wc -l`) e a lista de marcações
  `<!-- [verificar] -->` e `<!-- CONTEXTO-BR: ... -->` que você deixou.
