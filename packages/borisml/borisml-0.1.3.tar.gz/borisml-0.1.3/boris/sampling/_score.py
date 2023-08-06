import torch
import numpy as np


def _inf(M=1, eps=1e-8):
    return M + eps


def _pairwise_distance(X, Y):
    X_norm = (X ** 2).sum(1).view(-1, 1)
    Y_norm = (Y ** 2).sum(1).view(1, -1)
    XY = torch.mm(X, torch.transpose(Y, 0, 1))
    return X_norm + Y_norm - 2*XY


def _random_score_fn(state):
    """ random sampling score

    """
    n_data, selected, embeddings, scores = state
    return torch.randn_like(selected.float())


def _coreset_score_fn(state):
    """ coreset sampling score

    """

    n_data, selected, embeddings, uscores = state

    selected_clone = selected.clone()
    sscores = torch.zeros_like(selected).float()

    choice, nn_dist = None, None
    if not selected_clone.any():
        # make initial selection
        choice = torch.randint(0, n_data, [1]).to(selected.device)
        selected_clone[choice] = True
        nn_dist = torch.norm(embeddings - embeddings[choice], dim=1).pow(2)
        nn_dist_tmp = nn_dist if uscores is None else nn_dist * uscores
        sscores[choice] = nn_dist_tmp.max()

    n_selected = selected_clone.sum()
    while n_selected < n_data:

        batch = embeddings[~selected_clone]

        if choice is None:
            nn_dist = torch.zeros_like(selected).float()
            nn_dist[~selected_clone], _ = _pairwise_distance(
                batch, embeddings[selected_clone]
                ).min(1)
        else:
            dist = torch.norm(batch - embeddings[choice], dim=1).pow(2)
            nn_dist[~selected_clone] = torch.min(
                nn_dist[~selected_clone], dist)

        nn_dist_tmp = nn_dist if uscores is None else nn_dist * uscores

        sscore, choice = nn_dist_tmp.max(-1)
        selected_clone[choice] = True
        nn_dist[choice] = -_inf()
        sscores[choice] = sscore
        n_selected += 1

    sscores[selected] = _inf(sscores.max())
    return sscores


def _bit_score_fn(state, depth=None):
    """ quick but memory intense

    """

    n_data, selected, embeddings, scores = state
    _, n_dim = embeddings.shape

    if depth is None:
        # n_data ~= C * 2 ** (n_dim * depth)
        depth = int(np.log2(n_data)) - n_dim
        depth = max(min(8, depth), 1)

    if depth > 8:
        raise ValueError('Illegal depth (depth > 8): {}'.format(depth))

    if depth * n_dim > 62 or depth * n_dim <= 0:
        raise ValueError(
            'Illegal combination of depth {} and number of dimensions {}! \
            Requires 0 < depth * n_dim <= 64'
            .format(depth, n_dim))

    bitreps = torch.zeros_like(selected).long()

    m, _ = embeddings.min(0)
    M, _ = embeddings.max(0)

    intreps = (embeddings - m - 1e-5) / (M - m)
    intreps[intreps < 0.] = 0.
    intreps *= 2 ** depth
    intreps = intreps.long()

    bitreps = torch.zeros_like(selected).long()
    for d in range(n_dim):
        exp = (n_dim - d - 1) * depth
        shift = 2 ** exp
        bitreps += intreps[:, d] * shift

    sscores = torch.zeros_like(selected).float()
    lookup = {}

    # add previously selected to lookup
    sscores[selected] = _inf()
    indices = selected.nonzero()
    for i in indices:
        bitrep = bitreps[i].item()
        lookup[bitrep] = 1

    # sample next set
    indices = (~selected).nonzero()
    for i in indices[torch.randperm(len(indices))]:
        bitrep = bitreps[i].item()
        if lookup.get(bitrep) is None:
            lookup[bitrep] = 1
            sscores[i] = 1.
        else:
            lookup[bitrep] += 1
            sscores[i] = 1. / lookup[bitrep]

    # add tiny noise
    sscores = torch.normal(sscores,
                           1e-6 * torch.ones(n_data).to(selected.device))

    return sscores


def _uncertainty_score_fn(state):
    """Returns the uncertainty score for each sample.
       Useful for active learning without diversity sampling.

    """
    _, selected, _, scores = state
    if scores is None:
        msg = 'Uncertainty scores in state must not be None! '
        msg += 'Received state (_, _, _, uscore) = {}'.format(state)
        raise ValueError(msg)

    return scores
