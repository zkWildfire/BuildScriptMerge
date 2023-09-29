from algorithms.greedy_merge import merge_build_script_groups
from algorithms.hierarchical import hierarchical_clustering
import argparse
from build_script import BuildScript
from build_script_group import BuildScriptGroup
from evaluator import Evaluator
from typing import List, Dict
import numpy as np

def main(args):
    # Generate random build scripts based on command line arguments
    build_scripts = BuildScript.generate_random_build_scripts(
        num_scripts=args.num_build_scripts,
        num_unique_paths=args.num_unique_paths,
        seed=args.seed,
        min_paths=args.min_paths_per_script,
        max_paths=args.max_paths_per_script
    )

    # Collect unique paths
    unique_paths = BuildScript.collect_unique_paths(build_scripts)

    # Initialize BuildScriptGroup objects
    build_script_groups = [BuildScriptGroup([script], unique_paths) for script in build_scripts]

    # Merge BuildScriptGroups based on the chosen algorithm
    if args.algorithm == 'greedy':
        merged_groups = merge_build_script_groups(build_script_groups, args.threshold)
    elif args.algorithm == 'hierarchical':
        merged_groups = hierarchical_clustering(build_script_groups, args.threshold)
    else:
        print("Invalid algorithm specified.")
        return

    # Evaluate the merged BuildScriptGroups
    Evaluator.evaluate(merged_groups)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize CI/CD build script grouping.")

    parser.add_argument('--num_build_scripts', type=int, default=10, help="Number of build scripts to generate.")
    parser.add_argument('--num_unique_paths', type=int, default=30, help="Number of unique paths.")
    parser.add_argument('--max_paths_per_script', type=int, default=20, help="Maximum number of paths per build script.")
    parser.add_argument('--min_paths_per_script', type=int, default=5, help="Maximum number of paths per build script.")
    parser.add_argument('--seed', type=int, default=None, help="Random seed for reproducibility.")
    parser.add_argument('--threshold', type=float, default=2.0, help="Threshold for merging build script groups.")
    parser.add_argument('--algorithm', type=str, choices=['greedy', 'hierarchical'], default='greedy', help="Algorithm to use for merging.")

    args = parser.parse_args()
    main(args)

