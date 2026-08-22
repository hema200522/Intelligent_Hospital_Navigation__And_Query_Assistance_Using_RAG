from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


DOCUMENT_FOLDER = "data/documents"
VECTORSTORE_FOLDER = "vectorstore"


def create_vector_database():

    documents = []

    folder = Path(DOCUMENT_FOLDER)

    for file in folder.glob("*.txt"):

        loader = TextLoader(
            str(file),
            encoding="utf-8"
        )

        documents.extend(loader.load())

    if not documents:
        raise Exception(
            "No hospital documents found in data/documents/"
        )

    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS database
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(
        VECTORSTORE_FOLDER
    )

    print(
        f"Knowledge base created with {len(chunks)} chunks."
    )


def load_vector_database():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        VECTORSTORE_FOLDER,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def search_hospital_information(question):

    vectorstore = load_vector_database()

    documents = vectorstore.similarity_search(
        question,
        k=4
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context