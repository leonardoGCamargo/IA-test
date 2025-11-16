"""
Testes E2E do Dashboard usando Playwright.

Execute com: pytest tests/test_dashboard_e2e.py
"""

import pytest
from playwright.sync_api import Page, expect, sync_playwright
import time
import subprocess
import sys
from pathlib import Path

# Configuração
DASHBOARD_URL = "http://localhost:8508"
DASHBOARD_TIMEOUT = 30  # segundos para aguardar dashboard iniciar


@pytest.fixture(scope="module")
def dashboard_process():
    """Inicia o dashboard em background."""
    project_root = Path(__file__).parent.parent
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", 
         "src/apps/agent_dashboard.py", 
         "--server.port=8508",
         "--server.headless=true"],
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Aguarda dashboard iniciar
    import requests
    for _ in range(DASHBOARD_TIMEOUT):
        try:
            response = requests.get(DASHBOARD_URL, timeout=2)
            if response.status_code == 200:
                break
        except:
            time.sleep(1)
    else:
        pytest.fail("Dashboard não iniciou a tempo")
    
    yield process
    
    # Encerra o processo
    process.terminate()
    process.wait()


@pytest.fixture(scope="module")
def browser():
    """Inicializa o navegador Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser, dashboard_process):
    """Cria uma nova página para cada teste."""
    page = browser.new_page()
    page.goto(DASHBOARD_URL)
    yield page
    page.close()


def test_dashboard_loads(page: Page):
    """Testa se o dashboard carrega corretamente."""
    expect(page).to_have_title("IA-Test Dashboard")
    
    # Verifica se o header principal está presente
    expect(page.locator("text=IA-Test Dashboard")).to_be_visible()


def test_navigation_sidebar(page: Page):
    """Testa a navegação na sidebar."""
    # Verifica se a sidebar está visível
    sidebar = page.locator('[data-testid="stSidebar"]')
    expect(sidebar).to_be_visible()
    
    # Verifica se os itens de menu estão presentes
    expect(page.locator("text=Visão Geral")).to_be_visible()
    expect(page.locator("text=Agentes")).to_be_visible()
    expect(page.locator("text=Chat")).to_be_visible()


def test_overview_page(page: Page):
    """Testa a página de visão geral."""
    # Navega para visão geral (já deve estar por padrão)
    expect(page.locator("text=Visão Geral do Sistema")).to_be_visible()
    
    # Verifica métricas
    expect(page.locator("text=Total de Agentes")).to_be_visible()
    expect(page.locator("text=Agentes Ativos")).to_be_visible()


def test_agents_list(page: Page):
    """Testa a lista de agentes."""
    # Clica em "Agentes"
    page.click("text=Agentes")
    
    # Verifica se a lista de agentes aparece
    expect(page.locator("text=Lista de Agentes")).to_be_visible()
    
    # Verifica se alguns agentes estão listados
    expect(page.locator("text=Orchestrator")).to_be_visible()
    expect(page.locator("text=System Health Agent")).to_be_visible()


def test_diagnostics_page(page: Page):
    """Testa a página de diagnóstico."""
    # Clica em "Diagnóstico"
    page.click("text=Diagnóstico")
    
    # Verifica se a página de diagnóstico carrega
    expect(page.locator("text=Diagnóstico de Problemas")).to_be_visible()
    
    # Verifica se o botão de executar diagnóstico está presente
    expect(page.locator("text=Executar Diagnóstico Completo")).to_be_visible()


def test_chat_interface(page: Page):
    """Testa a interface de chat."""
    # Clica em "Chat"
    page.click("text=Chat")
    
    # Verifica se a interface de chat carrega
    expect(page.locator("text=Chat com Agentes")).to_be_visible()
    
    # Verifica se o seletor de agente está presente
    expect(page.locator("text=Selecione um agente")).to_be_visible()


def test_monitoring_page(page: Page):
    """Testa a página de monitoramento."""
    # Clica em "Monitoramento"
    page.click("text=Monitoramento")
    
    # Verifica se a página de monitoramento carrega
    expect(page.locator("text=Monitoramento")).to_be_visible()
    
    # Verifica se as métricas estão presentes
    expect(page.locator("text=Status dos Agentes")).to_be_visible()


def test_settings_page(page: Page):
    """Testa a página de configurações."""
    # Clica em "Configurações"
    page.click("text=Configurações")
    
    # Verifica se a página de configurações carrega
    expect(page.locator("text=Configurações")).to_be_visible()
    
    # Verifica se as seções estão presentes
    expect(page.locator("text=Variáveis de Ambiente")).to_be_visible()


def test_chat_message_send(page: Page):
    """Testa o envio de mensagem no chat."""
    # Navega para o chat
    page.click("text=Chat")
    
    # Aguarda o chat carregar
    expect(page.locator("text=Chat com Agentes")).to_be_visible()
    
    # Tenta enviar uma mensagem (se o input estiver disponível)
    chat_input = page.locator('input[placeholder*="mensagem"]')
    if chat_input.is_visible():
        chat_input.fill("teste")
        chat_input.press("Enter")
        
        # Aguarda um pouco para a resposta aparecer
        time.sleep(2)
        
        # Verifica se a mensagem foi adicionada ao histórico
        # (pode não ter resposta se o orchestrator não estiver configurado)
        expect(page.locator("text=teste")).to_be_visible()


def test_resolutions_page(page: Page):
    """Testa a página de resoluções."""
    # Clica em "Resoluções"
    page.click("text=Resoluções")
    
    # Verifica se a página de resoluções carrega
    expect(page.locator("text=Resoluções Sugeridas")).to_be_visible()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

