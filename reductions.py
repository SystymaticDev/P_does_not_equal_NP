# reductions.py

class ReductionError(Exception):
    """Custom exception for errors encountered during reductions."""
    pass

class ProblemReducer:
    """
    This class provides methods for reducing instances of one NP-complete
    problem into another. Each reduction function implements a known,
    standard transformation between problems.
    """
    @staticmethod
    def sat_to_3sat(cnf_formula):
        """
        Reduce a general SAT instance (in CNF form) into a 3-SAT instance.
        
        Parameters:
        cnf_formula (list of lists): Each sublist represents a clause, and each
                                     element in the sublist is a literal.
        
        Returns:
        list of lists: A new CNF formula in 3-SAT form (each clause has at most 3 literals).
        """
        three_sat_formula = []
        
        for clause in cnf_formula:
            if len(clause) <= 3:
                # Clause is already in 3-SAT form, just add it
                three_sat_formula.append(clause)
            else:
                # Break down larger clauses into multiple 3-literal clauses
                current_clause = clause[:3]
                remaining_literals = clause[3:]
                
                while remaining_literals:
                    # Create a new auxiliary variable
                    aux_var = f"aux_{len(three_sat_formula)}"
                    current_clause[-1] = aux_var
                    three_sat_formula.append(current_clause)
                    
                    # Prepare the next clause segment
                    current_clause = [f"~{aux_var}"] + remaining_literals[:2]
                    remaining_literals = remaining_literals[2:]
                
                # Add the final clause with 3 literals
                three_sat_formula.append(current_clause)
        
        return three_sat_formula
    
    @staticmethod
    def vertex_cover_to_clique(graph, k):
        """
        Reduce the Vertex Cover problem on a graph to the Clique problem on its complement.
        
        Parameters:
        graph (dict): An adjacency list representation of the graph.
        k (int): Size of the vertex cover to find.
        
        Returns:
        tuple: (complement_graph, k) where complement_graph is the complement graph,
               and k is the size of the clique to find.
        """
        # Create the complement graph
        nodes = list(graph.keys())
        complement_graph = {node: set() for node in nodes}
        
        for u in nodes:
            for v in nodes:
                if u != v and v not in graph[u]:
                    complement_graph[u].add(v)
        
        # The complement graph and the desired clique size
        return complement_graph, len(nodes) - k
    
    @staticmethod
    def clique_to_independent_set(graph, k):
        """
        Reduce the Clique problem to the Independent Set problem.
        
        Parameters:
        graph (dict): An adjacency list representation of the graph.
        k (int): Size of the clique to find.
        
        Returns:
        tuple: (complement_graph, k) where complement_graph is the complement graph,
               and k is the size of the independent set to find.
        """
        # The Independent Set problem on a graph is equivalent to
        # the Clique problem on its complement
        return ProblemReducer.vertex_cover_to_clique(graph, k)
    
    @staticmethod
    def subset_sum_to_knapsack(weights, target):
        """
        Convert a Subset Sum instance into a Knapsack problem instance.
        
        Parameters:
        weights (list of int): The weights (and values) of items.
        target (int): The target sum.
        
        Returns:
        tuple: (weights, weights, target) where the first weights list represents
               values, the second weights list represents weights, and target is the knapsack capacity.
        """
        # For Subset Sum, treat weights as both the values and the weights
        # of items in the Knapsack problem, and the target sum as the capacity.
        return weights, weights, target

# Example usage of reduction methods
if __name__ == "__main__":
    # Example SAT instance
    sat_formula = [[1, 2, 3], [4, 5, 6, 7], [8, 9]]
    reduced_3sat = ProblemReducer.sat_to_3sat(sat_formula)
    print("Reduced 3-SAT Formula:")
    print(reduced_3sat)

    # Example graph (as adjacency list) for Vertex Cover -> Clique
    graph = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B", "D"},
        "D": {"C"}
    }
    clique_graph, clique_size = ProblemReducer.vertex_cover_to_clique(graph, 2)
    print("\nComplement Graph (for Clique problem):")
    print(clique_graph)
    print("Clique Size to find:", clique_size)

    # Example Subset Sum instance
    weights = [1, 3, 5, 7]
    target = 8
    knapsack_instance = ProblemReducer.subset_sum_to_knapsack(weights, target)
    print("\nKnapsack Problem instance:")
    print("Values:", knapsack_instance[0])
    print("Weights:", knapsack_instance[1])
    print("Capacity:", knapsack_instance[2])
