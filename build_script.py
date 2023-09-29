from __future__ import annotations
import numpy as np
import random
from typing import List

class BuildScript:
    def __init__(self, paths: List[str]):
        """
        Initializes the build script.
        @param paths List of prerequisite paths for the build script.
        """
        # Sort the paths into alphabetical order.
        self._paths = sorted(paths)


    @property
    def paths(self) -> List[str]:
        """
        Gets the sorted list of prerequisite paths for the build script.
        """
        return self._paths


    def to_bit_string(self, unique_paths: List[str]) -> np.ndarray:
        """
        Converts the paths in the build script to a bit string based on the
          unique paths provided.
        @param unique_paths A sorted list of unique paths to map against.
        @returns A 1xN array representing the bit string, where N is the number
          of elements in the input list.
        """
        bit_string = np.zeros(len(unique_paths), dtype=int)
        for path in self._paths:
            index = unique_paths.index(path)
            bit_string[index] = 1

        return bit_string


    @staticmethod
    def generate_random_build_scripts(
        num_scripts: int,
        num_unique_paths: int,
        seed: int = None,
        min_paths: int = 1,
        max_paths: int = 10) -> List[BuildScript]:
        """
        Generates a list of randomized BuildScript instances.
        @param num_scripts The total number of build scripts to create.
        @param num_unique_paths The total number of unique paths to use across
          all build scripts.
        @param seed The seed for random number generation.
        @param min_paths The minimum number of paths that a single build script
          can have.
        @param max_paths The maximum number of paths that a single build script
          can have.
        @returns List of BuildScript instances.
        """
        # Initialize the random number generator.
        random.seed(seed)

        # Generate a pool of unique paths.
        unique_paths = [f"Path_{i}" for i in range(num_unique_paths)]

        # Generate build scripts.
        build_scripts = []
        for _ in range(num_scripts):
            num_paths_in_script = random.randint(min_paths, max_paths)
            paths_for_script = random.sample(unique_paths, num_paths_in_script)
            build_script = BuildScript(paths_for_script)
            build_scripts.append(build_script)

        return build_scripts


    def collect_unique_paths(build_scripts: List[BuildScript]) -> List[str]:
        """
        Collects all unique paths from a list of BuildScript objects.
        @param build_scripts A list of BuildScript objects.
        @returns A sorted list of unique paths.
        """
        unique_paths = set()

        for script in build_scripts:
            unique_paths.update(script.paths)

        return sorted(list(unique_paths))

