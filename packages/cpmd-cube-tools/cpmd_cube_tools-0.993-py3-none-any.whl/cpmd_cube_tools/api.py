from cpmd_cube_tools.core import *

#####################################################
def add_cubes(files):
    cubes = [cube(fin) for fin in files]
    print( "====== Adding cube files ======")
    cube_out = copy.deepcopy(cubes[0])
    for ctmp in cubes[1:]:
        cube_out.data += ctmp.data
    print( "====== Writing output cube as sum.cube ======")
    cube_out.write_cube('sum.cube')
    return cube_out

def align2cube(cube1,cube2):
    '''
    Align 2ed cube file to the first cube file
    '''
    #cubeout=copy.deepcopy(cube2)
    cube1.toorigin()
    cube2.toorigin()
    delt=np.array(cube1.atomsXYZ[0])-np.array(cube2.atomsXYZ[0])
    print('delta: ',delt)
    cube2.translate_cube(delt)
    return None

def diff_cubes(files):
    cubes = [cube(fin) for fin in files]
    print( "====== Subtracting cube files ======")
    cube_out = copy.deepcopy(cubes[0])
    for i in range(1,len(files)):
        ctmp=cubes[i]
        align2cube(cubes[0],ctmp)
        ctmp.write_cube(files[i]+'_alignTo0')
        cube_out.data -= ctmp.data
    print( "====== Writing output cube as diff.cube ======")
    cube_out.write_cube('diff.cube')
    return cube_out

def translate_cubes(files,tVector):
    cubes = [cube(fin) for fin in files]
    print( "====== Translating cube files ======")
    [ctmp.translate_cube(tVector) for ctmp in cubes]
    print( "====== Writing output cubes as translateN.cube ======")
    if len(cubes) == 1:
        cubes[0].write_cube('translate.cube')
    else:
        for ind,cout in enumerate(cubes):
            cout.write_cube('translate%d.cube' % ind)
    return None

def translate_cubes_xyz(files,tVector):
    cubes = [cube(fin) for fin in files]
    print( "====== Translating cube files ======")
    [ctmp.translate_xyz(tVector) for ctmp in cubes]
    print( "====== Writing output cubes as translateXYZN.cube ======")
    if len(cubes) == 1:
        cubes[0].write_cube('translateXYZ.cube')
    else:
        for ind,cout in enumerate(cubes):
            cout.write_cube('translateXYZ%d.cube' % ind)
    return None


def correct_cube(files,geom):
    cubes=cube(files)
    print('===== Correct CUBE coordinates=====')
    cubes.correct_cube(geom)
    print("====== Writing output cubes as "+files.split('.')[0]+"_corrected.cube ======")
    cubes.write_cube(files.split('.')[0]+'_corrected.cube')
    return None

def cube2vdd(files,geom,inpf,alists):
     cubes=cube(files)
     print('==== performing vdd analysis =====')
     cubes.cube2vdd(geom,inpf,alists)
     return None

def cube2dvdd(files,geom,inpf,alists):
     cubes=cube(files)
     print('==== performing vdd analysis for electrons only =====')
     cubes.cube2dvdd(geom,inpf,alists)
     return None

def cptest():
    data_path=pkg_resources.resource_filename('cpmd_cube_tools','test/')
    try:
       os.system('rm test -rf')
       print('Cleaned-up the test dataset at PWD')
    except:
       os.system('pwd')
    print('Copying the test dataset from',data_path,' to PWD')
    try:
       os.system('cp '+data_path+' . -rf')
       return 0
    except:
       print('Please copy the test dataset manually from:\n',data_path)
       return 1

