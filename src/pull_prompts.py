"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import logging
import sys
import yaml
from pathlib import Path
from langsmith import Client

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def pull_prompts_from_langsmith():
    client = Client()

    logging.info("Executando pull do prompt bug_to_user_story_v1 ....")
    pulled_prompt = client.pull_prompt("leonanluppi/bug_to_user_story_v1")
    logging.info("Pull finalizado")

    logging.info("Salvando prompt na para prompts")
    prompts_dir = Path("prompt")
    prompts_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.joinpath("bug_to_user_story_v1.yml").write_text(yaml.dump(pulled_prompt.model_dump(), default_flow_style=False))
    logging.info("Operação realizada com sucesso.")


def main():
    """Função principal"""
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
