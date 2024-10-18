import json
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
import requests

def load_parquet_config(data_name):
    """Helper function to load parquet and config JSON for a given dataset."""
    # Load parquet data
    data_url = f"https://github.com/soda-inria/carte/blob/main/data/single_tables/{data_name}.parquet?raw=true"
    data_pd = pd.read_parquet(data_url)
    data_pd.fillna(value=np.nan, inplace=True)

    # Load config data
    config_url = f"https://raw.githubusercontent.com/soda-inria/carte/main/data/single_tables/config_{data_name}.json"
    response = requests.get(config_url)

    if response.status_code == 200:
        config_data = response.json()
    else:
        raise FileNotFoundError(f"Config file not found for {data_name}. Status code: {response.status_code}")

    return data_pd, config_data

def set_split(data, config_data, num_train, random_state=42):
    """Helper function to split dataset into train and test."""
    # Extract target and features
    target_name = config_data["target_name"]
    X = data.drop(columns=target_name)
    y = data[target_name].to_numpy()

    if config_data.get("repeated", False):
        entity_name = config_data["entity_name"]
    else:
        entity_name = np.arange(len(y))

    groups = np.array(data.groupby(entity_name).ngroup())
    num_groups = len(np.unique(groups))

    gss = GroupShuffleSplit(
        n_splits=1,
        test_size=int(num_groups - num_train),
        random_state=random_state
    )

    idx_train, idx_test = next(iter(gss.split(X, y, groups=groups)))
    X_train, X_test = X.iloc[idx_train], X.iloc[idx_test]
    y_train, y_test = y[idx_train], y[idx_test]
    
    return X_train, X_test, y_train, y_test

# Define individual methods for each dataset

def spotify(num_train, random_state=42):
    """Load and split Spotify dataset."""
    data, config_data = load_parquet_config('spotify')
    return set_split(data, config_data, num_train, random_state)

def wina_pl(num_train, random_state=42):
    """Load and split Wina_PL dataset."""
    data, config_data = load_parquet_config('wine_pl')
    return set_split(data, config_data, num_train, random_state)

def wine_dot_com_prices(num_train, random_state=42):
    """Load and split Wine.com prices dataset."""
    data, config_data = load_parquet_config('wine_dot_com_prices')
    return set_split(data, config_data, num_train, random_state)

def wine_vivino_price(num_train, random_state=42):
    """Load and split Vivino wine prices dataset."""
    data, config_data = load_parquet_config('wine_vivino_price')
    return set_split(data, config_data, num_train, random_state)

# Example usage
#if __name__ == "__main__":
#    num_train = 1000  # Example: number of training entities
#    random_state = 42

    # Load and split each dataset
#    X_train_spotify, X_test_spotify, y_train_spotify, y_test_spotify = spotify(num_train, random_state)
#    print("Spotify dataset:", X_train_spotify.shape, X_test_spotify.shape)

#    X_train_wina, X_test_wina, y_train_wina, y_test_wina = wina_pl(num_train, random_state)
#    print("Wina_PL dataset:", X_train_wina.shape, X_test_wina.shape)

#    X_train_wine_dot, X_test_wine_dot, y_train_wine_dot, y_test_wine_dot = wine_dot_com_prices(num_train, random_state)
#    print("Wine.com Prices dataset:", X_train_wine_dot.shape, X_test_wine_dot.shape)

#    X_train_vivino, X_test_vivino, y_train_vivino, y_test_vivino = wine_vivino_price(num_train, random_state)
#    print("Vivino Wine Prices dataset:", X_train_vivino.shape, X_test_vivino.shape)