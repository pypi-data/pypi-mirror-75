#!/usr/bin/env python

import regress
import zebracorn


class SegfaultOnStop(regress.RegressTest):
    def test(self):
        zebracorn.Uc(zebracorn.UC_ARCH_X86, zebracorn.UC_MODE_64).emu_stop()
        self.assertTrue(True, "If not reached, then we have a crashing bug.")

if __name__ == '__main__':
    regress.main()
