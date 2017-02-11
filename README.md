# Persistence Of Vision Project
This repository contains the source code for a Persistence of Vision Bicycle Wheel project 
I completed as part of a university team project. The goal of the project was to be able to 
detect a magnet fixed to a bike fork and display an image on a 32-LED array using persistence 
of vision. Contributions to the final product were as follows:
- Computer Software produced by Megan Moore and Isabella Stephens
- Firmware produced by Isabella Stephens
- Hardware designed by Jack Hales, Isabella Stephens and Adam Tighe

This readme file contains my notes on the project's implementation (mostly around firmware and 
component selection), as well as details on software licensing. 

The video below demonstrates the final product (although unfortunately the camera was unable to 
capture the full persistence of vision effect).

[![Product Demo](http://img.youtube.com/vi/9pt-T8RMviw/0.jpg)](http://www.youtube.com/watch?v=9pt-T8RMviw "Persistence of Vision Project")


## Hardware Implementation
The final product consisted of the following main subsystems/components:
- Microcontroller: an ATMega328P with a 16MHz crystal oscillator
- Power Supply: two NiMH batteries with a [pololu 5V step-up converter](https://littlebirdelectronics.com.au/products/pololu-5v-step-up-voltage-regulator-u1v10f5)
- LEDs: two N-channel MOSFETs, two [74HC595N shift registers](http://au.element14.com/nxp/74hc595n/ic-74hc-cmos-shift-reg-5v-16dip/dp/3166028) and 32 red LEDs
- USB: USB jack, zener diodes and other passives as described [here](https://www.obdev.at/products/vusb/index.html)
- Rotation Sensing: a [hall effect switch](http://au.element14.com/allegro-microsystems/a3213eua-t/ic-hall-effect-sw-1ma-sip3/dp/1521681)

Here's a picture of the final product:
![Persistence of Vision PCB](http://i.imgur.com/K4dfBpH.jpg)



## Firmware Implementation
Coming soon!



## Licensing and Acknowledgements
This repository contains two discrete programs. One contained in Firmware/ and one in Computer/. 
This repository forms part of a larger project completed as follows: 
- Computer Software produced by Megan Moore and Isabella Stephens
- Firmware produced by Isabella Stephens
- Hardware designed by Jack Hales, Isabella Stephens and Adam Tighe


### Firmware Program Licenses

The contents of Firmware/usbdrv and the file Firmware/usbconfig.h comprise OBJECTIVE DEVELOPMENT's V-USB
Driver software. This software is distributed under the GNU GPL version 2. A copy of the license is located 
in Firmware/usbdrv/License.txt.

The makefile in Firmware/ is a modified version of the sample makefile written by Eric B. Weddington, 
Jorg Wunsch, et al.

All other source files in Firmware/ are the sole work of Isabella Stephens. This work is released under 
the BSD License 2.0:
```
Copyright (C) 2014, Isabella Stephens
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
	  notice, this list of conditions and the following disclaimer.
	* Redistributions in binary form must reproduce the above copyright
	  notice, this list of conditions and the following disclaimer in the
	  documentation and/or other materials provided with the distribution.
	* The name of Isabella Stephens may not be used to endorse or promote products
	  derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### Computer Program Licenses
The contents of Computer/ are a collaborative work between Megan Moore and Isabella Stephens. 
No license is provided for this work. 
- Copyright (C) 2014 Isabella Stephens. All Rights Reserved.
- Copyright (C) 2014 Megan Moore. All Rights Reserved.

The work makes use of the PyUSB Library and Python Imaging Library. Licenses for these libraries 
are available below.

#### PyUSB Software License
```
Copyright (C) 2009-2014 Wander Lairson Costa. All Rights Reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
OF THE POSSIBILITY OF SUCH DAMAGE.
```

#### Python Imaging Library Software License
```
The Python Imaging Library (PIL) is
  - Copyright (c) 1997-2011 by Secret Labs AB
  - Copyright (c) 1995-2011 by Fredrik Lundh

By obtaining, using, and/or copying this software and/or its associated 
documentation, you agree that you have read, understood, and will comply 
with the following terms and conditions:

Permission to use, copy, modify, and distribute this software and its 
associated documentation for any purpose and without fee is hereby granted, 
provided that the above copyright notice appears in all copies, and that 
both that copyright notice and this permission notice appear in supporting 
documentation, and that the name of Secret Labs AB or the author not be 
used in advertising or publicity pertaining to distribution of the 
software without specific, written prior permission.

SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL 
SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL 
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER 
IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN 
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```



