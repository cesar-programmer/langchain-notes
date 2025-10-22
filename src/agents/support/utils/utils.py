from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List

def clean_history_for_llm(history: List[BaseMessage]) -> List[BaseMessage]:
    """
    Limpia el historial de mensajes para que solo contenga texto plano 
    que un LLM sin herramientas pueda entender.
    
    Extrae el contenido de texto de los AIMessages que puedan contener
    partes de herramientas (como 'file_search_call') y descarta
    mensajes que no sean Human o AI.
    """
    cleaned_history = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            # Los HumanMessage siempre están limpios
            cleaned_history.append(msg)
        elif isinstance(msg, AIMessage):
            # Los AIMessage pueden estar "sucios"
            new_content = ""
            if isinstance(msg.content, list):
                # Si el contenido es una lista, busca la parte de texto
                for part in msg.content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        new_content = part.get("text", "")
                        break  # Encontramos el texto, salimos
            elif isinstance(msg.content, str):
                # Si ya es un string, está limpio
                new_content = msg.content
            
            if new_content:
                # Añadimos un NUEVO AIMessage solo con el texto
                cleaned_history.append(AIMessage(content=new_content))
                
    return cleaned_history