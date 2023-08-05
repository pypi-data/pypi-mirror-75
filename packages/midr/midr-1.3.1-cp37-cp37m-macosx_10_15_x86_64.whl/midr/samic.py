#!/usr/bin/python3

"""Compute the Irreproducible Discovery Rate (IDR) from NarrowPeaks files

Implementation of the IDR methods for two or more replicates.

LI, Qunhua, BROWN, James B., HUANG, Haiyan, et al. Measuring reproducibility
of high-throughput experiments. The annals of applied statistics, 2011,
vol. 5, no 3, p. 1752-1779.

Given a list of peak calls in NarrowPeaks format and the corresponding peak
call for the merged replicate. This tool computes and appends a IDR column to
NarrowPeaks files.
"""

from sys import float_info
from scipy.optimize import minimize
import numpy as np
import midr.log as log
import midr.archimedean as archimedean
from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
from midr.idr import sim_m_samples
import midr.archimediean_plots as archimediean_plots


COPULA_DENSITY = {
    'clayton': archimedean.pdf_clayton,
    'frank': archimedean.pdf_frank,
    'gumbel': archimedean.pdf_gumbel
}
DMLE_COPULA = {
    'clayton': archimedean.dmle_copula_clayton,
    'frank': archimedean.dmle_copula_frank,
    'gumbel': archimedean.dmle_copula_gumbel
}


def copula_density(copula):
    return {
        'clayton': archimedean.pdf_clayton,
        'frank': archimedean.pdf_frank,
        'gumbel': archimedean.pdf_gumbel
    }[copula]


def row_non_missing(u_values, missing=0.0):
    """
    return an array of bool on the presence of zeros in rows
    :param u_values:
    :param ncol:
    :return:
    >>> row_non_missing(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    ])
    ... )
    array([0, 1, 2])
    >>> row_non_missing(np.array([
    ...    [0.25148149, 0.0, 0.3378213],
    ...    ])
    ... )
    array([0, 2])
    >>> row_non_missing(np.array([
    ...    [0.39522060, 0.0, 0.0],
    ...    ])
    ... )
    array([0])
    """
    return np.where(~(u_values[0, :] == missing))[0]


def row_censored_copula_density(u_values, theta, copula, missing=0.0):
    """
    compute pdf of copula for censored data
    :param u_values:
    :param theta:
    :param copula:
    :return:
    >>> row_censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    ]),
    ...    theta=6,
    ...    copula="frank",
    ... )
    0.013995230486531306
    >>> row_censored_copula_density(np.array([
    ...    [0.0, 0.18285458, 0.9514195, 0.9514195],
    ...    ]),
    ...    theta=6,
    ...    copula="frank",
    ... )
    0.005890066856414175
    >>> row_censored_copula_density(np.array([
    ...    [0.0, 0.18285458, 0.0, 0.9514195],
    ...    ]),
    ...    theta=6,
    ...    copula="frank",
    ... )
    0.05957605144742631
    >>> row_censored_copula_density(np.array([
    ...    [0.0, 0.18285458, 0.0, 0.0],
    ...    ]),
    ...    theta=6,
    ...    copula="frank",
    ... )
    0.0
    """
    non_missing = row_non_missing(u_values=u_values, missing=missing)
    if len(non_missing) == 1:
        return 0.0
    else:
        return copula_density(copula)(
            u_values=u_values[:, non_missing],
            theta=theta
        )[0]


def censored_copula_density(u_values, theta, copula, missing=0.0):
    """
    compute pdf of copula for censored data
    :param u_values:
    :param theta:
    :param copula:
    :return:
    >>> censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    theta=6,
    ...    copula="frank",
    ... )
    array([0.01399523, 3.20545262, 0.05619478, 0.04574052, 1.02461261,
           3.41716738, 0.03672658, 4.78125643, 1.02599504, 1.07616887])
    """
    def row_density(x):
        return row_censored_copula_density(
            u_values=np.array([u_values[x, :]]),
            theta=theta,
            copula=copula,
            missing=missing
        )
    return np.array(list(map(row_density, range(u_values.shape[0]))))


def delta(params_list, threshold):
    """
    Return true if the difference between two iteration of samic if less than
    the threhsold
    :param params_list: list of model parameters
    :param threshold: flood withe the minimal difference to reach
    :return: bool
    >>> delta(
    ...    params_list={
    ...        'pi': 0.8,
    ...        'pi_old': 0.8,
    ...        'alpha': np.array([0.3333, 0.3333, 0.3333]),
    ...        'alpha_old': np.array([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'clayton': {'theta': 8, 'pi': 0.2, 'theta_old': 6, 'pi_old': 2.3}
    ...    },
    ...    threshold=0.1
    ... )
    True
    >>> delta(
    ...    params_list={
    ...        'pi': 0.8,
    ...        'pi_old': 0.8,
    ...        'alpha': np.array([0.3333, 0.3333, 0.3333]),
    ...        'alpha_old': np.array([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2}
    ...    },
    ...    threshold=0.1
    ... )
    False
    """
    max_delta = list()
    max_delta.append(max(abs(params_list['alpha'] - params_list['alpha_old'])))
    max_delta.append(abs(params_list['pi'] - params_list['pi_old']))
    for copula in COPULA_DENSITY.keys():
        max_delta.append(
            abs(params_list[copula]['theta'] - params_list[copula]['theta_old'])
        )
    return max(max_delta) >= threshold

