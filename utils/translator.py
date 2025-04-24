from deep_translator import GoogleTranslator
import time
import re
from tqdm import tqdm

def normalize_markdown(text):
    """
    Normaliza o texto markdown para preservar a formatação durante a tradução.
    
    Args:
        text (str): Texto markdown para normalizar
        
    Returns:
        str: Texto normalizado com marcadores especiais
    """
    # Preservar parágrafos
    text = re.sub(r'\n\s*\n', '\n[PARA]\n', text)
    
    # Cabeçalhos
    text = re.sub(r'# ([^\n]+)', r'[H1]\1[/H1]', text)
    text = re.sub(r'## ([^\n]+)', r'[H2]\1[/H2]', text)
    text = re.sub(r'### ([^\n]+)', r'[H3]\1[/H3]', text)
    text = re.sub(r'#### ([^\n]+)', r'[H4]\1[/H4]', text)
    text = re.sub(r'##### ([^\n]+)', r'[H5]\1[/H5]', text)
    text = re.sub(r'###### ([^\n]+)', r'[H6]\1[/H6]', text)
    
    # Listas
    text = re.sub(r'^\s*- ([^\n]+)', r'[UL]\1[/UL]', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\* ([^\n]+)', r'[UL]\1[/UL]', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\. ([^\n]+)', r'[OL]\1[/OL]', text, flags=re.MULTILINE)
    
    # Formatação
    text = re.sub(r'\*\*([^*]+)\*\*', r'[B]\1[/B]', text)
    text = re.sub(r'\*([^*]+)\*', r'[I]\1[/I]', text)
    text = re.sub(r'`([^`]+)`', r'[CODE]\1[/CODE]', text)
    
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'[LINK=\2]\1[/LINK]', text)
    
    return text

def restore_markdown(text):
    """
    Restaura a formatação markdown após a tradução.
    
    Args:
        text (str): Texto traduzido com marcadores
        
    Returns:
        str: Texto com formatação markdown restaurada
    """
    # Restaurar parágrafos
    text = re.sub(r'\n\[PARA\]\n', '\n\n', text)
    
    # Restaurar cabeçalhos
    text = re.sub(r'\[H1\](.*?)\[/H1\]', r'# \1', text, flags=re.DOTALL)
    text = re.sub(r'\[H2\](.*?)\[/H2\]', r'## \1', text, flags=re.DOTALL)
    text = re.sub(r'\[H3\](.*?)\[/H3\]', r'### \1', text, flags=re.DOTALL)
    text = re.sub(r'\[H4\](.*?)\[/H4\]', r'#### \1', text, flags=re.DOTALL)
    text = re.sub(r'\[H5\](.*?)\[/H5\]', r'##### \1', text, flags=re.DOTALL)
    text = re.sub(r'\[H6\](.*?)\[/H6\]', r'###### \1', text, flags=re.DOTALL)
    
    # Restaurar listas
    text = re.sub(r'\[UL\](.*?)\[/UL\]', r'- \1', text, flags=re.DOTALL)
    text = re.sub(r'\[OL\](.*?)\[/OL\]', r'1. \1', text, flags=re.DOTALL)
    
    # Restaurar formatação
    text = re.sub(r'\[B\](.*?)\[/B\]', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'\[I\](.*?)\[/I\]', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'\[CODE\](.*?)\[/CODE\]', r'`\1`', text, flags=re.DOTALL)
    
    # Restaurar links
    text = re.sub(r'\[LINK=(.*?)\](.*?)\[/LINK\]', r'[\2](\1)', text, flags=re.DOTALL)
    
    # Restaurar manualmente quaisquer marcadores que não foram substituídos
    text = re.sub(r'\[UL\] \$1 \[/UL\]', r'- Item', text, flags=re.IGNORECASE)
    text = re.sub(r'\[OL\] \$1 \[/OL\]', r'1. Item', text, flags=re.IGNORECASE)
    
    # Corrigir quebras de linha extras
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Corrigir problema de palavras em linhas separadas
    text = re.sub(r'(\w+)\s*\n\s*(\w+)', r'\1 \2', text)
    
    return text

def translate_chunk(text, source_lang, target_lang, retry_count=3, delay=1):
    """
    Traduz um pedaço de texto com tratamento de erro e retentativas.
    
    Args:
        text (str): Texto para traduzir
        source_lang (str): Idioma de origem
        target_lang (str): Idioma de destino
        retry_count (int): Número de tentativas em caso de erro
        delay (int): Tempo de espera entre tentativas (segundos)
        
    Returns:
        str: Texto traduzido
    """
    for attempt in range(retry_count):
        try:
            translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
            return translated
        except Exception as e:
            print(f"Erro na tentativa {attempt+1}/{retry_count}: {e}")
            if attempt < retry_count - 1:
                print(f"Aguardando {delay} segundos antes de tentar novamente...")
                time.sleep(delay)
                delay *= 2  # Aumento exponencial do tempo de espera
            else:
                print(f"Falha após {retry_count} tentativas.")
                raise e

