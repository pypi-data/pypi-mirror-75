#!/usr/bin/env python

"""https://github.com/zebracorn-engine/zebracorn/issues/165"""

import zebracorn

def hook_mem_read_unmapped(mu, access, address, size, value, user_data):
    pass

mu = zebracorn.Uc(zebracorn.UC_ARCH_X86, zebracorn.UC_MODE_32)

try:
    for x in range(0, 1000):
        mu.hook_add(zebracorn.UC_HOOK_MEM_READ_UNMAPPED, hook_mem_read_unmapped, None)
except zebracorn.UcError as e:
    print("ERROR: %s" % e)
