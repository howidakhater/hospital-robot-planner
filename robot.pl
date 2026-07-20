%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% LOCATIONS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

connected(pharmacy, corridor).
connected(corridor, room3).

path(A, B) :- connected(A, B).
path(A, B) :- connected(B, A).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ACTIONS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Move action (robot moves, medicine location unchanged)
action(move(From, To),
       state(From, Carrying, MedLoc),
       state(To, Carrying, MedLoc)) :-
       path(From, To).

% Pick up medicine (only if at pharmacy and not carrying)
action(pick_up_medicine,
       state(pharmacy, no, pharmacy),
       state(pharmacy, yes, robot)).

% Drop medicine (can drop wherever robot is carrying it)
action(drop_medicine,
       state(Room, yes, robot),
       state(Room, no, Room)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GOAL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

goal_state(state(room3, _, room3)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PLANNER
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

plan(State, _, []) :-
    goal_state(State), !.

plan(State, Visited, [Act|Rest]) :-
    action(Act, State, NewState),
    \+ member(NewState, Visited),
    plan(NewState, [NewState|Visited], Rest).