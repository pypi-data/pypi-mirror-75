import os,time,scipy,pkg_resources
import pandas as pd
import numpy as np
from os.path import isfile
from sys import exit,argv
from scipy import ndimage
from scipy.ndimage.filters import gaussian_filter
from scipy.constants import physical_constants
import argparse,copy
from argparse import RawTextHelpFormatter
from skimage import transform
from cpmd_cube_tools._version import *
from cpmd_cube_tools._citation import *

class cube():
    '''
    Cube Class:
    Includes a bunch of methods to manipulate cube data
    '''

    def __init__(self,fname=None):
        if fname != None:
            try:
                self.read_cube(fname)
            except IOError as e:
                print( "File used as input: %s" % fname )
                print( "File error ({0}): {1}".format(e.errno, e.strerror))
                self.terminate_code()
        else:
            self.default_values()
        return None

    def citation(self):
        print('Citation:\n',citation)
        print('Acknowledgement:\n',Acknowledgement)

    def show_version(self):
        print("Version: ",version)

    def toorigin(self):
        if float(self.origin[0])!=float(0) or float(self.origin[1])!=float(0) or float(self.origin[2])!=float(0):
           print('Moving structure and volumne data to origin point')
           self.translate_xyz(-self.origin)
           #self.origin=np.asarray([0,0,0])
           print('Original point has been set to ',self.origin)
        else:
           print('The initial original point is [0,0,0]')
       
    def get_mol_idx(self, inpf, alists):
        if '.txt' in alists:
           alist=[int(i[:-1]) for i in open(alists).readlines()] 
           return alist
        elif alists=='mol':
           return list(range(31))
        elif alists.split(',')[0]=='qm':
           return [int(i) for i in alists.split(',')[1:]]
        else:
           print('We will use the atoms order as listed in the inp file')
        try:
           inp=open(inpf).readlines()
        except:
           print('Missing inpfile, exit')
           exit()
        start=[i for i in range(len(inp)) if 'OVERLAPS' in inp[i]][0]
        nqm=int(inp[start+1][:-1])
        start=start+2
        end=start+nqm
        overlaps=[[float(i) for i in l[:-1].split()] for l in inp[start:end]]
        overlaps=np.asarray(overlaps,dtype=int)
        olp=pd.DataFrame(overlaps,columns='mm,mmid,qm,qmid'.split(','))
        olp['mmid']-=1
        olp['qmid']-=1
        olp.to_csv('overlaps.csv')
        if alists.split(',')[0]=='mm':
           molid=[int(i) for i in alists.split(',')[1:]]
           return olp.set_index('mmid').loc[molid]['qmid'].values
        else:
           print('No correct atom index can be specified!\n We will consider all QM atoms then!')
           return olp['qmid'].values
   
    def terminate_code(self):
        print( "Code terminating now")
        exit()
        return None

    def default_values(self):
        self.natoms=0
        self.comment1=0
        self.comment2=0
        self.origin=np.array([0,0,0])
        self.NX=0
        self.NY=0
        self.NZ=0
        self.X=0
        self.Y=0
        self.Z=0
        self.atoms=['0']
        self.atomsXYZ=[0,0,0]
        self.data=[0]
        return None
    
    def read_cube(self,fname):
        """
        Method to read cube file. Just needs the filename
        """

        with open(fname, 'r') as fin:
            self.filename = fname
            self.comment1 = fin.readline() #Save 1st comment
            self.comment2 = fin.readline() #Save 2nd comment
            nOrigin = fin.readline().split() # Number of Atoms and Origin
            self.natoms = int(nOrigin[0]) #Number of Atoms
            self.origin = np.array([float(nOrigin[1]),float(nOrigin[2]),float(nOrigin[3])]) #Position of Origin
            nVoxel = fin.readline().split() #Number of Voxels
            self.NX = int(nVoxel[0])
            self.X = np.array([float(nVoxel[1]),float(nVoxel[2]),float(nVoxel[3])])
            nVoxel = fin.readline().split() #
            self.NY = int(nVoxel[0])
            self.Y = np.array([float(nVoxel[1]),float(nVoxel[2]),float(nVoxel[3])])
            nVoxel = fin.readline().split() #
            self.NZ = int(nVoxel[0])
            self.Z = np.array([float(nVoxel[1]),float(nVoxel[2]),float(nVoxel[3])])
            self.atoms = []
            self.elements=[]
            self.atomsXYZ = []
            for atom in range(self.natoms):
                line= fin.readline().split()
                self.atoms.append(line[0])
                self.elements.append(line[1])
                self.atomsXYZ.append(list(map(float,[line[2], line[3], line[4]])))
            self.data = np.zeros((self.NX,self.NY,self.NZ))
            i= int(0)
            for s in fin:
                for v in s.split():
                    self.data[int(i/(self.NY*self.NZ)), int((i/self.NZ)%self.NY), int(i%self.NZ)] = float(v)
                    i+=1
            # if i != self.NX*self.NY*self.NZ: raise NameError, "FSCK!"
        return None

    def load_cube(self,fname):
        """
        Method to read cube file. Just needs the filename
        """
        with open(fname, 'r') as fin:
            self.filename = fname
            self.comment1 = fin.readline() #Save 1st comment
            self.comment2 = fin.readline() #Save 2nd comment
            nOrigin = fin.readline().split() # Number of Atoms and Origin
            self.natoms = int(nOrigin[0]) #Number of Atoms
            self.origin = np.array([float(nOrigin[1]),float(nOrigin[2]),float(nOrigin[3])]) #Position of Origin
            nVoxel = fin.readline().split() #Number of Voxels
            self.NX = int(nVoxel[0])
            self.X = np.array([float(nVoxel[1]),float(nVoxel[2]),float(nVoxel[3])])
            nVoxel = fin.readline().split() #
            self.NY = int(nVoxel[0])
            self.Y = np.array([float(nVoxel[1]),float(nVoxel[2]),float(nVoxel[3])])
            nVoxel = fin.readline().split() #
            self.NZ = int(nVoxel[0])
            self.Z = np.array([float(nVoxel[1]),float(nVoxel[2]),float(nVoxel[3])])
            self.atoms = []
            self.elements=[]
            self.atomsXYZ = []
            for atom in range(self.natoms):
                line= fin.readline().split()
                self.atoms.append(line[0])
                self.elements.append(line[1])
                self.atomsXYZ.append(list(map(float,[line[2], line[3], line[4]])))
            self.data = np.zeros((self.NX,self.NY,self.NZ))
            i= int(0)
            for s in fin:
                for v in s.split():
                    self.data[int(i/(self.NY*self.NZ)), int((i/self.NZ)%self.NY), int(i%self.NZ)] = float(v)
                    i+=1
            # if i != self.NX*self.NY*self.NZ: raise NameError, "FSCK!"
        return self


    def write_cube(self,fname,comment='Cube file written by Tools_Lib\nCpmd_Cube_Tools Version: '+str(version)):
        try:
            with open(fname,'w') as fout:
                if len(comment.split('\n')) != 2:
                    print( 'Comment line NEEDS to be two lines!')
                    self.terminate_code()
                fout.write('%s\n' % comment)
                fout.write("%8d %12.6f %12.6f %12.6f\n" % (self.natoms, self.origin[0], self.origin[1], self.origin[2]))
                fout.write("%8d %12.6f %12.6f %12.6f\n" % (self.NX, self.X[0], self.X[1], self.X[2]))
                fout.write("%8d %12.6f %12.6f %12.6f\n" % (self.NY, self.Y[0], self.Y[1], self.Y[2]))
                fout.write("%8d %12.6f %12.6f %12.6f\n" % (self.NZ, self.Z[0], self.Z[1], self.Z[2]))
                for atom,element,xyz in zip(self.atoms,self.elements,self.atomsXYZ):
                    fout.write("%8s %12s %12.6f %12.6f %12.6f\n" % (atom, element, xyz[0], xyz[1], xyz[2]))
                for ix in range(self.NX):
                   for iy in range(self.NY):
                       for iz in range(self.NZ):
                           fout.write("%12.5e " % self.data[ix,iy,iz]),
                           if (iz % 6 == 5): fout.write('\n')
                       fout.write("\n")
        except IOError as e:
            print( "File used as output does not work: %s" % fname)
            print( "File error ({0}): {1}".format(e.errno, e.strerror))
            self.terminate_code()
        return None

    def correct_cube(self,gfile):
        '''
        Correct the coordinates in cube file with the information from GEOMETRY file.
        '''
        geom=np.loadtxt(gfile)
        na=self.natoms
        print("Num of atoms: ",na)
        #print(geom[:na,:3])
        self.atomsXYZ=list(geom[:na,:3]+self.origin*2)
        #print('Corrected atomsXYZ:\n',self.atomsXYZ)
        return None

    def translate_cube(self,tVector):
        '''
        Translate cube data and xyz by some vector. The vector is given as a list to the tVector function.
        '''
        vx=tVector[0]/self.X[0]
        vy=tVector[1]/self.Y[1]
        vz=tVector[2]/self.Z[2]
        print(tVector)
        self.atomsXYZ+=np.array(tVector)
        print(self.atomsXYZ[0])
        self.data = ndimage.shift(self.data,[vx,vy,vz],order=5, mode='wrap')
        return None

    def translate_xyz(self,tVector):
        '''
        Translate cube xyz by some vector. The vector is given as a list to the tVector function.
        '''
        print(tVector)
        self.atomsXYZ+=np.array(tVector)
        self.origin+=np.array(tVector)
        print(self.atomsXYZ[0])
        return None


    def proton2ne(self,a):
        loc=[0,2,8,8,8,8,8,8]
        if a<2:
           return a
        for i in range(1,len(loc)):
            if a-sum(loc[:i])<=0:
               return a-sum(loc[:i-1])

    def pointinside(self,pxyz,regioni):
        dist0=scipy.spatial.distance.cdist(pxyz,regioni)[0]
        minid=np.argmin(dist0)
        dist0_sum=sum(dist0)-dist0[minid]
        dist1=scipy.spatial.distance.cdist([regioni[minid]],regioni)[0]
        dist1_sum=sum(dist1)
        if dist0_sum > dist1_sum:
           return False
        else:
           return True

    def vdd_analysis(self, inpf, alists):
        '''
        Perform VDD charge analysis of the atoms specified in alists (note that atom 0 is the first atom).
        '''
        alist=self.get_mol_idx(inpf,alists)
        #print('Read-in atom list: ',alist)
        t0=time.time()
        voxelMatrix = np.array([self.X,self.Y,self.Z])
        vol = np.linalg.det(voxelMatrix)
        atomXYZ = np.array(self.atomsXYZ) 
        atomgrid=atomXYZ/np.array([self.X[0],self.Y[1],self.Z[2]])
        vdgrid=-np.ones([self.NX,self.NY,self.NZ])
        vddcharge=np.zeros(atomgrid.shape[0])
        for gx in range(self.NX):
            for gy in range(self.NY):
                for gz in range(self.NZ):
                    dist=scipy.spatial.distance.cdist([[gx,gy,gz]],atomgrid)[0]
                    aid=np.argmin(dist)
                    vdgrid[gx,gy,gz]=aid
                    vddcharge[aid]+=self.data[gx,gy,gz]
        vddcharge*=-vol # charges from electron density are negative
        print('vddcharge: ',vddcharge.shape)
        #print('atoms: ',self.atoms)
        vddcharge+=np.array([self.proton2ne(x) for x in np.array(self.atoms).astype(int)]) # total charge adding positive charges from nuclei
        print('vdd_analysis is done: ',round(time.time()-t0, 2),' seconds')
        cubeout=copy.deepcopy(self)
        cubeout.data=vdgrid
        cubeout.write_cube('vdd_regions.cube')
        vddpd=pd.DataFrame(np.array([vddcharge,self.elements]).T,index=range(atomgrid.shape[0]),columns='charge,element'.split(','))
        vddpd.to_csv('vdd_charge_all.csv')
        vddpd.loc[alist].to_csv('vdd_charge_mol.csv')
        return vddpd,alist,cubeout

    def dvdd_analysis(self, inpf, alists):
        '''
        Perform VDD charge analysis for the atoms specified in alists (note that atom 0 is the first atom).
        '''
        alist=self.get_mol_idx(inpf,alists)
        #print('Read-in atom list: ',alist)
        t0=time.time()
        voxelMatrix = np.array([self.X,self.Y,self.Z])
        vol = np.linalg.det(voxelMatrix)
        atomXYZ = np.array(self.atomsXYZ)
        atomgrid=atomXYZ/np.array([self.X[0],self.Y[1],self.Z[2]])
        vdgrid=-np.ones([self.NX,self.NY,self.NZ])
        vddcharge=np.zeros(atomgrid.shape[0])
        for gx in range(self.NX):
            for gy in range(self.NY):
                for gz in range(self.NZ):
                    dist=scipy.spatial.distance.cdist([[gx,gy,gz]],atomgrid)[0]
                    aid=np.argmin(dist)
                    vdgrid[gx,gy,gz]=aid
                    vddcharge[aid]+=self.data[gx,gy,gz]
        vddcharge*=-vol # charges from electron density are negative
        print('dvddcharge: ',vddcharge.shape)
        #print('atoms: ',self.atoms)
        print('dvdd_analysis is done: ',round(time.time()-t0, 2),' seconds')
        cubeout=copy.deepcopy(self)
        cubeout.data=vdgrid
        cubeout.write_cube('vdd_regions.cube')
        vddpd=pd.DataFrame(np.array([vddcharge,self.elements]).T,index=range(atomgrid.shape[0]),columns='charge,element'.split(','))
        vddpd.to_csv('dvdd_charge_all.csv')
        vddpd.loc[alist].to_csv('dvdd_charge_mol.csv')
        return vddpd,alist,cubeout


    def vdd_mask(self, inpf, alists):
        '''
        Perform VDD mask for the atoms not specified in alists (note that atom 0 is the first atom).
        '''
        alist=self.get_mol_idx(inpf,alists)
        #print('Read-in atom list: ',alist)
        t0=time.time()
        voxelMatrix = np.array([self.X,self.Y,self.Z])
        vol = np.linalg.det(voxelMatrix)
        atomXYZ = np.array(self.atomsXYZ)
        atomgrid=atomXYZ/np.array([self.X[0],self.Y[1],self.Z[2]])
        vdgrid=-np.ones([self.NX,self.NY,self.NZ])
        vddcharge=np.zeros(atomgrid.shape[0])
        for gx in range(self.NX):
            for gy in range(self.NY):
                for gz in range(self.NZ):
                    dist=scipy.spatial.distance.cdist([[gx,gy,gz]],atomgrid)[0]
                    aid=np.argmin(dist)
                    vdgrid[gx,gy,gz]=aid
                    vddcharge[aid]+=self.data[gx,gy,gz]
        vddcharge*=-vol # charges from electron density are negative
        print('vddcharge: ',vddcharge.shape)
        #print('atoms: ',self.atoms)
        vddcharge+=np.array([self.proton2ne(x) for x in np.array(self.atoms).astype(int)]) # total charge adding positive charges from nuclei
        print('vdd_analysis is done: ',round(time.time()-t0, 2),' seconds')
        cubeout=copy.deepcopy(self)
        cubeout.data=vdgrid
        cubeout.write_cube('vdd_regions.cube')
        vddpd=pd.DataFrame(np.array([vddcharge,self.elements]).T,index=range(atomgrid.shape[0]),columns='charge,element'.split(','))
        vddpd.to_csv('vdd_charge_all.csv')
        vddpd.loc[alist].to_csv('vdd_charge_mol.csv')
        return vddpd,alist,cubeout
            
    def cube2vdd(self,gero,inpf, alists):
        if gero!=None:
           self.correct_cube(gero)
        vddpd,alist,vddcube=self.vdd_analysis(inpf,alists)
        print(pd.to_numeric(vddpd.loc[alist].charge).values.sum())
        return pd.to_numeric(vddpd.loc[alist].charge).values,vddcube

    def cube2vdd_test(self,gero,inpf):
        if gero!=None:
           self.correct_cube(gero)
        vddpd,alist,vddcube=self.vdd_analysis(inpf,'mol')
        print(pd.to_numeric(vddpd.loc[alist].charge).values.sum())
        return pd.to_numeric(vddpd.loc[alist].charge).values,vddcube

    def cube2dvdd_test(self,gero,inpf):
        if gero!=None:
           self.correct_cube(gero)
        vddpd,alist,vddcube=self.dvdd_analysis(inpf,'mol')
        print(pd.to_numeric(vddpd.loc[alist].charge).values.sum())
        return pd.to_numeric(vddpd.loc[alist].charge).values,vddcube

    def cube2dvdd(self,gero,inpf,alists):
        if gero!=None:
           self.correct_cube(gero)
        vddpd,alist,vddcube=self.dvdd_analysis(inpf,alists)
        print(pd.to_numeric(vddpd.loc[alist].charge).values.sum())
        return pd.to_numeric(vddpd.loc[alist].charge).values,vddcube

