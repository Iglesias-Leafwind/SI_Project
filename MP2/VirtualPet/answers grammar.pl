foodanswer(yes,Feeling,Food) --> acknowledgments, ["I"], feeling(Feeling), name(Food,Feeling).
foodanswer(_,Feeling,Food) --> ["I"], feeling(Feeling), name(Food,Feeling).

foodanswercheck(Feeling) --> ["I"], feeling(Feeling), [the].
foodanswercheck(Feeling) --> ["I"], feeling(Feeling).

nevertried(_) --> pausers, expressions, [it,so,let,me], food_testing, ["..."].
nevertried(Food) --> pausers, expressions, [Food],[so,let,me], food_testing, ["..."].

askquestion(likes_which_food,_) --> command(likes_which_food,_). 
askquestion(dislikes_which_food,_) --> command(dislikes_which_food,_). 
askquestion(want_to_play,Game) --> command(want_to_play,Game). 

accepting(yes) --> accept.
accepting(yes) --> pausers, accept.
accepting(no) --> decline.
accepting(no) --> pausers, decline.

accept --> [yes].
accept --> [sure].
accept --> [ok].
accept --> [lets,go].
accept --> ["I",would,love,to].
decline --> [no].
decline --> [nah].
decline --> [god,no].
decline --> [just,no].
decline --> [plz,no].
decline --> [please,no].

pausers --> [um].
pausers --> [uh].
pausers --> [er].
pausers --> [ah].
pausers --> [like].
pausers --> [okay,but].
pausers --> [right].
pausers --> [you,know].

expressions --> ["I",never,tried].
expressions --> [never,tried].

food_testing --> [see].
food_testing --> [try].
food_testing --> [taste].

acknowledgments --> [thanks].
acknowledgments --> [thanks,','].
acknowledgments --> [thank,you,','].

feeling(dislike) --> [hate].
feeling(dislike) --> ["don't", like].
feeling(dislike) --> [dislike].
feeling(like) --> [love].
feeling(like) --> [like].

name(Food,Feeling) --> [the], food(Food,Feeling).
name(Food,Feeling) --> food(Food,Feeling).

food(pineapple,like) --> [pineapple].
food(Food,Feeling) --> foodextension(Food,Feeling).

foodextension(null,null) --> [null].
