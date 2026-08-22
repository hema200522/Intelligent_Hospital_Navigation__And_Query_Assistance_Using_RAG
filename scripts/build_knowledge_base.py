from src.rag import create_vector_database


if __name__ == "__main__":

    print("Creating hospital knowledge base...")

    create_vector_database()

    print("Knowledge base created successfully!")