#!/usr/bin/env python3
"""
Passada editorial final sobre os arquivos traduzidos:

1. substitui os marcadores `<!-- CONTEXTO-BR: ... -->` escolhidos por caixas "No Brasil"
   de verdade (conteúdo escrito pelo revisor, com fonte verificada nesta sessão);
2. traduz os rótulos dos diagramas Mermaid que ficaram em inglês;
3. remove os marcadores `CONTEXTO-BR` restantes e os `[verificar]` deixados pelos agentes.

Os marcadores `[verificar]` que apontavam defeito do material original NÃO são consertados aqui:
o texto fica como no original e o defeito é registrado em `licenca.qmd`.

Fontes verificadas em 20/09/2026 (todas respondidas HTTP 200, exceto as três marcadas
"bloqueia HEAD", cujo conteúdo foi confirmado pelas páginas de busca):
  F1  https://datasus.saude.gov.br/populacao-residente/
  F2  https://cran.r-project.org/package=microdatasus
  F3  contactsurveys::list_surveys() -> 48 inquéritos, nenhum do Brasil (executado nesta sessão)
  F4  https://dadosabertos.saude.gov.br/dataset/srag-2019-a-2026
  F5  http://portalsinan.saude.gov.br/calendario-epidemiologico
  F6  https://si-pni.saude.gov.br/
  F7  https://www.scielosp.org/article/csc/2020.v25suppl1/2423-2446/pt/   (bloqueia HEAD)
  F8  https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/c/covid-19/publicacoes-tecnicas/
      guias-e-planos/plano-nacional-de-operacionalizacao-da-vacinacao-contra-a-covid-19
      (bloqueia HEAD)
  F9  https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/pdfs/
      dicionario_de_dados_srag_hosp_17_02_2022.pdf   (dicionário oficial de dados do SRAG)
  F10 http://cnes.datasus.gov.br/
  F11 https://gbdbr.com.br/
"""
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent.parent

F1 = "[População residente — DATASUS](https://datasus.saude.gov.br/populacao-residente/)"
F2 = "[microdatasus (CRAN)](https://cran.r-project.org/package=microdatasus)"
F4 = ("[Portal de Dados Abertos do SUS — SIVEP-Gripe](https://dadosabertos.saude.gov.br/"
      "dataset/srag-2019-a-2026)")
F5 = ("[Calendário epidemiológico do SINAN]"
      "(http://portalsinan.saude.gov.br/calendario-epidemiologico)")
F6 = "[SI-PNI](https://si-pni.saude.gov.br/)"
F7 = ("[Aquino et al. (2020), *Ciência & Saúde Coletiva* 25(supl. 1)](https://www.scielosp.org/"
      "article/csc/2020.v25suppl1/2423-2446/pt/)")
F9 = ("[dicionário de dados da ficha de SRAG hospitalizado]"
      "(https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/pdfs/"
      "dicionario_de_dados_srag_hosp_17_02_2022.pdf)")
F10 = "[CNES](http://cnes.datasus.gov.br/)"
F11 = "[Rede GBD Brasil](https://gbdbr.com.br/)"

