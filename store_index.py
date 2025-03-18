# run this one time to save the pdf as a vectordatabase in pinecone

from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
# from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
# from dotenv import load_dotenv
import os

# load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data = load_pdf_file(data="Data/")
text_chunks = text_split(extracted_data)
embeddings=download_hugging_face_embeddings()

# Retrieve the API key from your environment or set it directly
# PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# Create an instance of the Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medbot"

# Optionally, check if the index already exists before creating it
existing_indexes = [index.name for index in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
    batch_size=50
)