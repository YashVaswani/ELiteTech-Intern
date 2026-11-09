"""FastAPI app serving the trained K-means segmentation model.

Run directly with: uvicorn api.main:app --reload --port 8000
All the heavy lifting (RFM, K-means, labeling) already happened in
`retail-segment train`; this just reads the resulting CSV/model artifacts
into memory once at startup and exposes them over HTTP.
"""

from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from api.schemas import (
    ClusterPoint,
    Customer,
    KScorePoint,
    Overview,
    PredictRequest,
    PredictResponse,
    SegmentSummary,
)
from retail_segmentation.config import load_config
from retail_segmentation.insights import pca_2d
from retail_segmentation.model import FEATURE_COLUMNS, load_pipeline

state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg = load_config()
    model_path = Path(cfg["model"]["artifact_path"])
    labeled_path = Path(cfg["model"]["labeled_output_path"])
    if not model_path.exists() or not labeled_path.exists():
        raise RuntimeError(
            "No trained model found. Run `retail-segment train` before starting the API "
            "(see the README for setup instructions)."
        )

    state["cfg"] = cfg
    state["pipeline"] = load_pipeline(str(model_path))
    state["labeled"] = pd.read_csv(labeled_path)

    k_scores_path = Path(cfg["reports"]["k_scores_path"])
    state["k_scores"] = pd.read_csv(k_scores_path) if k_scores_path.exists() else pd.DataFrame()

    transformed = state["pipeline"][:-1].transform(state["labeled"][FEATURE_COLUMNS])
    coords, _ = pca_2d(transformed)
    state["pca_coords"] = coords

    yield
    state.clear()


app = FastAPI(title="Retail Customer Segmentation API", lifespan=lifespan)


def _segment_by_cluster() -> pd.Series:
    labeled = state["labeled"]
    return labeled.drop_duplicates("cluster").set_index("cluster")["segment"]


@app.get("/api/health", response_class=PlainTextResponse)
def health() -> str:
    return "ok"


@app.get("/api/overview", response_model=Overview)
def overview() -> Overview:
    labeled = state["labeled"]
    return Overview(
        customers=len(labeled),
        segments=labeled["segment"].nunique(),
        avg_monetary=round(float(labeled["monetary"].mean()), 2),
        k=labeled["cluster"].nunique(),
    )


@app.get("/api/segments/summary", response_model=list[SegmentSummary])
def segments_summary() -> list[SegmentSummary]:
    labeled = state["labeled"]
    summary = (
        labeled.groupby("segment")
        .agg(
            customers=("customer_id", "count"),
            avg_recency_days=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
        )
        .round(1)
        .sort_values("avg_monetary", ascending=False)
        .reset_index()
    )
    return [SegmentSummary(**row) for row in summary.to_dict(orient="records")]


@app.get("/api/segments/{segment}/customers", response_model=list[Customer])
def segment_customers(segment: str) -> list[Customer]:
    labeled = state["labeled"]
    subset = labeled[labeled["segment"] == segment]
    if subset.empty and segment not in labeled["segment"].unique():
        raise HTTPException(status_code=404, detail=f"Unknown segment: {segment}")
    return [Customer(**row) for row in subset.to_dict(orient="records")]


@app.get("/api/segments/{segment}/export")
def export_segment_csv(segment: str) -> Response:
    labeled = state["labeled"]
    subset = labeled[labeled["segment"] == segment]
    if subset.empty and segment not in labeled["segment"].unique():
        raise HTTPException(status_code=404, detail=f"Unknown segment: {segment}")
    filename = f"{segment.lower().replace(' ', '_')}.csv"
    return Response(
        content=subset.to_csv(index=False),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/api/k-selection", response_model=list[KScorePoint])
def k_selection() -> list[KScorePoint]:
    return [KScorePoint(**row) for row in state["k_scores"].to_dict(orient="records")]


@app.get("/api/clusters", response_model=list[ClusterPoint])
def clusters() -> list[ClusterPoint]:
    labeled = state["labeled"]
    coords = state["pca_coords"]
    return [
        ClusterPoint(
            pc1=float(coords[i, 0]), pc2=float(coords[i, 1]), cluster=int(row.cluster), segment=row.segment
        )
        for i, row in enumerate(labeled.itertuples())
    ]


@app.post("/api/predict", response_model=PredictResponse)
def predict(body: PredictRequest) -> PredictResponse:
    row = pd.DataFrame([body.model_dump()])
    cluster = int(state["pipeline"].predict(row[FEATURE_COLUMNS])[0])
    segment = _segment_by_cluster().get(cluster, f"Segment {cluster}")
    return PredictResponse(cluster=cluster, segment=segment)


# Serve the built React app (if present) so a single container/process can
# host both the API and the UI - no separate web server needed in production.
_frontend_dist = Path(__file__).resolve().parents[1] / "frontend" / "dist"
if _frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(_frontend_dist), html=True), name="frontend")
