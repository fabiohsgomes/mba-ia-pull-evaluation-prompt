"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    prompt = prompt_data.get("bug_to_user_story_v2", {})

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt["system_prompt"]),
        ("human", prompt["user_prompt"]),
    ])

    try:
        url = hub.push(
            prompt_name,
            chat_prompt,
            new_repo_is_public=True,
            new_repo_description=prompt.get("description", ""),
            tags=prompt.get("tags", []),
        )
        print(f"Prompt publicado em: {url}")
        return True
    except Exception as e:
        print(f"Erro ao publicar prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    prompt = prompt_data.get("bug_to_user_story_v2")
    if not prompt:
        return False, ["Prompt bug_to_user_story_v2 ausente"]

    is_valid, errors = validate_prompt_structure(prompt)

    if not prompt.get("user_prompt"):
        errors.append("user_prompt ausente ou vazio")

    return (is_valid and len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("Push de Prompt Otimizado para o LangSmith Hub")

    yaml_file = "prompts/bug_to_user_story_v2.yml"
    prompt_data = load_yaml(yaml_file)

    if prompt_data is None:
        print("Erro ao carregar prompt otimizado")
        sys.exit(1)

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("Prompt inválido:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    if not username:
        print("USERNAME_LANGSMITH_HUB não definida no ambiente.")
        sys.exit(1)

    prompt_name = f"{username}/bug_to_user_story_v2"

    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    if not success:
        print("Erro ao publicar prompt")
        sys.exit(1)

    print("Prompt publicado com sucesso!")


if __name__ == "__main__":
    sys.exit(main())
