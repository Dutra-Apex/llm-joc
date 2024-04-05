import argparse
import mistral_model as mistral
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

model = mistral.model
tokenizer = mistral.tokenizer
text_generation_pipeline = mistral.text_generation_pipeline
mistral_llm = mistral.llm

embedding_model = SentenceTransformerEmbeddings(model_name='BAAI/bge-large-zh-v1.5')

QA_TEMPLATE = """<s>[INST] You're helping students.
Use the following context to Answer the question below briefly:

{context}

{question} [/INST] </s>
"""


def push_file_to_rag(filepath):
    with open(filepath, encoding='utf-8') as file:
        data = file.read()

    docs = [Document(page_content=post) for post in [data]]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=10, separators=['\n\n', '\n', '.']
    )
    document_chunks = text_splitter.split_documents(docs)

    chroma_db = Chroma.from_documents(document_chunks, embedding_model)
    retriever = chroma_db.as_retriever()
    return retriever


def run_mistral_with_rag(user_prompt, retriever):
    QA_PROMPT = PromptTemplate.from_template(QA_TEMPLATE)
    qa_chain = RetrievalQA.from_chain_type(
        llm = mistral_llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_PROMPT},
        verbose=False
    )

    question = user_prompt
    response = qa_chain({"query": question})
    print("*" * 200)
    print(response['result'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pushes text file to vector database and uses it to")
    parser.add_argument("--textfile_path", help="Path to the input text file", 
                        default="demo.txt")

    args = parser.parse_args()
    textfile_path = args.textfile_path
    retriever = push_file_to_rag(textfile_path)
    user_input = input("\Hi! I'm your personal discord assistant, what do you need help with? \n")

    while True:
        run_mistral_with_rag(user_input, retriever)
        user_input = input(" ")
