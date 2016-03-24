from BenchmarkClass import Benchmark

class Benchmark4D(Benchmark):

    def init_moduleList(self):
        """ Initialize moduleList
        """

        self.m.add(DeflectionCK(self.bField, 1e-3, 10.*kpc, 1.*Mpc))
        self.m.add(MinimumEnergy(self.minEnergy))
        self.m.add(MaximumTrajectoryLength(self.maxTrajectory)) #remove?
        self.m.add(ReflectiveBox(self.boxOrigin, Vector3d(self.boxSize)))
        self.m.add(FutureRedshift())
        self.m.add(self.obs)

    def init_observer(self):
        Benchmark.init_observer(self)

        self.obs.add(ObserverRedshiftWindow(-0.05, 0.05))

    def init_source(self):
        Benchmark.init_sources(self)

        zmin = 0
        zmax = 4
        self.source.add(SourceUniformRedshift(zmin,zmax))

