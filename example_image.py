
# i dati sono stati presi da
# https://github.com/pynbody/genetic_example/blob/main/tutorial.ipynb

import numpy as np
import matplotlib.pyplot as plt
import pynbody

resolution = 512
size_fov   = 70

#-----------------------------------------
# "carica" un file; in realta la maggior parte dei dati (e.g. posizione delle particelle, densita delle particelle, etc) sono caricati su richiesta (qui, quando si chiama pynbody.plot.sph.image)
example_snapshot = pynbody.load("step_1_uniform/gadget_output/snapshot_047.hdf5")
# conversione in unita fisiche
example_snapshot.physical_units()

#-----------------------------------------
# scrivi alcune proprieta utili dello snapshot della simulazione
print("snapshot properties        ",example_snapshot.properties)
# scrive che tipi di dati sono contenuti nella simulazione, di solito dm (materia oscura), gas, e star (stelle)
print("avaiable types             ",example_snapshot.families())
# scrive le variabili per la materia oscura che sono contenute nell file .hdf5
print()
print("dm fields can be loaded    ",example_snapshot.dm.loadable_keys())
# scrive le variabili che potrebbero essere derivate dalle unita contenute nel file; 
print("dm fields that are defined ",example_snapshot.dm.all_keys())

#-----------------------------------------
# chiede la creazione di una mappa di densita, dentro sono impacchettate molte operazioni
map_out = pynbody.plot.sph.image(
                                   # seleziona la materia oscura
                                   example_snapshot.dm
                                   # prende un campo di vista quadrato da 70 Mpc (centrato sulla coordinata 0,0); Mpc e' 10^6 pc, con pc parsec, unita di distanza comune in astrofisica (circa 3.e18 centimetri)
                                 , width= str(size_fov)+" Mpc"
                                   # chiede di plottare la densita, che sara mediata lungo la linea di vista
                                 , qty="rho"
                                   # chiede di mediare uniformemente la qty selezionata
                                 , av_z=None
                                   # setta le unita fisiche della densita (massa/volume); Msol e' una massa solare, unita abbastanza comoda, kpc sono 1.e3kpc
                                 , units="Msol kpc^-3"
                                   # setta la risoluzione della mappa (qui 512x512)
                                 , resolution=resolution
                                   # set interni per matplotlib (una istanza di plt.fig() viene inizializzata internamente)
                                 , cmap="inferno",noplot=False
                                 )
plt.show()
#-----------------------------------------
# chiede la creazione di una mappa di densita, integrando lungo la linea di vista
map_out = pynbody.plot.sph.image(
                                   example_snapshot.dm
                                 , width= str(size_fov)+" Mpc"
                                 , qty="rho"
                                 , av_z=None
                                   # qui si sta richiedendo implicitamente l'integrazione, cambiando le unita; la densita verra integrata lungo la linea di vista; l'immagine e' piu gradevole                                  
                                 , units="Msol kpc^-2"
                                 , resolution=resolution
                                 , cmap="inferno",noplot=False
                                 )


plt.savefig('output_image.png')

