from gem5.prebuilt.demo.x86_demo_board import X86DemoBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# Here we setup the board. The prebuilt X86DemoBoard allows for Full-System X86
# simulation.
board = X86DemoBoard()

# We then set the workload. Here we use the "x86-ubuntu-18.04-boot" workload.
# This boots Ubuntu 18.04 with Linux 5.4.49. If the required resources are not
# found locally, they will be downloaded.
board.set_workload(obtain_resource("x86-ubuntu-18.04-boot"))

# The board is then passed to the simulator and it is run.
simulator = Simulator(board=board)
simulator.run(max_ticks=10**10)  # Run for 10 billion ticks.
