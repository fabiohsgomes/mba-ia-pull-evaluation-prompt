"""
Testes automatizados para validação de prompts.
"""
import pytest
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import load_yaml, validate_prompt_structure

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"
MISSING_SYSTEM_PROMPT_ERROR = "Campo obrigatório faltando: system_prompt"
EMPTY_SYSTEM_PROMPT_ERROR = "system_prompt está vazio"
TODO_ERROR = "system_prompt ainda contém TODOs"
MINIMUM_TECHNIQUES_ERROR_PREFIX = "Mínimo de 2 técnicas requeridas"


class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup_prompt(self):
        self.prompt_data = load_yaml(str(PROMPT_FILE))[PROMPT_KEY]
        self.system_prompt = self.prompt_data["system_prompt"]
        self.is_valid, self.validation_errors = validate_prompt_structure(self.prompt_data)

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert MISSING_SYSTEM_PROMPT_ERROR not in self.validation_errors
        assert EMPTY_SYSTEM_PROMPT_ERROR not in self.validation_errors

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        role_markers = [
            "Voce e um agente especializado",
            "Product Manager",
            "Product Owner",
        ]

        assert any(marker in self.system_prompt for marker in role_markers)

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        required_format_terms = [
            "Como um",
            "eu quero",
            "para que",
            "Criterios de Aceitacao",
        ]

        for term in required_format_terms:
            assert term in self.system_prompt

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        assert "Exemplos:" in self.system_prompt
        assert self.system_prompt.count("Entrada:") >= 2
        assert self.system_prompt.count("Saida:") >= 2

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        assert TODO_ERROR not in self.validation_errors

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        assert not any(
            error.startswith(MINIMUM_TECHNIQUES_ERROR_PREFIX)
            for error in self.validation_errors
        )

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
