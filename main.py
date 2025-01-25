from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from models import load_models, embed_text
from db import filter_channels_from_db
import faiss
import numpy as np

app = FastAPI()

# Load models
embedder, rank_model = load_models()

class FilterCriteria(BaseModel):
    category: str
    price_range: List[float]
    min_subs: int
    max_subs: int

class Channel(BaseModel):
    id: int
    name: str
    positive_frac: float
    estimated_price: float
    # Add other fields as necessary

@app.post("/get_channels/")
def get_channels(ad_text: str, 
                 filters: FilterCriteria,
                 num_channels: int = 50) -> List[Dict[str, Any]]:
    embedding = embed_text(embedder, ad_text)

    filtered_channels = filter_channels_from_db(filters.dict())

    if not filtered_channels:
        raise HTTPException(status_code=404, detail="No channels found with the given filters")

    index = faiss.IndexFlatL2(len(embedding))
    channel_embeddings = [ch["embedding"] for ch in filtered_channels]
    index.add(np.array(channel_embeddings))

    # Retrieve top 50 similar channels
    _, top_indices = index.search(np.array([embedding]), num_channels)
    top_channels = [filtered_channels[i] for i in top_indices[0]]

    features = np.array([
        [ch["positive_frac"], ch["estimated_price"]] for ch in top_channels
    ])
    rankings = rank_model.predict(features)

    for i, channel in enumerate(top_channels):
        channel["ranking"] = rankings[i]

    return sorted(top_channels, key=lambda x: x["ranking"], reverse=True) 