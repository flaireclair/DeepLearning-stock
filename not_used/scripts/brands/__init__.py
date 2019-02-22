# -*- coding: utf-8 -*-
from brands.nikkei225 import (
    nikkei225, nikkei225_s, nikkei225_excellent, nikkei225_excellent5,
    nikkei225_excellent10, nikkei225_excellent20, nikkei225_excellent30
)
from brands.tosho_1 import tosho_1
from brands.tosho_2 import tosho_2
from brands.tosho_jasdaq import tosho_jasdaq
from brands.tosho_mothers import tosho_mothers


#markets = [nikkei225, tosho_1, tosho_2, tosho_jasdaq, tosho_mothers]
#markets = [tosho_1, tosho_2, tosho_jasdaq, tosho_mothers]
all_brands = tosho_1 + tosho_2 + tosho_jasdaq + tosho_mothers


def brand_name(target_code):
    for (code, name, _) in all_brands:
        if code == target_code:
            return name
    return ''
