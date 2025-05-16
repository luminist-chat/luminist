from langchain_unstructured import UnstructuredLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai.chat_models import ChatOpenAI

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
CLEANUP_MODEL = "gpt-4o-mini"
SUMMARIZE_MODEL = "gpt-4o-mini"

TEST_DOC = "data/pdf/react.pdf"

loader = UnstructuredLoader(
    file_path=TEST_DOC,
    strategy="hi_res",
    mode="single",
    include_metadata=True,
    include_page_breaks=True
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    separators=["\n\n", "\n", ".", "!", "?", " ", ""],  # Split on natural boundaries
    is_separator_regex=False
)

print("Loading documents...")
docs = []
for doc in loader.lazy_load():
    doc.page_content = doc.page_content.strip()
    docs.append(doc)

print(f"Loaded {len(docs)} documents")

print("Splitting into chunks...")
chunks = text_splitter.split_documents(docs)

cleanupLLM = ChatOpenAI(model=CLEANUP_MODEL);
summarizeLLM = ChatOpenAI(model=SUMMARIZE_MODEL);

def clean_chunk(chunk):
    prompt = f"The following is a chunk of text from a PDF document - clean up any oddities that may have been left over from the PDF conversion process. \
    Do not change the content of the document, only clean up the formatting.  Output JUST the content, nothing else, no header or footer, etc. \n\nDocument: {chunk.page_content}"
    response = cleanupLLM.invoke(prompt)
    return response.content

def summarize_chunk(chunk):
    prompt = f"the following is a chunk of text from a PDF document - summarize the content in a few sentences. \
    Output JUST the summary, nothing else, no header or footer, etc. \
    If the document contains no content, return ONLY \"N/A\" \n\nDocument: {chunk.page_content}"
    response = summarizeLLM.invoke(prompt)
    return response.content

print("Processing chunks...")
for idx, chunk in enumerate(chunks):
    if idx < 10:
        chunk.page_content = clean_chunk(chunk)
        chunk.page_content = summarize_chunk(chunk) + "\n\n" + chunk.page_content
        print(chunk.page_content)
    chunk.metadata["id"] = idx

print(f"Created {len(chunks)} chunks")

print("Creating vector store...")
embeddings_model = OpenAIEmbeddings()
vector_store = FAISS.from_documents(chunks, embeddings_model)

vector_store.save_local("react_vector_store");

print("Done!")