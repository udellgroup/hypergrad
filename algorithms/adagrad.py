from bench_algo import *
from algo_config import *
import numpy as np

class AdaGrad(Optimizer):
    """
    Implements the AdaGrad optimization algorithm.
    The update rule is:
        G = G + grad_f(x_k)^2
        x_{k+1} = x_k - alpha / sqrt(G + eps) * grad_f(x_k)
    where
    - alpha is the step size
    - G accumulates the sum of squares of the gradients
    - eps is a small constant to avoid division by zero
    """

    def __init__(self, params: Dict[str, Any] = None):
        """
        Constructor for the AdaGrad optimizer.
        """
        if params is None:
            params = {}

        self.stats = {}

        super().__init__(params.get(ALG_UNIVERSAL_PARAM_NAME, "AdaGrad"), params)

    def optimize(self, x: np.ndarray, f: callable, grad_f: callable) -> Dict[str, Any]:
        """
        Optimize the function f using AdaGrad.

        Parameters
        ----------
        x : np.ndarray
            Initial point
        f : callable
            Objective function
        grad_f : callable
            Gradient of the objective function

        Returns
        -------
        Dict[str, Any]
            A dictionary containing optimization statistics
        """

        # Extract parameters
        tol = self.params.get(ALG_UNIVERSAL_PARAM_TOL, 1e-06)
        max_iter = self.params.get(ALG_UNIVERSAL_PARAM_MAXITER, 1000)
        eps = self.params.get(ALG_ADAGRAD_EPSILON, 1e-08)
        lr = self.params.get(ALG_ADAGRAD_LEARNING_RATE, 0.1)

        # Counters
        n_func_evals = 0
        n_grad_evals = 0
        n_iter = 0

        # Statistics
        fvals = np.zeros(max_iter)
        gnorms = np.zeros(max_iter)

        # Accumulator for gradients
        G = np.zeros_like(x)

        for i in range(max_iter):
            gx = grad_f(x)
            n_grad_evals += 1

            grad_norm = np.linalg.norm(gx, ord=np.inf)
            n_iter += 1

            # Save info for stats
            fvals[i] = f(x)  # function value
            gnorms[i] = grad_norm

            # Check stopping condition
            if grad_norm < tol:
                break

            # Accumulate square of gradients
            G += gx ** 2

            # AdaGrad update
            x = x - (lr / (np.sqrt(G) + eps)) * gx

        # If we ended early, fill trailing stats
        if n_iter < max_iter:
            fvals[n_iter:] = fvals[n_iter - 1]
            gnorms[n_iter:] = gnorms[n_iter - 1]

        # Collect stats
        stats = {
            ALG_STATS_ITERATIONS: n_iter,
            ALG_STATS_OPTIMAL_VALUE: f(x),
            ALG_STATS_OPTIMAL_SOL: x,
            ALG_STATS_RUNNING_TIME: 0,
            ALG_STATS_FUNCVALS: fvals,
            ALG_STATS_GNORMS: gnorms,
            ALG_STATS_FEVALS: n_func_evals,
            ALG_STATS_GEVALS: n_grad_evals
        }

        self.stats = stats
        return stats

    def get_optimizer_stats(self) -> Dict[str, Any]:
        """
        Get the optimizer statistics
        
        Returns
        -------
        Dict[str, Any]
            Statistics of the optimizer
        """
        return self.stats
    
if __name__ == "__main__":
    
    params = adagrad_params
    params[ALG_ADAGRAD_LEARNING_RATE] = 4.0
    
    # Initialize the optimizer
    adagrad = AdaGrad(params)
    
    # Initial guess
    x_init = np.array([0.0, 0.0])
    
    # Run optimization
    stats = adagrad.optimize(x_init, f, grad_f)
    
    # Print results
    print("Optimizer Stats:")
    print(f"Iterations:         {stats[ALG_STATS_ITERATIONS]}")
    print(f"Optimal Value:      {stats[ALG_STATS_OPTIMAL_VALUE]:.6f}")
    print(f"Optimal Solution:   {stats[ALG_STATS_OPTIMAL_SOL]}")
    print(f"Function Evaluations: {stats[ALG_STATS_FEVALS]}")
    print(f"Gradient Evaluations: {stats[ALG_STATS_GEVALS]}")
    print(f"Final Gradient Norm: {np.linalg.norm(grad_f(stats[ALG_STATS_OPTIMAL_SOL])):.6f}")
    print("\nFunction Values (first 5):", stats[ALG_STATS_FUNCVALS][0:5])
    print("Gradient Norms (first 5):", stats[ALG_STATS_GNORMS][0:5])
    print("\nTest completed!")