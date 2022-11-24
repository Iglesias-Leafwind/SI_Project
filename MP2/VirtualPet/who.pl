who(Whom) --> whoSubject(Whom,Context), whoContinuation(Context). 

whoSubject(me,i) --> [i].
whoSubject(me,im) --> [im].
whoSubject(me,my) --> [my].
whoSubject(you,you) --> [you].
whoSubject(you,youre) --> [youre].
whoSubject(you,your) --> [your].

whoContinuation(i) --> [am].
whoContinuation(i) --> [am],[called].
whoContinuation(im) --> [].
whoContinuation(im) --> [called].
whoContinuation(my) --> [name].
whoContinuation(you) --> [are].
whoContinuation(you) --> [are],[called].
whoContinuation(youre) --> [].
whoContinuation(youre) --> [called].
whoContinuation(your) --> [].
whoContinuation(your) --> [name].
whoContinuation(your) --> [called].