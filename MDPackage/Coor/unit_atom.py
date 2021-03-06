#-*- coding : utf-8 -*-
'''
Create on 2011-08-23
@version: 0.0.1
@change: \n
    - 2011-01-25\n
        - copy from Simple_atom.
'''

import string
import re

class unit_atom():
    '''
    It's a simple atom class. 
    '''
    def __init__(self,atom_name="",atom_serial=1, atom_id =1, \
        residue_name="", residue_id = 1, residue_serial=1, \
        coor_x=0.0,coor_y=0.0,coor_z=0.0):
        self.atom_name      = atom_name
        self.atom_serial    = atom_serial
        self.atom_id        = atom_id  # this one is from 1.
        self.residue_name   = residue_name
        self.residue_serial = residue_serial
        self.residue_id     = residue_id #  this one is from 1.
        self.coor_x         = coor_x
        self.coor_y         = coor_y
        self.coor_z         = coor_z
        self.charge         = 0.0
        self.radius           = 0.0

    def atom_2_PDBformat(self):
        temp_atom=""
        if re.match('^\d',self.atom_name) != None:
            temp_atom=self.atom_name.ljust(4)
        else:
            if len(self.atom_name)<4:
                temp_atom=(" "+self.atom_name).ljust(4)
            else:
                temp_atom=self.atom_name

        s = "%s%5d %s %3s  %4d    %8.3f%8.3f%8.3f%6.2f%6.2f "  \
                  % ("ATOM".ljust(6) , self.atom_serial , temp_atom , self.residue_name.rjust(3) , \
                  self.residue_serial , self.coor_x*10 , self.coor_y*10 , self.coor_z*10,\
                  1.00,0.00)
        return s

    def atom_2_PQRformat(self):
        temp_atom=""
        if re.match('^\d',self.atom_name) != None:
            temp_atom=self.atom_name.ljust(4)
        else:
            if len(self.atom_name)<4:
                temp_atom=(" "+self.atom_name).ljust(4)
            else:
                temp_atom=self.atom_name

        s = "%s%5d %s %3s  %4d    %8.3f%8.3f%8.3f%8.4f%7.4f "  \
                  % ("ATOM".ljust(6) , self.atom_serial , temp_atom , self.residue_name.rjust(3) , \
                  self.residue_serial , self.coor_x*10 , self.coor_y*10 , self.coor_z*10,\
                  self.charge,self.radius)
        return s        

    def atom_2_GROformat(self):
        s="%5d%5s%5s%5d%8.3f%8.3f%8.3f" \
                %(self.residue_serial , string.ljust(self.residue_name,5) , self.atom_name , self.atom_serial , \
                self.coor_x , self.coor_y , self.coor_z )
        return s