def expectation_k(u_values, params_list):
    """
    compute proba for each copula mix to describe the data
    :param u_values:
    :param params_list:
    :return:
    >>> expectation_k(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6}
    ...    }
    ... )
    array([0.21467668, 0.41721175, 0.20167246, 0.21337973, 0.21740186,
           0.48826352, 0.20725411, 0.22008768, 0.3581174 , 0.29793559])
    """
    k_state = np.zeros(u_values.shape[0])
    for copula in COPULA_DENSITY.keys():
        k_state += params_list['alpha'][params_list['order'][copula]] * \
            COPULA_DENSITY[copula](
                u_values,
                params_list[copula]['theta'],
            )
    k_state *= (1 - params_list['pi'])
    return k_state / (params_list['pi'] + k_state)

def expectation_l(u_values, params_list):
    """
    compute proba for each copula mix to describe the data
    :param u_values:
    :param params_list:
    :return:
    >>> np.sum(expectation_l(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2}
    ...    }
    ... ), axis=1)
    array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])
    """
    l_state = np.zeros((u_values.shape[0], len(COPULA_DENSITY)))
    dcopula = np.zeros((u_values.shape[0], len(COPULA_DENSITY)))
    for copula in COPULA_DENSITY.keys():
        dcopula[:, params_list['order'][copula]] = (
            params_list['alpha'][params_list['order'][copula]] *
            COPULA_DENSITY[copula](
                u_values,
                params_list[copula]['theta'],
            )
        )
    for copula in COPULA_DENSITY.keys():
        l_state[:, params_list['order'][copula]] = (
            dcopula[:, params_list['order'][copula]] /
            np.sum(dcopula, axis=1)
        )
    return l_state


def loglikelihood_theta(theta, u_values, copula, params_list):
    """
    pdf of the samic mixture for a given copula
    :param u_values:
    :param copula:
    :param theta:
    :return:
    >>> loglikelihood_theta(
    ...    theta=2,
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula = "frank",
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2}
    ...    }
    ... )
    1.8106392899084194
    """
    dcopula = np.zeros((u_values.shape[0], len(COPULA_DENSITY)))
    for other_copula in COPULA_DENSITY.keys():
        if other_copula == copula:
            other_theta = theta
        else:
            other_theta = params_list[copula]['theta']
        dcopula[:, params_list['order'][copula]] = (
                params_list['alpha'][params_list['order'][copula]] *
                COPULA_DENSITY[copula](
                    u_values,
                    other_theta,
                )
        )
    return -np.sum(
        np.log(
            params_list['pi'] +
            (1 - params_list['pi']) *
            np.sum(dcopula, axis=1)
        ),
        axis=0
    )


def local_idr(u_values, params_list):
    """
    Compute local idr for the samic method
    :param u_values:
    :param params_list:
    :return:
    >>> local_idr(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2}
    ...    }
    ... )
    array([0.79535495, 0.71654265, 0.79947661, 0.7957702 , 0.79447936,
           0.6802532 , 0.79771887, 0.79361233, 0.74281835, 0.76658261])
    """
    return 1 - expectation_k(u_values=u_values, params_list=params_list)

def minimize_alpha(l_state):
    """
    compute maximization of alpha
    >>> minimize_alpha(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]))
    array([0.46469085, 0.37489573, 0.16041342])
    """
    alpha = np.zeros(l_state.shape[1])
    alpha[:-1] = np.sum(l_state[:, :-1], axis=0) / float(l_state.shape[0])
    alpha[-1] = 1.0 - np.sum(alpha[:-1])
    return alpha


def build_bounds(copula, eps=1e-4):
    """
    return set of bound for a given copula
    :param copula:
    :param eps:
    :return:
    >>> build_bounds("frank")
    (0.0001, 744.9999)
    >>> build_bounds("clayton")
    (0.0001, 999.9999)
    >>> build_bounds("gumbel")
    (1.0001, 99.9999)
    """
    thetas = {
        'clayton': {
            'theta_min': 0.0,
            'theta_max': 1000.0
        },
        'frank': {
            'theta_min': 0.0,
            'theta_max': 745.0
        },
        'gumbel': {
            'theta_min': 1.0,
            'theta_max': 100
        }
    }
    return (
        thetas[copula]['theta_min'] + eps, thetas[copula]['theta_max'] - eps
    )


def minimize_pi(k_state):
    """
    find theta that minimize the likelihood of the copula density
    :param u_values:
    :param copula:
    :param params_list:
    :return:
    >>> minimize_pi(
    ...     k_state = np.array([0.99275263, 0.87291238, 0.99918233, 0.99339966,
    ...                         0.99138885, 0.81964467, 0.99643828, 0.99003915,
    ...                         0.91222219, 0.94832496]))
    0.95163051
    """
    return float(np.sum(k_state)) / float(len(k_state))


