foodquestion(Command,Food) --> command(Command,Food).

command(want_to_play,Game) -->  question(positive_directed), [want,to,play,a,game],[?].
command(want_to_play,Game) -->  question(positive_directed), [want,to,play], game(Game),[?].
command(want_to_play,Game) -->  [lets,play], game(Game),[?].
command(want_to_play,Game) -->  game(Game),[?].

command(like_certain_food,Food) --> question(positive_directed), [like], food(Food,_), [?].
command(hungry,_) --> question(positive_directed), [want,to,eat], [?].
command(hungry,Food) --> question(positive_directed), [want], food(Food,_), [?].
command(hungry,Food) --> question(positive_directed), [want,to,eat], food(Food,_), [?].
command(likes_which_food,_) --> question(what_non_negative), feelingQ(like), [?].
command(likes_which_food,_) --> question(what_non_negative), feelingQ(like), [to,eat,?].
command(dislikes_which_food,_) --> question(what_non_negative), feelingQ(hate), [?].
command(dislikes_which_food,_) --> question(what_non_negative), feelingQ(hate), [to,eat,?].
command(dislikes_which_food,_) --> question(what_negative), feelingQ(like), [?].
command(dislikes_which_food,_) --> question(what_negative), feelingQ(like), [to,eat,?].

question(positive_directed) --> [do,you].
question(what_non_negative) --> [what,do,you].
question(what_negative) --> [what,dont,you].

feelingQ(hate) --> [hate].
feelingQ(hate) --> [dislike].
feelingQ(hate) --> [not,like].
feelingQ(like) --> [love].
feelingQ(like) --> [like].

game(checkers) --> [checkers].