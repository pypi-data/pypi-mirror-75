'''
-----------
CPMD_Cube_Tools
-----------

Author: Wade LYU
email: lyuwade@gmail.com

A python library and tool to read in and manipulate Gaussian and CPMD cube files. This code allows you to:
    Read and write Gaussian/CPMD cube files
    Perform VDD charge analysis

Acknowledgment: This code is partially developed based on the Cube-Toolz @ https://github.com/funkymunkycool/Cube-Toolz/blob/master/cube_tools.py

Version      Date              Coder          Changes
=======   ==========        ===========       =======
0.6x       05/08/2019        Wade Lyu          Corrected the coordinates of cube file by external geometry information, and formated cube output
0.7x       02/10/2019        Wade Lyu          Implemention of Voronoi deformation density (VDD) method for charge analysis
0.8x       23/04/2020        Wade Lyu          Cleaned-up and Reformated the core of the package
0.99       25/04/2020        Wade Lyu          Added more detailed examples for users
0.991      26/04/2020        Wade Lyu          Fixed some typos
0.992      27/04/2020        Wade Lyu          Added the explanation of the inputs and outputs
0.993	   04/08/2020        Wade Lyu          Added a new method translate_xyz
'''
version= 0.993

