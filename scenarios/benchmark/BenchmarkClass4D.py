from BenchmarkClass import Benchmark

class Benchmark4D(Benchmark):

    def init_moduleList(self):
        Benchmark.init_moduleList(self)

        self.m.add(FutureRedshift())

    def init_observer(self):
        Benchmark.init_observer(self)

        self.obs.add(ObserverRedshiftWindow(-0.05, 0.05))

    def init_source(self):
        Benchmark.init_sources(self)

        zmin = 0
        zmax = 4
        self.source.add(SourceUniformRedshift(zmin,zmax))

