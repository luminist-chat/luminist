from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_core.prompts import ChatPromptTemplate

QUERY_MODEL = "gpt-4o-mini"
FETCH_CHUNKS = 1000
RERANK_CHUNKS = 100

print("Loading vector store...")
embeddings_model = OpenAIEmbeddings()
vector_store = FAISS.load_local("react_vector_store", embeddings_model, allow_dangerous_deserialization=True);
queryLLM = ChatOpenAI(model=QUERY_MODEL);

print("Fetching similar chunks...")
vector_retriever = vector_store.as_retriever(
    search_kwargs={"k": FETCH_CHUNKS}
)

print ("Reranking...")
hf_cross_encoder = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
compressor = CrossEncoderReranker(model=hf_cross_encoder, top_n=RERANK_CHUNKS)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vector_retriever
)

query = "What is the point of this framework?"

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant. Use the following context to answer the question.
    If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    
    Context: {context}
    """),
    ("human", "{question}")
])

def format_docs(docs):
    formatted = "\n\n".join(doc.page_content for doc in docs)
    return formatted

print("Running query...")
qa_chain = (
    {
        "context": compression_retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | queryLLM
    | StrOutputParser()
)

output = qa_chain.invoke(query)
print(output)