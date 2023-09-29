from algorithms.greedy_merge import merge_build_script_groups
from algorithms.hierarchical import hierarchical_clustering
import argparse
from build_script import BuildScript
from build_script_group import BuildScriptGroup
from collections import defaultdict
from evaluator import Evaluator
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple

def run_algorithm(
    num_build_scripts: int,
    num_unique_paths: int,
    max_paths_per_script: int,
    min_paths_per_script: int,
    seed: int,
    threshold: float,
    algorithm: Callable[[List[BuildScriptGroup], float],
                     List[BuildScriptGroup]]) -> Tuple[float, float, float]:
    """
    Runs the specified algorithm with the given parameters and returns the
      metrics.
    @param num_build_scripts Number of build scripts to generate.
    @param num_unique_paths Number of unique paths.
    @param max_paths_per_script Maximum number of paths per build script.
    @param min_paths_per_script Minimum number of paths per build script.
    @param seed The seed for random number generation.
    @param threshold The minimum dot product value to consider merging two groups.
    @param algorithm The algorithm to run.
    @returns The average build scripts per group, average unique paths per
      group, and average similarity within groups.
    """
    # Generate random build scripts based on command line arguments
    build_scripts = BuildScript.generate_random_build_scripts(
        num_scripts=num_build_scripts,
        num_unique_paths=num_unique_paths,
        seed=seed,
        min_paths=min_paths_per_script,
        max_paths=max_paths_per_script
    )

    # Collect unique paths
    unique_paths = BuildScript.collect_unique_paths(build_scripts)

    # Initialize BuildScriptGroup objects
    build_script_groups = [BuildScriptGroup([script], unique_paths) for script in build_scripts]

    # Merge BuildScriptGroups based on the chosen algorithm
    merged_groups = algorithm(build_script_groups, threshold)

    # Evaluate the merged BuildScriptGroups
    return Evaluator.evaluate(merged_groups)


def main(args):
    results = defaultdict(list)
    if args.algorithm == 'greedy':
        algo = merge_build_script_groups
    elif args.algorithm == 'hierarchical':
        algo = hierarchical_clustering
    else:
        raise ValueError("Invalid algorithm specified.")

    for seed in args.seed:
        for threshold in args.threshold:
            metrics = run_algorithm(
                args.num_build_scripts,
                args.num_unique_paths,
                args.max_paths_per_script,
                args.min_paths_per_script,
                seed,
                threshold,
                algo
            )
            results[threshold].append(metrics)

    # Aggregation and plotting code here
    x = sorted(results.keys())
	# TODO: replace sum with appropriate aggregation function
    y = [sum(results[threshold]) / len(results[threshold]) for threshold in x]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    plt.xlabel("Threshold")
    plt.ylabel("Metric")  # replace with the actual metric you are measuring
    plt.title(f"Performance Metrics for Algorithm: {args.algorithm}")
    plt.grid(True)
    plt.savefig("performance_metrics.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize CI/CD build script grouping.")

    parser.add_argument('--num_build_scripts', type=int, default=100, help="Number of build scripts to generate.")
    parser.add_argument('--num_unique_paths', type=int, default=30, help="Number of unique paths.")
    parser.add_argument('--max_paths_per_script', type=int, default=20, help="Maximum number of paths per build script.")
    parser.add_argument('--min_paths_per_script', type=int, default=5, help="Minimum number of paths per build script.")
    parser.add_argument('--seed', type=int, nargs='+', default=[0, 1, 2, 3, 4], help="Random seeds for reproducibility.")
    parser.add_argument('--threshold', type=float, nargs='+', required=True, help="Thresholds for merging build script groups.")
    parser.add_argument('--algorithm', type=str, choices=['greedy', 'hierarchical'], default='greedy', help="Algorithm to use for merging.")

    args = parser.parse_args()
    main(args)

