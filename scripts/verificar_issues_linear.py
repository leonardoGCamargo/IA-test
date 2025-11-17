"""
Script para verificar e listar as issues criadas no Linear
"""

import os
import sys
import requests
import json
from typing import Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
if os.path.exists("config/.env"):
    load_dotenv("config/.env")

# Configuração Linear
LINEAR_API_KEY = sys.argv[1] if len(sys.argv) > 1 else os.getenv("LINEAR_API_KEY")
LINEAR_TEAM_ID = os.getenv("LINEAR_TEAM_ID")
LINEAR_API_URL = "https://api.linear.app/graphql"

headers = {
    "Authorization": LINEAR_API_KEY,
    "Content-Type": "application/json",
} if LINEAR_API_KEY else {}

def get_team_id() -> Optional[str]:
    """Obtém o primeiro team ID disponível"""
    query = """
    query {
      teams {
        nodes {
          id
          key
          name
        }
      }
    }
    """
    
    response = requests.post(
        LINEAR_API_URL,
        json={"query": query},
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        teams = result.get("data", {}).get("teams", {}).get("nodes", [])
        if teams:
            print(f"\nTimes disponíveis:")
            for team in teams:
                print(f"  - {team['name']} ({team['key']}): {team['id']}")
            return teams[0]["id"]
    return None

def list_issues(team_id: str, limit: int = 100):
    """Lista todas as issues do time"""
    query = """
    query($teamId: String!, $first: Int!) {
      team(id: $teamId) {
        issues(first: $first) {
          nodes {
            id
            identifier
            title
            url
            priority
            state {
              name
            }
            assignee {
              name
              email
            }
            createdAt
          }
        }
      }
    }
    """
    
    variables = {
        "teamId": team_id,
        "first": limit
    }
    
    response = requests.post(
        LINEAR_API_URL,
        json={"query": query, "variables": variables},
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("data", {}).get("team"):
            issues = result["data"]["team"]["issues"]["nodes"]
            return issues
    return []

def main():
    """Função principal"""
    print("Verificando issues no Linear...\n")
    
    if not LINEAR_API_KEY:
        print("ERRO: LINEAR_API_KEY nao configurada")
        print("\nUse: python scripts/verificar_issues_linear.py lin_api_xxxxxxxxxxxxx")
        return
    
    # Obter team ID
    team_id = LINEAR_TEAM_ID or get_team_id()
    if not team_id:
        print("ERRO: Nao foi possivel obter o Team ID")
        return
    
    print(f"\nBuscando issues no time...")
    issues = list_issues(team_id, limit=100)
    
    if not issues:
        print("\nNenhuma issue encontrada!")
        return
    
    print(f"\n{'='*80}")
    print(f"Total de issues encontradas: {len(issues)}")
    print(f"{'='*80}\n")
    
    # Agrupar por prioridade
    by_priority = {
        "urgent": [],
        "high": [],
        "medium": [],
        "low": [],
        "none": []
    }
    
    for issue in issues:
        priority = issue.get("priority", 0)
        if priority == 1:
            by_priority["urgent"].append(issue)
        elif priority == 2:
            by_priority["high"].append(issue)
        elif priority == 3:
            by_priority["medium"].append(issue)
        elif priority == 4:
            by_priority["low"].append(issue)
        else:
            by_priority["none"].append(issue)
    
    # Exibir por prioridade
    priority_names = {
        "urgent": "P0 - Urgent",
        "high": "P1 - High",
        "medium": "P2 - Medium",
        "low": "Low",
        "none": "Sem Prioridade"
    }
    
    for priority, name in priority_names.items():
        if by_priority[priority]:
            print(f"\n{name} ({len(by_priority[priority])} issues):")
            print("-" * 80)
            for issue in sorted(by_priority[priority], key=lambda x: x.get("identifier", "")):
                assignee = issue.get("assignee")
                assignee_name = assignee["name"] if assignee else "Não atribuída"
                state = issue.get("state", {}).get("name", "Unknown")
                print(f"  {issue['identifier']}: {issue['title']}")
                print(f"    Estado: {state} | Atribuída a: {assignee_name}")
                print(f"    URL: {issue['url']}")
                print()
    
    # Verificar issues esperadas
    print(f"\n{'='*80}")
    print("Verificando issues esperadas (MY-5 a MY-52)...")
    print(f"{'='*80}\n")
    
    expected_ids = [f"MY-{i}" for i in range(5, 53)]
    found_ids = [issue["identifier"] for issue in issues]
    
    missing = [id for id in expected_ids if id not in found_ids]
    found = [id for id in expected_ids if id in found_ids]
    
    print(f"OK: Issues encontradas: {len(found)}/{len(expected_ids)}")
    if found:
        print(f"   IDs: {', '.join(found[:10])}{'...' if len(found) > 10 else ''}")
    
    if missing:
        print(f"\nAVISO: Issues nao encontradas: {len(missing)}")
        print(f"   IDs: {', '.join(missing[:10])}{'...' if len(missing) > 10 else ''}")
    
    # Salvar resultado
    with open("linear_issues_verificadas.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)
    
    print(f"\nOK: Resultado salvo em: linear_issues_verificadas.json")

if __name__ == "__main__":
    main()

