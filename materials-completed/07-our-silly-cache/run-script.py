import argparse

from our_private_l1_cache_hierarchy import OurPrivateL1CacheHierarchyIndirect

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

parser = argparse.ArgumentParser(
    description="This script shows how to use a suite. In this example, we "
    "will use the ARM Getting Started Benchmark Suite, and show "
    "the different functionalities of the suite.",
)

# Obtain the ARM "Getting Started" Benchmark Suite.
microbenchmarks = obtain_resource("arm-getting-started-benchmark-suite")

# Give these as an option to the user to select and run the benchmark of their
# choice.
parser.add_argument(
    "benchmark",
    type=str,
    choices=[benchmark.get_id() for benchmark in microbenchmarks],
    help=f"The benchmark from the {microbenchmarks.get_id()} suite to run.",
)

# Get the arguments from the command line parser.
args = parser.parse_args()

# get the benchmark from the suite the user selected.
benchmark = None
for option in microbenchmarks:
    if option.get_id() == args.benchmark:
        benchmark = option
        break


# This check ensures the gem5 binary is compiled to the ARM ISA target. If not,
# an exception will be thrown.
requires(isa_required=ISA.ARM)

cache_hierarchy = OurPrivateL1CacheHierarchyIndirect(l1i_size="32kB")

# We use a single channel DDR3_1600 memory system
memory = SingleChannelDDR3_1600(size="32MB")

# We use a simple Timing processor with one core.
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.ARM, num_cores=1)

# The gem5 library simble board which can be used to run simple SE-mode
# simulations.
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Here we set the benchmark to run on the board. This is dependent on what the
# user has selected.
board.set_workload(workload=benchmark)

# Lastly we run the simulation.
simulator = Simulator(board=board)
simulator.run()
