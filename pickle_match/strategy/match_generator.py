from random import shuffle
import collections
from pickle_match.models.match import Match

class MatchGenerator:
    def __init__(self, pairs, constraints):
        self.nodes = pairs
        self.constraints_map = collections.defaultdict(list)
        for constraint in constraints:
            self.constraints_map[constraint.pair].append(constraint)

    def _check_constraints(self, matches):
        for match in matches:
            first, second = match.first, match.second
            for constraint in self.constraints_map[first]:
                if not constraint.allowed(second):
                    return False

            for constraint in self.constraints_map[second]:
                if not constraint.allowed(first):
                    return False
        
        return True
    
    def generate(self):
        """
        Pick completely random matches, and if they don't match constraints try again.
        """
        while True:
            shuffled_nodes = [node for node in self.nodes]
            shuffle(shuffled_nodes)

            matches = [
                Match(first=self.nodes[idx], second=shuffled_nodes[idx])
                for idx in range(len(self.nodes))
            ]

            if self._check_constraints(matches):
                return matches





