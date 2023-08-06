
#Ramachandran Plot
#from __future__ import division, print_function
import math
import sys
import os
from os.path import abspath
import os.path
import matplotlib.pyplot as plt
import numpy as np
from Bio import PDB
from matplotlib import colors
import matplotlib.patches as mpatches
import matplotlib.markers as mmark
import matplotlib.lines as mlines




def plot_ramachandran(file):
    __pdb__=file

    """
    The preferences were calculated from the following artice:
    Lovell et al. Structure validation by Calpha geometry: phi,psi and Cbeta deviation. 2003
    DOI: 10.1002/prot.10286
    """

    # General variable for the background preferences
    rama_preferences = {
        "General": {
            "file": os.path.join('data',"rama500-general.data"),
            "cmap": colors.ListedColormap([]),
            "bounds": [0, 0.002, 0.02, 1],
        },
        "GLY": {
            "file": os.path.join('data',"rama500-gly-sym.data"),
            "cmap": colors.ListedColormap([]),
            "bounds": [0, 0.002, 0.02, 1],
        },
        "PRO": {
            "file": os.path.join('data',"rama500-pro.data"),
            "cmap": colors.ListedColormap(['#FFFFFF00', 'skyblue', 'deepskyblue']),
            "bounds": [0, 0.0005, 0.02, 1],
        },
        "PRE-PRO": {
            "file": os.path.join('data',"rama500-prepro.data"),
            "cmap": colors.ListedColormap(['#FFFFFF', '#FFE8C5', '#FFCC7F']),
            "bounds": [0, 0.002, 0.02, 1],
        }
    }
    
    r_path = os.path.abspath(os.path.dirname(__file__))
    rama_pref_values = {}
    for key, val in rama_preferences.items():
        rama_pref_values[key] = np.full((360, 360), 0, dtype=np.float64)
        with open(os.path.join(r_path, val["file"])) as fn:
              for line in fn:
                if not line.startswith("#"):
                    # Preference file has values for every second position only
                    rama_pref_values[key][int(float(line.split()[1])) + 180][int(float(line.split()[0])) + 180] = float(
                        line.split()[2])
                    rama_pref_values[key][int(float(line.split()[1])) + 179][int(float(line.split()[0])) + 179] = float(
                        line.split()[2])
                    rama_pref_values[key][int(float(line.split()[1])) + 179][int(float(line.split()[0])) + 180] = float(
                        line.split()[2])
                    rama_pref_values[key][int(float(line.split()[1])) + 180][int(float(line.split()[0])) + 179] = float(
                        line.split()[2])

    normals = {}
    outliers = {}
    for key, val in rama_preferences.items():
        normals[key] = {"x": [], "y": []}
        outliers[key] = {"x": [], "y": [],'Res':[]}

   # Calculate the torsion angle of the inputs
   # for inp in sys.argv[1:]:
        #if not os.path.isfile(inp):
           # print("{} not found!".format(inp))
            #continue
    structure = PDB.PDBParser().get_structure('input_structure', __pdb__)
    for model in structure:
        for chain in model:
            polypeptides = PDB.PPBuilder().build_peptides(chain)
            for poly_index, poly in enumerate(polypeptides):
                phi_psi = poly.get_phi_psi_list()
                for res_index, residue in enumerate(poly):
                    res_name = "{}".format(residue.resname)
                    res_num = residue.id[1]
                    phi, psi = phi_psi[res_index]
                    if phi and psi:
                        aa_type = ""
                        if str(poly[res_index + 1].resname) == "General":
                            aa_type = "PRE-PRO"
                        elif res_name == "PRO":
                            aa_type = "General"
                        elif res_name == "GLY":
                            aa_type = "PRE-PRO"
                        else:
                            aa_type = "PRO"
                            bb_type = "General"
                            cc_type = "PRE-PRO"
                            dd_type = "PRO"
                        if rama_pref_values[aa_type][int(math.degrees(psi)) + 180][int(math.degrees(phi)) + 180] < \
                                rama_preferences[aa_type]["bounds"][1]:
                            #print("{} {} {} {}{} is an outlier".format(__file__, model, chain, res_name, res_num))
                            outliers[aa_type]["x"].append(math.degrees(phi))
                            outliers[aa_type]["y"].append(math.degrees(psi))
                            outliers[aa_type]['Res'].append(res_name+'_'+str(res_num))
                        else:
                            normals[aa_type]["x"].append(math.degrees(phi))
                            normals[aa_type]["y"].append(math.degrees(psi))
                            

    # Generate the plots
    plt.figure(figsize=(10,10))
    for idx, (key, val) in enumerate(sorted(rama_preferences.items(), key=lambda x: x[0].lower())):       
        #plt.title(key,Ramachandran plot)
        plt.imshow(rama_pref_values[key], cmap=rama_preferences[key]["cmap"],
                   norm=colors.BoundaryNorm(rama_preferences[key]["bounds"], rama_preferences[key]["cmap"].N),
                   extent=(-180, 180, 180, -180),alpha=0.7)

        plt.scatter(normals[aa_type]["x"], normals[aa_type]["y"],color="k",s=[10],marker='o')
        plt.scatter(normals[bb_type]["x"], normals[bb_type]["y"],color="k",s=[35],marker='^')
        plt.scatter(normals[cc_type]["x"], normals[cc_type]["y"],color="k",s=[35],marker='x')
        plt.scatter(normals[dd_type]["x"], normals[dd_type]["y"],color="k",s=[25],marker='+')
        plt.scatter(outliers[key]["x"], outliers[key]["y"],color="red",s=[15],marker=',')

        for key in outliers:
            for i, name in enumerate (outliers[key]['Res']):
                plt.annotate(name, (outliers[key]["x"][i], outliers[key]["y"][i]))

        
        plt.xlim([-180, 180])
        plt.ylim([-180, 180])
        ax = plt.gca()
        ax.set_xlim(-180, 180)
        ax.set_ylim(-180, 180)
        ax.set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
        ax.set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
        plt.plot([-180, 180], [0, 0], linewidth=1,color="k",alpha=0.2)
        plt.plot([0, 0], [-180, 180], linewidth=1,color="k",alpha=0.2)
        plt.xlabel(r'$\phi$',fontsize=14,color="k",alpha=1)
        plt.ylabel(r'$\psi$',fontsize=14,color="k",alpha=1)
        plt.grid(linestyle='--',color="k",alpha=0.4)
        plt.title('Ramachandran Plot',fontsize=15,color="k",alpha=1,)
            
    A = mpatches.Patch(color='deepskyblue',lw=15)#good metho
    B = mpatches.Patch(color='skyblue',lw=15)
    C = mpatches.Patch(color='#FFCC7F',lw=15)
    D = mpatches.Patch(color='#FFE8C5',lw=15)
    E = mlines.Line2D([], [], color='red', marker='s',linestyle='None',
                          markersize=10)
    F = mlines.Line2D([], [], color='black', marker='o',linestyle='None',
                          markersize=7,label="  ")
    G = mlines.Line2D([], [], color='black', marker='^',linestyle='None',
                          markersize=7,label="General/Pre-Pro/Proline Allowed")   
    H = mlines.Line2D([], [], color='black', marker='^',linestyle='None',
                          markersize=7,label="General/Pre-Pro/Proline Favoured")
    I = mlines.Line2D([], [], color='black', marker='o',linestyle='None',
                          markersize=7,label="   ")
    J = mlines.Line2D([], [], color='black', marker='x',linestyle='None',
                          markersize=7,label="  ")
    k = mlines.Line2D([], [], color='black', marker='x',linestyle='None',
                          markersize=7)
    L = mlines.Line2D([], [], color='red', marker='',linestyle='None',
                          markersize=7,label=" ")
    M = mlines.Line2D([], [], color='black', marker='',linestyle='None',
                          markersize=7,label="Glycien Favoured")
    N = mlines.Line2D([], [], color='black', marker='',linestyle='None',
                          markersize=7,label="Glycien Allowed")
    o = mlines.Line2D([], [], color='black', marker='',linestyle='None',
                          markersize=7,label="Outliers")
    plt.legend(frameon=False,handles=[A,B,C,D,E,F,I,J,k,L,H,G,M,N,o],loc='upper left', labelspacing=2,fontsize=10,ncol=3,columnspacing=-2.8,bbox_to_anchor=(0.01, -0.06))
    plt.show() 
   
    # plt.show
    #plt.tight_layout()
    # plt.savefig("asd.png", dpi=300) #Uncommet this line of you want so save the plot in a specific location
