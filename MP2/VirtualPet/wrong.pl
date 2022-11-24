wrong(Times) --> startW(Times), continuationW, repeatW.


startW(0) --> appoligyW.
startW(0) --> [im], appoligyW.
startW(0) --> [i,am], appoligyW.
startW(1) --> [i,am], appoligyW, annoyedW.
startW(1) --> [im], appoligyW, annoyedW.
startW(2) --> [come,again,'?'].
startW(3) --> [come,again,'?'].
startW(3) --> ['...'].
startW(3) --> [i,dont,get,it].
startW(3) --> [i,do,not,get,it].
startW(4) --> ['...'].
startW(4) --> [i,dont,get,it].
startW(4) --> [i,do,not,get,it].
startW(5) --> [cmon,ffs,just,type,correctly].

annoyedW --> [i,still,did,not,get,that].
annoyedW --> [i,still,didnt,get,that].
appoligyW --> [sorry].

continuationW --> [].
continuationW --> [i,didnt,catch,that].
continuationW --> [i,did,not,catch,that].
continuationW --> [i,didnt,hear,what,you,said].
continuationW --> [i,did,not,hear,what,you,said].
continuationW --> [i,dont,understand].
continuationW --> [i,did,not,understand].

repeatW --> [].
repeatW --> [could,you,please,repeat,that].
repeatW --> [could,you,please,repeat].
repeatW --> [could,you,repeat].
repeatW --> [could,you,repeat,that].
repeatW --> [could,you,say,that,again].
repeatW --> [could,you,please,say,that,again].
repeatW --> [would,you,mind,repeating,that].

