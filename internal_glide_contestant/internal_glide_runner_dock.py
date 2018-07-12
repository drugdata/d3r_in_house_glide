#!/usr/bin/env python

__author__ = 'j5wagner@ucsd.edu'


from d3r.celppade.custom_dock import Dock
import os
import glob

class schrodinger_glide(Dock):
    """Abstract class defining methods for a custom docking solution
    for CELPP
    """
    Dock.SCI_PREPPED_LIG_SUFFIX = '_prepared.mae'
    Dock.SCI_PREPPED_PROT_SUFFIX = '_prepared.mae'


    def ligand_technical_prep(self, sci_prepped_lig, targ_info_dict = {}):
        """
        'Technical preparation' is the step immediate preceding
        docking. During this step, you may perform any file
        conversions or processing that are specific to your docking
        program. Implementation of this function is optional.
        :param sci_prepped_lig: Scientifically prepared ligand file
        :param targ_info_dict: A dictionary of information about this target and the candidates chosen for docking.
        :returns: A list of result files to be copied into the
        subsequent docking folder. The base implementation merely
        returns the input string in a list (ie. [sci_prepped_lig]) 
        """
        return super(schrodinger_glide,
                     self).ligand_technical_prep(sci_prepped_lig,
                                         targ_info_dict = targ_info_dict)



    def receptor_technical_prep(self, 
                                sci_prepped_receptor, 
                                pocket_center, 
                                targ_info_dict = {}):
        """
        'Technical preparation' is the step immediately preceding
        docking. During this step, you may perform any file
        conversions or processing that are specific to your docking
        program. Implementation of this function is optional.
        :param sci_prepped_receptor: Scientifically prepared receptor file
        :param pocket_center: list of floats [x,y,z] of predicted pocket center
        :param targ_info_dict: A dictionary of information about this target and the candidates chosen for docking.
        :returns: A list of result files to be copied into the
        subsequent docking folder. This implementation merely
        returns the input string in a list (ie [sci_prepped_receptor])
        """

        grid_lines = []
        grid_lines += ["GRID_CENTER \t %d, %d, %d " %(pocket_center[0],
                                                      pocket_center[1],
                                                      pocket_center[2])]
        grid_lines += ["GRIDFILE \t grid.zip " ]
        #grid_lines += ["INNERBOX \t 8, 8, 8 "]
        #grid_lines += ["INNERBOX \t 15, 15, 15 "]
        #grid_lines += ["OUTERBOX \t 15, 15, 15 "]
        grid_lines += ["INNERBOX \t 15, 15, 15 "]
        grid_lines += ["OUTERBOX \t 16, 16, 16 "]
        grid_lines += ["RECEP_FILE \t %s " %(sci_prepped_receptor)]
        with open ("grid.in", "w") as f:
            f.write('\n'.join(grid_lines))
        f.close()
        os.system("$SCHRODINGER/glide -WAIT grid.in" )
        os.system('sleep 10') # If it crashed it needs time to clean up
        if not(os.path.exists('grid.zip')):
            return False
        return ['grid.zip']




    def dock(self, 
             tech_prepped_lig_list, 
             tech_prepped_receptor_list, 
             output_receptor_pdb, 
             output_lig_mol, 
             targ_info_dict={}):
        """
        This function is the only one which the contestant MUST
        implement.  The dock() step runs the actual docking
        algorithm. Its first two arguments are the return values from
        the technical preparation functions for the ligand and
        receptor. These arguments are lists of file names (strings),
        which can be assumed to be in the current directory. 
        If prepare_ligand() and ligand_technical_prep() are not
        implemented by the contestant, tech_prepped_lig_list will
        contain a single string which names a SMILES file in the
        current directory.
        If receptor_scientific_prep() and receptor_technical_prep() are not
        implemented by the contestant, tech_prepped_receptor_list will
        contain a single string which names a PDB file in the current
        directory.
        The outputs from this step must be two files - a pdb with the
        filename specified in the output_receptor_pdb argument, and a
        mol with the filename specified in the output_ligand_mol
        argument.
        :param tech_prepped_lig_list: The list of file names resturned by ligand_technical_prep. These have been copied into the current directory.
        :param tech_prepped_receptor_list: The list of file names resturned by receptor_technical_prep. These have been copied into the current directory.
        :param output_receptor_pdb: The final receptor (after docking) must be converted to pdb format and have exactly this file name.
        :param output_lig mol: The final ligand (after docking) must be converted to mol format and have exactly this file name.
        :param targ_info_dict: A dictionary of information about this target and the candidates chosen for docking.
        :returns: True if docking is successful, False otherwise. Unless overwritten, this implementation always returns False
        """
        ligand_mae = tech_prepped_lig_list[0]
        grid_file = tech_prepped_receptor_list[0]
        allowed_precisions = ['SP','XP']
        precision = 'SP'
        if not(precision in allowed_precisions):
            logging.info('Invalid precision setting %s. Must be one of %r. Switching precision to %s' %(precision, allowed_precisions, allowed_precisions[0]))
            precision = allowed_precisions[0]
        dock_lines = []
        dock_lines += ["GRIDFILE \t %s " %(grid_file)]
        dock_lines += ["LIGANDFILE \t %s " %(ligand_mae)]
        dock_lines += ["POSES_PER_LIG \t 10 "]
        if precision == 'SP':
            #dock_lines += ["PRECISION \t XP "]
            dock_lines += ["PRECISION \t SP "]
        elif precision == 'XP':
            dock_lines += ["PRECISION \t XP "]
            dock_lines += ["POSTDOCK_XP_DELE \t 0.5 "]
            dock_lines += ["EXPANDED_SAMPLING \t True "]
            dock_lines += ["WRITE_XP_DESC \t False "]
        with open('dock.in', "w") as f:
            f.write('\n'.join(dock_lines))
        os.system("$SCHRODINGER/glide -WAIT dock.in")
        


        ## Split into a receptor mae file and one ligand mae for each pose
        os.system('$SCHRODINGER/run split_structure.py -m ligand -many_files dock_pv.maegz split.mae')
  

        ## Convert the receptor mae into pdb
        # This pdb is one of the final outputs from docking
        
        os.system('$SCHRODINGER/utilities/structconvert split_receptor1.mae ' + output_receptor_pdb)
                  
        ## Convert the ligand maes into mols
        docked_ligand_maes = glob.glob('./split_ligand*.mae')
        #print docked_ligand_maes
        for docked_ligand_mae in docked_ligand_maes:
            docked_ligand_mol = docked_ligand_mae.replace('.mae','.mol') 
            os.system('$SCHRODINGER/utilities/structconvert %s %s' %(docked_ligand_mae, docked_ligand_mol))
                    
        # Copy the top-ranked ligand mol to be one of the final outputs from this step
        os.system('cp split_ligand1.mol ' + output_lig_mol)
        
        return True


