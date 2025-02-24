from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_neo4j import Neo4jGraph
from neo4j_graphrag.retrievers import HybridRetriever
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
from neo4j import GraphDatabase
from certainty_estimator.predict_certainty import CertaintyEstimator
from simpletransformers.ner import NERModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

load_dotenv()
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
embeddings = OpenAIEmbeddings()
estimator = CertaintyEstimator('sentence-level')
hedge_model = NERModel(
    'bert',
    'jeniakim/hedgehog',
    use_cuda=False,
    labels=["C", "D", "E", "I", "N"],
)
tokenizer = AutoTokenizer.from_pretrained("finiteautomata/bertweet-base-sentiment-analysis")
conviction_model = AutoModelForSequenceClassification.from_pretrained("finiteautomata/bertweet-base-sentiment-analysis")

# estimator = CertaintyEstimator('sentence-level',cuda=True)

openai_llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

retriever = HybridRetriever(
    driver=driver,
    vector_index_name="reviewEmbeddings",
    fulltext_index_name="reviewFullText",
    embedder=embeddings,
    return_properties=["review", "certainty","conviction", "hedge", "id","confidence","rating"],
)

llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
rag = GraphRAG(retriever=retriever, llm=llm)
