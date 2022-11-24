like(1) --> [more,or,less,'.'].
like(1) --> [i,like,it,a,little,bit,'.'].
like(1) --> [i,like,it,a,bit,'.'].
like(2) --> [i,like,it,'.'].
like(2) --> [it,is,good,'.'].
like(2) --> [it,is,nice,'.'].
like(3) --> [i,love,it,'!'].
like(3) --> [i,like,it,so,much,'!'].
like(4) --> [i,love,it,so,much,'!'].
like(4) --> [i,loveeeee,it,'!'].
like(5) --> [it,is,fantastic,'!'].
like(5) --> [it,is,the,best,'!'].

dislike(1) --> [it,is,not,good,'.'].
dislike(1) --> [it,isnt,good,'.'].
dislike(2) --> [i,dont,like,it,'.'].
dislike(2) --> [i,do,not,like,it,'.'].
dislike(3) --> [it,is,very,bad,'.'].
dislike(3) --> [will,anyone,like,it,'?'].
dislike(4) --> [i,hate,it,'.'].
dislike(4) --> [what,a,rubbish,'!'].
dislike(4) --> [it,is,a,rubbish,'!'].
dislike(5) --> [it,is,the,worst,'!'].
dislike(5) --> [i,wanna,to,clean,my,brain,so,i,can,forget,about,it,'!'].

synonym(like, love).
synonym(love, love).
synonym(like, favorite).
synonym(like, like).
synonym(dislike, hate).
synonym(hate, dislike).
synonym(dislike, dislike).
synonym(hate, hate).
synonym(hate,'do not like').
synonym(hate,'dont like').
synonym(detest, detest).
synonym(hate,detest).

synonym(yes, 'of course').
synonym(yes, sure).
synonym(yes,yes).
synonym(no,no).


synonym(movie,movie).
synonym(movie,film).
