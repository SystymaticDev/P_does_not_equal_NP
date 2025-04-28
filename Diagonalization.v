(* Diagonalization.v *)
(* Construction of the Hard Language L* *)

Require Import Definitions.

Definition L_star (M : TM) (x : Input) : bool :=
  negb (verifier M x "default_cert").
