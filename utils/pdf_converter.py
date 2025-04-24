from docling.document_converter import DocumentConverter
import os

def convert_pdf_to_markdown(pdf_path):
    """
    Converte um arquivo PDF para formato markdown usando docling.
    
    Args:
        pdf_path (str): Caminho para o arquivo PDF.
        
    Returns:
        str: Conteúdo do PDF convertido para markdown.
    """
    try:
        # Inicializar o conversor docling
        converter = DocumentConverter()
        
        # Converter o documento
        result = converter.convert(pdf_path)
        
        # Extrair markdown
        markdown_content = result.document.export_to_markdown()
        
        return markdown_content
    except Exception as e:
        raise Exception(f"Erro ao converter PDF para markdown com docling: {e}")