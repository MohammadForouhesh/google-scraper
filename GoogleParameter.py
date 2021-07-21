
class DynamicParameters(object):
    file_path = None
    
    def __init__(self, load_path):
        super().__init__()
        __class__.file_path = load_path
        self.update()
    
    @classmethod
    def update(cls):
        array_line = []
        for line in open(cls.file_path).readlines():
            array_line.append(line)
            
        cls.sort_xpath_1 = array_line[0]                       #'//button[@data-value=\'Sort\']'
        cls.sort_xpath_2 = array_line[1]                       #"(//div[@class=\'gm2-body-1 k5lwKb\'])[position()=2]"
        cls.sort_menu_button_xpath = array_line[2]             #'//li[@role=\'menuitemradio\']'
        cls.channel_xpath = array_line[3]                      #"(//div[@class=\'gm2-body-1 k5lwKb\'])[position()=1]"
        cls.channel_menu_button_xpath = array_line[4]          #'//li[@role=\'menuitemradio\']'
        cls.get_reviews_xpath = array_line[5]                  #'ODSEW-ShBeI-content'  # section-review-content
        cls.section_review_id_review_button = array_line[6]    #'ODSEW-ShBeI-JIbuQc-menu ODSEW-ShBeI-JIbuQc-menu-SfQLQb-title'
        cls.section_review_id_review_span = array_line[7]      #"ODSEW-ShBeI-Hjleke-eEGnhe"
        cls.section_review_username_div = array_line[8]        #'ODSEW-ShBeI-title'
        cls.section_review_review_text_span = array_line[9]    #'ODSEW-ShBeI-text'
        cls.section_review_rating_span = array_line[10]        #'ODSEW-ShBeI-H1e3jb'
        cls.section_review_relative_date = array_line[11]      #'ODSEW-ShBeI-RgZmSc-date'
        cls.section_review_abnormal_rate = array_line[12]      #'ODSEW-ShBeI-RGxYjb-wcwwM'
        cls.section_review_abnorma_date = array_line[13]       #'ODSEW-ShBeI-RgZmSc-date-J42Xof-Hjleke'
        cls.section_review_subtiltle = array_line[14]          #'section-review-subtitle'
        cls.section_review_no_reviews = array_line[15]         #'ODSEW-ShBeI-VdSJob'
        cls.expand_reviews_xpath = array_line[16]              #"(//button[@jsaction=\'pane.review.expandReview\'])[position()=1]"
        cls.buggy_expand_button = array_line[17]               #"ODSEW-KoToPc-ShBeI.gXqMYb-hSRGPd"
        cls.more_button_link_xpath = array_line[18]            #'//button[@jsaction=\'pane.review.expandReview\']'
        cls.circle_loading_class = array_line[19]              #"wo1ice-loading-aZ2wEe"
        cls.scrollbox_css_selector = array_line[20]            #'div.section-layout.section-scrollbox.cYB2Ge-oHo7ed.cYB2Ge-ti6hGc'
        del array_line


if __name__ == '__main__':
    a = DynamicParameters('parameters.txt')
    print(a.scrollbox_css_selector)
    input()
    a.update()
    print(a.scrollbox_css_selector)
    