"""Pydantic request/response models for the segmentation API."""

from pydantic import BaseModel, Field


class Overview(BaseModel):
    customers: int
    segments: int
    avg_monetary: float
    k: int


class SegmentSummary(BaseModel):
    segment: str
    customers: int
    avg_recency_days: float
    avg_frequency: float
    avg_monetary: float


class Customer(BaseModel):
    customer_id: int
    recency: float
    frequency: float
    monetary: float
    cluster: int
    segment: str


class KScorePoint(BaseModel):
    k: int
    inertia: float
    silhouette: float


class ClusterPoint(BaseModel):
    pc1: float
    pc2: float
    cluster: int
    segment: str


class PredictRequest(BaseModel):
    recency: float = Field(ge=0, description="Days since the customer's last purchase")
    frequency: float = Field(gt=0, description="Number of orders placed")
    monetary: float = Field(ge=0, description="Total amount spent")


class PredictResponse(BaseModel):
    cluster: int
    segment: str
