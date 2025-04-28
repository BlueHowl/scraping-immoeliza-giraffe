import re
from pathlib import Path

import pandas as pd

columns_refs = [
    "propertyid",
    "localityname",
    "postalcode",
    "typeoproperty",
    "subtypeofproperty",
    "price",
    "typeofsale",
    "numberofrooms",
    "livingarea",
    "equippedkitchen",
    "furnished",
    "openfire",
    "terrace",
    "garden",
    "surfaceofgood",
    "numberoffacades",
    "swimmingpool",
    "stateofbuilding"
]
path = Path(".")
csv_paths = list(path.rglob("*.csv"))


def test_csv_exists():
    assert len(csv_paths) > 0

def test_columns():
    df = pd.read_csv(csv_paths[0])
    cols = [re.sub("[ \s\t]", "", c.lower()) for c in df.columns]
    assert set(columns_refs).issubset(cols)


def test_data_size():
    df = pd.read_csv(csv_paths[0])
    cols = [re.sub("[ \s\t]", "", c.lower()) for c in df.columns]
    df.columns = cols
    assert len(df.propertyid.unique()) >= 10000


def test_data_types():
    df = pd.read_csv(csv_paths[0])
    cols = [re.sub("[ \s\t]", "", c.lower()) for c in df.columns]
    df.columns = cols
    for x in ["price", "furnished", "numberofrooms", "openfire"]:
        assert df[x].dtype in ["float64", "int64"]
