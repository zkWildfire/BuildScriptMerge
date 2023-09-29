from build_script_group import BuildScriptGroup
from typing import List

class Evaluator:
    @staticmethod
    def evaluate(groups: List[BuildScriptGroup]):
        """
        Evaluate and print statistics about a collection of BuildScriptGroup objects.
        @param groups List of BuildScriptGroup objects to evaluate.
        """
        num_groups = len(groups)
        total_build_scripts = 0
        total_unique_paths_per_group = 0
        average_similarity = 0

        print("Evaluating BuildScript Groups:")
        print(f"Total Number of Groups: {num_groups}")

        for i, group in enumerate(groups):
            num_build_scripts = len(group._build_scripts)
            total_build_scripts += num_build_scripts

            unique_paths_in_group = sum(group.group_bit_string)
            total_unique_paths_per_group += unique_paths_in_group

            # Compute average similarity within the group (not in relation to other groups)
            if num_build_scripts > 0:
                average_similarity += unique_paths_in_group / num_build_scripts

            print(f"  Group {i+1}:")
            print(f"    Number of Build Scripts: {num_build_scripts}")
            print(f"    Number of Unique Paths: {unique_paths_in_group}")

        if num_groups > 0:
            print("\nGlobal Statistics:")
            print(f"  Average Build Scripts per Group: {total_build_scripts / num_groups}")
            print(f"  Average Unique Paths per Group: {total_unique_paths_per_group / num_groups}")
            print(f"  Average Similarity Within Groups: {average_similarity / num_groups}")

