"""
Script para criar todas as 47 issues no Linear
Usa a API GraphQL do Linear (equivalente ao MCP)
"""

import os
import sys
import requests
import json
import re
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
if os.path.exists("config/.env"):
    load_dotenv("config/.env")

# Configuração Linear
LINEAR_API_KEY = os.getenv("LINEAR_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else None)
LINEAR_TEAM_ID = os.getenv("LINEAR_TEAM_ID")
LINEAR_API_URL = "https://api.linear.app/graphql"

headers = {
    "Authorization": LINEAR_API_KEY,
    "Content-Type": "application/json"
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
            return teams[0]["id"]
    return None

def get_or_create_label(team_id: str, label_name: str) -> Optional[str]:
    """Obtém ou cria uma label"""
    # Primeiro, tenta obter label existente
    query = """
    query($teamId: String!, $filter: IssueLabelFilter) {
      issueLabels(filter: $filter, teamId: $teamId) {
        nodes {
          id
          name
        }
      }
    }
    """
    
    variables = {
        "teamId": team_id,
        "filter": {"name": {"eq": label_name}}
    }
    
    response = requests.post(
        LINEAR_API_URL,
        json={"query": query, "variables": variables},
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        labels = result.get("data", {}).get("issueLabels", {}).get("nodes", [])
        if labels:
            return labels[0]["id"]
    
    # Cria label se não existir
    mutation = """
    mutation($teamId: String!, $name: String!, $color: String!) {
      issueLabelCreate(
        input: {
          teamId: $teamId
          name: $name
          color: $color
        }
      ) {
        success
        issueLabel {
          id
        }
      }
    }
    """
    
    # Cores padrão para labels
    colors = {
        "critical": "#E5493A",
        "important": "#F2C94C",
        "enhancement": "#5E6AD2",
        "backend": "#0B5FFF",
        "frontend": "#0B5FFF",
        "security": "#E5493A",
        "performance": "#5E6AD2",
        "testing": "#0B5FFF",
        "documentation": "#5E6AD2",
        "infrastructure": "#0B5FFF",
        "ui": "#5E6AD2",
        "api": "#0B5FFF",
        "devops": "#0B5FFF",
        "ci-cd": "#0B5FFF",
        "logging": "#0B5FFF",
        "analytics": "#5E6AD2",
        "backup": "#0B5FFF",
        "validation": "#0B5FFF",
        "refactoring": "#5E6AD2",
        "memory": "#0B5FFF",
        "quality": "#5E6AD2",
        "integration": "#0B5FFF",
        "reliability": "#0B5FFF",
        "real-time": "#0B5FFF",
        "observability": "#0B5FFF",
        "configuration": "#0B5FFF"
    }
    
    color = colors.get(label_name.lower(), "#5E6AD2")
    
    variables = {
        "teamId": team_id,
        "name": label_name,
        "color": color
    }
    
    try:
        response = requests.post(
            LINEAR_API_URL,
            json={"query": mutation, "variables": variables},
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            if result and isinstance(result, dict) and result.get("data", {}).get("issueLabelCreate", {}).get("success"):
                return result["data"]["issueLabelCreate"]["issueLabel"]["id"]
    except Exception as e:
        print(f"  AVISO: Erro ao criar label '{label_name}': {e}")
    
    return None

def create_issue(
    team_id: str,
    title: str,
    description: str,
    priority: str = "medium",
    estimate: Optional[int] = None,
    label_names: List[str] = None
) -> tuple:
    """Cria uma issue no Linear"""
    
    # Mapear prioridade
    priority_map = {
        "urgent": 1,
        "high": 2,
        "medium": 3,
        "low": 4
    }
    priority_num = priority_map.get(priority.lower(), 3)
    
    # Obter IDs das labels
    label_ids = []
    if label_names:
        for label_name in label_names:
            label_id = get_or_create_label(team_id, label_name)
            if label_id:
                label_ids.append(label_id)
    
    mutation = """
    mutation($teamId: String!, $title: String!, $description: String!, $priority: Int!, $labelIds: [String!], $estimate: Int) {
      issueCreate(
        input: {
          teamId: $teamId
          title: $title
          description: $description
          priority: $priority
          labelIds: $labelIds
          estimate: $estimate
        }
      ) {
        success
        issue {
          id
          identifier
          url
          title
        }
      }
    }
    """
    
    variables = {
        "teamId": team_id,
        "title": title,
        "description": description,
        "priority": priority_num,
        "labelIds": label_ids
    }
    
    # Adiciona estimate apenas se fornecido e convertido para int
    if estimate:
        variables["estimate"] = int(estimate)
    
    response = requests.post(
        LINEAR_API_URL,
        json={"query": mutation, "variables": variables},
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("data", {}).get("issueCreate", {}).get("success"):
            issue = result["data"]["issueCreate"]["issue"]
            return issue["id"], issue["identifier"], issue["url"]
        else:
            errors = result.get("errors", [])
            print(f"ERRO: {errors}")
            return None, None, None
    else:
        print(f"ERRO HTTP {response.status_code}: {response.text}")
        return None, None, None

def parse_linear_issues_file(file_path: str = "LINEAR_ISSUES.md") -> List[Dict[str, Any]]:
    """Parseia o arquivo LINEAR_ISSUES.md"""
    issues = []
    
    if not os.path.exists(file_path):
        print(f"ERRO: Arquivo {file_path} nao encontrado")
        return issues
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Divide por seções de issues
    sections = content.split("### L-")
    
    for section in sections[1:]:
        if not section.strip():
            continue
        
        lines = section.split("\n")
        if not lines:
            continue
        
        # Primeira linha: L-XXX: Título
        first_line = lines[0].strip()
        if ":" not in first_line:
            continue
        
        issue_id = first_line.split(":")[0].strip()
        title = first_line.split(":", 1)[1].strip()
        
        issue_data = {
            "id": issue_id,
            "title": title,
            "priority": "medium",
            "labels": [],
            "estimate": None,
            "description": "",
            "files": [],
            "acceptance_criteria": []
        }
        
        current_section = None
        description_lines = []
        
        for line in lines[1:]:
            line = line.strip()
            
            if not line:
                continue
            
            if line.startswith("**Priority:**"):
                priority = line.split("**Priority:**")[1].strip()
                priority_map = {"P0": "urgent", "P1": "high", "P2": "medium", "P3": "low"}
                issue_data["priority"] = priority_map.get(priority, "medium")
            elif line.startswith("**Labels:**"):
                labels_str = line.split("**Labels:**")[1].strip()
                issue_data["labels"] = [l.strip() for l in labels_str.split(",") if l.strip()]
            elif line.startswith("**Estimate:**"):
                estimate_str = line.split("**Estimate:**")[1].strip()
                numbers = re.findall(r'\d+', estimate_str)
                if numbers:
                    issue_data["estimate"] = int(numbers[0])
            elif line.startswith("**Description:**"):
                current_section = "description"
            elif line.startswith("**Files:**"):
                current_section = "files"
            elif line.startswith("**Acceptance Criteria:**"):
                current_section = "acceptance"
            elif line.startswith("---"):
                break
            elif current_section == "description":
                if line and not line.startswith("**"):
                    description_lines.append(line)
            elif current_section == "files":
                if line.startswith("- `"):
                    try:
                        file_path = line.split("`")[1]
                        issue_data["files"].append(file_path)
                    except:
                        pass
            elif current_section == "acceptance":
                if line.startswith("- [ ]"):
                    issue_data["acceptance_criteria"].append(line.replace("- [ ]", "").strip())
        
        issue_data["description"] = "\n".join(description_lines)
        
        # Adiciona files e acceptance criteria à descrição
        if issue_data["files"]:
            issue_data["description"] += "\n\n**Arquivos:**\n" + "\n".join(f"- {f}" for f in issue_data["files"])
        
        if issue_data["acceptance_criteria"]:
            issue_data["description"] += "\n\n**Acceptance Criteria:**\n" + "\n".join(f"- [ ] {ac}" for ac in issue_data["acceptance_criteria"])
        
        if issue_data["title"]:
            issues.append(issue_data)
    
    return issues

def main():
    """Função principal"""
    print("Criando 47 issues no Linear...\n")
    
    if not LINEAR_API_KEY:
        print("ERRO: LINEAR_API_KEY nao configurada")
        print("\nConfigure a API key:")
        print("   1. Obtenha em: https://linear.app/settings/api")
        print("   2. Execute: python scripts/setup_linear.py")
        print("   3. Ou adicione ao .env: LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx")
        return
    
    # Obter team ID
    team_id = LINEAR_TEAM_ID or get_team_id()
    if not team_id:
        print("ERRO: Nao foi possivel obter o Team ID")
        return
    
    print(f"OK: Usando Team ID: {team_id}\n")
    
    # Parsear issues
    print("Lendo arquivo LINEAR_ISSUES.md...")
    issues = parse_linear_issues_file("LINEAR_ISSUES.md")
    
    # Se não encontrou todas, tenta o arquivo completo
    if len(issues) < 23:
        print(f"AVISO: Apenas {len(issues)} issues encontradas em LINEAR_ISSUES.md")
        print("Tentando LINEAR_ISSUES_COMPLETE.md...")
        issues_complete = parse_linear_issues_file("LINEAR_ISSUES_COMPLETE.md")
        if issues_complete:
            issues = issues_complete
    
    print(f"OK: {len(issues)} issues encontradas\n")
    
    # Criar issues
    print("Criando issues no Linear...\n")
    created = []
    failed = []
    
    for i, issue in enumerate(issues, 1):
        print(f"[{i}/{len(issues)}] Criando {issue['id']}: {issue['title']}...")
        
        issue_id, identifier, url = create_issue(
            team_id=team_id,
            title=f"{issue['id']}: {issue['title']}",
            description=issue["description"],
            priority=issue["priority"],
            estimate=issue["estimate"],
            label_names=issue["labels"]
        )
        
        if issue_id:
            created.append({
                "id": issue["id"],
                "linear_id": identifier,
                "url": url,
                "title": issue["title"]
            })
            print(f"  OK: Criada: {identifier} - {url}")
        else:
            failed.append(issue["id"])
            print(f"  ERRO: Falhou")
        
        print()
    
    # Resumo
    print("=" * 60)
    print(f"OK: {len(created)} issues criadas com sucesso")
    if failed:
        print(f"ERRO: {len(failed)} issues falharam: {', '.join(failed)}")
    print("=" * 60)
    
    # Salvar resultado
    with open("linear_issues_created.json", "w", encoding="utf-8") as f:
        json.dump(created, f, indent=2, ensure_ascii=False)
    
    print(f"\nResultado salvo em: linear_issues_created.json")

if __name__ == "__main__":
    main()

