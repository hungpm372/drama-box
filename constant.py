class DramaBoxConstant:
    BASE_URL = "https://www.dramaboxapp.com/browse/0/"
    TOTAL_PAGE = 17
    DEFAULT_DOWNLOAD_DIRECTORY = "D:\\Download"
    MOVIE_XPATH = '//*[@id="__next"]/main/div/div[2]/div[1]/div/a[1]'
    TITLE_XPATH = '//*[@id="__next"]/main/div[2]/div[1]/div[2]/div[1]/h1'
    DESCRIPTION_XPATH = '//*[@id="__next"]/main/div[2]/div[1]/div[2]/div[1]/p[2]'
    GENRE_XPATH = '//*[@id="__next"]/main/div[2]/div[1]/div[2]/div[1]/div/a'
    IMAGE_XPATH = '//*[@id="__next"]/main/div[2]/div[1]/div[1]/img'
    PLAY_BUTTON_XPATH = '//*[@id="__next"]/main/div[2]/div[1]/div[2]/div[2]/a'
    VIDEO_XPATH = '//*[@id="playVideo"]/video'
    EPISODES_XPATH = '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/a[2]'
    DOWNLOAD_BUTTON_XPATH = '//*[@id="__next"]/main/div[2]/div[1]/div[1]/a/button'


drama_box_constant = DramaBoxConstant()
