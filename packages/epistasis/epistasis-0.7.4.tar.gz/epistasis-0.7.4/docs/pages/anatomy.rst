Anatomy of an epistasis model
=============================

The X matrix
------------

The most critical piece of an epistasis models is the X (model) matrix.
This matrix maps genotypes to epistatic coefficients. You can read about this matrix
in this paper_.

There are two popular X matrices that exist in the epistasis literature, the
``global`` model (a.k.a. background-averaged model) and ``local`` model (a.k.a. biochemical model).
All epistasis models in this API takes a ``model_type`` keyword argument
that tells the model which matrix to use. Read the paper mentioned
above for more information on which model to use.

Constructing these matrices for your dataset is no easy task,
so each epistasis model can handle this construction internally. Most methods
automatically infer X from the genotype-phenotype map. (If you need to build your own X matrix, check out this page_)

Any X matrix used by an epistasis model is also stored in the ``Xbuilt`` attribute.
This speeds up fitting algorithms that may need resample fitting many times.

.. References in this document

.. _page: ./advanced.html
.. _paper: http://www.genetics.org/content/205/3/1079

Methods in every epistasis model
--------------------------------

Every epistasis model includes the following methods:

  * **fit** : fit the model to an attached genotype-phenotype map, *or* X and y data.
  * **predict** : predict phenotypes using the X matrix or keywords (listed above). If a keyword is used, the phenotypes are in the same order as the genotypes to the corresponding keyword.
  * **score** : the pearson coefficients between the predicted phenotypes and the given data (X/y data or attached genotype-phenotype map).
  * **thetas** : flattened array of 1) *nonlinear* parameters and 2) epistatic-coefficients estimated by model.
  * **hypothesis** : computes the phenotypes for X data given a ``thetas`` array.
  * **lnlike_of_data** : returns an array of log-likelihoods for each data point given a ``thetas`` array.
  * **lnlikelihood** : returns the total log-likelihood for X/y data given a ``thetas`` array.

Methods in nonlinear models
---------------------------

The extra attributes below are attached to **nonlinear** epistasis models.

  * **Additive** : a first-order EpistasisLinearRegression used to approximate the additive effects of mutations
  * **Nonlinear** : a ``lmfit.MinizerResults`` object returned by the ``lmfit.minimize`` function for estimating the nonlinear scale in a genotype-phenotype map.
