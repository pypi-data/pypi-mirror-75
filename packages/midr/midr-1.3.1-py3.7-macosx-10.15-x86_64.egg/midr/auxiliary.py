#!/usr/bin/python3

"""Compute the Irreproducible Discovery Rate (IDR) from NarrowPeaks files

This section of the project provides facilitites to handle NarrowPeaks files
and compute IDR on the choosen value in the NarrowPeaks columns
"""

from scipy.stats import rankdata
import numpy as np


def compute_rank(x_score):
    """
    transform x a n*m matrix of score into an n*m matrix of rank ordered by
    row.

    >>> compute_rank(np.array([[0,0],[10,30],[20,20],[30,10]]))
    array([[1, 1],
           [2, 4],
           [3, 3],
           [4, 2]])
    """
    rank = np.empty_like(x_score)
    for j in range(x_score.shape[1]):
        # we want the rank to start at 1
        rank[:, j] = rankdata(x_score[:, j], method="ordinal")
    return rank


def compute_empirical_marginal_cdf(rank, gaussian=False):
    """
    normalize ranks to compute empirical marginal cdf and scale by n / (n+1)

    >>> r = compute_rank(np.array(
    ...    [[0.0,0.0],
    ...    [10.0,30.0],
    ...    [20.0,20.0],
    ...    [30.0,10.0]]))
    >>> compute_empirical_marginal_cdf(r, gaussian=True)
    array([[0.99  , 0.99  ],
           [0.7425, 0.2475],
           [0.495 , 0.495 ],
           [0.2475, 0.7425]])
    >>> compute_empirical_marginal_cdf(r)
    array([[0.2, 0.2],
           [0.4, 0.8],
           [0.6, 0.6],
           [0.8, 0.4]])
    """
    if gaussian:
        x_score = np.empty_like(rank)
        n_value = float(rank.shape[0])
        m_sample = float(rank.shape[1])
        # scaling_factor = n_value / (n_value + 1.0)
        # we want a max value of 0.99
        scaling_factor = 0.99
        for i in range(int(n_value)):
            for j in range(int(m_sample)):
                x_score[i][j] = (1.0 - (float(rank[i][j] - 1) / n_value)) * \
                                scaling_factor
    else:
        x_score = (1.0 / (float(rank.shape[0]) + 1.0)) * rank
    return x_score


def benjamini_hochberg(p_vals):
    """
    compute fdr from pvalues
    :param p_vals:
    :return:
    """
    ranked_p_values = rankdata(p_vals)
    fdr = p_vals * len(p_vals) / ranked_p_values
    fdr[fdr > 1] = 1
    return fdr
