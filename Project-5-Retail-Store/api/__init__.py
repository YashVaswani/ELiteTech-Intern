"""FastAPI serving layer for the trained segmentation model.

Thin on purpose: all the actual ML logic lives in, and is unit-tested in,
`retail_segmentation`. This package only adapts that library to HTTP.
"""
