(* Definitions.v *)
(* Encoding of Turing Machines, Inputs, Certificates *)

Require Import Coq.Strings.String.
Require Import Coq.Lists.List.
Require Import Coq.Bool.Bool.
Import ListNotations.

Definition TM := string.
Definition Input := string.
Definition Certificate := string.

(* Abstract Verifier Definition *)
Definition verifier (M : TM) (x : Input) (c : Certificate) : bool :=
  true.
