# Ramachandranplot
Python3 implementation of the Ramachandran plot

*Package does work with Python2.7 but it is recommended to use Python3*

### For easy installation use pip:

    pip install ramachandranplot
    

### Usage:
    import os
    import ramachandarnplot as rama
	pdb = "example.pdb" #path of pdb file any pdb which is required to be ploted.
    rama.plot_ramachandran(pdb)

### Example output:

![Example output](https://imgur.com/HMUniy3)

### Dependencies:

Running ramachandarnplot requires *matplotlib*, *numpy* and *biopython*

To install these on a standard Linux system:

    pip install python3-matplotlib
    pip install python3-biopython
    pip install python3-numpy

For the standard PSI and PHI preferences see:

Lovell *et al*. Structure validation by Calpha geometry: phi,psi and Cbeta deviation. 2003; DOI: 10.1002/prot.10286
 
