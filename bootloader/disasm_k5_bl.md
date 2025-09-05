

# K5 Bootloader Disassemble


Bootloader size is 4 KB


```sh
python3 bin2hex.py dump_k5_egzumer022_full.bin --offset 0 --size 4096  > disasm_k5_bl.md
```

Vector table size: 48 * 4 = 192 (0xc0) 

```
offset = 0
base = 0
size = 0x00001000 (4096)
file size = 65536
0000: 15d8
0002: 2000
0004: 00d5
0006: 0000
0008: 00d9
000a: 0000
000c: 00db
000e: 0000
0010: 0000
0012: 0000
0014: 0000
0016: 0000
0018: 0000
001a: 0000
001c: 0000
001e: 0000
0020: 0000
0022: 0000
0024: 0000
0026: 0000
0028: 0000
002a: 0000
002c: 00dd
002e: 0000
0030: 0000
0032: 0000
0034: 0000
0036: 0000
0038: 00df
003a: 0000
003c: 00e1
003e: 0000
0040: 00e3
0042: 0000
0044: 00e5
0046: 0000
0048: 00e7
004a: 0000
004c: 00e9
004e: 0000
0050: 00eb
0052: 0000
0054: 00ed
0056: 0000
0058: 00ef
005a: 0000
005c: 00f1
005e: 0000
0060: 00f3
0062: 0000
0064: 00f5
0066: 0000
0068: 00f7
006a: 0000
006c: 00f9
006e: 0000
0070: 00fb
0072: 0000
0074: 00fd
0076: 0000
0078: 00ff
007a: 0000
007c: 0101
007e: 0000
0080: 0103
0082: 0000
0084: 0105
0086: 0000
0088: 0107
008a: 0000
008c: 0109
008e: 0000
0090: 010b
0092: 0000
0094: 010d
0096: 0000
0098: 010f
009a: 0000
009c: 0111
009e: 0000
00a0: 0113
00a2: 0000
00a4: 0115
00a6: 0000
00a8: 0117
00aa: 0000
00ac: 0119
00ae: 0000
00b0: 011b
00b2: 0000
00b4: 011d
00b6: 0000
00b8: 011f
00ba: 0000
00bc: 0121
00be: 0000
```


## Vector Table

Decode vector table: 

```sh
python3 dec_vec.py ../openocd/dump_k5_egzumer022_full.bin
```


```
Initial SP:     200015d8
Reset_Handler:  000000d4
NMI_Handler:    000000d8
HardFault_Handler:      000000da
SVCall_Handler:         <INVALID:0>
PendSV_Handler:         <INVALID:0>
SysTick_Handler:        <INVALID:0>
IRQ_0_WWDT_Handler:     <INVALID:0>
IRQ_1_IWDT_Handler:     <INVALID:0>
IRQ_2_RTC_Handler:      <INVALID:0>
IRQ_3_DMA_Handler:      <INVALID:0>
IRQ_4_SARADC_Handler:   000000dc
IRQ_5_TIMER_BASE0_Handler:      <INVALID:0>
IRQ_6_TIMER_BASE1_Handler:      <INVALID:0>
IRQ_7_TIMER_PLUS0_Handler:      000000de
IRQ_8_TIMER_PLUS1_Handler:      000000e0
IRQ_9_PWM_BASE0_Handler:        000000e2
IRQ_10_PWM_BASE1_Handler:       000000e4
IRQ_11_PWM_PLUS0_Handler:       000000e6
IRQ_12_PWM_PLUS1_Handler:       000000e8
IRQ_13_UART0_Handler:   000000ea
IRQ_14_UART1_Handler:   000000ec
IRQ_15_UART2_Handler:   000000ee
IRQ_16_SPI0_Handler:    000000f0
IRQ_17_SPI1_Handler:    000000f2
IRQ_18_IIC0_Handler:    000000f4
IRQ_19_IIC1_Handler:    000000f6
IRQ_20_CMP_Handler:     000000f8
IRQ_21_TIMER_BASE2_Handler:     000000fa
IRQ_22_GPIOA5_Handler:  000000fc
IRQ_23_GPIOA6_Handler:  000000fe
IRQ_24_GPIOA7_Handler:  00000100
IRQ_25_GPIOB0_Handler:  00000102
IRQ_26_GPIOB1_Handler:  00000104
IRQ_27_GPIOC0_Handler:  00000106
IRQ_28_GPIOC1_Handler:  00000108
IRQ_29_GPIOA_Handler:   0000010a
IRQ_30_GPIOB_Handler:   0000010c
IRQ_31_GPIOC_Handler:   0000010e
```

## 00c0 init1() 

```
00c0: 4803      ; ldr r0 [pc, #0xc] ; 00d0 -> 200015d8
00c2: 4685      ; mov sp, r0        ; sp = 0x200015d8
00c4: f000      ; [...]
00c6: f874      ; bl [pc, #0xe8]    ; 01b0, call 01b0 load_ram_fw1()
00c8: 4800      ; ldr r0 [pc, #0x0] ; 0911
00ca: 4700      ; bx r0             ; goto 0910 xxx()
00cc: 0911  ; literal
00ce: 0000
00d0: 15d8  ; literal
00d2: 2000
```

## 00d4 Reset_Handler() 

```
00d4: 4813      ; ldr r0 [pc, #0x4c]    ; 0124 -> 00c1
00d6: 4700      ; bx r0                 ; goto 00c0 init1()
```


## 00d8 _

```
00d8: e7fe
00da: e7fe
00dc: e7fe
00de: e7fe
00e0: e7fe
00e2: e7fe
00e4: e7fe
00e6: e7fe
00e8: e7fe
00ea: e7fe
00ec: e7fe
00ee: e7fe
00f0: e7fe
00f2: e7fe
00f4: e7fe
00f6: e7fe
00f8: e7fe
00fa: e7fe
00fc: e7fe
00fe: e7fe
0100: e7fe
0102: e7fe
0104: e7fe
0106: e7fe
0108: e7fe
010a: e7fe
010c: e7fe
010e: e7fe
0110: e7fe
0112: e7fe
0114: e7fe
0116: e7fe
0118: e7fe
011a: e7fe
011c: e7fe
011e: e7fe
0120: e7fe
0122: 0000
0124: 00c1  ; literal pool
0126: 0000
0128: b530
012a: 460b
012c: 4601
012e: 2000
0130: 2220
0132: 2401
0134: e009
0136: 460d
0138: 40d5
013a: 429d
013c: d305
013e: 461d
0140: 4095
0142: 1b49
0144: 4625
0146: 4095
0148: 1940
014a: 4615
014c: 1e52
014e: 2d00
0150: dcf1
0152: bd30
0154: 4603
0156: 430b
0158: 079b
015a: d003
015c: e009
015e: c908
0160: 1f12
0162: c008
0164: 2a04
0166: d2fa
0168: e003
016a: 780b
016c: 7003
016e: 1c40
0170: 1c49
0172: 1e52
0174: d2f9
0176: 4770
0178: b2d2
017a: e001
017c: 7002
017e: 1c40
0180: 1e49
0182: d2fb
0184: 4770
0186: 2200
0188: e7f6
018a: b510
018c: 4613
018e: 460a
0190: 4604
0192: 4619
0194: f7ff
0196: fff0
0198: 4620
019a: bd10
019c: 2103
019e: 1d00
01a0: 1e40
01a2: 7803
01a4: 0212
01a6: 431a
01a8: 1e49
01aa: d5f9
01ac: 4610
01ae: 4770
```

## 01b0 load_ram_fw1()

```
01b0: 4c06      ; ldr r4 [pc, #0x18]    ; 01cc -> p1 = 0a04
01b2: 2501      ; movs r5, #0x1
01b4: 4e06      ; ldr r6 [pc, #0x18]    ; 01d0 -> p2 = 0a34
01b6: e005      ; b [pc, #0xa]          ; goto 01c4
01b8: 68e3      ; ldr r3, [r4, #0xc]    ; f = p1[3]
01ba: cc07      ; ldm r4!, { r0 - r2 }  ; r2:r0 = p1[2:0] ; p1 += 3
01bc: 432b      ; orrs r3, r5           ; f |= 1, set thumb state
01be: 3c0c      ; subs r4, #0xc         ; p1 -= 3
01c0: 4798      ; blx r3                ; call f(r0, r1, r2)  
01c2: 3410      ; adds r4, #0x10        ; p1 += 4
01c4: 42b4      ; cmp r4, r6            ; if p1 < p2
01c6: d3f7      ; bcc [pc, #-0x12]      ; goto 01b8
01c8: f7ff      ; [...]
01ca: ff7e      ; bl [pc, #-0x104]      ; call 00c8 xxx()
```

In flash memory space `[0a04, 0a34)` (0x30 = 12 words), every 4 words (in the order below) are a function call 

```
arg0, arg1, arg2, func
```

