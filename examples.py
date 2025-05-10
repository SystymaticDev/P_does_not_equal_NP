# examples.py

from proof_systems import PropositionalProofSystem
from topology_tools import TopologicalAnalyzer
from experiments import run_sat_solver, analyze_instance_complexity

def example_workflow():
    # Demonstrate usage of the proof system
    proof_system = PropositionalProofSystem("PROOF_OF(P)")
    print("Proof valid:", proof_system.is_valid_proof("P"))
    print("Proof size:", proof_system.proof_size())

    # Demonstrate topology-based analysis
    analyzer = TopologicalAnalyzer("ComplexBooleanFunction")
    print("Topological complexity analysis:", analyzer.analyze_complexity())

    # Demonstrate SAT solver experiments
    print("SAT solver result:", run_sat_solver(10, 20))
    solve_times = analyze_instance_complexity(5)
    print("Instance solve times:", solve_times)

if __name__ == "__main__":
    example_workflow()
