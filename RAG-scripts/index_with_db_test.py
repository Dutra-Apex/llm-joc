# Import modules
import chromadb
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

# Create Chroma DB client and access the existing vector store
client = chromadb.PersistentClient(path="./chroma_db_data")
chroma_collection = client.get_collection(name="dicord_JOC")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Initialize Ollama and ServiceContext
llm = Ollama(model="mistral")
service_context = ServiceContext.from_defaults(llm=llm, embed_model="local")

# Create VectorStoreIndex and query engine with a similarity threshold of 20
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context, similarity_top_k=20)
query_engine = index.as_query_engine()

# Perform a query and print the response
response = query_engine.query("whats the easiest way to start learning about CI/CD?")
print(response)
