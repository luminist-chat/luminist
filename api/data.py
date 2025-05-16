from langchain_unstructured import UnstructuredLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain import hub;
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI

loader = UnstructuredLoader(
    file_path="data/pdf/react.pdf",
    strategy="fast",
)
embeddings_model = OpenAIEmbeddings();
text_splitter = SemanticChunker(embeddings_model)

docs = []
for doc in loader.lazy_load():
    docs.append(doc)


chunks = text_splitter.split_documents(docs)

for idx, chunk in enumerate(chunks):
    chunk.metadata["id"] = idx

vector_store = FAISS.from_documents(chunks, embeddings_model)

vector_retriever = vector_store.as_retriever(search_kwargs={"k": 20});


vector_store.add_documents(chunks)

query = "What is this document about?"

#compressor = CrossEncoderReranker();
#compression_retriever = ContextualCompressionRetriever(
#    base_compressor=compressor,
#    base_retriever=vector_retriever
#)


#compressed_docs = compression_retriever.invoke(query);


# See full prompt at https://smith.langchain.com/hub/rlm/rag-prompt
prompt = hub.pull("rlm/rag-prompt")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


#print(compressed_docs);

llm = ChatOpenAI(model="gpt-4o-mini");

qa_chain = (
    {
        "context": vector_retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)


output = qa_chain.invoke(query)

print(output);