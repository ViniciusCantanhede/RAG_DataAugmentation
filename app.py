import os
import streamlit as st
import tempfile
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Importar funções dos módulos utils
from utils.pdf_converter import convert_pdf_to_markdown
from utils.translator import translate_augmentation
from utils.translator import translate_augmentation, translate_and_retranslate
from utils.file_handler import create_output_directory, save_markdown_files

# Configurar página
st.set_page_config(
    page_title="Data Augmentation para RAG", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título da aplicação
st.title("Data Augmentation para RAG")
st.markdown("""
Esta aplicação processa documentos PDF, converte para markdown usando Docling
e realiza data augmentation através de traduções para melhorar a qualidade do RAG.
""")

# Sidebar para informações
st.sidebar.header("Sobre")
st.sidebar.info("""
Esta ferramenta realiza:
1. Conversão de PDF para markdown usando Docling
2. Data augmentation via traduções (PT → ES → PT, PT → IT → PT)
3. Salva resultados para uso em chatbot RAG
""")

# Upload do PDF
st.header("Upload de Documento")
pdf_file = st.file_uploader("Carregar PDF para processamento", type=["pdf"])

# Opções de processamento
st.header("Configurações")
with st.expander("Opções de Data Augmentation", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Idiomas")
        augment_spanish = st.checkbox("Português → Espanhol → Português", value=True)
        augment_italian = st.checkbox("Português → Italiano → Português", value=True)
    
    with col2:
        st.markdown("### Parâmetros")
        chunk_size = st.slider("Tamanho do chunk (caracteres)", 1000, 5000, 4000, 500)

# Iniciar processamento
if pdf_file:
    if st.button("Processar Documento", type="primary"):
        # Salvar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_file.read())
            pdf_path = temp_file.name
        
        try:
            # Criar diretório de saída
            output_dir = create_output_directory()
            
            # Processar documento
            with st.spinner("Convertendo PDF para markdown com Docling..."):
                markdown_content = convert_pdf_to_markdown(pdf_path)
                
                if markdown_content:
                    st.success("✅ PDF convertido para markdown com sucesso!")
                    
                    # Preview do markdown
                    with st.expander("Preview do Markdown", expanded=False):
                        st.markdown(markdown_content[:1500] + "..." if len(markdown_content) > 1500 else markdown_content)
                    
                    # Realizar data augmentation
                    with st.spinner("Realizando data augmentation... (pode demorar alguns minutos)"):
                        progress_bar = st.progress(0)
                        
                        # Processo de augmentation
                        augmented_texts = {'original': markdown_content}
                        
                        # Augmentation com espanhol
                        if augment_spanish:
                            st.text("Processando: Português → Espanhol → Português")
                            progress_bar.progress(25)
                            try:
                                spanish_augmented = translate_and_retranslate(
                                    markdown_content, 
                                    'es', 
                                    chunk_size=chunk_size
                                )
                                augmented_texts['spanish_augmented'] = spanish_augmented
                                st.success("✅ Tradução via Espanhol concluída!")
                            except Exception as e:
                                st.error(f"❌ Erro na tradução para Espanhol: {e}")
                        
                        progress_bar.progress(50)
                        
                        # Augmentation com italiano
                        if augment_italian:
                            st.text("Processando: Português → Italiano → Português")
                            progress_bar.progress(75)
                            try:
                                italian_augmented = translate_and_retranslate(
                                    markdown_content, 
                                    'it',
                                    chunk_size=chunk_size
                                )
                                augmented_texts['italian_augmented'] = italian_augmented
                                st.success("✅ Tradução via Italiano concluída!")
                            except Exception as e:
                                st.error(f"❌ Erro na tradução para Italiano: {e}")
                        
                        progress_bar.progress(100)
                        
                        # Salvar resultados
                        file_paths = save_markdown_files(augmented_texts, output_dir)
                        
                        # Exibir resumo
                        st.header("Resumo do Processamento")
                        st.markdown(f"**Total de arquivos gerados:** {len(file_paths)}")
                        st.markdown(f"**Diretório de saída:** `{output_dir}`")
                        
                        # Tabela com informações dos arquivos
                        file_info = []
                        for key, path in file_paths.items():
                            file_size = os.path.getsize(path) / 1024  # KB
                            file_info.append({
                                "Versão": key,
                                "Caminho": path,
                                "Tamanho (KB)": f"{file_size:.2f}"
                            })
                        
                        st.table(file_info)
                        
                        # Botão para download
                        st.markdown("### Download de Arquivos")
                        for key, path in file_paths.items():
                            with open(path, "r", encoding="utf-8") as file:
                                content = file.read()
                                file_name = os.path.basename(path)
                                st.download_button(
                                    label=f"Download {key}",
                                    data=content,
                                    file_name=file_name,
                                    mime="text/markdown"
                                )
            
            # Remover arquivo temporário
            os.unlink(pdf_path)
            
        except Exception as e:
            st.error(f"Erro ao processar o documento: {e}")

# Rodapé
st.markdown("---")
st.markdown("Data Augmentation para RAG com Docling e Deep Translator")