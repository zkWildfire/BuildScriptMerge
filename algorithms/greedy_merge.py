from build_script import BuildScript
from build_script_group import BuildScriptGroup
import numpy as np
from typing import List

def merge_build_script_groups(
    groups: List[BuildScriptGroup],
    threshold: float) -> List[BuildScriptGroup]:
    """
    Merges BuildScriptGroups based on the dot product of their bit strings.
    @param groups List of BuildScriptGroup objects.
    @param threshold The minimum dot product value to consider merging two groups.
    @returns A new list of BuildScriptGroup objects after merging.
    """
    merged_groups = []

    while groups:
        current_group = groups.pop(0)
        max_dot_product = 0
        best_match = None

        # Calculate the dot product with all other groups
        for other_group in groups:
            dot_product = np.dot(current_group.group_bit_string, other_group.group_bit_string)

            if dot_product > max_dot_product:
                max_dot_product = dot_product
                best_match = other_group

        # Decide whether to merge or not based on the highest dot product
        if max_dot_product >= threshold:
            groups.remove(best_match)

            # Merge the groups by combining their build scripts and recalculating the bit string
            merged_group = BuildScriptGroup(
                current_group._build_scripts + best_match._build_scripts,
                current_group._unique_paths
            )
            merged_groups.append(merged_group)
        else:
            merged_groups.append(current_group)

    return merged_groups
