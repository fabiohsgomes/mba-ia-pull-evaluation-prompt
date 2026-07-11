"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from utils import save_yaml, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    print_section_header("Pull de Prompt do LangSmith Hub")

    repo = "leonanluppi/bug_to_user_story_v1"

    print(f"Pulling prompt: {repo}")
    prompt = hub.pull(repo)
    print("Pull finalizado")

    system_prompt = None
    user_prompt = None

    for msg in prompt.messages:
        if isinstance(msg, SystemMessagePromptTemplate):
            system_prompt = msg.prompt.template
        elif isinstance(msg, HumanMessagePromptTemplate):
            user_prompt = msg.prompt.template

    prompt_data = {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }

    prompts_dir = Path("prompts")
    prompts_dir.mkdir(parents=True, exist_ok=True)
    output_file = prompts_dir.joinpath("bug_to_user_story_v1.yml")

    success = save_yaml(prompt_data, str(output_file))
    if not success:
        print("Erro ao salvar prompt")
        sys.exit(1)

    print(f"Prompt salvo em: {output_file}")
    print(f"Operação realizada com sucesso ...")


def main():
    """Função principal"""
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
