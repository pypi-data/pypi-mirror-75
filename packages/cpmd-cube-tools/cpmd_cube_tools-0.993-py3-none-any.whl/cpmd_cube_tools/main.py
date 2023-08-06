from cpmd_cube_tools.api import *

def main():
    parser = argparse.ArgumentParser(description="A python library and tool to read in and manipulate Gaussian/CPMD cube files. \nThis code allows you to:\nRead and write cube files\nPerform VDD analysis\nVersion:"+str(version),formatter_class=RawTextHelpFormatter)
#    Take the planar average")
    parser.add_argument("Files",help="Cube files used in program",nargs = '+')
    parser.add_argument("-g","--geom",help="Geometry file from CPMD run")
    parser.add_argument("-mol","--molecule",help="atom list ('mm/qm,atomid0,atomid1,...' or 'put the atomlist in a file named as *.txt' or 'mol'(for test dataset only, the first 31 atoms will be selected) )'")
    parser.add_argument("-inp","--inpfile",help="cpmd/mimic input file for atoms index selection")
    parser.add_argument("-vdd","--dovdd",help="yes/no")
    parser.add_argument("-dvdd","--dodvdd",help="yes/no (vdd charges for electrons or for delta_rho)")
    parser.add_argument("-net","--netcharge",help="Net charge of the selected atoms", nargs=1, type=float)
    parser.add_argument("-a","--add",help="Add two or more cube files together",action = "store_true")
    parser.add_argument("-s","--subtract",help="Subtract two or more cube files together",action = "store_true")
    parser.add_argument("-t","--translate",help="Translate cube and xyz data. Requires a translation vector as an argument.", nargs = 3,type=float)
    parser.add_argument("-tx","--translate_xyz",help="Translate xyz data. Requires a translation vector as an argument.", nargs = 3,type=float)

    if len(argv) <= 1:
        print('No enough input ....')
        parser.print_help()
        exit()

    args = parser.parse_args()
    print(args)
#########################
    
    if args.geom!=None:
       print('Correct corrdinates information in cube file with ',args.geom)
       if args.Files:
          correct_cube(args.Files[0],args.geom)
       else:
          print("No cube file is provided.")

    if args.molecule!=None:
       if args.molecule.split(',')[0]=='mm':
          if args.inpfile:
             print('Note: using ',args.inpfile,' to specify atom list for electrons integration')
          else:
             print('Error: no inpfile information supplied!')
             exit()
       elif args.molecule.split(',')[0]=='mol':
            print('Note: test run use only!')
       else:
          print('Note: please check your customized selection of atoms carefully\n',args.molecule)

    if args.netcharge ==None:
             print('Note: no netcharge of the considered region? Setup net charge as 0.')
             args.netcharge=[0]

    if args.dovdd!=None:
       if args.dovdd.lower()=='yes':
          print('Ready to perform vdd analysis')
          if args.molecule==None:
             args.molecule='qm'
          if args.molecule.split(',')[0] in ['mm','mol'] and args.inpfile==None:
             print('Please supply also the inpfile of cpmd/mimic calculation! Otherwise, you are allowed to specify the atom list by QM orders only!\n e.g. -mol qm,id0,id1,...')
             exit()
          if args.Files:
             cube2vdd(args.Files[0],args.geom, args.inpfile, args.molecule)
          else:
              print("No cube file is provided.")
       else:
          print('If you want to do vdd, please add option flage: -vdd yes')

    if args.dodvdd!=None:
       if args.dodvdd.lower()=='yes':
          print('Ready to perform vdd analysis')
          if args.molecule==None:
             args.molecule='qm'
          if args.molecule.split(',')[0] in ['mm','mol'] and args.inpfile==None:
             print('Please supply also the inpfile of cpmd/mimic calculation! Otherwise, you are allowed to specify the atom list by QM orders only!\n e.g. -mol qm,id0,id1,...')
             exit()
          if args.Files:
             cube2dvdd(args.Files[0],args.geom, args.inpfile,args.molecule)
          else:
              print("No cube file is provided.")
       else:
          print('If you want to do dvdd, please add option flage: -dvdd yes')


    if args.add:
        if len(args.Files) >= 2:
            add_cubes(args.Files)
        else:
            print( "Error: To use the add function, two or more cube files need to be specified.")

    if args.subtract:
        if len(args.Files) >= 2:
            diff_cubes(args.Files)
        else:
            print( "Error: To use the subtract function, two or more cube files need to be specified.")

    if args.translate:
        if args.Files:
            translate_cubes(args.Files,args.translate)

    if args.translate_xyz:
        if args.Files:
            translate_cubes_xyz(args.Files,args.translate_xyz)

    print('========== Job done! ===========')
    #print("Acknowledgment:\n",Acknowledgement)
    print("Citation:\n",citation)

    return None

