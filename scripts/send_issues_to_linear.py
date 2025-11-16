"""
Script para enviar issues para o Linear usando a API GraphQL
"""

import os
import sys
import requests
import json
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
if os.path.exists("config/.env"):
    load_dotenv("config/.env")

# Configuração Linear (pode ser passada via argumento ou .env)
LINEAR_API_KEY = os.getenv("LINEAR_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else None)
LINEAR_TEAM_ID = os.getenv("LINEAR_TEAM_ID")  # ID do time no Linear
LINEAR_PROJECT_ID = os.getenv("LINEAR_PROJECT_ID", None)  # Opcional: ID do projeto

# URL da API Linear
LINEAR_API_URL = "https://api.linear.app/graphql"

# Headers
headers = {
    "Authorization": LINEAR_API_KEY,
    "Content-Type": "application/json",
}

def get_team_id():
    """Obtém o ID do time padrão se não estiver configurado"""
    if LINEAR_TEAM_ID:
        return LINEAR_TEAM_ID
    
    query = """
    query {
      teams {
        nodes {
          id
          name
          key
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
        data = response.json()
        teams = data.get("data", {}).get("teams", {}).get("nodes", [])
        if teams:
            print(f"Times disponíveis:")
            for team in teams:
                print(f"  - {team['name']} ({team['key']}): {team['id']}")
            return teams[0]["id"]
    
    return None

def get_or_create_labels(team_id: str) -> Dict[str, str]:
    """Obtém ou cria labels necessárias"""
    labels_map = {}
    
    # Labels necessárias
    required_labels = [
        "backend", "frontend", "infrastructure", "observability",
        "performance", "security", "critical", "important", "enhancement",
        "testing", "documentation", "api", "memory", "real-time",
        "integration", "refactoring", "docker", "ui", "logging",
        "ci-cd", "configuration", "validation", "analytics", "backup"
    ]
    
    # Query para listar labels existentes
    query = """
    query($teamId: String!) {
      issueLabels(filter: { team: { id: { eq: $teamId } } }) {
        nodes {
          id
          name
        }
      }
    }
    """
    
    response = requests.post(
        LINEAR_API_URL,
        json={"query": query, "variables": {"teamId": team_id}},
        headers=headers
    )
    
    existing_labels = {}
    if response.status_code == 200:
        data = response.json()
        labels = data.get("data", {}).get("issueLabels", {}).get("nodes", [])
        existing_labels = {label["name"]: label["id"] for label in labels}
    
    # Criar labels que não existem
    for label_name in required_labels:
        if label_name in existing_labels:
            labels_map[label_name] = existing_labels[label_name]
        else:
            # Criar label
            create_query = """
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
                  name
                }
              }
            }
            """
            
            # Cores por categoria
            colors = {
                "backend": "#3B82F6",
                "frontend": "#8B5CF6",
                "infrastructure": "#10B981",
                "observability": "#F59E0B",
                "performance": "#EF4444",
                "security": "#DC2626",
                "critical": "#DC2626",
                "important": "#F59E0B",
                "enhancement": "#10B981",
            }
            
            color = colors.get(label_name, "#6B7280")
            
            create_response = requests.post(
                LINEAR_API_URL,
                json={
                    "query": create_query,
                    "variables": {
                        "teamId": team_id,
                        "name": label_name,
                        "color": color
                    }
                },
                headers=headers
            )
            
            if create_response.status_code == 200:
                result = create_response.json()
                if result.get("data", {}).get("issueLabelCreate", {}).get("success"):
                    label_id = result["data"]["issueLabelCreate"]["issueLabel"]["id"]
                    labels_map[label_name] = label_id
                    print(f"✅ Label criada: {label_name}")
    
    return labels_map

def create_issue(
    team_id: str,
    title: str,
    description: str,
    priority: str,
    estimate: int = None,
    labels: List[str] = None,
    project_id: str = None
) -> str:
    """Cria uma issue no Linear"""
    
    # Mapear prioridade
    priority_map = {
        "P0": "urgent",
        "P1": "high",
        "P2": "medium",
        "P3": "low"
    }
    
    linear_priority = priority_map.get(priority, "medium")
    
    # Construir mutation
    mutation = """
    mutation($teamId: String!, $title: String!, $description: String!, $priority: Int!, $labelIds: [String!], $projectId: String, $estimate: Float) {
      issueCreate(
        input: {
          teamId: $teamId
          title: $title
          description: $description
          priority: $priority
          labelIds: $labelIds
          projectId: $projectId
          estimate: $estimate
        }
      ) {
        success
        issue {
          id
          identifier
          title
          url
        }
      }
    }
    """
    
    # Prioridade numérica
    priority_num = {"urgent": 1, "high": 2, "medium": 3, "low": 4}.get(linear_priority, 3)
    
    variables = {
        "teamId": team_id,
        "title": title,
        "description": description,
        "priority": priority_num,
        "labelIds": labels or [],
        "estimate": estimate
    }
    
    if project_id:
        variables["projectId"] = project_id
    
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
            print(f"❌ Erro ao criar issue: {errors}")
            return None, None, None
    else:
        print(f"❌ Erro HTTP {response.status_code}: {response.text}")
        return None, None, None

def parse_linear_issues_file(file_path: str = "LINEAR_ISSUES.md") -> List[Dict[str, Any]]:
    """Parseia o arquivo LINEAR_ISSUES.md e extrai as issues"""
    issues = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Divide por seções de issues
    sections = content.split("### L-")
    
    for section in sections[1:]:  # Pula o header
        if not section.strip():
            continue
        
        lines = section.split("\n")
        issue_id = lines[0].split(":")[0].strip()
        title = lines[0].split(":", 1)[1].strip() if ":" in lines[0] else ""
        
        issue_data = {
            "id": issue_id,
            "title": title,
            "priority": None,
            "status": "Todo",
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
            
            if line.startswith("**Priority:**"):
                issue_data["priority"] = line.split("**Priority:**")[1].strip()
            elif line.startswith("**Status:**"):
                issue_data["status"] = line.split("**Status:**")[1].strip()
            elif line.startswith("**Labels:**"):
                labels_str = line.split("**Labels:**")[1].strip()
                issue_data["labels"] = [l.strip() for l in labels_str.split(",")]
            elif line.startswith("**Estimate:**"):
                estimate_str = line.split("**Estimate:**")[1].strip()
                # Extrai número de dias
                if "day" in estimate_str.lower():
                    try:
                        days = int(estimate_str.split()[0])
                        issue_data["estimate"] = days  # Em pontos (1 dia = 1 ponto)
                    except:
                        pass
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
                    file_path = line.split("`")[1]
                    issue_data["files"].append(file_path)
            elif current_section == "acceptance":
                if line.startswith("- [ ]"):
                    issue_data["acceptance_criteria"].append(line.replace("- [ ]", "").strip())
        
        issue_data["description"] = "\n".join(description_lines)
        
        # Adiciona files e acceptance criteria à descrição
        if issue_data["files"]:
            issue_data["description"] += "\n\n**Arquivos:**\n" + "\n".join(f"- {f}" for f in issue_data["files"])
        
        if issue_data["acceptance_criteria"]:
            issue_data["description"] += "\n\n**Acceptance Criteria:**\n" + "\n".join(f"- [ ] {ac}" for ac in issue_data["acceptance_criteria"])
        
        issues.append(issue_data)
    
    return issues

def main():
    """Função principal"""
    print("🚀 Enviando issues para o Linear...\n")
    
    # Verificar API key
    if not LINEAR_API_KEY:
        print("❌ LINEAR_API_KEY não configurada")
        print("\n📋 Opções:")
        print("   1. Configure no .env:")
        print("      LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx")
        print("\n   2. Execute o script de setup:")
        print("      python scripts/setup_linear.py")
        print("\n   3. Passe como argumento:")
        print("      python scripts/send_issues_to_linear.py lin_api_xxxxxxxxxxxxx")
        print("\n   Obtenha sua API key em: https://linear.app/settings/api")
        return
    
    # Obter team ID
    team_id = LINEAR_TEAM_ID or get_team_id()
    if not team_id:
        print("❌ Não foi possível obter o Team ID")
        print("   Configure LINEAR_TEAM_ID no .env ou certifique-se de ter acesso a um time")
        return
    
    print(f"✅ Usando Team ID: {team_id}\n")
    
    # Obter/criar labels
    print("📋 Obtendo/criando labels...")
    labels_map = get_or_create_labels(team_id)
    print(f"✅ {len(labels_map)} labels disponíveis\n")
    
    # Parsear issues
    print("📖 Lendo arquivo LINEAR_ISSUES.md...")
    issues = parse_linear_issues_file()
    print(f"✅ {len(issues)} issues encontradas\n")
    
    # Criar issues
    print("📝 Criando issues no Linear...\n")
    created = []
    failed = []
    
    for issue in issues:
        print(f"Criando {issue['id']}: {issue['title']}...")
        
        # Mapear labels
        label_ids = [labels_map[label] for label in issue["labels"] if label in labels_map]
        
        # Criar issue
        issue_id, identifier, url = create_issue(
            team_id=team_id,
            title=f"{issue['id']}: {issue['title']}",
            description=issue["description"],
            priority=issue["priority"],
            estimate=issue["estimate"],
            labels=label_ids,
            project_id=LINEAR_PROJECT_ID
        )
        
        if issue_id:
            created.append({
                "id": issue["id"],
                "linear_id": identifier,
                "url": url,
                "title": issue["title"]
            })
            print(f"  ✅ Criada: {identifier} - {url}")
        else:
            failed.append(issue["id"])
            print(f"  ❌ Falhou")
        
        print()
    
    # Resumo
    print("=" * 60)
    print(f"✅ {len(created)} issues criadas com sucesso")
    if failed:
        print(f"❌ {len(failed)} issues falharam: {', '.join(failed)}")
    print("=" * 60)
    
    # Salvar resultado
    with open("linear_issues_created.json", "w", encoding="utf-8") as f:
        json.dump(created, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Resultado salvo em: linear_issues_created.json")

if __name__ == "__main__":
    main()

