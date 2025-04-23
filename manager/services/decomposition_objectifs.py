import os
from dotenv import load_dotenv
load_dotenv()
from typing import List, Dict

import openai

# Load environment variables
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Prompt template
prompt_template = """
Vous êtes un assistant personnel. À partir de l'objectif donné, générez une liste de {nb_tasks} tâches concrètes, claires et réalisables.
Évitez les généralités. Commencez chaque tâche par un verbe à l'infinitif.
Formatez la réponse comme une liste à puces non numérotée, comme ceci :
"- [tâche]
- [tâche]
- [tâche]
- [tâche]
- [tâche]
- [tâche]"

Objectif : {objectif}
"""

def _verify_response_format(response: str) -> bool:
    """
    Checks if the model's response is in the correct format.
    
    Params:
    - response (str): The response from the model.
    
    Returns:
    - bool: True if the response is in the correct format, False otherwise.
    
    """
    lines = response.strip().split('\n')
    return all(line.startswith('- ') for line in lines) and 2 <= len(lines) <= 30


def decompose_objective(objectif: str, nb_tasks: int = 7) -> Dict[str, List[Dict[str, str]] | None]:
    """
    Decompose an objective into a list of tasks.
    
    Params:
    - objectif (str): The objective to decompose.
    - nb_tasks (int): The number of tasks to generate.
    
    Returns:
    - Dict[str, List[str] | None]: A dictionary containing the tasks and any errors.
    """

    prompt = prompt_template.format(objectif=objectif, nb_tasks=nb_tasks)

    client = openai.OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
        ).choices[0].message.content
        if response is None:
            return {"taches": None, "erreur": "Réponse du modèle est None"} # type: ignore

        lines = response.strip().split('\n')
        taches = [{'name': line[2:].strip()} for line in lines]

        if not _verify_response_format(response):
            return {"taches": None, "erreur": "Réponse du modèle mal formatée."} # type: ignore

        return {"taches": taches, "erreur": None}
    except Exception as e:
        return {"taches": [], "erreur": str(e)} # type: ignore
