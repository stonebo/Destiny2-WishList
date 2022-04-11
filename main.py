import logging
import sys
import os
from modules.utils import workspace
from modules import WishList


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    wish_file = os.path.join(workspace(), "wishlist", "sun.txt")
    wl = WishList()
    wl.import_dim_file(wish_file)
    wl.append_wish_list()
