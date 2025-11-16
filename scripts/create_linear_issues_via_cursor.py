"""
Script para criar issues no Linear usando a integração do Cursor
Este script prepara as issues para serem criadas via Cursor MCP ou API
"""

import json
import re
from typing import Dict, List, Any

def parse_linear_issues_file(file_path: str = "LINEAR_ISSUES.md") -> List[Dict[str, Any]]:
    """Parseia o arquivo LINEAR_ISSUES.md e extrai as issues em formato para Linear"""
    issues = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Divide por seções de issues
    sections = content.split("### L-")
    
    for section in sections[1:]:  # Pula o header
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
                # Mapear P0, P1, P2 para prioridades do Linear
                priority_map = {
                    "P0": "urgent",
                    "P1": "high", 
                    "P2": "medium",
                    "P3": "low"
                }
                issue_data["priority"] = priority_map.get(priority, "medium")
            elif line.startswith("**Status:**"):
                # Linear usa estados diferentes, mas vamos manter
                pass
            elif line.startswith("**Labels:**"):
                labels_str = line.split("**Labels:**")[1].strip()
                issue_data["labels"] = [l.strip() for l in labels_str.split(",") if l.strip()]
            elif line.startswith("**Estimate:**"):
                estimate_str = line.split("**Estimate:**")[1].strip()
                # Extrai número de dias
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

def format_issue_for_linear(issue: Dict[str, Any]) -> str:
    """Formata uma issue para ser criada no Linear via chat do Cursor"""
    priority_emoji = {
        "urgent": "🔴",
        "high": "🟡",
        "medium": "🟢",
        "low": "⚪"
    }
    
    emoji = priority_emoji.get(issue["priority"], "🟢")
    
    formatted = f"""
{emoji} **{issue['id']}: {issue['title']}**

**Prioridade:** {issue['priority'].upper()}
**Labels:** {', '.join(issue['labels']) if issue['labels'] else 'Nenhuma'}
**Estimativa:** {issue['estimate']} dias (se aplicável)

**Descrição:**
{issue['description']}
"""
    return formatted.strip()

def main():
    """Gera instruções para criar issues no Linear via Cursor"""
    print("📋 Preparando issues para Linear via Cursor...\n")
    
    issues = parse_linear_issues_file()
    print(f"✅ {len(issues)} issues parseadas\n")
    
    # Agrupar por prioridade
    by_priority = {
        "urgent": [],
        "high": [],
        "medium": [],
        "low": []
    }
    
    for issue in issues:
        priority = issue.get("priority", "medium")
        by_priority[priority].append(issue)
    
    # Gerar instruções
    instructions = []
    instructions.append("# 📋 Instruções para Criar Issues no Linear via Cursor\n")
    instructions.append("Como você já conectou sua conta do Cursor ao Linear, você pode criar as issues diretamente no chat do Cursor.\n")
    instructions.append("## 🚀 Método 1: Criar Issues Individualmente\n")
    instructions.append("Para cada issue, use este comando no chat do Cursor:\n")
    instructions.append("```\n")
    instructions.append("Crie uma issue no Linear com:\n")
    instructions.append("- Título: [TÍTULO]\n")
    instructions.append("- Prioridade: [PRIORIDADE]\n")
    instructions.append("- Descrição: [DESCRIÇÃO]\n")
    instructions.append("- Labels: [LABELS]\n")
    instructions.append("```\n\n")
    
    instructions.append("## 📝 Issues para Criar\n\n")
    
    # P0 - Urgent
    if by_priority["urgent"]:
        instructions.append("### 🔴 P0 - Crítico (Urgent)\n\n")
        for issue in by_priority["urgent"]:
            instructions.append(format_issue_for_linear(issue))
            instructions.append("\n\n---\n\n")
    
    # P1 - High
    if by_priority["high"]:
        instructions.append("### 🟡 P1 - Importante (High)\n\n")
        for issue in by_priority["high"]:
            instructions.append(format_issue_for_linear(issue))
            instructions.append("\n\n---\n\n")
    
    # P2 - Medium
    if by_priority["medium"]:
        instructions.append("### 🟢 P2 - Melhorias (Medium)\n\n")
        for issue in by_priority["medium"]:
            instructions.append(format_issue_for_linear(issue))
            instructions.append("\n\n---\n\n")
    
    # Salvar instruções
    output = "".join(instructions)
    
    with open("INSTRUCOES_CURSOR_LINEAR.md", "w", encoding="utf-8") as f:
        f.write(output)
    
    print("✅ Instruções salvas em: INSTRUCOES_CURSOR_LINEAR.md")
    print("\n📋 Próximos passos:")
    print("   1. Reinicie o Cursor para carregar o MCP do Linear")
    print("   2. Use o arquivo INSTRUCOES_CURSOR_LINEAR.md como referência")
    print("   3. Ou peça ao Cursor: 'Crie todas as issues do arquivo LINEAR_ISSUES.md no Linear'")

if __name__ == "__main__":
    main()

