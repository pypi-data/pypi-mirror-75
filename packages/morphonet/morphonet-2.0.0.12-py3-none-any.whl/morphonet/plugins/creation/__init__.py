# -*- coding: latin-1 -*-
defaultPlugins=[]

from .foundPeaksAsSeed import foundPeaksAsSeed
defaultPlugins.append(foundPeaksAsSeed())

from .watershedithNewSeeds import watershedithNewSeeds
defaultPlugins.append(watershedithNewSeeds())