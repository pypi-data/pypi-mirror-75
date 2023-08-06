#!/usr/bin/python

"""See https://github.com/zebracorn-engine/zebracorn/issues/65"""

import zebracorn
import regress

class EmuStopSegFault(regress.RegressTest):

    def runTest(self):
        ADDR = 0x10101000
        mu = zebracorn.Uc(zebracorn.UC_ARCH_X86, zebracorn.UC_MODE_32)
        mu.mem_map(ADDR, 1024 * 4)
        mu.mem_write(ADDR, b'\x41')
        mu.emu_start(ADDR, ADDR + 1, count=1)
        # The following should not trigger a null pointer dereference
        self.assertEqual(None, mu.emu_stop())

if __name__ == '__main__':
    regress.main()
