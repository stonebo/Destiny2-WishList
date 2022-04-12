import logging
import sys
import os
from modules.utils import workspace
from modules.wish_list.client import WishList
from modules.wish_list.export import ExcelExport


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # wish_file = os.path.join(workspace(), "wishlist", "sun.txt")
    # wl = WishList()
    # wl.import_dim_file(wish_file)
    # wl.append_wish_list()
    excel = ExcelExport("1.xlsx")
    excel.process()
    print("end")