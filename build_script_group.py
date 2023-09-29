from build_script import BuildScript
import numpy as np
from typing import List

class BuildScriptGroup:
    """
    Represents a set of build scripts that have been grouped together.
    """
    def __init__(self,
        build_scripts: List[BuildScript],
        unique_paths: List[str]):
        """
        Initializes the build script group.
        @param build_scripts A list of BuildScript objects in this group.
        @param unique_paths A sorted list of unique paths to map against.
        """
        self._build_scripts = build_scripts
        self._unique_paths = unique_paths

        # Initialize the bit string to all 1s (represents AND operation)
        self._group_bit_string = np.ones(len(unique_paths), dtype=int)

        # Compute the AND of all build script bit strings
        for script in build_scripts:
            self._group_bit_string &= script.to_bit_string(unique_paths)


    def add_build_script(self, build_script: BuildScript) -> None:
        """
        Adds a new BuildScript object to this group and updates the group's bit
          string.
        @param build_script The new BuildScript object to add.
        """
        self._build_scripts.append(build_script)
        self._group_bit_string &= build_script.to_bit_string(self._unique_paths)


    @property
    def group_bit_string(self) -> np.ndarray:
        """
        Gets the bit string representing all its member build scripts' bit
          strings AND'd together.
        """
        return self._group_bit_string

