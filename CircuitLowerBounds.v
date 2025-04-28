(* CircuitLowerBounds.v *)
(* Circuit Lower Bound Proof Sketch for L* *)

Require Import Definitions.
Require Import Diagonalization.

Theorem no_poly_circuit_L_star :
  forall (M : TM), exists (x : Input), L_star M x <> verifier M x "default_cert".
Proof.
  intros.
  (* Core Diagonalization Argument *)
  admit.
Admitted.
