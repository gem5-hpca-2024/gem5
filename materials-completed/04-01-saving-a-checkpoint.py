from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# An incredibly simple cache hierarchy. This is a NoCache, so it is just a
# passthrough from the processor to memory.
cache_hierarchy = NoCache()

memory = SingleChannelDDR3_1600(size="200MB")

# An Atomic core is used here because we don't care about anything before
# the checkpoint is created.
processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, isa=ISA.X86, num_cores=1)


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

board.set_kernel_disk_workload(
    kernel=obtain_resource("x86-linux-kernel-4.4.186"),
    disk_image=obtain_resource("x86-ubuntu-18.04-img"),
    readfile_contents=command,
)

simulator = Simulator(board=board)
simulator.run()

from pathlib import Path

simulator.save_checkpoint(
    Path(
        Path(__file__).parent.absolute()
        / "checkpoints"
        / "04-01-saved-checkpoint"
    )
)
