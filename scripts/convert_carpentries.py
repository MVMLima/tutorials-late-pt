#!/usr/bin/env python3
"""
Converte os episódios do Carpentries Workbench (sandpaper) do curso
"Scenario modelling for outbreak analytics with R" (Epiverse-TRACE tutorials-late)
para o formato Quarto usado no site PT-BR.

Uso: python3 scripts/convert_carpentries.py <entrada> <saida> [episodios|raiz]

Obs.: as reescritas de caminho usam `str.replace` com strings literais de propósito.
Regex escrita à mão aqui já quebrou uma vez por dobra de barras invertidas.
"""
import re
import sys

BLOCKS = {
    "questions":   ("note",      "Perguntas",           False),
    "objectives":  ("tip",       "Objetivos",           False),
    "prereq":      ("important", "Pré-requisitos",      False),
    "spoiler":     ("note",      "Detalhes",            True),
    "callout":     ("note",      None,                  False),
    "challenge":   ("tip",       "Desafio",             False),
    "hint":        ("note",      "Dica",                True),
    "solution":    ("note",      "Solução",             True),
    "checklist":   ("note",      "Checklist",           False),
    "caution":     ("warning",   "Atenção",             False),
    "discussion":  ("note",      "Discussão",           False),
    "keypoints":   ("note",      "Pontos-chave",        False),
    "instructor":  ("important", "Para o instrutor",    True),
    "checkpoint":  ("note",      "Checagem",            False),
    "testimonial": ("note",      "Para se aprofundar",  False),
    "tab":         ("panel-tabset", None,               False),
}

OPEN = re.compile("^(:{3,})[ \t]*([A-Za-z][A-Za-z0-9_-]*)[ \t]*$")
CLOSE = re.compile("^:{3,}[ \t]*$")

# slug original -> nome do arquivo no site PT-BR
EPISODIOS = {
    "contact-matrices":         "01-matrizes-de-contato",
    "simulating-transmission":  "02-simular-transmissao",
    "model-choices":            "03-escolher-modelo",
    "modelling-interventions":  "04-modelar-intervencoes",
    "compare-interventions":    "05-comparar-intervencoes",
    "vaccine-comparisons":      "06-comparar-vacinacao",
    "disease-burden":           "07-carga-de-doenca",
    "template":                 "template",
}

# Episódio opcional que NÃO entra no site (decisão do usuário em 20/09/2026):
# o único link para ele passa a apontar para a página publicada no site original.
FORA_DO_SITE = {
    "contact-normalization":
        "https://epiverse-trace.github.io/tutorials-late/learners/contact-normalization.html",
}

# Reescritas literais (texto que aparece -> texto novo). Sem regex à mão.
REWRITES = [
    ("(../learners/setup.md", "(../setup.qmd"),
    ("(../learners/reference.md", "(../glossario.qmd"),
    ("(./reference.md", "(glossario.qmd"),
    ("(reference.md", "(glossario.qmd"),
    ("(../profiles/learner-profiles.md)", "(../perfis.qmd)"),
    ("(profiles/learner-profiles.md)", "(perfis.qmd)"),
    ("(../instructors/instructor-notes.md)", "(../instrutor.qmd)"),
]
for slug, novo in EPISODIOS.items():
    REWRITES.append((f"(../episodes/{slug}.md", f"({novo}.qmd"))
for slug, url in FORA_DO_SITE.items():
    REWRITES.append((f"(../learners/{slug}.md)", f"({url})"))

# Caminhos de dados e imagens (também literais).
DL_ORIG = "https://epiverse-trace.github.io/tutorials-late/data/"
IMG_PREFIXOS = ["](../episodes/fig/", "](episodes/fig/", "](../learners/fig/",
                "](learners/fig/", "](../fig/", "](fig/", "](../img/"]
DATA_PREFIXOS = ["](../episodes/data/", "](episodes/data/", "](../data/", "](data/"]


def convert(text: str, destino: str) -> str:
    pref = "../" if destino in ("episodios", "notas") else ""
    out, stack, in_code = [], [], False

    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue

        m = OPEN.match(line)
        if m:
            cls = m.group(2).lower()
            if cls in BLOCKS:
                kind, title, collapse = BLOCKS[cls]
                if kind == "panel-tabset":
                    out.append("::: {.panel-tabset}")
                    stack.append("tab")
                else:
                    attrs = f".callout-{kind}"
                    if cls == "challenge":
                        attrs += " .desafio"
                    if cls == "solution":
                        attrs += " .solucao"
                    opts = f' title="{title}"' if title else ""
                    if collapse:
                        opts += ' collapse="true"'
                    out.append(f"::: {{{attrs}{opts}}}")
                    stack.append(cls)
                continue
            out.append(f"::: {{.{cls}}}")
            stack.append(cls)
            continue

        if CLOSE.match(line):
            if stack:
                stack.pop()
                out.append(":::")
            continue

        if stack and stack[-1] == "tab" and re.match(r"^#{3,4} ", line):
            line = line[1:]
        line = line.replace(DL_ORIG, f"{pref}data/")
        for pat, rep in REWRITES:
            line = line.replace(pat, rep)
        for p in IMG_PREFIXOS:
            if p.startswith("]("):
                line = line.replace(p, f"]({pref}img/")
        for p in DATA_PREFIXOS:
            if p.startswith("]("):
                line = line.replace(p, f"]({pref}data/")
        out.append(line)

    return "\n".join(out)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    tipo = sys.argv[3] if len(sys.argv) > 3 else "raiz"
    text = open(src, encoding="utf-8").read()
    res = convert(text, tipo)
    open(dst, "w", encoding="utf-8").write(res)
    print(f"[{tipo}] {src} -> {dst}: {len(text.splitlines())} -> {len(res.splitlines())} linhas")
    for name, (kind, title, _) in BLOCKS.items():
        a = len(re.findall("^:{3,}[ \\t]*" + name + "[ \\t]*$", text, re.M))
        needle = f'title="{title}"' if title else "{.callout-" + kind
        b = res.count(needle)
        if a and b < a:
            print(f"    ATENCAO: {a} blocos '{name}', {b} convertidos")
    sobras = [l for l in res.split("\n") if l.startswith(":::") and not l.startswith("::::")]
    if sobras:
        print(f"    {len(sobras)} linhas ':::' (fechamentos de callout)")


if __name__ == "__main__":
    main()