# (arquivo, prefixo único do marcador, caixa que entra no lugar)
CAIXAS = [
    ("episodios/01-matrizes-de-contato.qmd",
     "<!-- CONTEXTO-BR: Para análises no Brasil, a estrutura populacional",
     f"""::: {{.callout-note title="No Brasil: de onde tirar a estrutura populacional"}}

O `{{wpp2024}}` traz as projeções da ONU, que servem para qualquer país. Para usar a população
brasileira por faixa etária — nacional, estadual ou municipal —, o caminho é o Censo e as
estimativas/projeções do IBGE, publicadas pelo DATASUS ({F1}). Há também o pacote
`{{microdatasus}}`, que baixa esses microdados direto para o R ({F2}).

:::
"""),

    ("episodios/01-matrizes-de-contato.qmd",
     "<!-- CONTEXTO-BR: O trabalho de Prem et al. inclui projeções",
     """::: {.callout-note title="No Brasil: não existe inquérito de contato brasileiro aqui"}

A coleção consultada pelo `{contactsurveys}` não tem nenhum inquérito brasileiro: em 20/09/2026 a
`contactsurveys::list_surveys()` devolvia 48 inquéritos depositados, todos de outros países.

Na prática, isso significa que quem modela o Brasil precisa escolher uma matriz de contato
justificada — sintética, adaptada de outro país ou de um inquérito próprio — e não uma matriz
medida na população brasileira. Registre essa escolha junto com a análise: ela muda o resultado.

:::
"""),

    ("episodios/02-simular-transmissao.qmd",
     "<!-- CONTEXTO-BR: No Brasil, a vigilância de vírus respiratórios",
     f"""::: {{.callout-note title="No Brasil: onde esses dados existem"}}

O exemplo deste episódio usa uma cepa de influenza com potencial pandêmico. No Brasil, a vigilância
de vírus respiratórios combina a **rede sentinela de Síndrome Gripal (SG)** com a notificação de
**SRAG hospitalizado no SIVEP-Gripe**, cuja base é publicada aberta ({F4}).

:::
"""),

    ("episodios/02-simular-transmissao.qmd",
     "<!-- CONTEXTO-BR: Na vigilância epidemiológica brasileira, a incidência diária",
     f"""::: {{.callout-note title="No Brasil: a semana epidemiológica é a unidade de análise"}}

Na rotina de vigilância, a incidência diária raramente é analisada como está: ela é agregada por
**semana epidemiológica (SE)**, que no Brasil começa no domingo. O calendário oficial de semanas
está no SINAN ({F5}).

:::
"""),

    ("episodios/03-escolher-modelo.qmd",
     "<!-- CONTEXTO-BR: No SUS, internações e casos graves por SRAG",
     f"""::: {{.callout-note title="No Brasil: onde ficam os desfechos graves"}}

Casos graves e internações por SRAG estão no **SIVEP-Gripe**, com base aberta ({F4}); internações
por outros agravos aparecem no **SIH/SUS**, também no DATASUS. São essas as bases que alimentam a
pergunta "quantos casos graves e quantas internações este cenário produz?".

:::
"""),

    ("episodios/03-escolher-modelo.qmd",
     "<!-- CONTEXTO-BR: No Brasil, o PNI combina vacinação de rotina",
     """::: {.callout-note title="No Brasil: vacinação contínua e campanhas"}

O Programa Nacional de Imunizações (PNI) combina **vacinação de rotina**, ao longo do ano, com
**campanhas** de período definido. São dois formatos de intervenção diferentes: uma taxa de
vacinação constante (rotina) e uma taxa concentrada em uma janela curta (campanha).

:::
"""),

    ("episodios/04-modelar-intervencoes.qmd",
     "<!-- CONTEXTO-BR: No Brasil, medidas não farmacológicas (NPIs)",
     f"""::: {{.callout-note title="No Brasil: quem decide sobre as NPIs"}}

As intervenções não farmacológicas (fechamento de escolas, uso de máscaras, restrição de
circulação) foram adotadas no Brasil por **decretos estaduais e municipais**, com heterogeneidade
de conteúdo e de momento entre os entes — o que dificulta tratar o país como um cenário único.
O levantamento das medidas adotadas em 2020 está em {F7}.

:::
"""),

    ("episodios/04-modelar-intervencoes.qmd",
     "<!-- CONTEXTO-BR: No Brasil, o cálculo de doses diárias",
     f"""::: {{.callout-note title="No Brasil: de onde sai a taxa de vacinação"}}

Quando o cenário é brasileiro, o número que entra no modelo é a **dose aplicada por dia**. O
registro oficial de doses está no SI-PNI ({F6}); a capacidade operacional de uma campanha costuma
ser estimada a partir desse histórico. Vale conferir a série antes de assumir uma taxa fixa.

:::
"""),

    ("episodios/05-comparar-intervencoes.qmd",
     "<!-- CONTEXTO-BR: No SUS, desfechos de internação hospitalar",
     f"""::: {{.callout-note title="No Brasil: medindo a pressão assistencial"}}

Entre as medidas de impacto na saúde, as que a gestão do SUS usa no dia a dia são **internações** e
**ocupação de leitos de UTI**. As internações por SRAG estão no SIVEP-Gripe ({F4}) e as demais no
SIH/DATASUS; a oferta de leitos está cadastrada no CNES ({F10}).

:::
"""),

    ("episodios/06-comparar-vacinacao.qmd",
     "<!-- CONTEXTO-BR: No Brasil, o Plano Nacional de Operacionalização",
     """::: {.callout-note title="No Brasil: priorização de grupos"}

O Brasil operou a vacinação contra a COVID-19 por **grupos prioritários** definidos no Plano
Nacional de Operacionalização, e não por idade em ordem decrescente simples. Se o seu cenário é
brasileiro, a ordem de vacinação precisa reproduzir as prioridades que foram adotadas — é
justamente esse desenho que o episódio discute.

:::
"""),

    ("episodios/06-comparar-vacinacao.qmd",
     "<!-- CONTEXTO-BR: No Brasil, estimativas de letalidade e mortalidade",
     f"""::: {{.callout-note title="No Brasil: onde estão os óbitos por faixa etária"}}

Para calibrar o risco de morte por faixa etária, os dados brasileiros estão no **SIM** (óbitos,
DATASUS) e, no caso de SRAG, no **SIVEP-Gripe** ({F4}), que traz o campo de evolução e a data do
óbito. Calibre com a faixa etária da sua população, não com a do exemplo.

:::
"""),

    ("episodios/06-comparar-vacinacao.qmd",
     "<!-- CONTEXTO-BR: Durante emergências de saúde pública no Brasil",
     f"""::: {{.callout-note title="No Brasil: fechamento de escolas"}}

A suspensão das aulas presenciais foi uma das primeiras medidas adotadas no Brasil em 2020, também
por decisão de estados e municípios. A revisão das medidas e dos seus efeitos está em {F7}.

:::
"""),

    ("episodios/07-carga-de-doenca.qmd",
     "<!-- CONTEXTO-BR: No Brasil, dados individualizados de Síndrome Respiratória",
     f"""::: {{.callout-note title="No Brasil: as datas que o SIVEP-Gripe registra"}}

Na ficha de SRAG hospitalizado do SIVEP-Gripe existem, entre outros, os campos `DT_SIN_PRI` (primeiros
sintomas), `DT_INTERNA` (internação), `DT_ENTUTI` e `DT_SAIDUTI` (entrada e saída da UTI) e
`DT_EVOLUCA` (evolução do caso). Os nomes e a descrição de cada campo estão no {F9}.

Com essas datas, os atrasos que o episódio modela por distribuição Gamma podem ser estimados
diretamente dos dados da sua unidade.

:::
"""),

    ("episodios/07-carga-de-doenca.qmd",
     "<!-- CONTEXTO-BR: No SUS, a comparação entre a demanda projetada",
     f"""::: {{.callout-note title="No Brasil: projetar leitos só faz sentido com a oferta ao lado"}}

Uma projeção de demanda por internações e UTI só vira decisão quando comparada com a oferta
existente. A oferta instalada está cadastrada no CNES ({F10}); a disponibilidade do dia é gerida
pelas centrais de regulação. Sem esse segundo lado da conta, o número do modelo não ajuda a gestão.

:::
"""),

    ("glossario.qmd",
     "<!-- CONTEXTO-BR: a metodologia de DALYs",
     f"""::: {{.callout-note title="No Brasil: quem produz DALYs"}}

Os estudos de carga global de doença para o Brasil são produzidos pela rede GBD Brasil ({F11}), que
publica estimativas de DALYs por causa e por unidade federativa — uma referência externa útil para
saber se o seu resultado está na ordem de grandeza esperada.

:::
"""),
]

