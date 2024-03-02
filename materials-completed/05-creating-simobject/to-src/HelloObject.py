from m5.params import *
from m5.SimObject import SimObject


class HelloObject(SimObject):
    type = "HelloObject"
    cxx_header = "simobject-example/hello_object.hh"
    cxx_class = "gem5::HelloObject"
