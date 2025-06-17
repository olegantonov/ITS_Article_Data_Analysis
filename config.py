"""Global configuration for data paths used by the analysis scripts."""
import os
from pathlib import Path

# Base directory for all raw and processed data
# Use the environment variable ANAC_DATA_DIR to override the default `./data`
BASE_DIR = Path(os.getenv("ANAC_DATA_DIR", Path.cwd() / "data")).resolve()
RAW_DIR = BASE_DIR / "raw"
ANALYSIS_DIR = BASE_DIR / "analysis"

# Ensure directories exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
