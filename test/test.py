#!/bin/bash env
from MDPackage.Coor import amber_top
from MDPackage import Simple_atom

atoms = amber_top.Read_crd("com.top","com.crd")
Simple_atom.Save_file("com.pqr",atoms)