# Trechos que precisam de correção pontual (não são caixas)
SUBSTITUICOES = [
    # Mermaid do episódio 2 ficou com rótulos em inglês, ao contrário dos outros diagramas
    ("episodios/02-simular-transmissao.qmd",
     '    S -->|"infection<br>(transmission rate &beta;)"| E\n'
     '    E -->|"onset of infectiousness<br>(infectiousness rate &alpha;)"| I\n'
     '    I -->|"recovery<br>(recovery rate &gamma;)"| R',
     '    S -->|"infecção<br>(taxa de transmissão &beta;)"| E\n'
     '    E -->|"início da infecciosidade<br>(taxa de infecciosidade &alpha;)"| I\n'
     '    I -->|"recuperação<br>(taxa de recuperação &gamma;)"| R'),
    ("episodios/02-simular-transmissao.qmd",
     "    accTitle: SEIR compartmental model\n"
     "    accDescr: Four compartments: S (Susceptible), E (Exposed), I (Infectious), R (Recovered). "
     "Transitions: S to E by infection at transmission rate beta; E to I by onset of infectiousness "
     "at rate alpha; I to R by recovery at rate gamma.",
     "    accTitle: Modelo compartimental SEIR\n"
     "    accDescr: Quatro compartimentos: S (Suscetível), E (Exposto), I (Infeccioso), R (Recuperado). "
     "Transições: S para E por infecção à taxa de transmissão beta; E para I por início da "
     "infecciosidade à taxa alpha; I para R por recuperação à taxa gamma."),
]

