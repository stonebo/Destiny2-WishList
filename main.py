import logging
import sys
from modules import WishList


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    perks = [
        "dimwishlist:item=3886416794&perks=839105230,2420895100,509074078,3078487919",
        "dimwishlist:item=3886416794&perks=839105230,2420895100,2209918983,3078487919"
    ]
    wl = WishList()
    wl.import_dim_list(perks)
    wl.append_wish_list()
