+ [ ] OBS Text(FreeType2) has a size limitation. It seems that if ticker size goes above a certain threshold, it does not display it in OBS.
    + Max-width of texttype2 depends on font, font-size. Max-width for current selection (Roboto,Mono,22) is 1260.
    + When the file is rewritten the start of the file moves if the length of text changes.
+ [ ] Does changing font type affect the cpv and thereby cps?
+ [x] The width of all characters in a font is not the same. Calculate the no of blank space for a clean slate frame of ticker.
    __Workaround: Use Monospace fonts.__ Currently using Roboto Mono.
+ [ ] Make file location fetching cross platform.
+ [ ] One feed will have different padding based on different tickers. One ticker can have multiple feeds.
