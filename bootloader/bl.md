

## BL & fw

I disassembled a part of the bootloader (BL) binary just to find out that 

- The lower 4 KB of flash is allocated for BL

- How does the BL launch the fw: Mask the lower 4 KB of flash by FLASH_MASK register, 
and then request system reset ( soft rest of cortex-m0 CPU )
