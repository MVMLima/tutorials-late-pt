#!/usr/bin/env Rscript
# Instala os pacotes do curso "Scenario modelling for outbreak analytics with R"
# (Epiverse-TRACE tutorials-late) numa biblioteca LOCAL do projeto (.Rlib).
#
# Repos:
#  - CRAN via Posit Package Manager (binários para Ubuntu noble)
#  - epiverse-trace.r-universe.dev (epidemics NÃO está no CRAN; tem binário noble)
#  - PPgp/wpp2024 via GitHub (não está no CRAN nem no r-universe do Epiverse)
P <- "/home/marc/Documentos/Projetos/tutorials-late-pt"
lib <- file.path(P, ".Rlib")
dir.create(lib, showWarnings = FALSE)

options(
  repos = c(
    CRAN = "https://packagemanager.posit.co/cran/__linux__/noble/latest",
    epiverse = "https://epiverse-trace.r-universe.dev"
  ),
  HTTPUserAgent = sprintf(
    "R/%s R (%s)", getRversion(),
    paste(getRversion(), R.version$platform, R.version$arch, R.version$os)
  ),
  Ncpus = max(1, parallel::detectCores() - 2)
)
cat("R:", R.version.string, "\nlib:", lib, "\nNcpus:", getOption("Ncpus"), "\n\n")

pkgs <- c(
  # núcleo do curso
  "epidemics", "contactsurveys", "socialmixr", "epiparameter", "finalsize",
  # manipulação e gráficos
  "tidyverse", "dplyr", "ggplot2", "purrr", "scales", "knitr",
  # utilidades usadas nas páginas de apoio
  "here", "pak", "remotes"
)

cat("=== instalar.packages ===\n")
install.packages(pkgs, lib = lib, dependencies = TRUE, quiet = FALSE)

cat("\n=== wpp2024 (GitHub PPgp/wpp2024) ===\n")
tryCatch(
  remotes::install_github("PPgp/wpp2024", lib = lib, upgrade = "never", quiet = FALSE),
  error = function(e) cat("ERRO wpp2024:", conditionMessage(e), "\n")
)

cat("\n=== conferência ===\n")
alvo <- c(pkgs, "wpp2024")
inst <- rownames(installed.packages(lib.loc = lib))
faltando <- alvo[!alvo %in% inst]
cat("instalados:", length(inst), "pacotes em .Rlib\n")
cat("FALTANDO:", if (length(faltando)) paste(faltando, collapse = ", ") else "nenhum", "\n")

suppressWarnings(suppressMessages({
  ok <- c("epidemics", "contactsurveys", "socialmixr", "wpp2024", "epiparameter")
  for (p in ok) cat(sprintf("  %-16s %s\n", p, requireNamespace(p, lib.loc = lib, quietly = TRUE)))
}))
