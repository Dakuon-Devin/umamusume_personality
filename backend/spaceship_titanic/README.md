# Spaceship Titanic Competition

## Overview
This project aims to predict which passengers aboard the Spaceship Titanic were transported to an alternate dimension during a collision with a spacetime anomaly. The project is part of a Kaggle competition: [Spaceship Titanic](https://www.kaggle.com/competitions/spaceship-titanic).

## Project Structure
```
spaceship_titanic/
├── data/           # Data files (will contain train.csv and test.csv)
├── src/           # Source code
    ├── __init__.py
    ├── setup_kaggle.py      # Kaggle API setup
    ├── verify_kaggle_access.py  # Verify Kaggle API access
    ├── download_data.py     # Download competition data
    └── inspect_data.py      # Basic data inspection
```

## Setup Status
- [x] Project structure created
- [ ] Kaggle API authentication
- [ ] Data download
- [ ] Initial data inspection

## Getting Started
1. Install dependencies:
```bash
poetry install
```

2. Configure Kaggle API authentication:
```bash
python src/setup_kaggle.py
```

3. Download competition data:
```bash
python src/download_data.py
```

4. Inspect downloaded data:
```bash
python src/inspect_data.py
```

## Notes
- Competition data will be downloaded to the `data/` directory
- Kaggle API credentials are required for data download
