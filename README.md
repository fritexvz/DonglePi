# DonglePi

![pcb](http://gbin.github.io/DonglePi/pcb.png)

DonglePi is a device that gives you a Raspberry Pi P1 compatible connector for your PC.

P1 is a connector with:
- GPIO
- I2C
- SPI
- Serial
- PWM

More info [about the connector](http://elinux.org/RPi_Low-level_peripherals)

On the software side, it exposes APIs that are compatible with the ones used by the raspberry pi like [GPIO](https://pypi.python.org/pypi/RPi.GPIO/) and [smbus](http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2) under python.

## Hardware

It can be plugged to any USB2 port.

You can build a prototype on a breadboard using an Atmel SAMD21 development board.
I recommend [this one](http://www.ebay.com/itm/131296219501?_trksid=p2060778.m2749.l2649&var=430589049056&ssPageName=STRK%3AMEBIDX%3AIT)

![breadboard](http://gbin.github.io/DonglePi/images/breadboard.jpg)

## Software

### Dependencies

Get the [asf sdk](http://www.atmel.com/System/GetBinary.ashx?target=tcm:26-49230&type=soft&actualTarget=tcm:26-65233)
It needs to be linked to the asf directory in the root of the project (by default it looks for the latest version in your home directory).

Sync the submodule:

  git submodule update --init firmware/nanopb

Install google protobuf:

  pip install -user protobuf
  #(or under arch for example)
  sudo pacman -S protobuf python2-protobuf

Install gcc for arm bare metal:

  # (under arch)
  sudo pacman -S arm-none-eabi-gcc
  # Otherwise you can always get the binaries there:
  https://launchpad.net/gcc-arm-embedded/+download

Install pyserial:
  pip install pyserial

### Building the firmware

From the firmware:
  make

It will produce a flash.bin file.

### Installing the fimware

If you have the recommanded dev board, connect it on USB, press Reset + Button B. It will appear as a standard USB storage device.
The red led from the board should slowly blink.
Copy flash.bin to the root of it.
Unmount the disk.
Reset it, the led should switch to solid red = it has correctly initialized and wait for commands.

### Building the client side support.

From the python directory:
  make

This should generate some files from tht protobuf so the bindings could talk to the hardware.

Here you have a test.py showing how to use the bindings.

