hello(Time) --> greetingsH(Time), [username].

greetingsH(Time) --> startH(Time), continuationH.

startH(_) --> [hi].
startH(_) --> [hello].
startH(_) --> [hey].
startH(_) --> [howdy].
startH(morning) --> positiveH(good), [morning].
startH(afternoon) --> positiveH(good), [afternoon].
startH(evening) --> positiveH(good), [evening].
startH(night) --> positiveH(good), [night].
startH(_) --> [].

continuationH --> positiveH(continuation), [to,see,you].

positiveH(good) --> [good].
positiveH(good) --> [].
positiveH(continuation) --> [good].
positiveH(continuation) --> [great].
positiveH(continuation) --> [nice].
