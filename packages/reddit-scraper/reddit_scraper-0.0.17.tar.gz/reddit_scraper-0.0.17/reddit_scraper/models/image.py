# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Dict, List, Optional, Tuple

# Pip
from kcu import strings

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Image ------------------------------------------------------------- #

class Image:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        preview_dict: Dict
    ):
        try:
            img_dict = preview_dict['images'][0]['source']

            self.url = 'https://i.redd.it/' + strings.between(img_dict['url'], 'redd.it/', '?')
            self.width = img_dict['width']
            self.height = img_dict['height']
        except:
            self.url = None
            self.width = None
            self.height = None


# ---------------------------------------------------------------------------------------------------------------------------------------- #