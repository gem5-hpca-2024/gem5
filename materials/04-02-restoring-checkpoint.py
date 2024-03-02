from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import (
    PrivateL1CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# We can add a different cache hierarachy.
cache_hierarchy = PrivateL1CacheHierarchy(l1d_size="16kB", l1i_size="16kB")


# We can increase the memory size (Note: You can only increase, not decrease)
memory = SingleChannelDDR3_1600(size="3GB")

# Here we do a more detailed CPU core, O3.
processor = SimpleProcessor(cpu_type=CPUTypes.O3, isa=ISA.X86, num_cores=1)


board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

command = (
    "m5 exit;"
    + "echo 'This is running on O3 CPU cores.';"
    + "sleep 1;"
    + "m5 exit;"
)

from pathlib import Path

# You can change this to your checkpoint if you wish.
checkpoint_path = (
    Path(__file__).parent.parent.resolve()
    / "materials-completed"
    / "checkpoints"
    / "04-01-saved-checkpoint"
)

board.set_kernel_disk_workload(
    kernel=obtain_resource("x86-linux-kernel-4.4.186"),
    disk_image=obtain_resource("x86-ubuntu-18.04-img"),
    readfile_contents=command,
    checkpoint=checkpoint_path,
)

simulator = Simulator(board=board)
simulator.run()
