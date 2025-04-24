# Data Augmentation para RAG

Este projeto implementa uma ferramenta de processamento de documentos para melhorar sistemas de Retrieval Augmented Generation (RAG), focando especificamente no pré-processamento de documentos PDF através de data augmentation por tradução.

## 📋 Descrição

A Data Augmentation para RAG é uma aplicação Streamlit que:

1. Converte documentos PDF para formato markdown usando a biblioteca Docling
2. Realiza data augmentation através de traduções cíclicas (PT → ES → PT, PT → IT → PT)
3. Preserva formatação e estrutura durante o processo de tradução
4. Exporta o documento original e suas versões aumentadas para uso em sistemas RAG

O uso de data augmentation permite gerar variações do mesmo conteúdo, aumentando a diversidade léxica e melhorando a capacidade do sistema RAG de recuperar informações relevantes.

## ✨ Funcionalidades

- **Conversão PDF para Markdown**: Utiliza a biblioteca Docling para extrair o conteúdo de PDFs com preservação da estrutura
- **Data Augmentation por Tradução**: Traduz o conteúdo para espanhol e italiano e depois de volta para português
- **Preservação de Formatação**: Implementa um sistema de marcadores que preserva elementos markdown durante a tradução
- **Interface Amigável**: Interface Streamlit intuitiva para upload e processamento de documentos
- **Exportação Flexível**: Salva os resultados em arquivos markdown organizados

## 🔧 Pré-requisitos

- Python 3.8+
- Recomendado: ambiente virtual Python (venv, conda)

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/data-augmentation-rag.git
   cd data-augmentation-rag
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No macOS/Linux
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Instale o Docling (dependendo do seu sistema):
   
   Para a maioria dos sistemas:
   ```bash
   pip install docling
   ```
   
   Para Mac com processadores Intel:
   ```bash
   pip install "docling[mac_intel]"
   ```

## 📂 Estrutura do Projeto

```
data_augmentation/
├── app.py                # Aplicação Streamlit principal
├── requirements.txt      # Dependências do projeto
├── .env                  # Para variáveis de ambiente (opcional)
├── .gitignore            # Para ignorar arquivos desnecessários
└── utils/
    ├── __init__.py       # Arquivo vazio para tornar utils um pacote
    ├── pdf_converter.py  # Conversão de PDF para markdown usando docling
    ├── translator.py     # Funções de tradução com deep_translator
    └── file_handler.py   # Gerenciamento de arquivos
```

## 🚀 Como Usar

1. Execute a aplicação Streamlit:
   ```bash
   streamlit run app.py
   ```

2. Acesse a interface no navegador (geralmente em http://localhost:8501)

3. Faça upload de um documento PDF

4. Configure as opções de data augmentation:
   - Selecione os idiomas para tradução (Espanhol, Italiano)
   - Ajuste o tamanho dos chunks se necessário

5. Clique em "Processar Documento" e aguarde a conclusão

6. Baixe os arquivos resultantes ou utilize os arquivos salvos na pasta `output/`

## 🔍 Detalhes Técnicos

### Conversão PDF para Markdown

Foi utilizada a biblioteca Docling para extrair o conteúdo de documentos PDF e convertê-los para markdown. A Docling é uma ferramenta especializada em entender a estrutura de documentos e preservar elementos como cabeçalhos, listas e tabelas durante a conversão.

```python
from docling.document_converter import DocumentConverter

def convert_pdf_to_markdown(pdf_path):
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    markdown_content = result.document.export_to_markdown()
    return markdown_content
```

### Data Augmentation via Tradução

O processo de data augmentation segue estas etapas:

1. **Normalização**: Substitui elementos markdown por marcadores especiais
2. **Divisão em Chunks**: Divide o texto em pedaços menores para respeitar limites da API
3. **Tradução de Ida**: Traduz para o idioma intermediário (espanhol/italiano)
4. **Tradução de Volta**: Traduz de volta para o português
5. **Restauração**: Converte os marcadores de volta para a formatação markdown

### Preservação de Formatação

Foi implementado um sistema robusto para preservar a formatação markdown durante o processo de tradução:

- Cabeçalhos são marcados como `[H1]texto[/H1]`, `[H2]texto[/H2]`, etc.
- Listas são marcadas como `[UL]item[/UL]` ou `[OL]item[/OL]`
- Formatação de texto é preservada com `[B]texto[/B]`, `[I]texto[/I]`, etc.

----
Desenvolvido para melhorar a qualidade de sistemas RAG através de técnicas de data augmentation.