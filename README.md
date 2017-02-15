# eQTL_GTD_TensorFlow

We do Genetic Tensor Decomposition (GTD) with TensorFlow.

We build 3D tensor decomposition model for cross-tissue gene expression profiles, and model the individual factors affected by genetics of these individuals.

The scale of this model will be ~: (28, 450, 20000), (2500000, 400), where d=400 is an empirical number for amount of factors.

We will try to achieve sparsity from both wise initialization and sparsity priors.

Next stage will involve non-genetic effects in the modeling.



