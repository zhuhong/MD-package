'''
Add on 2011.08.23
@change:\n
    - 2011.09.06\n
        - make some change in Read_crd()\n

'''

import string
import unit_atom
import sys

def Read_top(filename):
    '''
    Read in an amber top file and output the atom list.
    '''
    try:
        fp=open(filename,'r')
    except IOError, e:
        print e
        sys.exit()
    all_lines=fp.readlines()
    fp.close()
    find_resi_label =False
    find_resi_point =False
    find_atom_name  =False
    find_charge     = False
    find_radius       = False

    atom_charge     = list()
    residue_label   =[]
    residue_pointer =[]
    atom_name       =[]
    atom_radius       = list()

    for line in all_lines:
        if "%FORMAT" in line:
            continue
        if "%FLAG" in line:
            if "RESIDUE_LABEL" in line:
                find_resi_label =True
                find_resi_point =False
                find_atom_name  =False
                find_charge     = False
                find_radius = False
            elif "RESIDUE_POINTER" in line:
                find_resi_point =True
                find_resi_label =False
                find_atom_name  =False
                find_charge     = False
                find_radius = False
            elif "ATOM_NAME" in line:
                find_atom_name  =True
                find_resi_label =False
                find_resi_point =False
                find_charge     = False
                find_radius     = False
            elif "CHARGE" in line:
                find_atom_name  = False
                find_resi_label = False
                find_resi_point = False
                find_charge     = True
                find_radius     = False
            elif "RADII" in line:
                find_atom_name  = False
                find_resi_label = False
                find_resi_point = False
                find_charge     = False
                find_radius     = True
            else:
                find_resi_label =False
                find_resi_point =False
                find_atom_name  =False
                find_charge     = False
                find_radius       = False
        else:
            if find_resi_label:
                residue_label.append(line[:-1])
            elif find_resi_point:
                residue_pointer.append(line[:-1])
            elif find_atom_name:
                atom_name.append(line[:-1])
            elif find_charge:
                items = line.split()
                for item in items:
                    atom_charge.append(float(item)/18.2223)
            elif find_radius:
                items = line.split()
                for item in items:
                    atom_radius.append(float(item))
            else:
                pass
    residue_label=string.split(string.join(residue_label))
    residue_pointer=string.split(string.join(residue_pointer))

    atom=[]
    for name in atom_name:
        for i in range(len(name)/4):
            atom.append(string.strip(name[4*i:4*i+4]))

    atom_name=atom

    result_list=[]

    print atom_name
    print len(atom_name)
    print residue_label

    temp_num=0
    for i in range(len(atom_name)):
        atom_unit=unit_atom.unit_atom()
        atom_unit.atom_name=atom_name[i]
        atom_unit.atom_serial=(i+1)
        atom_unit.charge = atom_charge[i]
        atom_unit.radius = atom_radius[i]
#        for j in range(len(residue_pointer)-1):
#            if (i+1) > int(residue_pointer[j])-1 and (i+1) < int(residue_pointer[j+1]):
#                atom_unit.residue_name=residue_label[j]
#                atom_unit.residue_serial=j+1
#            elif (i+1) > int(residue_pointer[-1])-1:
#                atom_unit.residue_name=residue_label[-1]
#                atom_unit.residue_serial=len(residue_pointer)
#            else:
#                pass
        if (i+1) > int(residue_pointer[temp_num])-1 and (i+1) < int(residue_pointer[temp_num+1]):
            atom_unit.residue_name=residue_label[temp_num]
            atom_unit.residue_serial=temp_num+1
        elif (i+1) > int(residue_pointer[-1])-1:
            atom_unit.residue_name=residue_label[-1]
            atom_unit.residue_serial=len(residue_pointer)
        else:
            if temp_num < len(residue_pointer)-1:
                temp_num=temp_num+1
            else:
                pass
            atom_unit.residue_name=residue_label[temp_num]
            atom_unit.residue_serial=temp_num+1
#        if (i+1) > ni_pointer and (i+1) < nj_pointer:
#            atom_unit.residue_name=ni_label
#            atom_unit.residue_serial=
#        else:

        result_list.append(atom_unit)
        print atom_unit.atom_2_PQRformat()
    
    return result_list
    
def Read_crd(top_file, crd_file):
    '''
    Read in a crd coordinates file and  add the coordinates to the atom list. 
    '''
    atom_list=Read_top(top_file)
    try:
        fp=open(crd_file,'r')
    except IOError,e:
        print e
        return atom_list


    all_lines=fp.readlines()
    fp.close()
    number_line=int(string.split(all_lines[1])[0])
    if number_line != len(atom_list):
        print "Error: the atom number in top file not equal the crd file."
        sys.exit(1)
    coor=all_lines[2:]
    for i,atom in enumerate(atom_list):
        j=i%2
        # print coor
        # print len(coor)
        atom_list[i].coor_x=float(string.strip(coor[i/2][36*j   :36*j+12]))/10
        atom_list[i].coor_y=float(string.strip(coor[i/2][36*j+12:36*j+24]))/10
        atom_list[i].coor_z=float(string.strip(coor[i/2][36*j+24:36*j+36]))/10

    return atom_list


#    for name in atom_name[1:]:
#       for i in range(len(name)/4):
#           atom.append(string.strip(name[4*i:4*i+4]))
