bye(Time,Bot) --> greetingsB(Time,Bot), [entity].
bye(Time,Bot) --> greetingsB(Time,Bot), [aligator].
bye(Time,Bot) --> greetingsB(Time,Bot).

greetingsB(Time,Bot) --> startB(Time,Bot), continuationB(Bot).
greetingsB(Time,Bot) --> continuationB(Bot).
greetingsB(Time,Bot) --> startB(Time,Bot).

startB(morning,yes) --> positiveB(good), [morning].
startB(afternoon,yes) --> positiveB(good), [afternoon].
startB(evening,yes) --> positiveB(good), [evening].
startB(night,yes) --> positiveB(good), [night].
startB(_,yes) --> [goodbye].
startB(_,yes) --> [bye].
startB(_,yes) --> [bye,bye].

continuationB(yes) --> [have,a],positiveB(continuation), [day].
continuationB(yes) --> [it,was],positiveB(continuation), [to,see,you].
continuationB(yes) --> [see,you,later].
continuationB(yes) --> [see,you,soon].
continuationB(no) --> [talk,to,you,later].
continuationB(no) --> [ive,got,to,get,going].
continuationB(no) --> [i,have,got,to,get,going].
continuationB(no) --> [i,must,be,going].
continuationB(yes) --> [take,it,easy].
continuationB(no) --> [im,off].
continuationB(no) --> [i,am,off].
continuationB(yes) --> [i,look,forward,to,our,next,meeting].
continuationB(yes) --> [until,next,time].
continuationB(yes) --> [take,care].
continuationB(yes) --> [later].
continuationB(yes) --> [laters].
continuationB(no) --> [catch,you,later].
continuationB(no) --> [peace].
continuationB(no) --> [peace,out].
continuationB(no) --> [im,out].
continuationB(no) --> [i,am,out].
continuationB(no) --> [im,out,of,here].
continuationB(no) --> [i,am,out,of,here].
continuationB(no) --> [i,gotta,jet].
continuationB(no) --> [i,gotta,take,off].
continuationB(no) --> [i,gotta,hit,the,road].
continuationB(no) --> [i,gotta,head,out].

positiveB(good) --> [good].
positiveB(good) --> [].
positiveB(continuation) --> [good].
positiveB(continuation) --> [great].
positiveB(continuation) --> [nice].
