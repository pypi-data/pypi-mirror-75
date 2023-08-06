import pandas as pd
import numpy as np


class Logger(object):

    def __init__(self, name):
        self.name = 'benchmark.' + name
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def to_pandas(self, header):
        df = pd.DataFrame(columns=header)
        for row in self.rows:
            df = df.append(
                dict(zip(header, row)), ignore_index=True
            )
        return df

    def backup(self, header):
        df = self.to_pandas(header)
        df.to_csv(self.name + '.csv')


def dump_embeddings(embeddings, labels, id_):

    embeddings = np.array(embeddings).astype(float)
    labels = np.array(labels).astype(float).reshape(-1, 1)

    data = np.concatenate((embeddings, labels), 1)
    np.savetxt('embeddings-' + str(id_) + '.csv', data)
