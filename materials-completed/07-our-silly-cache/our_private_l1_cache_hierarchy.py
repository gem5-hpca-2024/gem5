from l1dcacheIndirect import L1DCacheIndirect as L1DCache

from m5.objects import (
    BadAddr,
    BaseXBar,
    Cache,
    Port,
    SystemXBar,
)

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.abstract_cache_hierarchy import (
    AbstractCacheHierarchy,
)
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import (
    AbstractClassicCacheHierarchy,
)
from gem5.components.cachehierarchies.classic.caches.l1icache import L1ICache
from gem5.components.cachehierarchies.classic.caches.mmu_cache import MMUCache
from gem5.isas import ISA
from gem5.utils.override import overrides


class OurPrivateL1CacheHierarchyIndirect(AbstractClassicCacheHierarchy):
    """
    A cache setup where each core has a private L1 data and instruction Cache.
    """

    @staticmethod
    def _get_default_membus() -> SystemXBar:
        """
        A method used to obtain the default memory bus of 64 bit in width for
        the PrivateL1CacheHierarchy.

        :returns: The default memory bus for the PrivateL1PrivateL2
                  CacheHierarchy.
        """
        membus = SystemXBar(width=64)
        membus.badaddr_responder = BadAddr()
        membus.default = membus.badaddr_responder.pio
        return membus

    def __init__(
        self,
        l1i_size: str,
        membus: BaseXBar = _get_default_membus.__func__(),
    ) -> None:
        """
        :param l1d_size: The size of the L1 Data Cache (e.g., "32kB").

        :param  l1i_size: The size of the L1 Instruction Cache (e.g., "32kB").

        :param membus: The memory bus. This parameter is optional parameter and
                       will default to a 64 bit width SystemXBar is not specified.
        """

        AbstractClassicCacheHierarchy.__init__(self=self)
        self.membus = membus
        self._l1i_size = l1i_size

    @overrides(AbstractClassicCacheHierarchy)
    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports

    @overrides(AbstractClassicCacheHierarchy)
    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports

    @overrides(AbstractCacheHierarchy)
    def incorporate_cache(self, board: AbstractBoard) -> None:
        # Set up the system port for functional access from the simulator.
        board.connect_system_port(self.membus.cpu_side_ports)

        for _, port in board.get_memory().get_mem_ports():
            self.membus.mem_side_ports = port

        self.l1icaches = [
            L1ICache(size=self._l1i_size)
            for i in range(board.get_processor().get_num_cores())
        ]

        self.l1dcaches = [
            L1DCache() for i in range(board.get_processor().get_num_cores())
        ]
        # ITLB Page walk caches
        self.iptw_caches = [
            MMUCache(size="8KiB")
            for _ in range(board.get_processor().get_num_cores())
        ]
        # DTLB Page walk caches
        self.dptw_caches = [
            MMUCache(size="8KiB")
            for _ in range(board.get_processor().get_num_cores())
        ]

        if board.has_coherent_io():
            self._setup_io_cache(board)

        for i, cpu in enumerate(board.get_processor().get_cores()):
            cpu.connect_icache(self.l1icaches[i].cpu_side)
            cpu.connect_dcache(self.l1dcaches[i].cpu_side)

            self.l1icaches[i].mem_side = self.membus.cpu_side_ports
            self.l1dcaches[i].mem_side = self.membus.cpu_side_ports

            self.iptw_caches[i].mem_side = self.membus.cpu_side_ports
            self.dptw_caches[i].mem_side = self.membus.cpu_side_ports

            cpu.connect_walker_ports(
                self.iptw_caches[i].cpu_side, self.dptw_caches[i].cpu_side
            )

            if board.get_processor().get_isa() == ISA.X86:
                int_req_port = self.membus.mem_side_ports
                int_resp_port = self.membus.cpu_side_ports
                cpu.connect_interrupt(int_req_port, int_resp_port)
            else:
                cpu.connect_interrupt()

    def _setup_io_cache(self, board: AbstractBoard) -> None:
        """Create a cache for coherent I/O connections"""
        self.iocache = Cache(
            assoc=8,
            tag_latency=50,
            data_latency=50,
            response_latency=50,
            mshrs=20,
            size="2kB",
            tgts_per_mshr=12,
            addr_ranges=board.mem_ranges,
        )
        self.iocache.mem_side = self.membus.cpu_side_ports
        self.iocache.cpu_side = board.get_mem_side_coherent_io_port()