See [0a04](#0a04-load_ram_fw1_tbl) 

```
01cc: 0a04  ; literal
01ce: 0000
01d0: 0a34  ; 
01d2: 0000
```

## 01d4 _

```
01d4: b403
01d6: 4801
01d8: 9001
01da: bd01
01dc: 0381
01de: 2000
01e0: b403
01e2: 4801
01e4: 9001
01e6: bd01
01e8: 0115
01ea: 2000
01ec: b403
01ee: 4801
01f0: 9001
01f2: bd01
01f4: 0225
01f6: 2000
```

## 01f8 init_flash_safe()

Args:
- r0: read_mode


```
01f8: b403      ; push { r0, r1 }
01fa: 4801      ; ldr r0 [pc, #0x4]     ; 2000008d
01fc: 9001      ; str r0, [sp, #0x4]
01fe: bd01      ; pop { r0, pc }        ; Restore r0, pc = 2000008d : goto 2000008c
0200: 008d      ; literal
0202: 2000    
```

Branch to RAM fw at 0x2000008c (init_flash())


## 0204 init_chip_safe()


```
0204: b403      ; push { r0, r1 }
0206: 4801      ; ldr r0 [pc, #0x4]     ; 20000295
0208: 9001      ; str r0, [sp, #0x4]
020a: bd01      ; pop { r0, pc }        ; Restore r0 ; pc = 20000294
020c: 0295      ; literal 
020e: 2000     
```

Branch to [ram_fw1](#0a34-ram_fw1) at 0x20000294 (init_chip())


## 0210 _

```
0210: b403      ; push { r0, r1 }
0212: 4801      ; ldr r0 [pc, #0x4]
0214: 9001      ; str r0, [sp, #0x4]
0216: bd01
0218: 0001
021a: 2000
021c: b510
021e: 4809
0220: 4a09
0222: 8801
0224: 1889
0226: d006
0228: 2903
022a: d007
022c: 291a
022e: d101
0230: f000
0232: f80c
0234: bd10
0236: f000
0238: f819
023a: bd10
023c: f000
023e: f82a
0240: bd10
0242: 0000
0244: 0bc4
0246: 2000
0248: faea
024a: ffff
024c: 4905
024e: 7900
0250: 7809
0252: 4288
0254: d001
0256: 282a
0258: d102
025a: 4903
025c: 2001
025e: 7048
0260: 4770
0262: 0000
0264: 09fc
0266: 0000
0268: 03b4
026a: 2000
026c: b510
026e: 1d01
0270: 2268
0272: 4807
0274: f7ff
0276: ff6e
0278: b672
027a: 221a
027c: 2001
027e: 4904
0280: 0240
0282: f7ff
0284: ffa7
0286: b662
0288: 2000
028a: f000
028c: f879
028e: bd10
0290: 0fc4
0292: 2000
0294: b5f8
0296: 4c37
0298: 4605
029a: 7860
029c: 2801
029e: d005
02a0: 2100
02a2: 2201
02a4: 4608
02a6: f000
02a8: f879
02aa: bdf8
02ac: 7a68
02ae: 7a29
02b0: 0200
02b2: 4308
02b4: d01c
02b6: 7820
02b8: 2802
02ba: d1f6
02bc: 482e
02be: 6801
02c0: 2208
02c2: 4051
02c4: 6001
02c6: 7a68
02c8: 7a29
02ca: 0200
02cc: 4308
02ce: 8861
02d0: 1c49
02d2: 4288
02d4: d105
02d6: 1d28
02d8: f7ff
02da: ff60
02dc: 68a1
02de: 4288
02e0: d021
02e2: 2100
02e4: 2201
02e6: 4608
02e8: f000
02ea: f858
02ec: 2001
02ee: e03e
02f0: 1d28
02f2: f7ff
02f4: ff53
02f6: 60a0
02f8: 7ae8
02fa: 7aa9
02fc: 0200
02fe: 4308
0300: 80a0
0302: 2000
0304: 8060
0306: 2002
0308: 7020
030a: 2778
030c: b672
030e: 2600
0310: 2001
0312: 0271
0314: 0300
0316: 1808
0318: f7ff
031a: ff62
031c: 1c76
031e: b2b6
0320: 42be
0322: d3f5
0324: b662
0326: 22ff
0328: 4629
032a: 3201
032c: 3110
032e: 4813
0330: f7ff
0332: ff10
0334: b672
0336: 7a68
0338: 7a29
033a: 0200
033c: 4308
033e: 0201
0340: 2001
0342: 0300
0344: 1808
0346: 2240
0348: 490c
034a: f7ff
034c: ff4f
034e: b662
0350: 7a68
0352: 7a2a
0354: 0201
0356: 4311
0358: 8061
035a: 2200
035c: 68a0
035e: f000
0360: f81d
0362: 8860
0364: 88a1
0366: 1c40
0368: 4288
036a: d19e
036c: 2003
036e: 7020
0370: bdf8
0372: 0000
0374: 03b4
0376: 2000
0378: 1000
037a: 4006
037c: 0fc4
037e: 2000
0380: b51c
0382: 4a05
0384: 4669
0386: 800a
0388: 2204
038a: 804a
038c: 7108
038e: 2108
0390: 4668
0392: f000
0394: fa51
0396: bd1c
0398: 0517
039a: 0000
039c: b53e
039e: 4c06
03a0: 466b
03a2: 801c
03a4: 2408
03a6: 805c
03a8: 9001
03aa: 8119
03ac: 729a
03ae: 210c
03b0: 4668
03b2: f000
03b4: fa41
03b6: bd3e
03b8: 051a
03ba: 0000
03bc: b500
03be: b089
03c0: 21a3
03c2: 00c9
03c4: 4668
03c6: 8001
03c8: 2120
03ca: 8041
03cc: 4807
03ce: c80f
03d0: 9304
03d2: ab01
03d4: c307
03d6: 2210
03d8: 4905
03da: a805
03dc: f7ff
03de: feba
03e0: 2124
03e2: 4668
03e4: f000
03e6: fa28
03e8: b009
03ea: bd00
03ec: 11c4
03ee: 2000
03f0: 09fc
03f2: 0000
03f4: 4601
03f6: 4803
03f8: 014a
03fa: 1880
03fc: 6900
03fe: 0500
0400: 0d00
0402: 4770
0404: 1100
0406: 4000
0408: e00c
040a: bf00
040c: bf00
040e: bf00
0410: bf00
0412: bf00
0414: bf00
0416: bf00
0418: bf00
041a: bf00
041c: bf00
041e: bf00
0420: bf00
0422: 1e40
0424: 2800
0426: d1f0
0428: 4770
042a: 0000
042c: 4906
042e: 6809
0430: 6001
0432: 4905
0434: 6849
0436: 6041
0438: 4903
043a: 6889
043c: 6081
043e: 4902
0440: 68c9
0442: 60c1
0444: 4770
0446: 0000
0448: 0080
044a: 4000
044c: b530
044e: 4602
0450: 460b
0452: 4c0c
0454: 6824
0456: 2501
0458: 432c
045a: 4d0a
045c: 602c
045e: 2100
0460: e004
0462: 5c54
0464: 4d07
0466: 60ac
0468: 1c4c
046a: b2a1
046c: 4299
046e: dbf8
0470: 4c04
0472: 68e4
0474: b2a0
0476: 4c03
0478: 6824
047a: 0864
047c: 0064
047e: 4d01
0480: 602c
0482: bd30
0484: 3000
0486: 4000
```


## 0488 config_crc() 



```
0488: 20ff      ; movs r0, #0xff
048a: 3001      ; adds r0, #0x1         ; 0x100
048c: 4902      ; ldr r1 [pc, #0x8]     ; CRC
048e: 6008      ; str r0, [r1]          ; CRC_CR = 0x100
0490: 2000      ; movs r0, #0x0
0492: 6048      ; str r0, [r1, #0x4]    ; CRC_IV = 0
0494: 4770      ; bx lr
0496: 0000
0498: 3000  ; literal
049a: 4000
```


## 049c config_gpio() 



```
049c: 200f      ; movs r0, #0xf
049e: 0280      ; lsls r0, r0, #0xa     ; 3c00
04a0: 4904      ; ldr r1 [pc, #0x10]    ; 40060000, GPIOA
04a2: 6048      ; str r0, [r1, #0x4]    ; GPIODIR = 0x3c00, set output [13:10]
```

```
04a4: 2008      ; movs r0, #0x8
04a6: 4904      ; ldr r1 [pc, #0x10]    ; 40061000, GPIOC
04a8: 6048      ; str r0, [r1, #0x4]    ; GPIODIR = 0x8, set output [3]
04aa: 200f      ; movs r0, #0xf
04ac: 0280      ; lsls r0, r0, #0xa     ; 3c00
04ae: 6008      ; str r0, [r1]          ; GPIODATA = 0x3c00, set high [13:10]
04b0: 4770      ; bx lr
04b2: 0000
04b4: 0000  ; literal
04b6: 4006
04b8: 1000 ; 
04ba: 4006
```


## 04bc config_port()


IO config: 

- PA3, PA4: input, PU
- PA7: UART1_TX
- PA8: UART1_RX
- PC5: input, PU


```
04bc: 2001      ; movs r0, #0x1
04be: 0700      ; lsls r0, r0, #0x1c    ; 1 << 28
04c0: 4908      ; ldr r1 [pc, #0x20]    ; 04e4 -> 400b0000, PORTCON
04c2: 6008      ; str r0, [r1]          ; PORTA_SEL0 = 1 << 28 , PORTA7 = UART1_TX
04c4: 2001      ; movs r0, #0x1
04c6: 6048      ; str r0, [r1, #0x4]    ; PORTA_SEL1 = 1 , PORTA8 = UART1_RX
04c8: 20ff      ; movs r0, #0xff
04ca: 3019      ; adds r0, #0x19        ; 0x118
04cc: 4906      ; ldr r1 [pc, #0x18]    ; 04e8 -> 400b0100, PORTA_IE
04ce: 6008      ; str r0, [r1]          ; PORTA_IE = 0x118 , enable 3, 4, 8
04d0: 2018      ; movs r0, #0x18
04d2: 4906      ; ldr r1 [pc, #0x18]    ; 04ec -> 400b0200, PORTA_PU
04d4: 6008      ; str r0, [r1]          ; PORTA_PU = 0x18, enable 3, 4
04d6: 2020      ; movs r0, #0x20
04d8: 4903      ; ldr r1 [pc, #0xc]     ; 04e8 -> 400b0100, PORTA_IE
04da: 6088      ; str r0, [r1, #0x8]    ; PORTC_IE = 0x20, enable 5
04dc: 4903      ; ldr r1 [pc, #0xc]     ; 04ec -> 400b0200, PORTA_PU
04de: 6088      ; str r0, [r1, #0x8]    ; PORTC_PU = 0x20, enable 5
04e0: 4770      ; bx lr
04e2: 0000      ; lsls r0, r0, #0x0
```

```
04e4: 0000      ;  literal 
04e6: 400b       
04e8: 0100     ; 
04ea: 400b      
04ec: 0200      ; 
04ee: 400b   
```


## 04f0 _


```
04f0: b5f8      
04f2: 2001
04f4: 0780
04f6: 6880
04f8: 2180
04fa: 4308
04fc: 05c9
04fe: 6088
0500: 4825
0502: 6800
0504: 0840
0506: 0040
0508: 4923
050a: 6008
050c: 4823
050e: 6b84
0510: 0060
0512: 0b06
0514: 0fe7
0516: 2f00
0518: d002
051a: 4821
051c: 1834
051e: e001
0520: 481f
0522: 1b84
0524: 491f
0526: 4620
0528: f7ff
052a: fdfe
052c: 4605
052e: 481a
0530: 6045
0532: 200e
0534: 4918
0536: 6008
0538: 2004
053a: 6208
053c: 2000
053e: 61c8
0540: 20c7
0542: 6188
0544: 2000
0546: 6108
0548: 4817
054a: 6800
054c: 0840
054e: 0040
0550: 4915
0552: 6008
0554: 4910
0556: 310c
0558: 4814
055a: 6081
055c: 4914
055e: 60c1
0560: 21ff
0562: 3111
0564: 6041
0566: 2000
0568: 490f
056a: 6048
056c: 4811
056e: 6088
0570: 4811
0572: 490e
0574: 6008
0576: 2020
0578: 4907
057a: 6148
057c: 480a
057e: 6800
0580: 2101
0582: 4308
0584: 4908
0586: 6008
0588: 4803
058a: 6800
058c: 2101
058e: 4308
0590: 4901
0592: 6008
0594: bdf8
0596: 0000
0598: b800
059a: 4006
059c: 0040
059e: 4000
05a0: 6c00
05a2: 02dc
05a4: 988d
05a6: 0000
05a8: 1000
05aa: 4000
05ac: 1100
05ae: 4000
05b0: 03c4
05b2: 2000
05b4: 0f0f
05b6: 0000
05b8: 6fff
05ba: 0000
05bc: b5f0
05be: b087
05c0: 488e
05c2: 8804
05c4: 2000
05c6: f7ff
05c8: ff15
05ca: 4606
05cc: 488c
05ce: 9006
05d0: e10e
05d2: e012
05d4: 9806
05d6: 5d00
05d8: 28ab
05da: d100
05dc: e00f
05de: 4987
05e0: 8809
05e2: 1c48
05e4: 17c1
05e6: 0d49
05e8: 1809
05ea: 12c9
05ec: 02c9
05ee: 1a41
05f0: 4a82
05f2: 8011
05f4: 4610
05f6: 8804
05f8: bf00
05fa: 42b4
05fc: d1ea
05fe: bf00
0600: 42b4
0602: d103
0604: 2000
0606: 43c0
0608: b007
060a: bdf0
060c: 42b4
060e: da03
0610: 1b30
0612: b280
0614: 9003
0616: e005
0618: 2001
061a: 02c0
061c: 1830
061e: 1b00
0620: b280
0622: 9003
0624: 9803
0626: 2808
0628: da02
062a: 2000
062c: 43c0
062e: e7eb
0630: 1c60
0632: 17c1
0634: 0d49
0636: 1809
0638: 12c9
063a: 02c9
063c: 1a42
063e: 9906
0640: 5c89
0642: 29cd
0644: d00d
0646: 496d
0648: 8809
064a: 1c48
064c: 17c1
064e: 0d49
0650: 1809
0652: 12c9
0654: 02c9
0656: 1a41
0658: 4a68
065a: 8011
065c: 4610
065e: 8804
0660: e0c6
0662: 1ca0
0664: 17c1
0666: 0d49
0668: 1809
066a: 12c9
066c: 02c9
066e: 1a41
0670: b28c
0672: 1c60
0674: 17c1
0676: 0d49
0678: 1809
067a: 12c9
067c: 02c9
067e: 1a42
0680: 9906
0682: 5c89
0684: 020f
0686: 9a06
0688: 5d12
068a: 4317
068c: 4638
068e: 3008
0690: 2101
0692: 02c9
0694: 4288
0696: d904
0698: 4858
069a: 8006
069c: 2000
069e: 43c0
06a0: e7b2
06a2: 4638
06a4: 3008
06a6: 9903
06a8: 4281
06aa: d202
06ac: 2000
06ae: 43c0
06b0: e7aa
06b2: 1ca0
06b4: 17c1
06b6: 0d49
06b8: 1809
06ba: 12c9
06bc: 02c9
06be: 1a41
06c0: b28c
06c2: 19e1
06c4: 1c88
06c6: 17c1
06c8: 0d49
06ca: 1809
06cc: 12c9
06ce: 02c9
06d0: 1a41
06d2: b28d
06d4: 4629
06d6: 17ea
06d8: 0d52
06da: 1852
06dc: 12d2
06de: 02d2
06e0: 1aab
06e2: 9a06
06e4: 5cd2
06e6: 2adc
06e8: d10a
06ea: 1c68
06ec: 17c2
06ee: 0d52
06f0: 1812
06f2: 12d2
06f4: 02d2
06f6: 1a83
06f8: 9a06
06fa: 5cd2
06fc: 2aba
06fe: d004
0700: 483e
0702: 8006
0704: 2000
0706: 43c0
0708: e77e
070a: 42a5
070c: da11
070e: 2001
0710: 02c0
0712: 1b02
0714: 483a
0716: 1901
0718: 483a
071a: f7ff
071c: fd1b
071e: 2101
0720: 02c9
0722: 1b09
0724: 4a37
0726: 1888
0728: 462a
072a: 4935
072c: f7ff
072e: fd12
0730: e005
0732: 1b2a
0734: 4832
0736: 1901
0738: 4832
073a: f7ff
073c: fd0b
073e: 1ca8
0740: 17c1
0742: 0d49
0744: 1809
0746: 12c9
0748: 02c9
074a: 1a41
074c: b289
074e: 9104
0750: 482a
0752: 8800
0754: 9904
0756: 4281
0758: da0f
075a: 4a28
075c: 8812
075e: 2301
0760: 02db
0762: 1a99
0764: 4a26
0766: 4b25
0768: 881b
076a: 18d0
076c: f7ff
076e: fd0b
0770: 4823
0772: 9904
0774: f7ff
0776: fd07
0778: e009
077a: 4b20
077c: 881b
077e: 9a04
0780: 1ad1
0782: 4a1f
0784: 4b1d
0786: 881b
0788: 18d0
078a: f7ff
078c: fcfc
078e: 491b
0790: 9804
0792: 8008
0794: 481c
0796: 9005
0798: 2000
079a: 9002
079c: e00f
079e: 4919
07a0: 9802
07a2: 5c08
07a4: 9902
07a6: 070a
07a8: 0f12
07aa: 9905
07ac: 5c89
07ae: 4048
07b0: 4a14
07b2: 9902
07b4: 5450
07b6: 9802
07b8: 1c40
07ba: b280
07bc: 9002
07be: 1cb9
07c0: 9802
07c2: 4288
07c4: dbeb
07c6: 480f
07c8: 5dc0
07ca: 4a0e
07cc: 1c79
07ce: 5c51
07d0: 0209
07d2: 4308
07d4: 9001
07d6: 4639
07d8: 4610
07da: f7ff
07dc: fe37
07de: 4601
07e0: 9801
07e2: 4281
07e4: d002
07e6: 2000
07e8: 43c0
07ea: e70d
07ec: 2000
07ee: e70b
07f0: 42b4
07f2: d000
07f4: e6ed
07f6: 2000
07f8: 43c0
07fa: e705
07fc: 03b0
07fe: 2000
0800: 03c4
0802: 2000
0804: 0bc4
0806: 2000
0808: 09ec
080a: 0000
080c: b510
080e: 4602
0810: 2000
0812: e00b
0814: 5c13
0816: 4c07
0818: 60a3
081a: bf00
081c: 4b05
081e: 695b
0820: 2401
0822: 03a4
0824: 4023
0826: 2b00
0828: d1f8
082a: 1c40
082c: 4288
082e: d3f1
0830: bd10
0832: 0000
0834: b800
0836: 4006
0838: b5f8
083a: 4606
083c: 460d
083e: 4f14
0840: 2400
0842: e007
0844: 5d30
0846: 0721
0848: 0f09
084a: 5c79
084c: 4048
084e: 5530
0850: 1c60
0852: b284
0854: 42ac
0856: dbf5
0858: 21ab
085a: 4668
085c: 7001
085e: 21cd
0860: 7041
0862: 7085
0864: 1229
0866: 70c1
0868: 2104
086a: f7ff
086c: ffcf
086e: 4629
0870: 4630
0872: f7ff
0874: ffcb
0876: 21ff
0878: 4668
087a: 7001
087c: 7041
087e: 21dc
0880: 7081
0882: 21ba
0884: 70c1
0886: 2104
0888: f7ff
088a: ffc0
088c: bdf8
088e: 0000
0890: 09ec
0892: 0000
```

## 0894 init_clock()


```
0894: 2000      ; movs r0, #0x0
0896: 4909      ; ldr r1 [pc, #0x24]    ; 40000800, PMU
0898: 6908      ; ldr r0, [r1, #0x10]   ; SRC_CFG -> reg
089a: 2101      ; movs r1, #0x1
089c: 4308      ; orrs r0, r1           ; reg.RCHF_EN = 1
089e: 2202      ; movs r2, #0x2
08a0: 4601      ; mov r1, r0            ; 
08a2: 4391      ; bics r1, r2           ; reg.RCHF_FSEL = 0, select 48 MHz
08a4: 4608      ; mov r0, r1
08a6: 4905      ; ldr r1 [pc, #0x14]    ; 
08a8: 6108      ; str r0, [r1, #0x10]   ; SRC_CFG = reg
08aa: 2102      ; movs r1, #0x2
08ac: 074a      ; lsls r2, r1, #0x1d    ; 40000000, SYSCON
08ae: 6011      ; str r1, [r2]          ; CLK_SEL = 2 , ??
08b0: 0749      ; lsls r1, r1, #0x1d
08b2: 6849      ; ldr r1, [r1, #0x4]    ; DIV_CLK_GATE -> reg
08b4: 0849      ; lsrs r1, r1, #0x1
08b6: 0049      ; lsls r1, r1, #0x1     ; reg.DIV_CLK_GATE =0
08b8: 6051      ; str r1, [r2, #0x4]
08ba: 4770      ; bx lr
08bc: 0800  ; literal
08be: 4000
```


## 08c0 init_chip1()

```
08c0: b510      ; push { r4, lr }
08c2: 2000      ; movs r0, #0x0
08c4: f7ff      ; [...]
08c6: fc98      ; bl [pc, #-0x6d0]      ; call 01f8 init_flash_safe(0)  
08c8: f7ff      ; [...]
08ca: fc9c      ; bl [pc, #-0x6c8]      ; call 0204 init_chip_safe()
08cc: f7ff      ; [...]
08ce: ffe2      ; bl [pc, #-0x3c]       ; call 0894 init_clock()
08d0: 4804      ; ldr r0 [pc, #0x10]    ; 02dc6c00 = 48000000
08d2: 4905      ; ldr r1 [pc, #0x14]    ; 200003a8, sys_clock_freq
08d4: 6008      ; str r0, [r1]          ; sys_clock_freq = 48000000
08d6: 2030      ; movs r0, #0x30
08d8: 4904      ; ldr r1 [pc, #0x10]    ; 200003ac, sys_clock_freq_mhz
08da: 6008      ; str r0, [r1]          ; sys_clock_freq_mhz = 48
08dc: 2001      ; movs r0, #0x1
08de: f7ff      ; [...]
08e0: fc8b      ; bl [pc, #-0x6ea]      ; call 01f8, init_flash_safe(1)  
08e2: bd10      ; pop { r4, pc }
08e4: 6c00  ; literal
08e6: 02dc
08e8: 03a8  ; 
08ea: 2000
08ec: 03ac ; 
08ee: 2000
```

## 08f0 copy_words()

Args:
- r0: src
- r1: dest
- r2: bytes

Copy `bytes / 4` words from `dest` to `src`


```
08f0: e002      ; b [pc, #0x4]      ; goto 08f8
08f2: c808      ; ldm r0!, { r3 }   ; r3 = src[0] ; src++
08f4: 1f12      ; subs r2, #0x4     ; bytes -= 4
08f6: c108      ; stm r1!, { r3 }   ; dest[0] = r3 ; dest ++
08f8: 2a00      ; cmp r2, #0x0
08fa: d1fa      ; bne [pc, #-0xc]   ; if bytes != 0, goto 08f2
08fc: 4770      ; bx lr             ; return
08fe: 4770      ; bx lr
```

## 0900 set_words_0() 

Args:
- r0: src (unused)
- r1: dest
- r2: bytes

Set `bytes / 4` words at base address `dest` to zero


```
0900: 2000      ; movs r0, #0x0
0902: e001      ; b [pc, #0x2]          ; goto 0908
0904: c101      ; stm r1!, { r0 }       ; dest[0] = 0
0906: 1f12      ; subs r2, #0x4         ; bytes -= 4
0908: 2a00      ; cmp r2, #0x0          ; if ..
090a: d1fb      ; bne [pc, #-0xa]       ; bytes != 0, goto 0904
090c: 4770      ; bx lr                 ; return
090e: 0000      ; lsls r0, r0, #0x0
```

## 0910 xxxx()


```
0910: b5f8      ; push { r3 - r7, lr }
0912: f7ff      ; [...]
0914: ffd5      ; bl [pc, #-0x56]           ; call 08c0, init_chip1()
```

```
0916: 482a      ; ldr r0 [pc, #0xa8]        ; 09c0 -> 08000085
0918: 0781      ; lsls r1, r0, #0x1e    ; 40000000, SYSCON
091a: 6088      ; str r0, [r1, #0x8]    ; DEV_CLK_GATE = 08000085
```

Enbaled periperal clock: 

- 0: GPIOA_CLK_GATE
- 2: GPIOC_CLK_GATE
- 7: UART1_CLK_GATE
- 27: CRC_CLK_GATE


```
091c: f7ff      ; [...]
091e: fdce      ; bl [pc, #-0x464]      ; call 04bc, config_port()
0920: f7ff      ; [...]
0922: fdbc      ; bl [pc, #-0x488]      ; call 049c, config_gpio()
0924: f7ff      ; [...]
0926: fdb0      ; bl [pc, #-0x4a0]      ; call 0488, config_crc()
0928: f7ff      ; [...]
092a: fde2      ; bl [pc, #-0x43c]      ; call 
092c: 4825      ; ldr r0 [pc, #0x94]
092e: f7ff      ; [...]
0930: fd7d      ; bl [pc, #-0x506]
0932: 4825      ; ldr r0 [pc, #0x94]
0934: 6800      ; ldr r0, [r0]
0936: 4c25      ; ldr r4 [pc, #0x94]
0938: 06c0      ; lsls r0, r0, #0x1b
093a: 0f80      ; lsrs r0, r0, #0x1e
093c: 4f24      ; ldr r7 [pc, #0x90]
093e: 4d25      ; ldr r5 [pc, #0x94]
0940: 2803      ; cmp r0, #0x3
0942: d10c      ; bne [pc, #0x18]
0944: 6820      ; ldr r0, [r4]
0946: 0680      ; lsls r0, r0, #0x1a
0948: d409      ; bmi [pc, #0x12]
094a: 4638      ; mov r0, r7
094c: f7ff      ; [...]
094e: fd5c      ; bl [pc, #-0x548]
0950: 6820      ; ldr r0, [r4]
0952: 0680      ; lsls r0, r0, #0x1a
0954: d403      ; bmi [pc, #0x6]
0956: 2001      ; movs r0, #0x1
0958: 7028      ; strb r0, [r5]
095a: 2008      ; movs r0, #0x8
095c: 6020      ; str r0, [r4]
095e: 210c      ; movs r1, #0xc
0960: 481d      ; ldr r0 [pc, #0x74]
0962: f7ff      ; [...]
0964: ff53      ; bl [pc, #-0x15a]
0966: 2102      ; movs r1, #0x2
0968: a01c      ; add r0, pc, #0x70
096a: f7ff      ; [...]
096c: ff4f      ; bl [pc, #-0x162]
096e: 7828      ; ldrb r0, [r5]
0970: 4e1b      ; ldr r6 [pc, #0x6c]
0972: 2801      ; cmp r0, #0x1
0974: d111      ; bne [pc, #0x22]
0976: f7ff      ; [...]
0978: fe21      ; bl [pc, #-0x3be]
097a: 2800      ; cmp r0, #0x0
097c: d101      ; bne [pc, #0x2]
097e: f7ff      ; [...]
0980: fc4d      ; bl [pc, #-0x766]
0982: 7828      ; ldrb r0, [r5]
0984: 2801      ; cmp r0, #0x1
0986: d00f      ; beq [pc, #0x1e]
0988: 2802      ; cmp r0, #0x2
098a: d014      ; beq [pc, #0x28]
098c: 2803      ; cmp r0, #0x3
098e: d1f2      ; bne [pc, #-0x1c]
0990: 2000      ; movs r0, #0x0
0992: 6020      ; str r0, [r4]
0994: 4813      ; ldr r0 [pc, #0x4c]
0996: f7ff      ; [...]
0998: fd37      ; bl [pc, #-0x592]
099a: 4630      ; mov r0, r6
099c: f7ff      ; [...]
099e: fd34      ; bl [pc, #-0x598]
09a0: f7ff      ; [...]
09a2: fc36      ; bl [pc, #-0x794]
09a4: 2000      ; movs r0, #0x0
09a6: bdf8      ; pop { r3 - r7, pc }
09a8: 4638      ; mov r0, r7
09aa: f7ff      ; [...]
09ac: fd2d      ; bl [pc, #-0x5a6]
09ae: f7ff
09b0: fd05
09b2: 4630
09b4: e000
09b6: 480c
09b8: f7ff
09ba: fd26
09bc: e7db
09be: 0000
09c0: 0085  ; literal 
09c2: 0800
09c4: 11c4
09c6: 2000
09c8: 0000
09ca: 4006
09cc: 1000
09ce: 4006
09d0: 0d40
09d2: 0003
09d4: 03b4
09d6: 2000
09d8: 09fc
09da: 0000
09dc: 0a0d
09de: 0000
09e0: 86a0
09e2: 0001
09e4: 93e0
09e6: 0004
09e8: 2710
09ea: 0000
09ec: 6c16
09ee: e614
09f0: 912e
09f2: 400d
09f4: 3521
09f6: 40d5
09f8: 0313
09fa: 80e9
09fc: 2e32
09fe: 3030
0a00: 302e
0a02: 0036
```

## 0a04 load_ram_fw1_tbl

See [01b0](#01b0-load_ram_fw1)


```
0a04: 0a34  ; 1 ---------
0a06: 0000
0a08: 0000
0a0a: 2000
0a0c: 03a8  ; 0x3a8 = 936
0a0e: 0000
0a10: 08f0  ; 08f0 copy_words()
0a12: 0000
0a14: 0ddc  ; 2 -----------
0a16: 0000
0a18: 03a8
0a1a: 2000
0a1c: 001c  ; 0x1c = 28 
0a1e: 0000
0a20: 08f0  ; 08f0 copy_words()
0a22: 0000
0a24: 0df8  ; 3 -------
0a26: 0000
0a28: 03c4
0a2a: 2000
0a2c: 1214
0a2e: 0000
0a30: 0900  ; 0900 set_words_0()
0a32: 0000
```

```c
copy_words(0x0a34, 0x20000000, 0x03a8);     // Copy from [0a34, 0ddc) to [20000000, 200003a8)
copy_words(0x0ddc, 0x200003a8, 0x1c);       // Copy from [0ddc, 0df8) to [200003a8, 200003c4 )
set_words_0(0, 0x200003c4, 0x1214)          // Set [200003c4, 200015d8) to zero
```

Copy from flash `[0a34, 0df8)` to RAM address `[20000000, 200003c4)` (the beginning of the RAM).
Clear the rest of the RAM (until SP 0x200015d8) to zero


## 0a34 ram_fw1

Flash content `[0a34, 0df8)` (0x3c4 = 964 bytes) will be loaded to RAM (at the base address 0x20000000) 

See [01b0](#01b0-load_ram_fw1)


```sh
python3 bin2hex.py dump_k5_egzumer022_full.bin --offset 0x0a34 --base 0x20000000 --size 964 > tmp.txt
```

```
offset = 0x00000a34 (2612)
base = 0x20000000 (536870912)
size = 0x000003c4 (964)
file size = 65536
20000000: 2000
20000002: 4907
20000004: 6208
20000006: 2002
20000008: 6208
2000000a: 2006
2000000c: 6208
2000000e: f3bf
20000010: 8f4f
20000012: 4804
20000014: 4904
20000016: 60c8
20000018: f3bf
2000001a: 8f4f
2000001c: bf00
2000001e: e7fe
20000020: f000
20000022: 4006
20000024: 0004
20000026: 05fa
20000028: ed00
2000002a: e000
2000002c: 4804
2000002e: 6940
20000030: 2104
20000032: 4008
20000034: 2800
20000036: d001
20000038: 2001
2000003a: 4770
2000003c: 2000
2000003e: e7fc
20000040: f000
20000042: 4006
```

### 20000044 flash_is_busy()


```
20000044: 4804  ; ldr r0 [pc, #0x10]    ; FLASH _CTRL
20000046: 6940  ; ldr r0, [r0, #0x14]   ; FLASH_ST -> reg
20000048: 2102  ; movs r1, #0x2
2000004a: 4008  ; ands r0, r1           ; reg.BUSY
2000004c: 2800  ; cmp r0, #0x0
2000004e: d001  ; beq [pc, #0x2]        ; if !reg.BUSY, goto 20000054 ; else ..
20000050: 2001  ; movs r0, #0x1
20000052: 4770  ; bx lr                 ; return 1
20000054: 2000  ; movs r0, #0x0
20000056: e7fc  ; b [pc, #-0x8]     ; return 0
20000058: f000  ; literal
2000005a: 4006
```

### 2000005c flash_init_done()


```
2000005c: 4804  ; ldr r0 [pc, #0x10]        ; 4006f000, FLASH _CTRL
2000005e: 6940  ; ldr r0, [r0, #0x14]       ; FLASH_ST
20000060: 07c0  ; lsls r0, r0, #0x1f
20000062: 0fc0  ; lsrs r0, r0, #0x1f        ; FLASH_ST.INIT_BUSY
20000064: 2800  ; cmp r0, #0x0
20000066: d001  ; beq [pc, #0x2]            ; if FLASH_ST.INIT_BUSY == 0, goto 2000006c ; else ..
20000068: 2000  ; movs r0, #0x0
2000006a: 4770  ; bx lr                     ; return 0 
2000006c: 2001  ; movs r0, #0x1
2000006e: e7fc  ; b [pc, #-0x8]         ; goto 2000006a -> return 1
20000070: f000  ; literal 
20000072: 4006
```


### 20000074 flash_start()


```
20000074: b500  ; push { lr }
20000076: f000  ; [...]
20000078: f821  ; bl [pc, #0x42]        ; call 200000bc flash_unlock()
2000007a: 4803  ; ldr r0 [pc, #0xc]     ; 
2000007c: 6900  ; ldr r0, [r0, #0x10]   ; FLASH_START -> reg
2000007e: 2101  ; movs r1, #0x1
20000080: 4308  ; orrs r0, r1           ; reg.START = 1
20000082: 4901  ; ldr r1 [pc, #0x4]
20000084: 6108  ; str r0, [r1, #0x10]
20000086: bd00  ; pop { pc }
20000088: f000  ; literal 
2000008a: 4006
```

### 2000008c init_flash()


Args:
- r0: read_mode

 

```
2000008c: b510  ; push { r4, lr }
2000008e: 4604  ; mov r4, r0            ; read_mode
20000090: f000  ; [...]
20000092: f888  ; bl [pc, #0x110]       ; call 200001a4 flash_lp_exit()
20000094: 2000  ; movs r0, #0x0
20000096: f000  ; [...]
20000098: f895  ; bl [pc, #0x12a]       ; call 200001c4 flash_set_op_mode(0), set Flash mode as READ
2000009a: 4620  ; mov r0, r4            ; read_mode
2000009c: f000  ; [...]
2000009e: f85c  ; bl [pc, #0xb8]        ; call 20000158 flash_set_read_mode(read_mode)
200000a0: f000  ; [...]
200000a2: f86e  ; bl [pc, #0xdc]        ; call 20000180 flash_config_erase_time()
200000a4: f000  ; [...]
200000a6: f89e  ; bl [pc, #0x13c]       ; call 200001e4 flash_config_prog_time()
200000a8: f000  ; [...]
200000aa: f802  ; bl [pc, #0x4]         ; call 200000b0 flash_lock()
200000ac: bd10  ; pop { r4, pc }        ; return
200000ae: 0000  ; lsls r0, r0, #0x0
```

### 200000b0 flash_lock()

```
200000b0: 2055  ; movs r0, #0x55
200000b2: 4901  ; ldr r1 [pc, #0x4]     ; FLASH _CTRL
200000b4: 6188  ; str r0, [r1, #0x18]   ; FLASH_LOCK = 0x55
200000b6: 4770  ; bx lr
200000b8: f000  ; literal
200000ba: 4006
```

### 200000bc flash_unlock()


```
200000bc: 20aa  ; movs r0, #0xaa
200000be: 4901  ; ldr r1 [pc, #0x4]
200000c0: 61c8  ; str r0, [r1, #0x1c]   ; FLASH_UNLOCK = 0xaa
200000c2: 4770  ; bx lr
200000c4: f000
200000c6: 4006
```


### 200000c8 get_word() 

Args:
- r0:  addr


```
200000c8: 4601  ; mov r1, r0
200000ca: 0888  ; lsrs r0, r1, #0x2
200000cc: 0081  ; lsls r1, r0, #0x2     ; Clear bits [1:0]
200000ce: 6808  ; ldr r0, [r1]          ; de-ref
200000d0: 4770  ; bx lr
200000d2: 0000  ; lsls r0, r0, #0x0
```

### 200000d4 flash_set_op_mode5()

Args:
- r0: addr

Return: 
- ?? FLASH_CTRL offset 0x0c


```
200000d4: b530  ; push { r4, r5, lr }
200000d6: 4604  ; mov r4, r0
200000d8: 2500  ; movs r5, #0x0
200000da: bf00  ; nop
200000dc: f7ff  ; [...]
200000de: ffb2  ; bl [pc, #-0x9c]       ; call 20000044 flash_is_busy() -> busy
200000e0: 2800  ; cmp r0, #0x0
200000e2: d1fb  ; bne [pc, #-0xa]       ; if busy, goto 200000dc
200000e4: 2005  ; movs r0, #0x5
200000e6: f000  ; [...]
200000e8: f86d  ; bl [pc, #0xda]        ; call 200001c4 flash_set_op_mode(5) ?? 
200000ea: 08a0  ; lsrs r0, r4, #0x2     ; addr / 4
200000ec: 4908  ; ldr r1 [pc, #0x20]    ; FLASH _CTRL
200000ee: 6048  ; str r0, [r1, #0x4]    ; FLASH_ADDR = (addr / 4)
200000f0: f7ff  ; [...]
200000f2: ffc0  ; bl [pc, #-0x80]       ; call 20000074 flash_start()
200000f4: bf00  ; nop
200000f6: f7ff  ; [...]
200000f8: ffa5  ; bl [pc, #-0xb6]       ; call 20000044 flash_is_busy() -> busy
200000fa: 2800  ; cmp r0, #0x0
200000fc: d1fb  ; bne [pc, #-0xa]       ; if busy goto ...
200000fe: 4804  ; ldr r0 [pc, #0x10]    ; FLASH _CTRL
20000100: 68c5  ; ldr r5, [r0, #0xc]    ; ??
20000102: 2000  ; movs r0, #0x0
20000104: f000  ; [...]
20000106: f85e  ; bl [pc, #0xbc]        ; call 200001c4 flash_set_op_mode(0)  
20000108: f7ff  ; [...]
2000010a: ffd2  ; bl [pc, #-0x5c]       ; call 200000b0 flash_lock() 
2000010c: 4628  ; mov r0, r5
2000010e: bd30  ; pop { r4, r5, pc }
```

```
20000110: f000  ; literal 
20000112: 4006
```


### 20000114 _


```
20000114: b510
20000116: 4604
20000118: bf00
2000011a: f7ff
2000011c: ff93
2000011e: 2800
20000120: d1fb
20000122: 2002
20000124: f000
20000126: f84e
20000128: 08a0
2000012a: 4902
2000012c: 6048
2000012e: f000
20000130: f86b
20000132: bd10
20000134: f000
20000136: 4006
```

### 20000138 flash_sel_nvr()

Args:
- r0: nvr


```
20000138: 4601  ; mov r1, r0
2000013a: 2000  ; movs r0, #0x0
2000013c: 4a05  ; ldr r2 [pc, #0x14]    ; FLASH _CTRL
2000013e: 6810  ; ldr r0, [r2]          ; FLASH_CFG -> reg
20000140: 2302  ; movs r3, #0x2
20000142: 4602  ; mov r2, r0
20000144: 439a  ; bics r2, r3           ; Clear bits [1], reg.NVR_SEL = 0
20000146: 4610  ; mov r0, r2
20000148: 004a  ; lsls r2, r1, #0x1
2000014a: 4310  ; orrs r0, r2           ; reg |= (nvr << 1)
2000014c: 4a01  ; ldr r2 [pc, #0x4]
2000014e: 6010  ; str r0, [r2]
20000150: 4770  ; bx lr
20000152: 0000
20000154: f000  ; literal 
20000156: 4006
```

### 20000158 flash_set_read_mode()

Args:
- r0: mode


```
20000158: 2800  ; cmp r0, #0x0
2000015a: d106  ; bne [pc, #0xc]        ; if mode, goto 2000016a; else ..
2000015c: 4907  ; ldr r1 [pc, #0x1c]    ; 4006f000, FLASH _CTRL
2000015e: 6809  ; ldr r1, [r1]          ; reg = FLASH_CFG
20000160: 0849  ; lsrs r1, r1, #0x1
20000162: 0049  ; lsls r1, r1, #0x1     ; Clear bits [0], reg.READ_MD =0, set read speed to 1 system clock period
20000164: 4a05  ; ldr r2 [pc, #0x14]    ; 
20000166: 6011  ; str r1, [r2]          ; FLASH_CFG = reg
20000168: e007  ; b [pc, #0xe]          ; goto 2000017a, return
```

```
2000016a: 2801  ; cmp r0, #0x1
2000016c: d105  ; bne [pc, #0xa]        ; if mode != 1, goto 2000017a, return
2000016e: 4903  ; ldr r1 [pc, #0xc]     ; 
20000170: 6809  ; ldr r1, [r1]          ; reg = FLASH_CFG
20000172: 2201  ; movs r2, #0x1
20000174: 4311  ; orrs r1, r2           ; Set bits [0], reg.READ_MD =1, set read speed to 2 system clock period
20000176: 4a01  ; ldr r2 [pc, #0x4]
20000178: 6011  ; str r1, [r2]
2000017a: 4770  ; bx lr                 ; return
2000017c: f000  ; literal 
2000017e: 4006
```

### 20000180 flash_config_erase_time() 


Configure Flash FLASH_ERASETIME register
- .TRCV = 52 * sys_clock_freq
- .TERASE = 3600 * sys_clock_freq


```
20000180: 4806  ; ldr r0 [pc, #0x18]    ; 200003ac 
20000182: 8800  ; ldrh r0, [r0]         ; sys_clock_freq_mhz -> v1
20000184: 2134  ; movs r1, #0x34
20000186: 4348  ; muls r0, r1, r0       ; v1 * 52
20000188: 04c1  ; lsls r1, r0, #0x13    ; (v1 * 52) << 19
2000018a: 4804  ; ldr r0 [pc, #0x10]    ;  200003ac, v1
2000018c: 6800  ; ldr r0, [r0]          ; v1
2000018e: 22e1  ; movs r2, #0xe1
20000190: 0112  ; lsls r2, r2, #0x4     ; 0xe10 = 3600
20000192: 4350  ; muls r0, r2, r0       ; v1 * 3600
20000194: 1808  ; adds r0, r1, r0       ; ((v1 * 52) << 19) + (v1 * 3600) -> x
20000196: 4902  ; ldr r1 [pc, #0x8]     ; 4006f000, FLASH _CTRL
20000198: 6248  ; str r0, [r1, #0x24]   ; FLASH_ERASETIME = x
2000019a: 4770  ; bx lr         ; return
```

```
2000019c: 03ac  ;  literal
2000019e: 2000  
200001a0: f000 ;
200001a2: 4006
```

### 200001a4 flash_lp_exit()

Configure flash to exit low power mode ( enter normal mode )


```
200001a4: b500  ; push { lr }
200001a6: 4806  ; ldr r0 [pc, #0x18]    ; 4006f000, FLASH_CTRL
200001a8: 6800  ; ldr r0, [r0]          ; FLASH_CFG
200001aa: 0040  ; lsls r0, r0, #0x1     ; 
200001ac: 0840  ; lsrs r0, r0, #0x1     ; Clear bits [31]: FLASH_CFG.DEEP_PD = 0 
200001ae: 4904  ; ldr r1 [pc, #0x10]    ; FLASH_CTRL
200001b0: 6008  ; str r0, [r1]          ; Update FLASH_CFG
200001b2: bf00  ; nop
200001b4: f7ff  ; [...]
200001b6: ff52  ; bl [pc, #-0x15c]      ; call 2000005c flash_init_done() -> ok
200001b8: 2800  ; cmp r0, #0x0
200001ba: d0fb  ; beq [pc, #-0xa]       ; if !ok, goto 200001b4
200001bc: bd00  ; pop { pc }            ; return 
200001be: 0000
200001c0: f000  ; literal 
200001c2: 4006
```

### 200001c4 flash_set_op_mode()

Args: 
- r0: mode 


```
200001c4: 4601  ; mov r1, r0            ; mode
200001c6: 2000  ; movs r0, #0x0
200001c8: 4a05  ; ldr r2 [pc, #0x14]    ; 4006f000, FLASH_CTRL
200001ca: 6810  ; ldr r0, [r2]          ; reg = FLASH_CFG
200001cc: 231c  ; movs r3, #0x1c
200001ce: 4602  ; mov r2, r0
200001d0: 439a  ; bics r2, r3           ; Clear bits [4:2] : reg.MODE = 0
200001d2: 4610  ; mov r0, r2
200001d4: 008a  ; lsls r2, r1, #0x2     ; mode << 2
200001d6: 4310  ; orrs r0, r2           ; reg |= (mode << 2)
200001d8: 4a01  ; ldr r2 [pc, #0x4]     ; FLASH_CTRL
200001da: 6010  ; str r0, [r2]          ; FLASH_CFG = reg 
200001dc: 4770  ; bx lr             ; return
200001de: 0000
200001e0: f000  ; literal 
200001e2: 4006
```

### 200001e4 flash_config_prog_time()


```
200001e4: 4806  ; ldr r0 [pc, #0x18]    ; 200003ac, sys_clock_freq_mhz
200001e6: 6800  ; ldr r0, [r0]          ; sys_clock_freq_mhz -> v1
200001e8: 2116  ; movs r1, #0x16
200001ea: 4348  ; muls r0, r1, r0       ; v1 * 22
200001ec: 02c1  ; lsls r1, r0, #0xb     ; (v1 * 22) << 11
200001ee: 4804  ; ldr r0 [pc, #0x10]    
200001f0: 6800  ; ldr r0, [r0]          ; v1
200001f2: 2212  ; movs r2, #0x12
200001f4: 4350  ; muls r0, r2, r0       ; v1 * 18
200001f6: 1808  ; adds r0, r1, r0       ; ((v1 * 22) << 11) + (v1 * 18) -> x
200001f8: 4902  ; ldr r1 [pc, #0x8]     ; 4006f000
200001fa: 6288  ; str r0, [r1, #0x28]   ; FLASH_PROGTIME = x
200001fc: 4770  ; bx lr
200001fe: 0000
```

```
20000200: 03ac  ; literal
20000202: 2000
20000204: f000 ; 
20000206: 4006
20000208: b500
2000020a: f7ff
2000020c: ff33
2000020e: bf00
20000210: f7ff
20000212: ff18
20000214: 2800
20000216: d1fb
20000218: f7ff
2000021a: ffd4
2000021c: f7ff
2000021e: ff48
20000220: bd00
20000222: 0000
20000224: b5f0
20000226: 4605
20000228: 460e
2000022a: 4614
2000022c: 2700
2000022e: 2c40
20000230: dc04
20000232: 0628
20000234: 0e80
20000236: 1900
20000238: 2840
2000023a: d901
2000023c: 2001
2000023e: bdf0
20000240: bf00
20000242: f7ff
20000244: feff
20000246: 2800
20000248: d1fb
2000024a: 2001
2000024c: f7ff
2000024e: ffba
20000250: 08a8
20000252: 490f
20000254: 6048
20000256: 6830
20000258: 6088
2000025a: f7ff
2000025c: ff0b
2000025e: 2701
20000260: e009
20000262: bf00
20000264: f7ff
20000266: fee2
20000268: 2800
2000026a: d0fb
2000026c: 00b8
2000026e: 5830
20000270: 4907
20000272: 6088
20000274: 1c7f
20000276: 42a7
20000278: d3f3
2000027a: bf00
2000027c: f7ff
2000027e: fee2
20000280: 2800
20000282: d1fb
20000284: f7ff
20000286: ff9e
20000288: f7ff
2000028a: ff12
2000028c: 2000
2000028e: e7d6
20000290: f000
20000292: 4006
```

### 20000294 init_chip()


```
20000294: b510  ; push { r4, lr }
20000296: 2400  ; movs r4, #0x0
20000298: 2001  ; movs r0, #0x1
2000029a: f7ff  ; [...]
2000029c: ff4d  ; bl [pc, #-0x166]          ; call 20000138 flash_sel_nvr(1), select NVR (instead of Main Flash)
2000029e: 4832  ; ldr r0 [pc, #0xc8]        ; 20000368 -> f018 , a1
200002a0: f7ff  ; [...]
200002a2: ff18  ; bl [pc, #-0x1d0]          ; call 200000d4, flash_set_op_mode5(a1) -> x
200002a4: 4931  ; ldr r1 [pc, #0xc4]        ; 2000036c -> 40000080, CHIP_ID0
200002a6: 6008  ; str r0, [r1]              ; CHIP_ID0 = x
200002a8: 482f  ; ldr r0 [pc, #0xbc]        ; 20000368 -> f018, a1
200002aa: 1d00  ; adds r0, #0x4             ; a1 + 4
200002ac: f7ff  ; [...]
200002ae: ff12  ; bl [pc, #-0x1dc]          ; call 200000d4, flash_set_op_mode5(a1 + 4) -> x
200002b0: 492e  ; ldr r1 [pc, #0xb8]        ; 2000036c
200002b2: 6048  ; str r0, [r1, #0x4]        ; CHIP_ID1 = x
200002b4: 482c  ; ldr r0 [pc, #0xb0]        ; 20000368 -> f018, a1
200002b6: 3008  ; adds r0, #0x8
200002b8: f7ff  ; [...]
200002ba: ff0c  ; bl [pc, #-0x1e8]          ; call 200000d4, flash_set_op_mode5(a1 + 8) -> x
200002bc: 492b  ; ldr r1 [pc, #0xac]
200002be: 6088  ; str r0, [r1, #0x8]        ; CHIP_ID2 = x
200002c0: 4829  ; ldr r0 [pc, #0xa4]
200002c2: 300c  ; adds r0, #0xc
200002c4: f7ff  ; [...]
200002c6: ff06  ; bl [pc, #-0x1f4]
200002c8: 4928  ; ldr r1 [pc, #0xa0]
200002ca: 60c8  ; str r0, [r1, #0xc]        ; CHIP_ID3 = ..
```

```
200002cc: 20f9  ; movs r0, #0xf9
200002ce: 00c0  ; lsls r0, r0, #0x3     ; 0x7c8
200002d0: f7ff  ; [...]
200002d2: fefa  ; bl [pc, #-0x20c]      ; call 200000c8 get_word(0x7c8)  -> x
200002d4: 4925  ; ldr r1 [pc, #0x94]    ; 2000036c -> 40000080, CHIP_ID0
200002d6: 3940  ; subs r1, #0x40        ; 
200002d8: 6388  ; str r0, [r1, #0x38]   ; RC_FREQ_DELTA = x
200002da: 4825  ; ldr r0 [pc, #0x94]    ; 20000370 -> 07c4
200002dc: f7ff  ; [...]
200002de: fef4  ; bl [pc, #-0x218]      ; call 200000c8 get_word(0x7c4)  -> x
200002e0: 4922  ; ldr r1 [pc, #0x88]    ; 2000036c -> 40000080, CHIP_ID0
200002e2: 3940  ; subs r1, #0x40
200002e4: 63c8  ; str r0, [r1, #0x3c]   ; 4000007c, VREF_VOLT_DELTA = x
200002e6: 4822  ; ldr r0 [pc, #0x88]    ; 20000370 -> 07c4
200002e8: 3020  ; adds r0, #0x20        ; 7e4
200002ea: f7ff  ; [...]
200002ec: feed  ; bl [pc, #-0x226]      ; call 200000c8 get_word(0x7e4)  -> x 
200002ee: 4921  ; ldr r1 [pc, #0x84]    ; 20000374 -> 40000800, PMU
200002f0: 6208  ; str r0, [r1, #0x20]   ; TRIM _POW0 = x
200002f2: 203f  ; movs r0, #0x3f
200002f4: 0140  ; lsls r0, r0, #0x5     ; 7e0
200002f6: f7ff  ; [...]
200002f8: fee7  ; bl [pc, #-0x232]      ; call 200000c8 get_word(0x7e0)  -> x
200002fa: 491e  ; ldr r1 [pc, #0x78]    ; 20000374 -> 40000800, PMU
200002fc: 6248  ; str r0, [r1, #0x24]   ; TRIM _POW1 = x
200002fe: 20fb  ; movs r0, #0xfb
20000300: 00c0  ; lsls r0, r0, #0x3     ; 7d8
20000302: f7ff  ; [...]
20000304: fee1  ; bl [pc, #-0x23e]      ; call 200000c8 get_word(0x7d8)  -> x
20000306: 491b  ; ldr r1 [pc, #0x6c]    ; 
20000308: 6308  ; str r0, [r1, #0x30]   ; TRIM_RCHF = x
2000030a: 4819  ; ldr r0 [pc, #0x64]    ; 20000370 -> 07c4
2000030c: 3010  ; adds r0, #0x10        ; 7d4
2000030e: f7ff  ; [...]
20000310: fedb  ; bl [pc, #-0x24a]      ; call 200000c8 get_word(0x7d4)  -> x
20000312: 4918  ; ldr r1 [pc, #0x60]    ; 20000374 -> 40000800, PMU
20000314: 6348  ; str r0, [r1, #0x34]   ; TRIM_RCLF = x
20000316: 207d  ; movs r0, #0x7d
20000318: 0100  ; lsls r0, r0, #0x4
2000031a: f7ff  ; [...]
2000031c: fed5  ; bl [pc, #-0x256]
2000031e: 4915  ; ldr r1 [pc, #0x54]
20000320: 6388  ; str r0, [r1, #0x38]
20000322: 4813  ; ldr r0 [pc, #0x4c]
20000324: 3008  ; adds r0, #0x8
20000326: f7ff  ; [...]
20000328: fecf  ; bl [pc, #-0x262]
2000032a: 4912  ; ldr r1 [pc, #0x48]
2000032c: 63c8  ; str r0, [r1, #0x3c]
2000032e: 20f7  ; movs r0, #0xf7
20000330: 00c0  ; lsls r0, r0, #0x3
20000332: f7ff  ; [...]
20000334: fec9  ; bl [pc, #-0x26e]
20000336: 4910  ; ldr r1 [pc, #0x40]
20000338: 6008  ; str r0, [r1]
2000033a: 480d  ; ldr r0 [pc, #0x34]
2000033c: 3808  ; subs r0, #0x8
2000033e: f7ff  ; [...]
20000340: fec3  ; bl [pc, #-0x27a]
20000342: 4604  ; mov r4, r0
20000344: 2001  ; movs r0, #0x1
20000346: 0780  ; lsls r0, r0, #0x1e
20000348: 6880  ; ldr r0, [r0, #0x8]
2000034a: 2101  ; movs r1, #0x1
2000034c: 0649  ; lsls r1, r1, #0x19
2000034e: 4308  ; orrs r0, r1
20000350: 0149  ; lsls r1, r1, #0x5
20000352: 6088  ; str r0, [r1, #0x8]
20000354: b2e0  ; uxtb r0, r4
20000356: 4909  ; ldr r1 [pc, #0x24]
20000358: 6308  ; str r0, [r1, #0x30]
2000035a: 01a0  ; lsls r0, r4, #0x6
2000035c: 0d80  ; lsrs r0, r0, #0x16
2000035e: 6348  ; str r0, [r1, #0x34]
20000360: 2000  ; movs r0, #0x0
20000362: f7ff  ; [...]
20000364: fee9  ; bl [pc, #-0x22e]
20000366: bd10  ; pop { r4, pc }
```

```
20000368: f018  ; literal 
2000036a: 0000
2000036c: 0080 ; 
2000036e: 4000
20000370: 07c4 ; 
20000372: 0000
20000374: 0800 ; 
20000376: 4000
20000378: 03c0
2000037a: 2000
2000037c: a0c0
2000037e: 400b
20000380: b570
20000382: 4604
20000384: 460d
20000386: 4616
20000388: 2001
2000038a: f7ff
2000038c: fed5
2000038e: 4620
20000390: f7ff
20000392: fec0
20000394: 4632
20000396: 4629
20000398: 4620
2000039a: f7ff
2000039c: ff43
2000039e: 2000
200003a0: f7ff
200003a2: feca
200003a4: bd70
200003a6: 0000
```


### 200003a8 Global variables

Global variables

```
200003a8: 6c00 ; sys_clock_freq
200003aa: 02dc
200003ac: 0030  ; sys_clock_freq_mhz
200003ae: 0000
200003b0: 0000
200003b2: 0000
200003b4: 0000
200003b6: 0000
200003b8: 0000
200003ba: 0000
200003bc: 0000
200003be: 0000
200003c0: 0000
200003c2: 0000
```

## 0df8 _

```
0df8: 0000
0dfa: 0000
0dfc: 0000
0dfe: 0000
0e00: 0000
0e02: 0000
0e04: 0000
0e06: 0000
0e08: 0000
0e0a: 0000
0e0c: 0000
0e0e: 0000
0e10: 0000
0e12: 0000
0e14: 0000
0e16: 0000
0e18: 0000
0e1a: 0000
0e1c: 0000
0e1e: 0000
0e20: 0000
0e22: 0000
0e24: 0000
0e26: 0000
0e28: 0000
0e2a: 0000
0e2c: 0000
0e2e: 0000
0e30: 0000
0e32: 0000
0e34: 0000
0e36: 0000
0e38: 0000
0e3a: 0000
0e3c: 0000
0e3e: 0000
0e40: 0000
0e42: 0000
0e44: 0000
0e46: 0000
0e48: 0000
0e4a: 0000
0e4c: 0000
0e4e: 0000
0e50: 0000
0e52: 0000
0e54: 0000
0e56: 0000
0e58: 0000
0e5a: 0000
0e5c: 0000
0e5e: 0000
0e60: 0000
0e62: 0000
0e64: 0000
0e66: 0000
0e68: 0000
0e6a: 0000
0e6c: 0000
0e6e: 0000
0e70: 0000
0e72: 0000
0e74: 0000
0e76: 0000
0e78: 0000
0e7a: 0000
0e7c: 0000
0e7e: 0000
0e80: 0000
0e82: 0000
0e84: 0000
0e86: 0000
0e88: 0000
0e8a: 0000
0e8c: 0000
0e8e: 0000
0e90: 0000
0e92: 0000
0e94: 0000
0e96: 0000
0e98: 0000
0e9a: 0000
0e9c: 0000
0e9e: 0000
0ea0: 0000
0ea2: 0000
0ea4: 0000
0ea6: 0000
0ea8: 0000
0eaa: 0000
0eac: 0000
0eae: 0000
0eb0: 0000
0eb2: 0000
0eb4: 0000
0eb6: 0000
0eb8: 0000
0eba: 0000
0ebc: 0000
0ebe: 0000
0ec0: 0000
0ec2: 0000
0ec4: 0000
0ec6: 0000
0ec8: 0000
0eca: 0000
0ecc: 0000
0ece: 0000
0ed0: 0000
0ed2: 0000
0ed4: 0000
0ed6: 0000
0ed8: 0000
0eda: 0000
0edc: 0000
0ede: 0000
0ee0: 0000
0ee2: 0000
0ee4: 0000
0ee6: 0000
0ee8: 0000
0eea: 0000
0eec: 0000
0eee: 0000
0ef0: 0000
0ef2: 0000
0ef4: 0000
0ef6: 0000
0ef8: 0000
0efa: 0000
0efc: 0000
0efe: 0000
0f00: 0000
0f02: 0000
0f04: 0000
0f06: 0000
0f08: 0000
0f0a: 0000
0f0c: 0000
0f0e: 0000
0f10: 0000
0f12: 0000
0f14: 0000
0f16: 0000
0f18: 0000
0f1a: 0000
0f1c: 0000
0f1e: 0000
0f20: 0000
0f22: 0000
0f24: 0000
0f26: 0000
0f28: 0000
0f2a: 0000
0f2c: 0000
0f2e: 0000
0f30: 0000
0f32: 0000
0f34: 0000
0f36: 0000
0f38: 0000
0f3a: 0000
0f3c: 0000
0f3e: 0000
0f40: 0000
0f42: 0000
0f44: 0000
0f46: 0000
0f48: 0000
0f4a: 0000
0f4c: 0000
0f4e: 0000
0f50: 0000
0f52: 0000
0f54: 0000
0f56: 0000
0f58: 0000
0f5a: 0000
0f5c: 0000
0f5e: 0000
0f60: 0000
0f62: 0000
0f64: 0000
0f66: 0000
0f68: 0000
0f6a: 0000
0f6c: 0000
0f6e: 0000
0f70: 0000
0f72: 0000
0f74: 0000
0f76: 0000
0f78: 0000
0f7a: 0000
0f7c: 0000
0f7e: 0000
0f80: 0000
0f82: 0000
0f84: 0000
0f86: 0000
0f88: 0000
0f8a: 0000
0f8c: 0000
0f8e: 0000
0f90: 0000
0f92: 0000
0f94: 0000
0f96: 0000
0f98: 0000
0f9a: 0000
0f9c: 0000
0f9e: 0000
0fa0: 0000
0fa2: 0000
0fa4: 0000
0fa6: 0000
0fa8: 0000
0faa: 0000
0fac: 0000
0fae: 0000
0fb0: 0000
0fb2: 0000
0fb4: 0000
0fb6: 0000
0fb8: 0000
0fba: 0000
0fbc: 0000
0fbe: 0000
0fc0: 0000
0fc2: 0000
0fc4: 0000
0fc6: 0000
0fc8: 0000
0fca: 0000
0fcc: 0000
0fce: 0000
0fd0: 0000
0fd2: 0000
0fd4: 0000
0fd6: 0000
0fd8: 0000
0fda: 0000
0fdc: 0000
0fde: 0000
0fe0: 0000
0fe2: 0000
0fe4: 0000
0fe6: 0000
0fe8: 0000
0fea: 0000
0fec: 0000
0fee: 0000
0ff0: 0000
0ff2: 0000
0ff4: 0000
0ff6: 0000
0ff8: 0000
0ffa: 0000
0ffc: 0000
0ffe: 0000
```
