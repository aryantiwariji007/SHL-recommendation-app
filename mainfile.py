from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

app = FastAPI(title="SHL Assessment Recommendation API")


assessment_catalog = [
    {
        "name": "Agile Testing (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/agile-testing-new/",
        "remote_testing": "Yes",
        "adaptive_irt": "No",
        "duration_mins": 13,
        "type": "Knowledge & Skills"
    },
    {
        "name": "Manual Testing (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/manual-testing-new/",
        "remote_testing": "Yes",
        "adaptive_irt": "Yes",
        "duration_mins": 14,
        "type": "Knowledge & Skills"
    },
    {
        "name": "Leadership Judgement Indicator",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/leadership-judgement-indicator/",
        "remote_testing": "Yes",
        "adaptive_irt": "Yes",
        "duration_mins": 35,
        "type": "Situational Judgement"
    },
    {
        "name": "Verify Numerical Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-numerical-ability/",
        "remote_testing": "Yes",
        "adaptive_irt": "Yes",
        "duration_mins": 20,
        "type": "Cognitive Ability"
    },
    {
        "name": "Global Skills Assessment",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/global-skills-assessment/",
        "remote_testing": "Yes",
        "adaptive_irt": "Yes",
        "duration_mins": 16,
        "type": "Competencies, Knowledge & Skills"
    },
    {
        "name": "Operations Management",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/operations-management-new/",
        "remote_testing": "Yes",
        "adaptive_irt": "Yes",
        "duration_mins": 7,
        "type": "Knowledge and Skills"
    },
    {
        "name": "Occupational Personality Questionnaire (OPQ)",
        "url": "https://www.shl.com/solutions/products/assessments/personality-assessment/shl-occupational-personality-questionnaire-opq/",
        "remote_testing": "Yes",
        "adaptive_irt": "No",
        "duration_mins": 30,
        "type": "Personality Assessment"
    },
    {
        "name": "Verify Inductive Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-inductive-reasoning-2014/",
        "remote_testing": "Yes",
        "adaptive_irt": "Yes",
        "duration_mins": 25,
        "type": "Cognitive Ability"
    }
]

class RecommendationRequest(BaseModel):
    input_query: str

class Assessment(BaseModel):
    name: str
    url: str
    remote_testing: str
    adaptive_irt: str
    duration_mins: int
    type: str

class RecommendationResponse(BaseModel):
    input_query: str
    recommended_assessments: List[Assessment]

@app.post("/recommend", response_model=RecommendationResponse)
def recommend_assessments(request: RecommendationRequest):
    query = request.input_query.lower()
    results = []

    for item in assessment_catalog:
        score = 0
        if re.search(re.escape(item["type"].lower()), query):
            score += 1
        if "adaptive" in query and item["adaptive_irt"] == "Yes":
            score += 1
        if "remote" in query and item["remote_testing"] == "Yes":
            score += 1
        if re.search(r"numerical|logical|reasoning", query) and "reasoning" in item["name"].lower():
            score += 1

        if score > 0:
            results.append((item, score))

    results.sort(key=lambda x: x[1], reverse=True)
    recommended = [x[0] for x in results[:10]]

    return RecommendationResponse(
        input_query=request.input_query,
        recommended_assessments=recommended
    )
