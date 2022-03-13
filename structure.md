+ Ticker
    + SCREEN_SIZE (cpv)
    + SPEED (cps)
    + switchToNextFeed()
        + changeFeedText()
        + changeFeedImage()
    + SAVE_FILE
    + FONT_SIZE
    + EMPTY_TIME : Amount of time in secs we want to ticker to go blank in order to switch feeds
    + startFeed()
    + Feed
        + SOURCE_NAME
        + SOURCE_IMAGE
        + SOURCE_URL
        + SIZE
        + TIME_TO_CYCLE
        + calculateTimeToCycle(SIZE,SCREEN_SIZE,SPEED,EMPTY_TIME)
        + FeedText
            + HEADLINES_LIST
            + extractHeadlines()
            + SEPARATOR
            + PADDING
            + calculatePadding()
            + addPadding()
            + NUMBER_OF_HEADLINES
            + COURTESY_TEXT
            + saveToFile()
        

