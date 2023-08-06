#!python

from cpmd_cube_tools.api import *

print('Loading test dataset...')
cptest()

print('\nLoading a cube file\n')
cube0=cube('test/DENSITY.cube')
print(cube0.atoms)
# calculate the vdd charge
print('\nCalculate the vdd charges\n')
vddcharge, vddcube=cube0.cube2vdd_test('test/GEOMETRY', 'test/mm2qm_overlap.inp')
# show the vdd charges
print(vddcharge)

# calculate the vdd charge with customized atoms selection
print('\nCalculate the vdd charges with customized atoms selection\n e.g. selected the first 5 atoms in the cube file\n')
vddcharge, vddcube=cube0.cube2vdd('test/GEOMETRY', 'test/mm2qm_overlap.inp','qm,0,1,2,3,4')
# show the vdd charges
print(vddcharge)

# calculate the vdd charge with customized atoms selection
print('\nCalculate the vdd charges with customized atoms selection\n e.g. selected the first 5 atoms in the mm atom order list\n')
vddcharge, vddcube=cube0.cube2vdd('test/GEOMETRY', 'test/mm2qm_overlap.inp','mm,0,1,2,3,4')
print(vddcharge)


#calculate the vdd electronic only charges 0
print('\nCalculate the vdd charges of electrons only\nSelected all the atoms in the test cube file\n')
vddcharge, vddcube=cube0.cube2dvdd_test('test/GEOMETRY', 'test/mm2qm_overlap.inp')
# show the vdd charges
print(vddcharge)


# calculate the vdd electronic only charges 1
print('\nCalculate the vdd charges of electrons only, with customized atoms selection\ne.g. Selected the first 5 atoms in the test cube file\n')
vddcharge, vddcube=cube0.cube2dvdd('test/GEOMETRY', 'test/mm2qm_overlap.inp','qm,0,1,2,3,4')
# show the vdd charges
print(vddcharge) 

# calculate the vdd electronic only charges 2
print('\nCalculate the vdd charges of electrons only, with customized atoms selection\ne.g. Selected the first 5 atoms in the mm atom order list\n')
vddcharge, vddcube=cube0.cube2dvdd('test/GEOMETRY', 'test/mm2qm_overlap.inp','mm,0,1,2,3,4')                                                 
print(vddcharge)