def minimize_theta(u_values, copula, params_list):
    """
    find theta that minimize the likelihood of the copula density
    :param u_values:
    :param copula:
    :param params_list:
    :return:
    >>> minimize_theta(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula="frank",
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2}
    ...    }
    ... )
    6.0
    >>> minimize_theta(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula="gumbel",
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2}
    ...    }
    ... )
    1.0000999999999998
    >>> minimize_theta(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula="clayton",
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2}
    ...    }
    ... )
    6.0
    """
    log.logging.debug("%s", copula + " minimize_theta")
    old_theta = params_list[copula]['theta']
    log.logging.debug("%s", str([build_bounds(copula)]) + " minimize() bounds")
    log.logging.debug("%s", str(old_theta) + " old_theta")
    if log.logging.root.level == log.logging.DEBUG:
        archimediean_plots.pdf_copula_plot(
            lower=build_bounds(copula)[0],
            upper=build_bounds(copula)[1],
            copula=copula,
            pdf_function=loglikelihood_theta,
            u_values=u_values,
            params_list=params_list,
        )
    res = minimize(
        fun=loglikelihood_theta,
        args=(u_values, copula, params_list),
        x0=old_theta,
        bounds=[build_bounds(copula)],
    )
    log.logging.debug("%s", res)
    if np.isnan(res.x[0]):
        log.logging.debug("%s", str(old_theta) + " new_theta = old_theta")
        return old_theta
    else:
        log.logging.debug("%s", str(res.x[0]) + " new_theta")
        return res.x[0]


def samic(x_score, threshold=1e-4):
    """
    implementation of the samic method for m samples
    :param x_score np.array of score (measures x samples)
    :param threshold float min delta between every parameters between two
    iterations
    :return (theta: dict, lidr: list) with theta the model parameters and
    lidr the local idr values for each measures
    >>> THETA_TEST_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> THETA_TEST_1 = {'pi': 0.1, 'mu': 4.0, 'sigma': 3.0, 'rho': 0.75}
    >>> DATA = sim_m_samples(n_value=10000,
    ...                      m_sample=4,
    ...                      theta_0=THETA_TEST_0,
    ...                      theta_1=THETA_TEST_1)
    >>> lidr = samic(DATA["X"], threshold=0.0001)
    >>> (np.sum((lidr < 0.5).all() == DATA["K"]) / len(lidr)) <= 0.11
    True
    """
    log.logging.info("%s", "computing idr")
    u_values = compute_empirical_marginal_cdf(compute_rank(x_score))
    params_list = dict()
    params_list['order'] = dict()
    i = 0
    for copula in COPULA_DENSITY.keys():
        params_list[copula] = {
            'theta': DMLE_COPULA[copula](u_values),
            'theta_old': np.nan,
        }
        params_list['order'][copula] = i
        i += 1
    params_list['k_state'] = np.zeros(u_values.shape[0])
    params_list['l_state'] = np.zeros((u_values.shape[0], len(COPULA_DENSITY)))
    params_list['pi'] = 0.5
    params_list['pi_old'] = 0.0
    params_list['alpha'] = np.repeat(1.0 / len(COPULA_DENSITY), len(COPULA_DENSITY))
    params_list['alpha_old'] = params_list['alpha'][:]
    while delta(params_list, threshold):
        params_list['k_state'] = expectation_k(
            u_values=u_values,
            params_list=params_list,
        )
        params_list['l_state'] = expectation_l(
            u_values=u_values,
            params_list=params_list,
        )
        params_list['alpha_old'] = params_list['alpha'][:]
        params_list['pi_old'] = params_list['pi']
        params_list['pi'] = minimize_pi(
            k_state=params_list['k_state']
        )
        params_list['alpha'] = minimize_alpha(
            l_state=params_list['l_state']
        )
        log.logging.info(
            "%s",
            log_samic(params_list)
        )
        for copula in COPULA_DENSITY:
            params_list[copula]['theta_old'] = params_list[copula]['theta']
            params_list[copula]['theta'] = minimize_theta(
                u_values=u_values,
                copula=copula,
                params_list=params_list
            )
            log.logging.info(
                "%s %s",
                copula,
                log_samic(params_list)
            )
    return local_idr(
        u_values=u_values,
        params_list=params_list
    )


def log_samic(params_list):
    """
    return str of pseudo_likelihood parameter estimate
    :param params_list:
    :return:
    >>> log_samic(
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2}
    ...    })
    '{"pi": 0.8, \n"alpha": [0.3333, 0.3333, 0.3333], \n"clayton": \
    {"theta": 6}, \n"frank": {"theta": 6}, \n"gumbel": {"theta": 6} }'
    """
    log_str = str('{' +
                  '"pi": ' + str(params_list['pi'])
                  )
    for copula in COPULA_DENSITY.keys():
        log_str += str(
            ', \n"' + copula + '": {' +
            '"alpha": ' +
            str(params_list['alpha'][params_list["order"][copula]]) +
            ', ' '"theta": ' +
            str(params_list[copula]['theta']) +
            '}')
    return log_str + ' }'


if __name__ == "__main__":
    import doctest

    doctest.testmod()
