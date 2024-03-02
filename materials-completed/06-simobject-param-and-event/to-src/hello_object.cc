#include <iostream>

#include "simobject-example/hello_object.hh"

namespace gem5
{

HelloObject::HelloObject(const HelloObjectParams &params) :
    SimObject(params),
    event([this]{ processEvent(); }, name() + ".event"),
    myName(params.name),
    latency(params.time_to_wait),
    timesLeft(params.number_of_fires)
{
    std::cout << "Created the HelloObject with name " << myName << std::endl;
}

void
HelloObject::startup()
{
    schedule(event, latency);
}

void
HelloObject::processEvent()
{
    std::cout << "Hello world! Processing the event! " << std::endl;
    timesLeft--;

    if (timesLeft <= 0) {
        std::cout << "No more Hello Worlds left. Not scheduling another "
                     "event! " << std::endl;

    } else {
        std::cout << timesLeft << " Hello Worlds left. Scheduling next "
                                  "event" << std::endl;
        schedule(event, curTick() + latency);
    }
}

} // namespace gem5
