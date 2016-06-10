import os

from crpropa import *
import numpy as np

class Benchmark(object):
    """ Benchmark scenario
        Specs: https://www.auger.unam.mx/AugerWiki/BenchmarkScenario
        PA GAP note: GAP-2012-138
    """

    def __init__(self):
        """ Initialize required objects and parameters on default values
            All parameters can be overridden
        """

        # Containers
        self.m = ModuleList()
        self.bField = None
        self.obs = Observer()
        self.source = Source()
        self.outputFileName = 'default_output.txt'

        # Box proporties
        self.boxOrigin = Vector3d(54, 54, 54)*Mpc
        self.boxSize = 132*Mpc
        self.gridFile = os.path.expanduser(
                '~/.virtualenvs/crpropa/share/crpropa/bench_54-186Mpc_440bins.raw')
        self.Brms = 1.
        self.Bnorm = 1.
        self.sources_file = 'BenchmarkSources.txt'
        self.composition = None

        # Observer size and position
        self.obsPosition = Vector3d(118.34, 117.69, 119.2)*Mpc
        self.obsSize = 1.*Mpc

        # Propagational proporties
        self.minEnergy = 1.*EeV
        self.maxTrajectory = redshift2ComovingDistance(2)

        # General source properties
        self.sourceMinEnergy = 1.*EeV
        self.sourceMaxEnergy = 26*1000.*EeV
        self.sourceSpectralIndex = -1.
        
        # Random seeds
        self.turbulenceSeed = 2308
        self.generalSeed = 185652056

        # Candidates
        self.NEvents = 5000
        self.A = 1
        self.Z = 1

    def init_bField(self):
        """ Initialize magnetic field
        """
        
        # modulation grid
        mgrid = ScalarGrid( self.boxOrigin, 440, self.boxSize / 440 )
        loadGrid(mgrid, self.gridFile, self.Bnorm)

        # turbulent vector grid
        boxSpacing = 13.2*Mpc/440
        vgrid = VectorGrid(self.boxOrigin, 440, boxSpacing)
        initTurbulence(vgrid, self.Brms, 2.*boxSpacing, 2.2*Mpc, -11./3., self.turbulenceSeed)

        # total magnetic field
        self.bField = ModulatedMagneticFieldGrid(vgrid, mgrid)

    def init_observer(self):
        """ Insert observer(s)
        """

        self.obs.add( ObserverSmallSphere( self.obsPosition, self.obsSize ) )
        # Generally candidate is not deactivated on detection
        self.obs.setDeactivateOnDetection( False )
        out = TextOutput( self.outputFileName, Output.Event3D )

        self.obs.onDetection( out )
    
    def add_composition( self ):
        """ Composition table 
        """ 
        composition_table = [
                (1, 1, 92000.),
                (4, 2, 13000.),
                (9, 4, 4.5),
                (11, 5, 4.5),
                (12, 6, 447.4),
                (14, 7, 34.2),
                (16, 8, 526.3),
                (19, 9, 0.3),
                (20, 10, 58.),
                (23, 11, 3.2),
                (24, 12, 108.),
                (27, 13, 7.8),
                (28, 14, 100.),
                (32, 16, 13.1),
                (40, 18, 2.2),
                (40, 20, 6.5),
                (45, 21, 0.97),
                (48, 22, 0.97),
                (51, 23, 0.97),
                (52, 24, 1.5),
                (55, 25, 1.1),
                (56, 26, 97.)
        ]

        self.composition = SourceComposition(self.sourceMinEnergy,
                                             self.sourceMaxEnergy,
                                             self.sourceSpectralIndex)

        for A, Z, a in composition_table:
            if Z > 2:
        	    a *= 10 # Bisi's scaling factor
            self.composition.add(nucleusId(A, Z), a)		

    def init_sources( self ):
        """ Deploy CR sources and their proporties
        """

        data = np.genfromtxt(self.sources_file, comments='#', delimiter=' ', dtype=np.float64)
        sX, sY, sZ = data[:,0], data[:,1], data[:,2]
        sourceList = SourceMultiplePositions()
        for x, y, z in zip(sX, sY, sZ):
            sourceList.add(Vector3d(x, y, z))

        self.source.add(sourceList)
        self.source.add(SourceIsotropicEmission())

        if self.A and self.Z: # if inserting single type particle source
            self.source.add(SourceParticleType(nucleusId(self.A, self.Z )))
            self.source.add(SourcePowerLawSpectrum(self.sourceMinEnergy,
                                                   self.sourceMaxEnergy,
                                                   self.sourceSpectralIndex))
        else:
            self.add_composition()
            self.source.add( self.composition )

    def init_interactions(self):
        """ Used interactions
        """

        EBL = IRB_Gilmore12
        self.m.add(PhotoPionProduction(CMB))
        self.m.add(PhotoPionProduction(EBL))
        self.m.add(PhotoDisintegration(CMB))
        self.m.add(PhotoDisintegration(EBL))
        self.m.add(NuclearDecay())
        self.m.add(ElectronPairProduction(CMB))
        self.m.add(ElectronPairProduction(EBL))

    def init_moduleList(self):
        """ Initialize moduleList
        """

        self.m.add(DeflectionCK(self.bField, 1e-3, 10.*kpc, 10.*Mpc))
        self.m.add(MinimumEnergy(self.minEnergy))
        self.m.add(MaximumTrajectoryLength(self.maxTrajectory))
        self.m.add(ReflectiveBox(self.boxOrigin, Vector3d(self.boxSize)))
        self.m.add(self.obs)

    def init(self):
        """ Initialized everything before the start of simulation
        """

        Random_seedThreads(self.generalSeed)

        self.init_bField()
        self.init_sources()
        self.init_observer()
        self.init_interactions()
        self.init_moduleList()

    def run(self):
        """ Run the simulation
        """

        self.m.setShowProgress(True)
        self.m.run(self.source, self.NEvents, True)

