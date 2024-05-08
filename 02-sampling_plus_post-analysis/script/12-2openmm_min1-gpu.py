import os

base_directory = os.path.abspath(os.path.join(os.getcwd(), "../.."))
matched_folder = ""

for folder in os.listdir(base_directory):
    folder_path = os.path.join(base_directory, folder)
    if os.path.isdir(folder_path) and "_0-aacg-" in folder:
        matched_folder = folder_path
        break  

if matched_folder:
    aa_ua_residues = []
    index = 0
    start_reading = False

    with open(os.path.join(matched_folder, "AA-UA-CG-DIVISION.inp"), 'r') as file:
        for line in file:
            line = line.strip()
            if "template_id" in line:
                start_reading = True
                continue

            if start_reading:
                if "/" in line:
                    break

                for number in line.split():
                    index += 1
                    if number in ["2", "3", "4"]:
                        aa_ua_residues.append(index)

    ua_aa_index = ' '.join(map(str, aa_ua_residues))

    print("\nAA UA Residues Indexes:")
    print(ua_aa_index)
else:
    print("No folder matches the specified pattern.")

from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout

# Load topology and coordinates
prmtop = app.AmberPrmtopFile('./system_solv.prmtop')
inpcrd = app.AmberInpcrdFile('./system_solv.inpcrd')

# set up
system = prmtop.createSystem(nonbondedMethod=app.NoCutoff, constraints=None, implicitSolvent=None)

# position restrain
force = CustomExternalForce('k*((x-x0)^2+(y-y0)^2+(z-z0)^2)')
force.addGlobalParameter('k', 500*kilocalories_per_mole/angstroms**2)
force.addPerParticleParameter('x0')
force.addPerParticleParameter('y0')
force.addPerParticleParameter('z0')

# parse restraintmask
restraint_ranges = f'{ua_aa_index}'
restrained_atoms = []
restraint_residues = [int(res) for res in restraint_ranges.split()]
for residue in prmtop.topology.residues():
    if residue.index + 1 in restraint_residues:  
        for atom in residue.atoms():
            if atom.element.symbol != 'H':  
                restrained_atoms.append(atom.index)


for i in range(system.getNumParticles()):
    if i in restrained_atoms:  
        x0, y0, z0 = inpcrd.positions[i]
        force.addParticle(i, [x0, y0, z0])
system.addForce(force)

platform = Platform.getPlatformByName('CUDA')
properties = {'CudaPrecision': 'mixed'} 

integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 2*femtoseconds)
simulation = Simulation(prmtop.topology, system, integrator, platform, properties)
simulation.context.setPositions(inpcrd.positions)
if inpcrd.boxVectors is not None:
    simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)

simulation.minimizeEnergy(maxIterations=30000)

positions = simulation.context.getState(getPositions=True).getPositions()
app.PDBFile.writeFile(simulation.topology, positions, open('minimized.pdb', 'w'))     
