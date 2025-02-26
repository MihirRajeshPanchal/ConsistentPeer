# **ConsistentPeer: GraphRAG-Driven Counterfactual Insights for Evaluating Reviewer Consistency in Peer Review**  

This repository contains the dataset, code, and methodologies developed for the research project, *ConsistentPeer: GraphRAG-Driven Counterfactual Insights for Evaluating Reviewer Consistency in Peer Review*.  

The project introduces a **Consistency Score**, designed to assess alignment between textual review content and assigned confidence scores, ensuring transparency in the peer review process. The study leverages **Knowledge Graphs, Counterfactual Reasoning, and Retrieval-Augmented Generation (RAG)** to identify inconsistencies in self-reported reviewer confidence levels.  

---

![image](https://github.com/user-attachments/assets/1a68e1b0-f2e1-4594-a981-548f0db58776)

## **Folder Structure**  

```plaintext
├── LICENSE
├── .gitattributes
├── .gitignore
├── README.md
├── consistentpeer/
│   ├── app.py                      # Main application file (FastAPI)
│   ├── requirements.txt             # Required dependencies
│   ├── constants/
│   │   ├── consistentpeer.py
│   │   └── graph.py
│   ├── endpoints/
│   │   ├── counterfactual.py        # Counterfactual analysis on reviews
│   │   ├── graph.py                 # Graph-based consistency evaluation
│   │   ├── query.py                 # Query mechanisms for reviews
│   │   └── vector.py                 # Vector similarity-based retrieval
│   ├── models/
│   │   ├── counterfactual.py
│   │   ├── graph.py
│   │   └── query.py
│   ├── utils/
│   │   ├── certainty.py             # Certainty analysis functions
│   │   ├── conviction.py            # Conviction scoring implementation
│   │   ├── counterfactual.py        # Counterfactual scenario evaluation
│   │   ├── graph.py                 # Graph utilities and functions
│   │   ├── hedge.py                 # Hedge detection and scoring
│   │   └── vector.py                # Vector-based retrieval utilities
└── notebooks/
    ├── graph-create-certainty.ipynb # Notebook for knowledge graph creation
    └── hedge-certainty-conviction-results.ipynb # Experiment results
```

---

## **Project Overview**  

### **Objective**  
The project aims to enhance fairness and transparency in peer reviews by:  
1. **Quantifying Review Consistency**: Introduces a **Consistency Score** based on conviction, certainty, rating, and hedge values.  
2. **Identifying Misleading Reviews**: Detects cases where reviewers overestimate or underestimate their confidence in assessments.  
3. **Leveraging Knowledge Graphs**: Visualizes relationships between review text, confidence scores, and critique depth.  
4. **Using Counterfactual Reasoning**: Simulates alternate confidence scores based on review textual depth.  
5. **Automating Consistency Evaluation**: Uses GraphRAG for efficient retrieval and structured reasoning.  

---

## **Dataset**  
- **Source**: Peer reviews from OpenReview (ICLR 2017-2020, NeurIPS 2016-2019).  
- **Key Attributes**:  
  - **Review Text**: Full-text content of the peer review.  
  - **Confidence Score**: Self-reported reviewer confidence.  
  - **Rating**: Reviewer’s overall recommendation for the paper.  
  - **Hedge Score**: Quantifies uncertainty in the review text.  
  - **Certainty Score**: Evaluates linguistic confidence in statements.  
  - **Conviction Score**: Measures assertiveness and logical cohesion.  
- **Graph Representation**: Data is stored in a **Neo4j knowledge graph** for structured querying and retrieval.  

---

## **Installation & Running the API**  

1. **Install Dependencies**  
```sh
pip install -r requirements.txt
```

2. **Start the API Server**  
```sh
uvicorn consistentpeer.app:app --reload
```
This launches a **FastAPI server** at `http://127.0.0.1:8000/`.  

3. **Access API Documentation**  
Visit `http://127.0.0.1:8000/docs` for interactive API endpoints.  

---

### **Our Contributions**  

- In this paper, we propose a **novel pipeline** that leverages **graphs** to visualize the relationships between **review text, confidence score, rating, and aspect categories**.  
- Additionally, we demonstrate both the **practical applications** and **theoretical implications** of the proposed pipeline, including the use of **counterfactual reasoning** to make informed decisions.  
- Finally, we present a **complete pipeline** to **identify and resolve inconsistencies** in review text and its **cohesiveness** with **self-annotated confidence scores and ratings**.

---

## **Contact**  

For queries, reach out to:  
- **Prabhat Kumar Bharti**: [dept.csprabhat@gmail.com](mailto:dept.csprabhat@gmail.com)  
- **Mihir Panchal**: [mihirpanchal5400@gmail.com](mailto:mihirpanchal5400@gmail.com)  
- **Viral Dalal**: [viraldalal04@gmail.com](mailto:viraldalal04@gmail.com)  

---

## **License**  

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.  

---
