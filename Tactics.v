(* Tactics.v *)
(* Helper Tactics *)

Ltac crush := repeat (simpl in *; try congruence; try contradiction; auto).
