class DynamicParameters():
    def __init__(self):
        self.sort_xpath_1 = '//button[@data-value=\'Sort\']'
        self.sort_xpath_2 = "(//div[@class=\'gm2-body-1 k5lwKb\'])[position()=2]"
        self.sort_menu_button_xpath = '//li[@role=\'menuitemradio\']'
        self.channel_xpath = "(//div[@class=\'gm2-body-1 k5lwKb\'])[position()=1]"
        self.channel_menu_button_xpath = '//li[@role=\'menuitemradio\']'
        self.get_reviews_xpath = 'ODSEW-ShBeI-content'  # section-review-content
        self.section_review_id_review_button = 'ODSEW-ShBeI-JIbuQc-menu ODSEW-ShBeI-JIbuQc-menu-SfQLQb-title'
        self.section_review_id_review_span = "ODSEW-ShBeI-Hjleke-eEGnhe"
        self.section_review_username_div = 'ODSEW-ShBeI-title'
        self.section_review_review_text_span = 'ODSEW-ShBeI-text'
        self.section_review_rating_span = 'ODSEW-ShBeI-H1e3jb'
        self.section_review_relative_date = 'ODSEW-ShBeI-RgZmSc-date'
        self.section_review_abnormal_rate = 'ODSEW-ShBeI-RGxYjb-wcwwM'
        self.section_review_abnorma_date = 'ODSEW-ShBeI-RgZmSc-date-J42Xof-Hjleke'
        self.section_review_subtiltle = 'section-review-subtitle'
        self.section_review_no_reviews = 'ODSEW-ShBeI-VdSJob'
        self.expand_reviews_xpath = "(//button[@jsaction=\'pane.review.expandReview\'])[position()=1]"
        self.buggy_expand_button = "ODSEW-KoToPc-ShBeI.gXqMYb-hSRGPd"
        self.more_button_link_xpath = '//button[@jsaction=\'pane.review.expandReview\']'
        self.circle_loading_class = "wo1ice-loading-aZ2wEe"
        self.scrollbox_css_selector = 'div.section-layout.section-scrollbox.cYB2Ge-oHo7ed.cYB2Ge-ti6hGc'
    
    def update(self):
        pass