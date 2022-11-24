checkersmoveC(From,To) --> beforeFromC, moveC(From), beforeToC, moveC(To).
checkersmoveC(From,To) --> moveC(From), moveC(To).

beforeFromC --> [].
beforeFromC --> [from].
beforeFromC --> [move], pieceC, [from].
beforeFromC --> [move], pieceC.
beforeFromC --> [i,want,to,play], pieceC.
beforeFromC --> [i,want,to,move], pieceC.
beforeFromC --> [yes,sir,the],pieceC.
beforeFromC --> [yes,sir], pieceC.

beforeToC --> [to].
beforeToC --> [goes,to].
beforeToC --> [will,be,moved,to].
beforeToC --> [will,be,moved,to,the,point].

pieceC --> [].
pieceC --> [piece].
pieceC --> [object].

moveC('8b') --> ['8b'].
moveC('8d') --> ['8d'].
moveC('8f') --> ['8f'].
moveC('8h') --> ['8h'].
moveC('7a') --> ['7a'].
moveC('7c') --> ['7c'].
moveC('7e') --> ['7e'].
moveC('7g') --> ['7g'].
moveC('6b') --> ['6b'].
moveC('6d') --> ['6d'].
moveC('6f') --> ['6f'].
moveC('6h') --> ['6h'].
moveC('5a') --> ['5a'].
moveC('5c') --> ['5c'].
moveC('5e') --> ['5e'].
moveC('5g') --> ['5g'].
moveC('4b') --> ['4b'].
moveC('4d') --> ['4d'].
moveC('4f') --> ['4f'].
moveC('4h') --> ['4h'].
moveC('3a') --> ['3a'].
moveC('3c') --> ['3c'].
moveC('3e') --> ['3e'].
moveC('3g') --> ['3g'].
moveC('2b') --> ['2b'].
moveC('2d') --> ['2d'].
moveC('2f') --> ['2f'].
moveC('2h') --> ['2h'].
moveC('1a') --> ['1a'].
moveC('1c') --> ['1c'].
moveC('1e') --> ['1e'].
moveC('1g') --> ['1g'].

moveC('8b') --> ['b8'].
moveC('8d') --> ['d8'].
moveC('8f') --> ['f8'].
moveC('8h') --> ['h8'].
moveC('7a') --> ['a7'].
moveC('7c') --> ['c7'].
moveC('7e') --> ['e7'].
moveC('7g') --> ['g7'].
moveC('6b') --> ['b6'].
moveC('6d') --> ['d6'].
moveC('6f') --> ['f6'].
moveC('6h') --> ['h6'].
moveC('5a') --> ['a5'].
moveC('5c') --> ['c5'].
moveC('5e') --> ['e5'].
moveC('5g') --> ['g5'].
moveC('4b') --> ['b4'].
moveC('4d') --> ['d4'].
moveC('4f') --> ['f4'].
moveC('4h') --> ['h4'].
moveC('3a') --> ['a3'].
moveC('3c') --> ['c3'].
moveC('3e') --> ['e3'].
moveC('3g') --> ['g3'].
moveC('2b') --> ['b2'].
moveC('2d') --> ['d2'].
moveC('2f') --> ['f2'].
moveC('2h') --> ['h2'].
moveC('1a') --> ['a1'].
moveC('1c') --> ['c1'].
moveC('1e') --> ['e1'].
moveC('1g') --> ['g1'].

        