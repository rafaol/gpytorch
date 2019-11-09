#!/usr/bin/env python3

import warnings
import torch
from ..module import Module
from abc import ABC, abstractmethod


class _VariationalDistribution(Module, ABC):
    r"""
    Abstract base class for all Variational Distributions.
    """

    def __init__(self, num_inducing_points, batch_shape=torch.Size([])):
        super().__init__()
        self.num_inducing_points = num_inducing_points
        self.batch_shape = batch_shape

    def forward(self):
        r"""
        Constructs and returns the variational distribution

        :rtype: :obj:`~gpytorch.distributions.MultivariateNormal`
        :return: The distribution :math:q(\mathbf u)"
        """
        raise NotImplementedError

    @abstractmethod
    def initialize_variational_distribution(self, prior_dist):
        r"""
        Method for initializing the variational distribution, based on the prior distribution.

        :param ~gpytorch.distribution.Distribution prior_dist: The prior distribution :math:`p(\mathbf u)`.
        """
        raise NotImplementedError

    def __call__(self):
        try:
            return self.forward()
        # Deprecation added for 0.4 release
        except NotImplementedError:
            warnings.warn(
                "_VariationalDistribution.variational_distribution is deprecated. "
                "Please implement a `forward` method instead.",
                DeprecationWarning
            )
            return self.variational_distribution

    # Deprecation added for 0.4 release
    def __getattr__(self, attr):
        if attr == "variational_distribution":
            warnings.warn(
                "_VariationalDistribution.variational_distribution is deprecated. "
                "To get q(u), call the _VariationalDistribution object instead.",
                DeprecationWarning
            )
            return self.forward()
        else:
            return super().__getattr__(attr)
