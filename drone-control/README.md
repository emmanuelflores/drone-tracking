# drone-control

## Description:
This is a guide to setup a development environment for software to control the crazyflie.

## Requires:
    git
    CMake >= 2.8

## Step 0
- Create global directory for all code repositories; e.g. ~/User/code
- Navigate to this directory
- Setup git on your workstation

## Step 1
- On github fork https://github.com/emmanuelflores/drone-tracking to your account.
- Clone this fork

  ```
  git clone git@github.com:gh-username/drone-tracking.git
  ```

## Step 2
Get and build libusb-1.0 (for Windows follow the instructions from libusb/INSTALL_WIN.txt)

    git clone git@github.com:libusb/libusb.git
    ./autogen.sh
    ./configure
    make
    make install

## Step 3
Get and build libcflie

    git clone git@github.com:boaz001/libcflie.git
    mkdir build
    cd build
    cmake ..
    make

## Step 4
Build the drone-control demo

    cd ~/code/drone-tracking/drone-control
    mkdir build
    cd build
    cmake ..
    make
    make install

Demo executable is in /bin