MARCADOR_CONTEXTO = re.compile(r"[ \t]*<!--\s*CONTEXTO-BR:.*?-->[ \t]*\n?", re.S)
MARCADOR_VERIFICAR = re.compile(r"[ \t]*<!--\s*\[verificar[^>]*?-->[ \t]*\n?")
VERIFICAR_INLINE = re.compile(r"[ \t]*<!--\s*\[verificar[^>]*?-->")


def inserir_caixa(txt: str, prefixo: str, caixa: str):
    """Troca o marcador pela caixa.

    Marcador sozinho na linha -> a caixa entra no lugar dele.
    Marcador no meio de um parágrafo -> o comentário sai e a caixa entra depois do parágrafo.
    """
    i = txt.find(prefixo)
    if i < 0:
        return None
    fim = txt.find("-->", i)
    fim = len(txt) if fim < 0 else fim + 3
    marcador = txt[i:fim]

    ini_linha = txt.rfind("\n", 0, i) + 1
    fim_linha = txt.find("\n", fim)
    fim_linha = len(txt) if fim_linha < 0 else fim_linha
    so_linha = not txt[ini_linha:i].strip() and not txt[fim:fim_linha].strip()

    caixa_txt = caixa.rstrip("\n")
    if so_linha:
        return txt[:ini_linha] + caixa_txt + txt[fim_linha:]

    sem = txt[:i] + txt[i + len(marcador):]
    desloc = len(marcador)
    para_fim = txt.find("\n\n", fim)
    if para_fim < 0:
        para_fim = len(txt)
    corte = para_fim - desloc
    return sem[:corte].rstrip() + "\n\n" + caixa_txt + "\n" + sem[corte:]


def main() -> None:
    for rel, prefixo, caixa in CAIXAS:
        p = P / rel
        txt = p.read_text(encoding="utf-8")
        novo = inserir_caixa(txt, prefixo, caixa)
        if novo is None:
            print(f"FALHA: marcador nao encontrado em {rel}: {prefixo[:70]}")
            continue
        p.write_text(novo, encoding="utf-8")
        print(f"caixa inserida em {rel}")

    for rel, de, para in SUBSTITUICOES:
        p = P / rel
        txt = p.read_text(encoding="utf-8")
        if de not in txt:
            print(f"FALHA substituicao em {rel}: {de[:60]!r}")
            continue
        p.write_text(txt.replace(de, para), encoding="utf-8")
        print(f"substituicao aplicada em {rel}")

    alvos = (sorted(P.glob("*.qmd")) + sorted(P.glob("episodios/*.qmd"))
             + sorted(P.glob("notas/*.qmd")))
    for p in alvos:
        txt = p.read_text(encoding="utf-8")
        novo = MARCADOR_CONTEXTO.sub("", txt)
        novo = MARCADOR_VERIFICAR.sub("", novo)
        novo = VERIFICAR_INLINE.sub("", novo)
        novo = re.sub(r"\n{3,}", "\n\n", novo)
        novo = re.sub(r"[ \t]+\n", "\n", novo)
        if novo != txt:
            p.write_text(novo, encoding="utf-8")
            print(f"marcadores removidos de {p.relative_to(P)}")


if __name__ == "__main__":
    main()
