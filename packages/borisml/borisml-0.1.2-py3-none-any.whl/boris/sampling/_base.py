import torch

from boris.sampling._score import _inf
from boris.sampling._score import _random_score_fn
from boris.sampling._score import _coreset_score_fn
from boris.sampling._score import _bit_score_fn
from boris.sampling._score import _uncertainty_score_fn


def _permutation_sample(scores):
    _, indices = torch.sort(scores, descending=True)
    return indices


def _unpack_state(state):
    """Unpack state into 4-tuple.

    """

    if type(state) is tuple:
        if len(state) == 4:
            return state

    elif type(state) is torch.Tensor:
        n_data = state.shape[0]
        selected = torch.zeros(n_data).bool().to(state.device)
        return (n_data, selected, state, None)

    length = len(state) if type(state) is tuple else 0
    raise ValueError(
        'Illegal state! Must be 4-tuple or torch.Tensor but is {} with len {}'
        .format(type(state), length)
    )


def _parse_state(state):
    """Parse state and make sure format is ok.

    """

    n_data, selected, embeddings, uscores = _unpack_state(state)

    if selected.dtype is not torch.bool:
        raise ValueError(
            'selected must be dtype torch.bool, is {}.'
            .format(selected.dtype)
        )

    if embeddings is not None and embeddings.dtype is not torch.float:
        raise ValueError(
            'embeddings must be dtype torch.float, is {}'
            .format(embeddings.dtype)
        )

    if uscores is not None and uscores.dtype is not torch.float:
        raise ValueError(
            'uscores must be dtype torch.float, is {}'
            .format(uscores.dtype)
        )

    return (n_data, selected, embeddings, uscores)


def _sample(n_samples, state, score_fn=_random_score_fn, **kwargs):
    """ Update sample state based on current state, embeddings,
        and the score function.

    Args:
        n_samples: (int) Number of samples
        state: (n_data, selected, embeddings, scores)
            n_data: (int) size of the dataset
            selected: (torch.BoolTensor) selected samples
            embeddings: (torch.FloatTensor) TODO
            uscores: (torch.FloatTensor) uncertainty scores
        score_fn: (callable) computes new importance scores
            based on current scores and embeddings

    Returns:
        new_state: (n_data, selected, embeddings, uscores)
        sscores: (torch.FloatTensor) sampling scores

    """

    n_data, selected, embeddings, uscores = state
    n_selected = selected.sum()

    if n_samples <= 0:
        return state
    if n_selected >= n_data:
        return state

    if embeddings is None and uscores is None:
        sscores = _random_score_fn(state)
    elif embeddings is not None:
        sscores = score_fn(state, **kwargs)

    max_val = _inf(sscores.max())
    min_val = sscores.min()
    sscores[selected] = max_val
    sscores = (sscores - min_val) / _inf(max_val - min_val)

    indices = _permutation_sample(sscores)

    n_samples = min(n_data, n_selected + n_samples)
    selected[indices[n_selected:n_samples]] = True

    return (n_data, selected, embeddings, uscores), sscores


def sample(n_samples, state, strategy='random', **kwargs):
    """ Update sample state based on current state, embeddings,
        and the chosen strategy.

    Args:
        n_samples: (int) Number of samples
        state: (n_data, selected, embeddings, scores)
            n_data: (int) size of the dataset
            selected: (torch.BoolTensor) selected samples
            embeddings: (torch.FloatTensor) TODO
            uscores: (torch.FloatTensor) uncertainty scores
        strategy: (str) sampling strategy from
            {random, coreset}

    Returns:
        new_state: (n_data, selected, embeddings, scores)
        sscores: (torch.FloatTensor) sampling scores

    Examples:

        >>> n_data = len(dataset)
        >>> selected = torch.zeros(n_data).bool()
        >>> state = (n_data, selected, embeddings, None)
        >>> state, sscores = sample(n_samples, state, strategy='coreset')

        >>> n_data = len(dataset)
        >>> selected = torch.zeros(n_data).bool()
        >>> selected[0] = True ## manual initial choice
        >>> uscores = # get uncertainty scores for active learning
        >>> state = (n_data, selected, embeddings, uscores)
        >>> state, sscores = sample(n_samples, state, strategy='coreset')
    """

    state = _parse_state(state)

    if strategy == 'random':
        score_fn = _random_score_fn
    elif strategy == 'coreset':
        score_fn = _coreset_score_fn
    elif strategy == 'bit':
        score_fn = _bit_score_fn
    elif strategy == 'uncertainty':
        score_fn = _uncertainty_score_fn
    else:
        raise ValueError(
            'Illegal strategy: {}'.format(strategy))

    state, sscores = _sample(n_samples, state, score_fn=score_fn, **kwargs)
    return state, sscores
