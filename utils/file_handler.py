import os
import json
from datetime import datetime

def create_output_directory():
    """
    Cria o diretório de saída para os arquivos processados.
    
    Returns:
        str: Caminho do diretório de saída
    """
    # Criar diretório de saída com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("output", f"augmentation_{timestamp}")
    
    # Garantir que o diretório existe
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "markdown"), exist_ok=True)
    
    return output_dir

def save_markdown_files(augmented_texts, output_dir):
    """
    Salva os textos aumentados como arquivos markdown.
    
    Args:
        augmented_texts (dict): Dicionário com textos aumentados
        output_dir (str): Diretório de saída
    
    Returns:
        dict: Dicionário com caminhos dos arquivos salvos
    """
    file_paths = {}
    markdown_dir = os.path.join(output_dir, "markdown")
    
    for key, text in augmented_texts.items():
        file_name = f"{key}.md"
        file_path = os.path.join(markdown_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        
        file_paths[key] = file_path
    
    # Salvar metadados
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "file_count": len(augmented_texts),
        "files": file_paths
    }
    
    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as file:
        json.dump(metadata, file, indent=2)
    
    return file_paths