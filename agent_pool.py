from swarm import Agent
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete, gpt_4o_complete
import dotenv
from langchain_unstructured import UnstructuredLoader

dotenv.load_dotenv()

# ------------------ Prepare the Database ------------------

WORKING_DIR = "lightrag_files"

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete  # Use gpt_4o_mini_complete LLM model
    # llm_model_func=gpt_4o_complete  # Optionally, use a stronger model
)

# # -- INSERTING KNOWLEDGE START--
# file_path = ("proceeding_publications/Vom Brocke et al. - 2020 - Introduction to Design Science Research.pdf")

# loader = UnstructuredLoader(
#     file_path=file_path,
#     #strategy="hi_res",
#     strategy="fast",
#     partition_via_api=True,
#     coordinates=True,
# )

# docs = []
# for doc in loader.lazy_load():
#     docs.append(doc)

# # ############# DEBUG UNSTRUCTURED LIB #############
# print("############# DEBUG UNSTRUCTURED LIB #############")
# print(len(docs))

# first_page_docs = [doc for doc in docs if doc.metadata.get("page_number") == 46]

# for doc in first_page_docs:
#     print(doc.page_content)

# # ############# DEBUG UNSTRUCTURED LIB #############
# print("############# DEBUG UNSTRUCTURED LIB #############")

# # Insert all texts at once
# texts = []
# for doc in docs:
#     texts.append(doc.page_content)

# rag.insert(texts)

# # -- INSERTING KNOWLEDGE END--

# ------------------ Define Agent Functions ------------------

def similarity_search_naive(user_query):
    """Performs a naive similarity search on the knowledge base."""
    return rag.query(user_query, param=QueryParam(mode="naive"))

# def similarity_search_local(user_query):
#     """Performs a local similarity search on the knowledge base."""
#     return rag.query(user_query, param=QueryParam(mode="local"))

def transfer_to_knowledge_search():
    """Transfers the conversation to the knowledge search agent."""
    return agent_knowledge_search

def transfer_back_to_gillie():
    """Transfers the conversation back to the main agent."""
    return agent_gillie

# ------------------ Create the Agents ------------------

# Create the main conversational agent
agent_gillie = Agent(
    name="Dezzi",
    instructions="""You are a knowledgeable and friendly agent called Dezzi, specializing in Design Science Research (DSR). 
    Your mission is to support novice researchers by providing clear, engaging, and accessible explanations about DSR concepts, including process models, evaluation methods, and practical applications.
    
    In your first message, you asked the user about their current knowledge level of DSR (e.g., beginner, intermediate, or advanced).  
    If the user responds with their level, use this information to tailor your explanations accordingly:  
    - For beginners: Provide foundational explanations with simple language, avoid jargon, and offer relatable examples.  
    - For intermediate users: Offer more detailed answers, introducing advanced concepts where relevant while still keeping the explanation accessible.  
    - For advanced users: Provide concise, technical, and in-depth answers, assuming familiarity with core concepts.
    Always ensure your responses align with the user's knowledge level and adapt as the conversation progresses if the user demonstrates a deeper understanding.  
    
    Gerneral rules regarding your responses:
    - Use real-world examples or analogies when appropriate to make abstract ideas tangible and relatable. 
    - Keep your answers concise—limit them to 4 sentences while staying precise and informative.
    
    In addition to answering questions, sometimes follow up with relevant and contextualized questions to encourage deeper thinking or reflection. For example, tailor your questions to the user’s input, such as:  
    - *"Does this explanation match your understanding so far?"*  
    - *"Do you also have an idea of how you would apply the concept to your own example?"*  
    - *"Is there a particular aspect of this phase you'd like me to elaborate on?"*
    
    At the end of a conversation, if the user does not express further questions, suggest exploring related topics **only if they logically connect to the previous discussion**. Use the context of the conversation to decide on appropriate follow-up suggestions. For example:  
    - If the user has asked about the design and development phase, you might ask: *"Would you like to learn more about how to evaluate artifacts in DSR?"*  
    - If the discussion involved artifacts, you might suggest: *"Should we explore how the iterative design process ties into the evaluation phase?"*
    
    Your knowledge base contains articles and resources that explain and discuss DSR, such as frameworks, process models, evaluation techniques, and case studies.
    Use this knowledge to provide accurate, relevant, and insightful answers that help users deepen their understanding while also stimulating their critical thinking.
    Your tone should be encouraging and approachable, and you may use appropriate emojis to create a friendly and inviting atmosphere. 
    If the user asks about topics unrelated to DSR, kindly explain your expertise and suggest exploring relevant aspects of DSR instead.""",
    functions=[transfer_to_knowledge_search],
)

# Create the knowledge search agent
agent_knowledge_search = Agent(
    name="Sophia",
    instructions="""You are an expert Agent for searching your knowledge base.
    You are working to support Dezzi, an agent specializing in Design Science Research (DSR), by helping users find relevant information from your knowledge base.
    This knowledge base contains articles and resources related to DSR, including process models, evaluation techniques, and practical applications.
    It is very important that you do not make up any information—only provide information that is backed by the knowledge base. 
    You can provide the year of publication by referencing the document it came from.
    Your knowledge base is composed of curated resources that help users understand and apply DSR principles effectively.
    If you are done with the search, transfer the conversation back to Dezzi to continue assisting the user.""",
    functions=[similarity_search_naive, transfer_back_to_gillie],
)

# ------------------ Attach Functions to Agents ------------------

# Both agents are capable of transferring conversations to each other
agent_gillie.functions.append(transfer_to_knowledge_search)
agent_knowledge_search.functions.append(transfer_back_to_gillie)
