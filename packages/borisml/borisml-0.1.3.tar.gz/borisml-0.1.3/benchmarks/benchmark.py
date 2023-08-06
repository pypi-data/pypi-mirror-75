import numpy as np
import torch
import sys
import os

import hydra

import boris.sampling as sampling

from configure import configure_embedding
from configure import configure_evaluatable
from configure import configure_trainable
from helpers import init_seed
from helpers import load_config_file
from log import Logger
from log import dump_embeddings

HYDRA_PATH_PREFIX = '../../../config/'


@hydra.main(config_path='config/config.yaml', strict=False)
def main(cfg):
    """
        BENCHMARK TIME COMPLEXITY:
        the benchmark trains and evaluates:

            #repetitions x #embedding_configs x #sample_configs x #percentages
            -> this takes a LOT of time!
    """

    # redirect output
    out = open('benchmark.log.txt', 'w')
    sys.stdout = out

    # benchmark every ten percent of the dataset
    sample_percentages = np.arange(.25, 1.1, .25)

    # check for cuda
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    # if a sampler_cfg file was passed -> use it, otherwise load all
    sampler_cfg = []
    if cfg['sampler_cfg']:
        path_to_config = os.path.join(HYDRA_PATH_PREFIX, 'sampler/')
        path_to_config = os.path.join(path_to_config, cfg['sampler_cfg'])
        sampler_cfg = [path_to_config]
    else:
        path_to_config = os.path.join(HYDRA_PATH_PREFIX, 'sampler/')
        files = os.listdir(path_to_config)
        sampler_cfg = [path_to_config + cfg for cfg in files]

    # if an embedding_cfg file was passed -> use it, otherwise load all
    embedding_cfg = []
    if cfg['embedding_cfg']:
        path_to_config = os.path.join(HYDRA_PATH_PREFIX, 'embedding/')
        path_to_config = os.path.join(path_to_config, cfg['embedding_cfg'])
        embedding_cfg = [path_to_config]
    else:
        path_to_config = os.path.join(HYDRA_PATH_PREFIX, 'embedding/')
        files = os.listdir(path_to_config)
        embedding_cfg = [path_to_config + cfg for cfg in files]

    # initialize the logger to keep track of results
    log = Logger(cfg['name'])

    # run benchmark n_repetitions times for each setting
    for rep in range(cfg['n_repetitions']):

        # fix seed for reproducibility
        init_seed(rep)

        # run benchmark for each embedding configuration
        for i in range(len(embedding_cfg)):

            try:

                # get new embedding model
                embedding_cfg_inst = load_config_file(embedding_cfg[i])

                embedding_model, embedding_loader = \
                    configure_embedding(embedding_cfg_inst,
                                        cfg['training']['data'],
                                        cfg['training']['transform'])

                # train embedding and get embeddings
                embedding_model = embedding_model.train_embedding(
                    **embedding_cfg_inst['trainer'])

                embeddings, labels, _ = embedding_model.embed(
                    embedding_loader, device=device)

                dump_embeddings(embeddings, labels, rep)

                embeddings = torch.from_numpy(
                    embeddings.astype(float)
                    ).float().to(device)

                # run benchmark for each sampler configuration
                for j in range(len(sampler_cfg)):

                    # load sample cfg file
                    sampler_cfg_inst = load_config_file(sampler_cfg[j])

                    # make new sampling state
                    n_data = embeddings.shape[0]
                    selected = torch.zeros(n_data).bool().to(device)
                    state = (n_data, selected, embeddings, None)

                    n_samples = int(sample_percentages[0] * n_data)

                    # run benchmark for each sample percentage
                    for k in range(len(sample_percentages)):

                        # sample
                        print(sampler_cfg_inst)
                        state, _ = sampling.sample(n_samples, state,
                                                   **sampler_cfg_inst)

                        # train
                        trainable, trainer = configure_trainable(cfg, state)
                        trainer.fit(trainable)

                        # evaluate
                        evaluatable = configure_evaluatable(cfg)
                        evaluatable.evaluate(trainable, device=device)

                        # make a backup of the results
                        row = [rep]
                        row += [os.path.basename(embedding_cfg[i])]
                        row += [os.path.basename(sampler_cfg[j])]
                        row += [sample_percentages[k]]
                        row += [
                            metric.result
                            for metric in evaluatable.eval_metrics
                        ]
                        log.add_row(row)

                        header = ['run_id']
                        header += ['embedding_model']
                        header += ['sampling_strategy']
                        header += ['sample_percentage']
                        header += [
                            metric.identifier
                            for metric in evaluatable.eval_metrics
                        ]
                        log.backup(header)

                        if not cfg['active_learning']:
                            # make new sampling state
                            selected = torch.zeros(n_data).bool().to(device)
                            state = (n_data, selected, embeddings, None)
                            if k + 1 < len(sample_percentages):
                                n_samples = sample_percentages[k+1] * n_data
                                n_samples = int(n_samples)
                        else:
                            state = (n_data, selected, embeddings, None)
                            n_samples = int(sample_percentages[0] * n_data)

            except KeyError:
                print('WARNING: Benchmark encountered: KeyError!')
                print('Skipping iteration...')
            except NotImplementedError:
                print('WARNING: Benchmark encountered: NotImplementedError!')
                print('Skipping iteration...')
            except ValueError:
                print('WARNING: Benchmark encountered: ValueError!')
                print('Skipping iteration...')


if __name__ == '__main__':
    main()