def translate_and_retranslate(text, intermediate_lang, chunk_size=4000):
    """
    Traduz um texto para outro idioma e depois de volta para o idioma original,
    preservando a formatação markdown.
    
    Args:
        text (str): Texto original em português
        intermediate_lang (str): Código do idioma intermediário (ex: 'es', 'it')
        chunk_size (int): Tamanho máximo de cada pedaço para tradução
        
    Returns:
        str: Texto retraduzido para português
    """
    # Normalizar o texto para preservar a formatação
    normalized_text = normalize_markdown(text)
    
    # Dividir o texto em pedaços menores
    chunks = []
    remaining = normalized_text
    while remaining:
        # Encontrar um ponto de quebra seguro (fim de frase ou parágrafo)
        if len(remaining) <= chunk_size:
            chunks.append(remaining)
            break
            
        split_pos = remaining[:chunk_size].rfind('. ')
        if split_pos == -1:
            split_pos = remaining[:chunk_size].rfind('\n')
        if split_pos == -1:
            split_pos = chunk_size - 1
        else:
            split_pos += 2  # Incluir o ponto e espaço
            
        chunks.append(remaining[:split_pos])
        remaining = remaining[split_pos:]
    
    # Traduzir para o idioma intermediário
    translated_chunks = []
    print(f"\nTraduzindo para {intermediate_lang}...")
    for i, chunk in enumerate(tqdm(chunks, desc=f"PT → {intermediate_lang.upper()}")):
        translated = translate_chunk(chunk, 'pt', intermediate_lang)
        translated_chunks.append(translated)
        # Pequena pausa para não sobrecarregar a API
        if i < len(chunks) - 1:
            time.sleep(0.5)
    
    intermediate_text = ''.join(translated_chunks)
    
    # Retraduzir para português
    retranslated_chunks = []
    print(f"\nRetraduzindo para português...")
    # Dividir novamente em chunks porque o texto traduzido pode ter tamanho diferente
    rechunks = []
    remaining = intermediate_text
    while remaining:
        if len(remaining) <= chunk_size:
            rechunks.append(remaining)
            break
            
        split_pos = remaining[:chunk_size].rfind('. ')
        if split_pos == -1:
            split_pos = remaining[:chunk_size].rfind('\n')
        if split_pos == -1:
            split_pos = chunk_size - 1
        else:
            split_pos += 2
            
        rechunks.append(remaining[:split_pos])
        remaining = remaining[split_pos:]
    
    for i, chunk in enumerate(tqdm(rechunks, desc=f"{intermediate_lang.upper()} → PT")):
        retranslated = translate_chunk(chunk, intermediate_lang, 'pt')
        retranslated_chunks.append(retranslated)
        # Pequena pausa para não sobrecarregar a API
        if i < len(rechunks) - 1:
            time.sleep(0.5)
    
    # Restaurar formatação markdown
    combined_text = ''.join(retranslated_chunks)
    restored_text = restore_markdown(combined_text)
    
    return restored_text

def translate_augmentation(markdown_text):
    """
    Realiza data augmentation via tradução para textos grandes.
    
    Args:
        markdown_text (str): Texto em markdown para realizar augmentation.
        
    Returns:
        list: Lista contendo o texto original e versões traduzidas/retraduzidas.
    """
    augmented_texts = [markdown_text]  # Texto original
    
    # Tradução para espanhol e retradução
    try:
        print("\n=== Iniciando augmentation via Espanhol ===")
        spanish_augmented = translate_and_retranslate(markdown_text, 'es')
        augmented_texts.append(spanish_augmented)
        print("✓ Augmentation via Espanhol concluída!\n")
    except Exception as e:
        print(f"✗ Erro na tradução via Espanhol: {e}\n")
    
    # Processo similar para italiano
    try:
        print("\n=== Iniciando augmentation via Italiano ===")
        italian_augmented = translate_and_retranslate(markdown_text, 'it')
        augmented_texts.append(italian_augmented)
        print("✓ Augmentation via Italiano concluída!\n")
    except Exception as e:
        print(f"✗ Erro na tradução via Italiano: {e}\n")
    
    return augmented_texts