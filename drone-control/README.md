# drone-control

## Description:
This is a guide to setup a development environment for software to control the crazyflie.

## Step 0
- Create global directory for all code repositories; e.g. ~/User/code
- Navigate to this directory
- Setup git on your workstation

## Step 1
- On github fork https://github.com/emmanuelflores/drone-tracking to your account.
- Clone this fork
    git clone git@github.com:gh-username/drone-tracking.git

## Step 2
- Get and build libusb-1.0
    git clone git://git.libusb.org/libusb.git
    ./autogen.sh
    ./configure.sh
    make
    make install

## Step 3
- Get and build libcflie
    git clone git@github.com:boaz001/libcflie.git
    mkdir build
    cd build
    cmake ..
    make

## Step 4
- Build the drone-control demo
    cd ~/code/drone-tracking/drone-control
    mkdir build
    cd build
    cmake ..
    make
    make install
- Demo executable is in /bin

## Requires:
    CMake >= 2.8
    OpenCV >= 2.4 (can also be a own-built version, edit the CMakeLists.txt accordingly)

## Install:
    mkdir build
    cd build
    cmake ..

## Run:
    ./color-tracking-demo
