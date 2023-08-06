from typing import List

import numpy as np
import pandas as pd


def embeddings_to_pandas(embeddings: np.ndarray,
                         labels: List[int],
                         filenames: List[str]) -> pd.DataFrame:
    """Creates pandas dataframe from embeddings, labels and filenames

    Args:
        embeddings: 2-dimensional numpy array containing embeddings
        labels: List of label number (e.g. different subfolders)
        filenames: List of filenames

    Returns:
        Pandas dataframe ready to be saved to csv
    """
    all_equal_length = True
    all_equal_length = all_equal_length and (len(embeddings) == len(labels))
    all_equal_length = all_equal_length and (len(labels) == len(filenames))

    if not all_equal_length:
        raise ValueError(f'Length of embeddings {len(embeddings)} \
            labels ({len(labels)}) and filenames ({len(filenames)}) \
            do not match!')
    df = pd.DataFrame.from_records(embeddings)
    df.index = filenames
    df["label"] = labels
    df = df.reset_index()
    cols = ['filename']
    cols += [f'embedding_{i}' for i in range(embeddings.shape[1])]
    cols += ['label']
    df.columns = cols
    return df


def pandas_to_dict(df: pd.DataFrame) -> dict:
    """Converts pandas dataframe into dictionary with proper format for uploading

    Args:
        df: Pandas dataframe with embeddings and filenames

    Returns:
        A dictionary
    """
    columns = list(df)
    embedding_columns = list(filter(lambda x: 'embedding' in x, columns))
    embeddings = df[embedding_columns].values.tolist()
    filenames = [row for row in df['filename']]
    labels = [row for row in df['label']]
    data = {}
    data['embeddingName'] = 'default'
    data['embeddings'] = []
    for (embedding, fname, label) in zip(embeddings, filenames, labels):
        item = {}
        item['fileName'] = fname
        item['value'] = embedding
        item['label'] = label
        data['embeddings'].append(item)

    return data
