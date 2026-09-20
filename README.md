# Modelagem de cenários para análise de surtos com R — adaptação PT-BR

Site do curso **Modelagem de cenários para análise de surtos com R: matrizes de contato, simulação
da transmissão, intervenções e carga de doença**, adaptação para o português brasileiro do tutorial
*Epiverse-TRACE Tutorials Late*.

**Site publicado:** https://mvmlima.github.io/tutorials-late-pt/

## O que tem aqui

| Arquivo | Conteúdo |
|---|---|
| `index.qmd` | Página inicial: sobre o curso, público, pré-requisitos |
| `setup.qmd` | Preparação do ambiente (R, ferramentas de compilação, pacotes, projeto do R) |
| `episodios/01-matrizes-de-contato.qmd` | Matrizes de contato: estimativa a partir de inquéritos com `{socialmixr}` |
| `episodios/02-simular-transmissao.qmd` | Simular trajetórias de doença com `{epidemics}` |
| `episodios/03-escolher-modelo.qmd` | Como escolher o modelo adequado à pergunta |
| `episodios/04-modelar-intervencoes.qmd` | Intervenções não farmacológicas no modelo |
| `episodios/05-comparar-intervencoes.qmd` | Cenário de base e métricas de comparação |
| `episodios/06-comparar-vacinacao.qmd` | Efeitos diretos e indiretos da vacinação |
| `episodios/07-carga-de-doenca.qmd` | Demanda por serviços de saúde e anos de vida perdidos |
| `glossario.qmd` | Glossário de termos |
| `perfis.qmd` | Personas de aprendiz do treinamento |
| `instrutor.qmd` | Notas e plano de aula para quem conduz a oficina |
| `licenca.qmd` | Licença e créditos |
| `img/` | Figuras do material original |
| `_source/` | Arquivos originais em inglês (formato Carpentries), mantidos para conferência |

## Como renderizar localmente

Requisitos: [Quarto](https://quarto.org/) 1.8+ e R 4.2+.

```bash
# 1. pacotes do curso numa biblioteca local do projeto (não mexe na biblioteca global do R)
Rscript scripts/instalar_pacotes.R

# 2. renderizar
quarto render
```

O site sai em `_site/`. Para pré-visualizar com recarregamento automático: `quarto preview`.

O `_quarto.yml` usa `execute: freeze: auto`, então os resultados dos blocos de código ficam
guardados em `_freeze/` e o build no GitHub Actions **não precisa do R nem dos pacotes**.

> **Regra que evita publicar conteúdo velho.** O CI usa `freeze: true`, que reaproveita o resultado
> congelado e **não regenera o HTML de um arquivo cujo `.qmd` mudou**. Se você editar qualquer
> coisa — inclusive só o texto — e der push sem renderizar, o CI fica verde e a página no ar
> continua a antiga. Por isso, depois de qualquer edição:
>
> ```bash
> quarto render && python3 scripts/freshness.py --update
> git add -A && git commit -m "..." && git push
> ```
>
> O CI roda `scripts/freshness.py --check` antes de publicar e **falha** se algum `.qmd` estiver
> mais novo que o último render local, dizendo qual arquivo e o que rodar.

> **Rede é obrigatória neste curso.** Os dados de contato vêm do Zenodo (via `{contactsurveys}`) e
> a demografia vem do pacote `{wpp2024}` — não há arquivos CSV no projeto. O render local precisa
> de internet.

> **Tempo de execução:** não há MCMC aqui — os modelos do `{epidemics}` são equações diferenciais
> resolvidas direto. O episódio mais pesado (o 6, com dezoito simulações) leva cerca de 47 segundos
> para renderizar; o site inteiro sai em poucos minutos.

## Publicação

O workflow `.github/workflows/publish.yml` renderiza o site e publica na branch `gh-pages` a
cada push na `main`. O GitHub Pages serve a partir dessa branch.

## Verificação da tradução

```bash
python3 scripts/verificar_traducao.py
```

Compara cada episódio traduzido com o original convertido (`_source/en-quarto/`) e aponta: blocos
de código que foram alterados, callouts perdidos, links internos quebrados e imagens ausentes.

## Como a versão PT-BR foi produzida

1. `scripts/convert_carpentries.py` converte as lições do formato Carpentries Workbench (divs
   cercados com `::::`) para o formato Quarto (callouts), ajustando imagens e links internos.
2. Oito agentes tradutores (CLI `agy`) traduzem cada episódio seguindo `scripts/BRIEF-traducao.md`
   (termbase e regras: código intocado, nada inventado).
3. `scripts/passada_editorial.py` insere as caixas de contexto brasileiro e remove os marcadores
   de trabalho.
4. `scripts/verificar_traducao.py` confere a integridade do código.

## Licença

O material original é publicado sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Esta adaptação é publicada sob a **mesma licença**. Créditos completos em `licenca.qmd`.

Citação do original:

> Minter A, Degoot A, Valle-Campos A, Gruson H, Bah B, Funk S, Eggo R, Kucharski A (2026).
> *Epiverse-TRACE Tutorials Late: Scenario modelling for outbreak analytics with R.* DOI:
> [10.5281/zenodo.21512057](https://doi.org/10.5281/zenodo.21512057)
