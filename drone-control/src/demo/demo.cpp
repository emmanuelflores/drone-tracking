// demo.cpp

#include <cflie/CCrazyflie.h>

int
main(int argc, char** argv)
{
  CCrazyRadio* crazyRadio = new CCrazyRadio("radio://0/10/250K");

  if (crazyRadio->startRadio())
  {
    CCrazyflie* myCrazyflie = new CCrazyflie(crazyRadio);

    // https://www.youtube.com/watch?v=YaB66KFLECU 2:50

    delete myCrazyflie;
  }
  delete crazyRadio;
  return 0;
}
