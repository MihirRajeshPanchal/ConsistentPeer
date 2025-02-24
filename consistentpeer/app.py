from consistentpeer.endpoints import counterfactual, graph, vector, query
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(graph.router)
app.include_router(vector.router)
app.include_router(query.router)
app.include_router(counterfactual.router)

@app.get("/")
def root():
    return {"message": "Welcome to consistentpeer!"}