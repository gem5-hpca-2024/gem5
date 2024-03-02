from typing import Type

from m5.objects import (
    BasePrefetcher,
    Cache,
    IndirectMemoryPrefetcher,
)


class L1DCacheIndirect(Cache):
    def __init__(
        self,
        size: str = "32kB",
        assoc: int = 8,
        tag_latency: int = 1,
        data_latency: int = 1,
        response_latency: int = 1,
        mshrs: int = 16,
        tgts_per_mshr: int = 20,
        writeback_clean: bool = False,
        PrefetcherCls: Type[BasePrefetcher] = IndirectMemoryPrefetcher,
    ):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = tag_latency
        self.data_latency = data_latency
        self.response_latency = response_latency
        self.mshrs = mshrs
        self.tgts_per_mshr = tgts_per_mshr
        self.writeback_clean = writeback_clean
        self.prefetcher = PrefetcherCls()