if ("__main__") == (__name__):
    import os
    import logging
    import shutil
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-l", "--ligsciprepdir", metavar="PATH", help = "PATH where we can find the scientific ligand prep output")
    parser.add_argument("-p", "--protsciprepdir", metavar="PATH", help = "PATH where we can find the scientific protein prep output")
    parser.add_argument("-o", "--outdir", metavar = "PATH", help = "PATH where we will put the docking output")
    # Leave option for custom logging config here
    logger = logging.getLogger()
    logging.basicConfig( format  = '%(asctime)s: %(message)s', datefmt = '%m/%d/%y %I:%M:%S', filename = 'final.log', filemode = 'w', level   = logging.INFO )
    opt = parser.parse_args()
    lig_sci_prep_dir = opt.ligsciprepdir
    prot_sci_prep_dir = opt.protsciprepdir
    dock_dir = opt.outdir
    #running under this dir
    abs_running_dir = os.getcwd()
    log_file_path = os.path.join(abs_running_dir, 'final.log')
    log_file_dest = os.path.join(os.path.abspath(dock_dir), 'final.log')
    docker = schrodinger_glide()
    docker.run_dock(prot_sci_prep_dir,
                    lig_sci_prep_dir,
                    dock_dir)
    #move the final log file to the result dir
    shutil.move(log_file_path, log_file_dest)
