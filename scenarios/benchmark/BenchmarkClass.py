import os

from crpropa import *
import numpy as np

class Benchmark( object ):
    """ Benchmark scenario
        Specs: https://www.auger.unam.mx/AugerWiki/BenchmarkScenario
        PA GAP note: GAP-2012-138
    """

    def __init__( self ):
        """ Initialize required objects and parameters on default values      
        """

        self.bField = None
        self.obs = Observer()
        self.m = ModuleList()
        self.source = Source()
        self.OutputName = None
        

        self.boxOrigin = Vector3d(54,54,54) * Mpc
        self.boxSize = 132 * Mpc
        self.grid = os.path.expanduser('~/crpropa_virtenv/share/crpropa/bench_54-186Mpc_440bins.raw')
        self.Brms = 1.
        self.sources_file = 'BenchmarkSources.txt'
        self.composition = None

        self.obsPosition = Vector3d( 118.34, 117.69, 119.2 ) * Mpc
        self.obsSize = 1. * Mpc

        self.NEvents = 5000
        self.A = 1
        self.Z = 1

    def init_bField( self ):
        """ Initialize magnetic field
        """
        
        # modulation grid
        mgrid = ScalarGrid( self.boxOrigin, 440, self.boxSize / 440 )
        loadGrid( mgrid, self.grid, 1. )

        # turbulent vector grid
        boxSpacing = 13.2 * Mpc / 440
        vgrid = VectorGrid( self.boxOrigin, 440, boxSpacing )
        initTurbulence(vgrid, self.Brms, 2. * boxSpacing, 2.2 * Mpc, -11./3., 2308)

        # total magnetic field
        self.bField = ModulatedMagneticFieldGrid(vgrid, mgrid)

    def init_observer( self ):
        """ Insert observer(s)
        """

        self.obs.add( ObserverSmallSphere( self.obsPosition, self.obsSize ) )
        out = TextOutput( self.OutputName )
        out.printHeader()
        self.obs.onDetection( out )
    
    def add_composition( composition ):
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

        minEnergy = 1. * EeV
        maxRigidity = 1000. * EeV
        spectralIndex = -1.
	    
        self.composition = SourceComposition( minEnergy, maxRigidity, spectralIndex)

        for A, Z, a in composition_table:
		    if Z > 2:
			    a *= 10 # Bisi's scaling factor
		    self.composition.add( nucleusId( A, Z ), a )		

    def init_sources( self ):
        """ Deploy CR sources and their proporties
        """
        
        data = np.genfromtxt( self.sources_file, comments='#', delimiter=' ', dtype=np.float64)
        sX, sY, sZ = data[:,0], data[:,1], data[:,2]
        sourceList = SourceMultiplePositions()
        for x, y, z in zip(sX, sY, sZ):
            sourceList.add(Vector3d(x, y, z))

        minEnergy = 1. * EeV
        maxRigidity = 1000. * EeV
        spectralIndex = -1.
        
        self.source.add(sourceList)
        self.source.add(SourceIsotropicEmission())
        self.source.add(SourceParticleType( nucleusId( self.A, self.Z ) ))
        self.source.add(SourcePowerLawSpectrum(minEnergy, maxRigidity, spectralIndex))        
        
        #self.source.add( sourceList )
        #self.source.add( SourceIsotropicEmission() )
        #self.source.add( composition )

    def init_interactions( self ):
        """ Used interactions
        """
        
        # interactions
        EBL = IRB_Gilmore12
        self.m.add(PhotoPionProduction(CMB))
        self.m.add(PhotoPionProduction(EBL))
        self.m.add(PhotoDisintegration(CMB))
        self.m.add(PhotoDisintegration(EBL))
        self.m.add(NuclearDecay())
        self.m.add(ElectronPairProduction(CMB))
        self.m.add(ElectronPairProduction(EBL))

    def init_moduleList( self ):
        """ Initialize moduleList
        """
        
        self.m.add( DeflectionCK( self.bField, 1e-3, 10. * kpc, 10. * Mpc ) )
        self.m.add( MinimumEnergy( 1. * EeV ) )
        self.m.add( MaximumTrajectoryLength( redshift2ComovingDistance(2) ) )
        self.m.add( ReflectiveBox( self.boxOrigin, Vector3d( self.boxSize ) ) )
        self.m.add( self.obs )
         
    def init( self ):
        """ Initialized everything before the start of simulation
        """
      
        self.init_bField()
        self.init_sources()
        self.init_observer()
        self.init_interactions()
        self.init_moduleList()

    def run( self ):
        """ Run simulation
        """
        
        self.m.setShowProgress( True )
        self.m.run( self.source, self.NEvents, True )

