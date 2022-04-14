import logging
import sys
import os
from modules.utils import workspace
from modules.wish_list.client import WishList
from modules.wish_list.export import HTMLExport


def find_wishlist(name: str):
    return os.path.join(workspace(), "wishlist", f"{name}.txt")


def html_output(name: str):
    return os.path.join(workspace(), "docs", f"{name}.html")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    wishlist_name = "stonebo"
    wish_file = find_wishlist(wishlist_name)
    wl = WishList(profile=wishlist_name)
    wl.import_dim_file(wish_file)
    wl.append_wish_list()

    excel = HTMLExport(html_output(wishlist_name), profile=wishlist_name)
    excel.process()
    excel.save()