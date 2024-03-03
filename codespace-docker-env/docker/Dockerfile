FROM ghcr.io/gem5/ubuntu-22.04_all-dependencies:v23-1 as builder

RUN git clone -b stable https://github.com/gem5-hpca-2024/gem5

WORKDIR /gem5

RUN scons -j`nproc` build/ALL/gem5.opt

FROM ghcr.io/gem5/ubuntu-22.04_all-dependencies:v23-1

COPY --from=builder /gem5/build/ALL/gem5.opt /usr/bin/gem5.opt
