
from os.path import exists
from pathlib import Path
import numpy as np
import pandas as pd


HEADER = ['id_review', 'caption', 'relative_date', 'retrieval_date', "absolute_date", 'rating', 'username',
          'n_review_user', 'n_photo_user', 'url_user']


class PlaceInfo:
    def __init__(self, name, location, channel, sort_by):
        self.name = name
        self.location = location
        self.channel = channel
        self.sort_by = sort_by
        
    def __str__(self):
        return 'data/' + self.name + "@" + str(self.location) + "/" + self.channel + "_" + self.sort_by + '_gm_reviews.xlsx'
    
    def get_name(self):
        return self.name + "@" + str(self.location)


class ExcelStorage():
    def __init__(self):
        pass
    
    def continue_process(self, place_info:PlaceInfo):
        outfile = str(place_info)
        return not exists(outfile)

    def save_reviews(self, place_info:PlaceInfo, list_reviews:list):
        Path('data/' + place_info.get_name()).mkdir(parents=True, exist_ok=True)
        outfile = str(place_info)
        writer = pd.ExcelWriter(outfile)
        sheet = np.array(list_reviews)
        temp_dataframe = pd.DataFrame(sheet, columns=HEADER)
        temp_dataframe.to_excel(writer, sheet_name=place_info.get_name())
        try:
            writer.close()
        except:
            del writer  # ; os.remove(path)
        return writer, outfile