import glob
import os

from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import ChatbotSettings

load_dotenv()

DEFAULT_RAG_DIRECTORY = os.path.join(os.path.dirname(__file__), "documuents")
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 50
DEFAULT_RAG_K = 4
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

retriever = None
_document_paths = []


def _find_pdf_paths(directory: str) -> list[str]:
    if not os.path.isdir(directory):
        return []
    return sorted(glob.glob(os.path.join(directory, "*.pdf")))


def _load_documents(document_paths: list[str]):
    documents = []
    for path in document_paths:
        loader = PyPDFLoader(path)
        documents.extend(loader.load())
    return documents


def _split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def _build_rag_retriever():
    document_paths = _find_pdf_paths(DEFAULT_RAG_DIRECTORY)
    if not document_paths:
        raise FileNotFoundError(
            f"No PDF documents found in {DEFAULT_RAG_DIRECTORY}. Add files to the folder and reload RAG."
        )

    documents = _load_documents(document_paths)
    if not documents:
        raise ValueError("Loaded PDF documents, but no document content was extracted.")

    chunks = _split_documents(documents)
    embeddings = OpenAIEmbeddings(model=DEFAULT_EMBEDDING_MODEL)
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever_instance = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": DEFAULT_RAG_K},
    )

    return retriever_instance, document_paths


def initialize_rag():
    global retriever, _document_paths

    if retriever is None:
        settings = ChatbotSettings()
        settings.validate()

        retriever, _document_paths = _build_rag_retriever()

    return retriever


def get_rag_document_count() -> int:
    initialize_rag()
    return len(_document_paths)


def save_uploaded_pdfs(uploaded_files, target_dir: str = DEFAULT_RAG_DIRECTORY) -> list[str]:
    os.makedirs(target_dir, exist_ok=True)
    saved_paths = []

    for uploaded_file in uploaded_files:
        file_name = os.path.basename(uploaded_file.name)
        target_path = os.path.join(target_dir, file_name)
        base_name, extension = os.path.splitext(file_name)
        suffix = 1

        while os.path.exists(target_path):
            target_path = os.path.join(target_dir, f"{base_name}_{suffix}{extension}")
            suffix += 1

        with open(target_path, "wb") as output_file:
            output_file.write(uploaded_file.getbuffer())

        saved_paths.append(target_path)

    return saved_paths


def reload_rag_data() -> str:
    global retriever, _document_paths

    retriever = None
    _document_paths = []
    initialize_rag()

    return f"RAG corpus reloaded with {len(_document_paths)} PDF document(s)."


@tool
def rag_tool(query: str) -> str:
    """
    Retrieve relevant information from the RAG document corpus.
    """

    retriever_instance = initialize_rag()
    documents = retriever_instance.get_relevant_documents(query)
    if not documents:
        return "No relevant documents found in the RAG corpus."

    answers = []
    for index, document in enumerate(documents, start=1):
        content = document.page_content.strip()
        if len(content) > 1200:
            content = content[:1200] + "..."

        answers.append(
            f"Document {index}:\n{content}\nMETADATA: {document.metadata}"
        )

    return "\n\n".join(answers)
