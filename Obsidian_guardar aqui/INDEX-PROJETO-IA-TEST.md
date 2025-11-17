---
tags:
  - projeto
  - ia-test
  - indice
---

# Índice Principal – Projeto IA-TEST

Esta nota é o ponto de entrada para entender o projeto IA-TEST, sua arquitetura, fluxos e infraestrutura.

## Visão geral

- **Arquitetura geral do sistema**: [[ARQUITETURA-GERAL-IA-TEST]]
- **Serviços Docker, portas e URLs**: [[INFRA-SERVICOS-PORTAS]]
- **Usuários e senhas (nota privada)**: [[SENHAS-SERVICOS-PRIVADO]]
- **Agentes e LLMs usados**: [[AGENTES-E-LLMS]]
- **Organização de notas e NotebookLM**: [[RESUMO-ORGANIZACAO-OBSIDIAN]] e pasta `NotebookLM/`

## Fluxo rápido de uso

1. **Subir infraestrutura principal** (Neo4j, API, front, dashboard):
2. **Subir ferramentas** (Kestra, MCP manager, N8N, etc.).
3. **Criar e monitorar workflows de orquestração** no Kestra e no N8N.
4. **Explorar e melhorar agentes / chains** usando os dashboards e as notas técnicas.

Detalhes de cada etapa estão em: [[ARQUITETURA-GERAL-IA-TEST]].








