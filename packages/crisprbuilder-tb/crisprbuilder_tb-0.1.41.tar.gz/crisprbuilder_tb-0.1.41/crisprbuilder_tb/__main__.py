"""
This module gathers the main() function of the package crisprbuilder_tb and
the most important function collect_sra().
The user is given the choice of
"""
import subprocess  # allows to connect to input/output/error pipes of processes
from argparse import ArgumentParser
from csv import reader, writer, QUOTE_MINIMAL
from os import remove, listdir, rename, system, name, path
from pathlib import Path  # creates path
from pathlib import PurePath
from shutil import rmtree, move

import crisprbuilder_tb
import crisprbuilder_tb.fonctions as fonctions
import crisprbuilder_tb.bdd as bdd


# =========
# CONSTANTS
# =========

# We define different useful paths
#P_REP = str(PurePath(crisprbuilder_tb.__path__[0], 'REP'))
P_REP = path.join(path.dirname(__file__), 'REP')
#P_SEQUENCES = str(PurePath(crisprbuilder_tb.__path__[0], 'REP', 'sequences'))
P_SEQUENCES = path.join(path.dirname(__file__), 'REP', 'sequences')
#P_TXT_POSIX = crisprbuilder_tb.__path__[0] + '/tmp/nb.txt'
P_TXT_POSIX = path.join(path.dirname(__file__), 'tmp', 'nb.txt')
P_TXT_WIN = 'C:\\Windows\\Temp\\nb.txt'

TAILLE_GEN = len(fonctions.H37RV)


# =========
# FUNCTIONS
# =========

def collect_sra(item):
    """
    When the user specifies a SRA reference called {item}, collect_sra(item)
    provides the genome information dictionary by filling in dico_afr[item] and
    printing its elements.

    Args:
        item(str): a SRA reference

    Returns:
        (None)
    """
    # We initialize the genome information dictionary dico_afr.
    dico_afr = {}

    # We create a tmp folder
    #Path.cwd().joinpath(crisprbuilder_tb.__path__[0], 'tmp').mkdir(
    # exist_ok=True,
                                                         #parents=True)

    # ==== CHECKING IF THE SRA IS ALREADY IN THE DATABASE ===================

    # If {item} is not in 'REP/sequences', we create a directory called
    # 'REP/sequences/{item}'
    if item not in listdir(P_SEQUENCES):
        #Path.cwd().joinpath(crisprbuilder_tb.__path__[0], 'REP', 'sequences',
                            #item).mkdir(exist_ok=True, parents=True)
        Path(path.dirname(__file__), 'REP', 'sequences',
                   item).mkdir(exist_ok=True, parents=True)

        #Path.cwd().joinpath(crisprbuilder_tb.__path__[0], 'REP', 'sequences',
                            #item, item).mkdir(exist_ok=True, parents=True)
        Path(path.dirname(__file__), 'REP', 'sequences',
             item, item).mkdir(exist_ok=True, parents=True)
        print(f"We're creating a directory {item}.")

    # We create paths to 'REP/sequences/{item}' and 'REP/sequences/{item}/{item}'
    #rep = str(PurePath(crisprbuilder_tb.__path__[0], 'REP', 'sequences', item))
    rep = path.join(path.dirname(__file__), 'REP', 'sequences', item)
    #repitem = str(PurePath(crisprbuilder_tb.__path__[0], 'REP', 'sequences',
                           #item, item))
    repitem = path.join(path.dirname(__file__), 'REP', 'sequences', item, item)

    # If {item} is not in dico_afr, we add it to dico_afr
    if item not in dico_afr:
        print(f"We're adding {item} to the database.")
        dico_afr[item] = {}

    # ==== DOWNLOADING FASTA FILES FOR THE SRA ===========================

    # If the REP/sequences/{item} directory contains no file in fasta format,
    # we download directly from NCBI into REP the fasta files regarding this SRA.
    # Then we tranfer these files to REP/sequences/{item}.
    if len([u for u in listdir(rep) if 'fasta' in u]) == 0:
        print("We're downloading the files in fasta format")

        #try:
        completed = subprocess.run(['parallel-fastq-dump', '-t', '8',
                                        '--split-files', '--fasta', '-O', P_REP,
                                        '-s', item])
            #completed.check_returncode()
            # if the download worked
        if completed.returncode == 0:
            print("fasta files successfully downloaded.")
            for k in listdir(P_REP):
                if k.endswith('.fasta'):
                    #p_item_k = str(PurePath(crisprbuilder_tb.__path__[0], 'REP',
                                            #'sequences', item, k))
                    p_item_k = path.join(path.dirname(__file__),'REP',
                                         'sequences', item, k)
                    #p_k = str(PurePath(crisprbuilder_tb.__path__[0], 'REP', k))
                    p_k = path.join(path.dirname(__file__), 'REP', k)
                    try:
                        move(p_k, p_item_k)
                    except FileNotFoundError:
                        print("We can't transfer the fasta files in the proper "
                              "repository.")
        #except subprocess.CalledProcessError:
        else:
            # if the download didn't work, we delete the SRA from dico_afr
            #else:
            #del dico_afr[item]
            print("Failed to download fasta files.")

    # If {item}_1.fasta or {item}_2.fasta is not in the REP/sequences/{item}
    # directory, we delete {item} from dico_afr and remove the
    # REP/sequences/{item} directory.
    if (item + '_1.fasta' not in listdir(rep) or
            item + '_2.fasta' not in listdir(rep)):
        #del dico_afr[item]
        rmtree(rep)
        print("The fasta files don't have the proper format. The operation "
              "wasn't successful.")

    # If {item}_shuffled.fasta is not in the REP/sequences/{item} directory,
    # we change "item + '.'" into "item + '_1.'" or "item + '_2.'" in the files
    # REP/sequences/{item}/{item}_1.fasta and
    # REP/sequences/{item}/{item}_2.fasta. Then we concatenate those files
    # into a new file called REP/sequences/{item}/{item}_shuffled.fasta.
    #p_shuffled = str(PurePath(crisprbuilder_tb.__path__[0], 'REP', 'sequences',
                              #item, item + '_shuffled.fasta'))
    p_shuffled = path.join(path.dirname(__file__),'REP', 'sequences',
                              item, item + '_shuffled.fasta')
    if item + '_shuffled.fasta' not in listdir(rep):

        print("We're mixing both fasta files, which correspond to the two "
              "splits ends.")

        #p_fasta_1 = str(PurePath(crisprbuilder_tb.__path__[0], 'REP',
                                 #'sequences', item, item + '_1.fasta'))
        p_fasta_1 = path.join(path.dirname(__file__), 'REP',
                                 'sequences', item, item + '_1.fasta')
        #p_fasta_2 = str(PurePath(crisprbuilder_tb.__path__[0], 'REP',
                                 #'sequences', item, item + '_2.fasta'))
        p_fasta_2 = path.join(path.dirname(__file__), 'REP',
                                 'sequences', item, item + '_2.fasta')

        if name == 'posix':
            system("sed -i 's/" + item + './' + item + "_1./g' " + p_fasta_1)
            system("sed -i 's/" + item + './' + item + "_2./g' " + p_fasta_2)
            system("cat " + p_fasta_1 + " " + p_fasta_2 + " > " + p_shuffled)
        else:
            fonctions.change_elt_file(p_fasta_1, '_1', item)
            fonctions.change_elt_file(p_fasta_2, '_2', item)
            fonctions.concat(p_fasta_1, p_fasta_2, p_shuffled)

    # ==== UPDATING NB_READS IN DICO_AFR ================================

    # If there's no nb_reads reference in dico_afr[{item}], we count the number
    # of '>' in REP/sequences/{item}/shuffled.fasta, keep it in tmp/nb.txt
    # and assign it to nb_reads.
    if 'nb_reads' not in dico_afr[item] or dico_afr[item]['nb_reads'] == '':
        if name == 'posix':
            system("cat " + p_shuffled + " | grep '>' | wc -l > " + P_TXT_POSIX)
            nb_reads = eval(open(P_TXT_POSIX).read().split('\n')[0])
        else:
            with open(p_shuffled, 'r') as f_in, open(P_TXT_WIN, 'w') as f_out:
                lignes = f_in.readlines()
                cpt = 0
                for elt in lignes:
                    cpt += elt.count('>')
                    f_out.write(str(cpt))
            nb_reads = eval(open(P_TXT_WIN).read().split('\n')[0])

        dico_afr[item]['nb_reads'] = nb_reads

    # ==== UPDATING LEN_READS IN DICO_AFR ====================================

    # If there's no 'len_reads' reference in dico_afr[{item}], we evaluate
    # it from the REP/sequences/{item}/{item}_shuffled.fasta file
    if 'len_reads' not in dico_afr[item]:
        nb_len = len(''.join(open(p_shuffled).read(10000).split('>')[1].split(
            '\n')[1:]))
        dico_afr[item]['len_reads'] = nb_len

    # ==== UPDATING COVERAGE IN DICO_AFR ======================================

    # If there's no 'couverture' reference in dico_afr[{item}], we evaluate it
    # before assigning the result to dico_afr.
    if 'couverture' not in dico_afr[item] or \
            dico_afr[item].get('couverture') == '':
        dico_afr[item]['couverture'] = round(dico_afr[item].get('nb_reads') *
                                             dico_afr[item].get('len_reads') /
                                             TAILLE_GEN, 2)

    # If {item} in dico_afr has a low coverage, we delete {item} from dico_afr.
    if dico_afr[item].get('couverture') < 50:
        del dico_afr[item]
        print(f"The coverage is too low. {item} is being removed from the "
              "database")
    else:
        # ==== IF THE COWERAGE IS GOOD ENOUGH ================================

        # If {item} in dico_afr has a good coverage, we create in
        # REP/sequences/{item} a database for Blast called {item}
        if item+'.nal' not in listdir(rep) and item+'.nin' not in listdir(rep):
            print("We're creating a database for Blast")
            try:
                completed = subprocess.run(['makeblastdb', '-in', p_shuffled,
                                            '-dbtype', 'nucl', '-title', item,
                                            '-out', repitem], check=True)
                completed.check_returncode()
                # assert completed.returncode == 0
            except subprocess.CalledProcessError:
                print("We can't proceed blasting file.")

        # === UPDATING SOURCE, AUTHOR, ACCESSION NBER, LOCATION IN DICO_AFR ===

        # If there's no 'source' reference in dico_afr[{item}], we browse
        # the list 'Origines'. if {item} is in the 'run accessions' section,
        # we update dico_afr[{item}].
        if 'Source' not in dico_afr[item]:
            for ref in bdd.Origines:
                if item in ref['run accessions']:
                    for elt in ['Source', 'Author', 'study accession number',
                                'location']:
                        dico_afr[item][elt] = ref.get(elt)

        # ==== UPDATING DICO_AFR FROM NCBI ===============================

        # If there's no 'taxid' reference in dico_afr[{item}],we collect data
        # from NCBI to update dico_afr
        if 'taxid' not in dico_afr[item]:
            dicobis = fonctions.get_info(item)
            for elt in dicobis:
                dico_afr[item][elt] = dicobis[elt]

        # ==== UPDATING DICO_AFR WITH THE DATASET BRYNILDSRUD ================

        # We check the presence of {item} in the file
        # 'data/Brynildsrud_Dataset_S1.xls' to update dico_afr.
        brynildsrud = fonctions.to_brynildsrud()
        if item in brynildsrud:
            for elt in brynildsrud[item]:
                dico_afr[item][elt] = brynildsrud[item][elt]
                print(f"{item} is in the database Brynildsrud")
        else:
            print(f"{item} is not in the database Brynildsrud")

        # ==== UPDATING THE SPOLIGOTYPES IN DICO_AFR ========================

        # If 'spoligo' for {item} is not in dico_afr or is undefined,
        # then

        if 'spoligo' not in dico_afr[item] or dico_afr[item]['spoligo'] == '':
            print("The spoligotypes are being blasted")
            dico_afr[item]['spoligo'] = ''
            dico_afr[item]['spoligo_new'] = ''

            #p_spoligo_old = str(PurePath(crisprbuilder_tb.__path__[0], 'data',
                                         #'spoligo_old.fasta'))
            p_spoligo_old = path.join(path.dirname(__file__), 'data',
                                         'spoligo_old.fasta')
            #p_spoligo_new = str(PurePath(crisprbuilder_tb.__path__[0], 'data',
                                         #'spoligo_new.fasta'))
            p_spoligo_new = path.join(path.dirname(__file__), 'data',
                                         'spoligo_new.fasta')
            #p_old_blast = str(PurePath(crisprbuilder_tb.__path__[0], 'tmp', item
                                       #+ "_old.blast"))
            p_old_blast = path.join(path.dirname(__file__), 'tmp', item
                                       + "_old.blast")
            #p_new_blast = str(PurePath(crisprbuilder_tb.__path__[0], 'tmp', item
                                       #+ "_new.blast"))
            p_new_blast = path.join(path.dirname(__file__), 'tmp', item
                                       + "_new.blast")

            try:
                completed = subprocess.run("blastn -num_threads 12 -query " +
                                           p_spoligo_old + " -evalue 1e-6 -task "
                                           "blastn -db " + repitem + " -outfmt "
                                           "'10 qseqid sseqid sstart send qlen "
                                           "length score evalue' -out " +
                                           p_old_blast, shell=True, check=True)
                completed.check_returncode()
                # assert completed.returncode == 0
            except subprocess.CalledProcessError:
                print("We can't proceed blasting file.")

            try:
                completed = subprocess.run("blastn -num_threads 12 -query " +
                                           p_spoligo_new + " -evalue 1e-6 -task "
                                           "blastn -db " + repitem + " -outfmt "
                                           "'10 qseqid sseqid sstart send qlen "
                                           "length score evalue' -out " +
                                           p_new_blast, shell=True, check=True)
                completed.check_returncode()
                # assert completed.returncode == 0
            except subprocess.CalledProcessError:
                print("We can't proceed blasting file.")

            for pos, spol in enumerate(['old', 'new']):
                #p_blast = str(PurePath(crisprbuilder_tb.__path__[0], 'tmp', item
                                       #+ '_' + spol + '.blast'))
                p_blast = path.join(path.dirname(__file__), 'tmp', item
                                       + '_' + spol + '.blast')
                #p_fasta = str(PurePath(crisprbuilder_tb.__path__[0], 'data',
                                       #'spoligo_' + spol + '.fasta'))
                p_fasta = path.join(path.dirname(__file__), 'data',
                                       'spoligo_' + spol + '.fasta')


                with open(p_blast) as file:
                    matches = file.read()
                    nb_max = open(p_fasta).read().count('>')
                    for k in range(1, nb_max + 1):
                        if matches.count('espaceur' + spol.capitalize() + str(k)
                                         + ',') >= 5:
                            dico_afr[item]['spoligo' + ['', '_new'][pos]] \
                                    += '\u25A0'
                        else:
                            dico_afr[item]['spoligo' + ['', '_new'][pos]] \
                                    += '\u25A1'

                dico_afr[item]['spoligo' + ['', '_new'][pos] + '_nb'] = [
                    matches.count('espaceur' + spol.capitalize() + str(k) + ',')
                    for k in range(1, nb_max + 1)]
                try:
                    if item + '_' + spol + '.blast' not in listdir(rep):
                        move(p_blast, rep)
                except FileNotFoundError:
                    print(p_blast, " is already in the SRA directory.")

            print("     " + dico_afr[item]['spoligo'])
            print("     " + str(dico_afr[item]['spoligo_nb']))
            print("     " + dico_afr[item]['spoligo_new'])
            print("     " + str(dico_afr[item]['spoligo_new_nb']))

        # If 'spoligio_vitro' is undefined for {item} in dico_afr, we blast
        # the spoligo_vitro, and update both lineage.csv and dico_afr.
        if 'spoligo_vitro' not in dico_afr[item]:
            print("The spoligo-vitro are being blasted")
            dico_afr[item]['spoligo_vitro'] = ''
            dico_afr[item]['spoligo_vitro_new'] = ''

            #p_spoligo_vitro = str(PurePath(crisprbuilder_tb.__path__[0], 'data',
                                           #'spoligo_vitro.fasta'))
            p_spoligo_vitro = path.join(path.dirname(__file__), 'data',
                                           'spoligo_vitro.fasta')
            #p_spoligo_vitro_new = str(PurePath(crisprbuilder_tb.__path__[0],
                                               #'data',
                                               #'spoligo_vitro_new.fasta'))
            p_spoligo_vitro_new = path.join(path.dirname(__file__), 'data',
                                               'spoligo_vitro_new.fasta')
            #p_vitro_blast = str(PurePath(crisprbuilder_tb.__path__[0], 'tmp',
                                         #item + '_vitro.blast'))
            p_vitro_blast = path.join(path.dirname(__file__), 'tmp',
                                         item + '_vitro.blast')
            #p_vitro_new_blast = str(PurePath(crisprbuilder_tb.__path__[0],
            # 'tmp',
                                             #item + '_vitro_new.blast'))
            p_vitro_new_blast = path.join(path.dirname(__file__), 'tmp',
                                             item + '_vitro_new.blast')

            try:
                completed = subprocess.run("blastn -num_threads 8 -query " +
                                           p_spoligo_vitro + " -evalue 1e-6 "
                                           "-task blastn -db " + repitem +
                                           " -outfmt '10 qseqid sseqid sstart "
                                           "send qlen length score evalue' "
                                           "-out " + p_vitro_blast, shell=True,
                                           check=True)
                completed.check_returncode()
                # assert completed.returncode == 0
            except subprocess.CalledProcessError:
                print("We can't proceed blasting file.")

            try:
                completed = subprocess.run("blastn -num_threads 8 -query " +
                                           p_spoligo_vitro_new + " -evalue 1e-6 "
                                           "-task blastn -db " + repitem + " "
                                           "-outfmt '10 qseqid sseqid sstart "
                                           "send qlen length score evalue' "
                                           "-out " + p_vitro_new_blast,
                                           shell=True, check=True)
                completed.check_returncode()
                # assert completed.returncode == 0
            except subprocess.CalledProcessError:
                print("We can't proceed blasting file.")

            with open(p_vitro_blast) as f_vitro_blast:
                matches = f_vitro_blast.read()
                nb_max_svitro = int(open(p_spoligo_vitro).read().count('>') / 2)

                fonctions.condition_spol_vitro('espaceur_vitroOld',
                                               'espaceur_vitroBOld',
                                               'spoligo_vitro', nb_max_svitro,
                                               matches, item, dico_afr)

            dico_afr[item]['spoligo_vitro_nb'] = [(matches.count(
                'espaceur_vitroOld' + str(k) + ','), matches.count(
                    'espaceur_vitroBOld' + str(k) + ',')) for k in
                                                  range(1, nb_max_svitro + 1)]

            with open(p_vitro_new_blast) as f_vitro_nblast:
                matches = f_vitro_nblast.read()
                nb_max_nsvitro = int(open(p_spoligo_vitro_new).read().count(
                    '>') / 2)

                fonctions.condition_spol_vitro('espaceur_vitro_new',
                                               'espaceur_vitro_newB',
                                               'spoligo_vitro_new',
                                               nb_max_nsvitro, matches,
                                               item, dico_afr)

            dico_afr[item]['spoligo_vitro_new_nb'] = [(matches.count(
                'espaceur_vitro_new' + str(k) + ','), matches.count(
                    'espaceur_vitro_newB' + str(k) + ',')) for k in
                                                      range(1, nb_max_nsvitro +
                                                            1)]

            print("     " + dico_afr[item]['spoligo_vitro'])
            print("     " + dico_afr[item]['spoligo_vitro_new'])

            #p_any_blast = str(PurePath(crisprbuilder_tb.__path__[0], 'tmp', item
                                       #+ '_*.blast'))
            p_any_blast = path.join(path.dirname(__file__), 'tmp', item
                                       + '_*.blast')
            try:
                if item + '_*.blast' not in listdir(rep):
                    move(p_any_blast, rep)
            except FileNotFoundError:
                print(p_any_blast, " is already in the SRA directory.")
            # system('mv /tmp/' + item + '_*.blast ' + rep)

            print("     " + str(dico_afr[item]['spoligo_vitro_nb']))
            print("     " + str(dico_afr[item]['spoligo_vitro_new_nb']))

        # We transform data from 1_3882_SORTED.xls into a dictionary called
        # spol_sit containing spoligotypes with their corresponding SITs.
        spol_sit = fonctions.to_spol_sit()

        # When there's no 'SIT' reference for {item} in dico_afr, or if this
        # reference is undefined, we check in spol_sit a corresponding
        # spoligotype and update dico_afr with this spoligotype.
        if 'SIT' not in dico_afr[item] or dico_afr[item]['SIT'] == '':
            fonctions.add_spoligo_dico('SIT', dico_afr, item, spol_sit)

        # We proceed the same way with the 'SIT_silico' reference as previously
        # with the 'SIT' reference.
        if 'SIT_silico' not in dico_afr[item]:
            fonctions.add_spoligo_dico('SIT_silico', dico_afr, item, spol_sit)

        # ==== TESTING LINEAGE L6+ANIMAL =================================

        # if {item} in dico_afr doesn't have a L6+animal lineage, then
        if 'lineage_L6+animal' not in dico_afr[item]:
            print("We're adding the lineage according to the SNPs L6+animal")
            seq1 = 'ACGTCGATGGTCGCGACCTCCGCGGCATAGTCGAA'
            seq2 = "ACGTCGATGGTCGCGACTTCCGCGGCATAGTCGAA"
            formatted_results = fonctions.to_formatted_results(seq2, repitem,
                                                               "12")
            nb_seq1 = fonctions.to_nb_seq(seq1, formatted_results, 13, 17, 18,
                                          22)
            nb_seq2 = fonctions.to_nb_seq(seq2, formatted_results, 13, 17, 18,
                                          22)

            if nb_seq1 > nb_seq2:
                dico_afr[item]['lineage_L6+animal'] = '1'
            elif nb_seq2 > nb_seq1:
                dico_afr[item]['lineage_L6+animal'] = '2'
            else:
                dico_afr[item]['lineage_L6+animal'] = 'X'

        # ==== TESTING PGG LINEAGE ======================================

        # If dico_afr has no information about 'lineage_PGG' regarding {item},
        # we select a read 'seq1' around position 2154724 and define its
        # length by twice 'DEMI-LONGUEUR'. From the read 'seq1', we define a
        # read 'seq2' which is 'seq1' with a nitrogenous base replaced by 'A' at
        # the 'debut_suffixe-1' position, we serialize the read 'seq2' into
        # 'snp.fasta' and blast the obtained file.
        # We repeat this process with another read 'seq1' around position
        # 7585-1. Thenthe lineage is updated into dico_afr[{item}].
        #
        # Examples:
        # In this example, we decide to change in position 323 the nitrogenous
        # base into A. We thus assign 324 to 'pos' and 20 to 'DEMI_LONGUEUR'.
        # h represents H37RV. The 2 different reads are composed of the
        # following strings
        #
        # seq1 = h[304] ... h[344]
        # seq2 = h[304] ... h[322] A  h[324] ... h[344]
        #
        # Both if conditions revolve around A or h[323].
        #
        # nb_seq1 represents the 2 following strings which should be in the
        # formatted results
        #                            h[323] ... h[327]
        #                 h[319] ... h[323]
        #
        # nb_seq2 represents the 2 following strings which should be in the
        # formatted results
        #                               A ... h[327]
        #                    h[319] ... A
        #
        # which is formally interpreted by
        #                                A  debut_suffixe ... fin_suffixe
        # debut_prefixe ... fin_suffixe  A
        if 'lineage_PGG' not in dico_afr[item]:
            lignee = []
            print("We're adding the lineage according to the SNPs PGG")
            pos = 2154724
            seq1 = fonctions.H37RV[pos - fonctions.DEMI_LONGUEUR:pos +
                                   fonctions.DEMI_LONGUEUR + 1]
            seq2 = seq1[:19] + 'A' + seq1[20:]
            formatted_results = fonctions.to_formatted_results(seq2, repitem,
                                                               "12")
            nb_seq1 = fonctions.to_nb_seq(seq1, formatted_results, 15, 19, 20,
                                          24)
            nb_seq2 = fonctions.to_nb_seq(seq2, formatted_results, 15, 19, 20,
                                          24)

            if nb_seq1 > nb_seq2:
                lignee.append(2)
            elif nb_seq2 > nb_seq1:
                lignee.append('1')
            else:
                lignee.append('X')

            pos = 7585-1
            seq1 = fonctions.H37RV[pos - fonctions.DEMI_LONGUEUR:pos +
                                   fonctions.DEMI_LONGUEUR + 1]
            seq2 = seq1[:20] + 'A' + seq1[21:]
            formatted_results = fonctions.to_formatted_results(seq2, repitem,
                                                               "12")
            nb_seq1 = fonctions.to_nb_seq(seq1, formatted_results, 16, 20, 21,
                                          25)
            nb_seq2 = fonctions.to_nb_seq(seq2, formatted_results, 16, 20, 21,
                                          25)

            if nb_seq1 > nb_seq2:
                lignee.append(3)
            elif nb_seq2 > nb_seq1:
                lignee.append('1')
            else:
                lignee.append('X')
            print("The lineage is being updated.")
            dico_afr[item]['lineage_PGG_cp'] = lignee
            if lignee == ['1', '1']:
                dico_afr[item]['lineage_PGG'] = '1'
            elif lignee in [['1', '2'], ['2', '1']]:
                dico_afr[item]['lineage_PGG'] = '2'
            elif lignee in [['2', '3'], ['3', '2']]:
                dico_afr[item]['lineage_PGG'] = '3'
            else:
                dico_afr[item]['lineage_PGG'] = 'X'

            # ==== TESTING LINEAGE COLL =======================================

            # If 'lineage_Coll' is undefined for {item} in dico_afr, we parse a
            # file containing Coll lineage SNPs to compare with chosen reads and
            # update dico_afr.
            if 'lineage_Coll' not in dico_afr[item] or \
                    dico_afr[item]['lineage_Coll'] == '':
                lignee = []
                print("We're adding the lineage according to the SNPs Coll")
                with open(fonctions.P_CSV, 'r') as file:
                    csv_reader = reader(file, delimiter=',', quotechar='"')
                    next(csv_reader)
                    for row in csv_reader:
                        if row[16] == 'Coll' and row[1] != '':
                            pos = int(row[1].strip()) - 1
                            assert fonctions.H37RV[pos] == row[3].strip().split(
                                '/')[0]
                            seq1 = fonctions.H37RV[pos -
                                                   fonctions.DEMI_LONGUEUR:pos +
                                                   fonctions.DEMI_LONGUEUR + 1]

                            if '*' not in row[0].strip():
                                seq2 = seq1[:20] + row[3].strip().split('/')[
                                    1] + seq1[21:]
                            else:
                                seq1 = seq1[:20] + row[3].strip().split('/')[
                                    1] + seq1[21:]
                                seq2 = seq1[:20] + row[3].strip().split('/')[
                                    0] + seq1[21:]

                            formatted_results = fonctions.to_formatted_results(
                                seq2, repitem, "8")

                            nb_seq1 = fonctions.to_nb_seq(seq1,
                                                          formatted_results,
                                                          16, 20, 21, 25)
                            nb_seq2 = fonctions.to_nb_seq(seq2,
                                                          formatted_results,
                                                          16, 20, 21, 25)

                            if nb_seq2 > nb_seq1:
                                lignee.append(row[0].strip().replace(
                                    'lineage', '').replace('*', ''))
                    lignee = sorted(set(lignee))
                    dico_afr[item]['lineage_Coll'] = lignee

        # ==== TESTING PALI LINEAGE =============================

        # If dico_afr has no information about 'lineage_Pali' regarding {item}
        # we extract data from Palittapon_SNPs.xlsx into the dictionary
        # Lignee_Pali containing positions, reads and lineage numbers, we
        # select several reads seq1 and several reads seq2 in a specific
        # position.
        # We open the 'snp.fasta' file and write on it the 2nd read from before,
        # we blast the SRA from 'snp.fasta' in relation to the 'item', we keep
        # only the results that contain selected parts of the reads 'seq1' and
        # 'seq2', and put them in sequences, we assign the length of those
        # sequences to 'nb_seq1' and 'nb_seq2'.
        # We create an empty list called 'lignee'. If 'nb_seq2' is greater than
        # 'nb_seq1', then we add the 3rd read from the initial dictionary to
        # 'lignee', we sort the elements of 'lignee' and add them to
        # dico_afr[item]['lineage...'].
        if 'lineage_Pali' not in dico_afr[item]:
            lignee = []
            lignee_snp = fonctions.to_reads('Pali')
            print("We're adding the lineage according to the SNPs Pali")

            for item2, pos0 in enumerate(lignee_snp):
                seq1, seq2 = lignee_snp[pos0][:2]
                #p_blast = str(PurePath(crisprbuilder_tb.__path__[0], 'tmp',
                                       #'snp_Pali.blast'))
                p_blast = path.join(path.dirname(__file__), 'tmp',
                                       'snp_Pali.blast')
                with open(fonctions.P_FASTA, 'w') as f_fasta:
                    f_fasta.write('>\n' + seq2)
                cmd = "blastn -query " + fonctions.P_FASTA + " -num_threads 12" \
                      " -evalue 1e-5 -task blastn -db " + repitem + \
                      " -outfmt '10 sseq' -out " + p_blast
                system(cmd)
                with open(p_blast) as f_blast:
                    formatted_results = f_blast.read().splitlines()

                nb_seq1 = fonctions.to_nb_seq(seq1, formatted_results, 16, 20,
                                              21, 25)
                nb_seq2 = fonctions.to_nb_seq(seq2, formatted_results, 16, 20,
                                              21, 25)

                if nb_seq2 > nb_seq1:
                    lignee.append(lignee_snp[pos0][2])

            lignee = [u for u in sorted(set(lignee))]

            dico_afr[item]['lineage_Pali'] = lignee

        # ==== TESTING SHITIKOV LINEAGE =================================

        # If dico_afr has no information about 'lineage_Shitikov' regarding the
        # SRA, we extract data from Shitikov_L2_SNPs.xlsx into the dictionary
        # Lignee_Shitikov containing positions, reads and lineage numbers, we
        # select a read in a specific position before blasting it and updating
        # the lineage in dico_afr[SRA].
        if 'lineage_Shitikov' not in dico_afr[item]:
            lignee = []
            lignee_snp = fonctions.to_reads('Shiti')
            print("We're adding the lineage according to the SNPs Shitikov")

            for item2, pos0 in enumerate(lignee_snp):
                seq1, seq2 = lignee_snp[pos0][:2]
                #p_blast = str(PurePath(crisprbuilder_tb.__path__[0], 'tmp',
                                       #'snp_Shitikov.blast'))
                p_blast = path.join(path.dirname(__file__), 'tmp',
                                       'snp_Shitikov.blast')
                with open(fonctions.P_FASTA, 'w') as f_fasta:
                    f_fasta.write('>\n' + seq2)
                cmd = "blastn -query " + fonctions.P_FASTA + " -num_threads 12" \
                      " -evalue 1e-5 -task blastn -db " + repitem + \
                      " -outfmt '10 sseq' -out " + p_blast
                system(cmd)
                with open(p_blast) as f_blast:
                    formatted_results = f_blast.read().splitlines()

                nb_seq1 = fonctions.to_nb_seq(seq1, formatted_results, 16, 20,
                                              21, 25)
                nb_seq2 = fonctions.to_nb_seq(seq2, formatted_results, 16, 20,
                                              21, 25)

                if nb_seq2 > nb_seq1:
                    lignee.append(lignee_snp[pos0][2])

            lignee = [u for u in sorted(set(lignee))]
            dico_afr[item]['lineage_Shitikov'] = lignee

        # ==== TESTING STUCKI LINEAGE ====================================

        # If dico_afr has no information about 'lineage-Stucki' regarding the
        # SRA, we extract data from Stucki_L4-SNPs.xlsx into the dictionary
        # Lignee_Stucki containing positions, reads and lineage numbers, we
        # select a read in a specific position before blasting it and updating
        # the lineage in dico_afr[SRA].
        if 'Lignee_Stucki' not in dico_afr[item]:
            lignee = []
            lignee_snp = fonctions.to_reads('Stucki')
            print("We're adding the lineage according to the SNPs Stucki")

            for item2, pos0 in enumerate(lignee_snp):
                seq1, seq2 = lignee_snp[pos0][:2]
                #p_blast = str(PurePath(crisprbuilder_tb.__path__[0], 'tmp',
                                       #'snp_Stucki.blast'))
                p_blast = path.join(path.dirname(__file__), 'tmp',
                                       'snp_Stucki.blast')
                with open(fonctions.P_FASTA, 'w') as f_fasta:
                    f_fasta.write('>\n' + seq2)
                cmd = "blastn -query " + fonctions.P_FASTA + " -num_threads 12" \
                      " -evalue 1e-5 -task blastn -db " + repitem + \
                      " -outfmt '10 sseq' -out " + p_blast
                system(cmd)
                with open(p_blast) as f_blast:
                    formatted_results = f_blast.read().splitlines()

                nb_seq1 = fonctions.to_nb_seq(seq1, formatted_results, 16, 20,
                                              21, 25)
                nb_seq2 = fonctions.to_nb_seq(seq2, formatted_results, 16, 20,
                                              21, 25)

                if nb_seq2 > nb_seq1:
                    lignee.append(lignee_snp[pos0][2])

            lignee = [u for u in sorted(set(lignee))]

            if '4.10' in lignee:
                lignee.remove('4.10')
            else:
                lignee.append('4.10')

            dico_afr[item]['Lignee_Stucki'] = lignee

    # We check if {item} is in the database Origines, and update the location
    # of {item} in dico_afr[item]
    booleen_origines = False
    for k in bdd.Origines:
        if item in k['run accessions']:
            booleen_origines = True
            if 'location' in k:
                dico_afr[item]['location'] = k.get('location')
    if booleen_origines:
        print(f"{item} is in the database Origines")
    else:
        print(f"{item} is not in the database Origines")

    if item in dico_afr:
        dico_afr[item].setdefault('name', '')

        # If {item} is a metagenome, we delete it from dico_afr and delete the
        # repository in 'REP/sequences'.
        if 'metagenome' in dico_afr[item]['name'] and item in listdir(
                P_SEQUENCES):
            print(f"The item {item} is a metagenome. We delete it from the "
                  "database.")
            del dico_afr[item]
            try:
                rmtree(rep)
            except FileNotFoundError:
                print("The file couldn't be found in the repository.")

    # We display information regarding {item} if dico_afr wasn't deleted.
    if dico_afr:
        print('\n==== SUMMERY ====\n')
        for elt in dico_afr[item]:
            print(f"{elt}: {dico_afr[item][elt]}")

    # We empty the directory tmp by removing the bn.txt file
    if name == 'posix':
        #system('rm -f ' + crisprbuilder_tb.__path__[0] + '/tmp/nb.txt')
        system('rm -f ' + path.join(path.dirname(__file__), 'tmp', 'nb.txt'))
    else:
        remove('C:\\Windows\\Temp\\nb.txt')


# ==============
# MAIN PROCEDURE
# ==============


def main():
    """
    We define the different options for the user to choose (--collect, --list,
    --add, --remove, --change, --print).
    We change the 'lineage.csv' file if requested.
    We print the characteristics of a specific SRA reference or the
    characteristics of a list of SRA references.

    Returns:
        (None)
    """
    # ==== DEFINING THE OPTIONS TO CHOOSE =====================================

    # We ask the user for the option to choose
    mp_cli = ArgumentParser(prog='crisprbuilder_tb',
                            description="Collects and annotates Mycobacterium "
                                        "tuberculosis whole genome sequencing "
                                        "data for CRISPR investigation.")
    mp_cli.add_argument("sra", type=str, help="requires the reference of a SRA, "
                        "the path to a file of SRA references or 0. See "
                        "documentation crisprbuilder_tb.md.")
    mp_cli.add_argument("--collect", action='store_true', help="collects the "
                        "reference of a SRA to get information about this SRA. "
                        "See documentation crisprbuilder_tb.md.")
    mp_cli.add_argument("--list", action='store_true', help="collects the path "
                        "to a file of SRA references to get information about. "
                        "See documentation crisprbuilder_tb.md.")
    mp_cli.add_argument("--add", action='store_true', help="collects data to "
                        "add to the file lineage.csv. Requires 0 as argument. "
                        "See documentation crisprbuilder_tb.md.")
    mp_cli.add_argument("--remove", action='store_true', help="removes data "
                        "from the file lineage.csv. Requires 0 as argument. See "
                        "documentation crisprbuilder_tb.md.")
    mp_cli.add_argument("--change", action='store_true', help="collects data to "
                        "update the file lineage.csv. Requires 0 as argument. "
                        "See documentation crisprbuilder_tb.md.")
    mp_cli.add_argument("--print", action='store_true', help="prints the file "
                        "lineage.csv. Requires 0 as argument. See documentation "
                        "crisprbuilder_tb.md.")
    args = mp_cli.parse_args()

    # item represents the RSA reference
    valeur_option = args.sra

    # ==== WHEN THE SELECTED OPTION IS COLLECT ===============================

    if args.collect:
        collect_sra(valeur_option)

    # ==== WHEN THE SELECTED OPTION IS LIST =====================================

    # We read the content of the file valeur_option, transform it into a list
    # without spaces and \n symbols. We browse the list to apply collect_sra().
    if args.list:
        with open(valeur_option, 'r') as file:
            chaine_sra = file.read()
            liste_sra = chaine_sra.strip().split()
            liste_sra = [elt.replace('\n', '') for elt in liste_sra]
        for item in liste_sra:
            collect_sra(item.strip())

    # ==== WHEN THE SELECTED OPTION IS ADD =====================================

    # We collect data to append the file data/lineage.csv.
    if args.add:
        reponse = input("You're about to add a new content to the file "
                        "lineage.csv. Do you wish to proceed ? (y/n)")
        if reponse == 'y':
            chaine_csv = input("Please fill in the various fields. If you don't "
                               "know the value of a specific field, press enter."
                               "\nLineage ?\n").strip()
            chaine_csv += ',' + input("Position ?\n").strip()
            chaine_csv += ',' + input("Gene coord. ?\n").strip()
            chaine_csv += ',' + input("Allele change ?\n").strip()
            chaine_csv += ',' + input("Codon number ?\n").strip()
            chaine_csv += ',' + input("Codon change ?\n").strip()
            chaine_csv += ',' + input("Amino acid change ?\n").strip()
            chaine_csv += ',' + input("Locus Id ?\n").strip()
            chaine_csv += ',' + input("Gene name ?\n").strip()
            chaine_csv += ',' + input("Gene type ?\n").strip()
            chaine_csv += ',' + input("Type of mutation ?\n").strip()
            chaine_csv += ',' + input("5' gene ?\n").strip()
            chaine_csv += ',' + input("3' gene ?\n").strip()
            chaine_csv += ',' + input("Strand ?\n").strip()
            chaine_csv += ',' + input("Sublineage surname ?\n").strip()
            chaine_csv += ',' + input("Essential ?\n").strip() + ',,'

            chaine_csv = chaine_csv.strip()
            liste_csv = chaine_csv.split(',')

            with open(fonctions.P_CSV, 'a', newline='') as file:
                csv_writer = writer(file, delimiter=',', quotechar='"',
                                    quoting=QUOTE_MINIMAL)
                csv_writer.writerow(liste_csv)
            print("The line was  added.")
        else:
            print("Your request was cancelled")

    # ==== WHEN THE SELECTED OPTION IS PRINT ==================================

    # We print the file data/lineage.csv
    if args.print:
        print("Here is the content of the file data/lineage.csv:\n")
        with open(fonctions.P_CSV, 'r', newline='') as file:
            csv_reader = reader(file, delimiter=',', quotechar='"')
            for row in csv_reader:
                print(', '.join(row))

    # ==== WHEN THE SELECTED OPTION IS REMOVE =================================

    # We select the line to change, create a new file lineage2.csv to record all
    # the data from lineage.csv except for the selected line. Then we rename
    # lineage2.csv to lineage.csv.
    if args.remove:
        reponse = input("You're about to remove a content from the file "
                        "lineage.csv. Do you wish to proceed ? (y/n)")
        if reponse == 'y':
            ligne_lineage_csv = input("Which lineage would you like to delete "
                                      "?\n")
            ligne_pos_csv = input("Confirm the position in this lineage you "
                                  "would like to delete:\n")
            with open(fonctions.P_CSV, 'r', newline='') as csvin, \
                    open(fonctions.P_CSV_TMP, 'w', newline='') as csvout:
                csv_reader = reader(csvin, delimiter=',', quotechar='"',
                                    quoting=QUOTE_MINIMAL)
                csv_writer = writer(csvout, delimiter=',', quotechar='"',
                                    quoting=QUOTE_MINIMAL)
                for row in csv_reader:
                    if row[0].strip() != ligne_lineage_csv or \
                            row[1].strip() != ligne_pos_csv:
                        csv_writer.writerow(row)
            remove(fonctions.P_CSV)
            rename(fonctions.P_CSV_TMP, fonctions.P_CSV)
            print("The line has been removed.")
        else:
            print("Your request was cancelled.")

    # ==== WHEN THE SELECTED OPTION IS CHANGE =================================

    # We collect data to update the file lineage.csv, select the line to change,
    # create a new file lineage2.csv to record all the data from lineage.csv
    # except for the selected line where we add the collected data. Then we
    # rename lineage2.csv to lineage.csv.
    if args.change:
        reponse = input("You're about to change the content from the file "
                        "lineage.csv. Do you wish to proceed ? (y/n)")
        if reponse == 'y':
            ligne_lineage_csv = input("Which lineage would you like to change "
                                      "?\n")
            ligne_pos_csv = input("Confirm the position in this lineage you "
                                  "would like to make change:\n")
            chaine_csv = input("Please fill in the various fields. If you don't "
                               "know the value of a specific field, press enter."
                               "\nLineage "
                               "?\n").strip()
            chaine_csv += ',' + input("Position ?\n").strip()
            chaine_csv += ',' + input("Gene coord. ?\n").strip()
            chaine_csv += ',' + input("Allele change ?\n").strip()
            chaine_csv += ',' + input("Codon number ?\n").strip()
            chaine_csv += ',' + input("Codon change ?\n").strip()
            chaine_csv += ',' + input("Amino acid change ?\n").strip()
            chaine_csv += ',' + input("Locus Id ?\n").strip()
            chaine_csv += ',' + input("Gene name ?\n").strip()
            chaine_csv += ',' + input("Gene type ?\n").strip()
            chaine_csv += ',' + input("Type of mutation ?\n").strip()
            chaine_csv += ',' + input("5' gene ?\n").strip()
            chaine_csv += ',' + input("3' gene ?\n").strip()
            chaine_csv += ',' + input("Strand ?\n").strip()
            chaine_csv += ',' + input("Sublineage surname ?\n").strip()
            chaine_csv += ',' + input("Essential ?\n").strip() + ',,'
            chaine_csv = chaine_csv.strip()
            liste_csv = chaine_csv.split(',')

            with open(fonctions.P_CSV, 'r', newline='') as csvin, \
                    open(fonctions.P_CSV_TMP, 'w', newline='') as csvout:
                csv_reader = reader(csvin, delimiter=',', quotechar='"',
                                    quoting=QUOTE_MINIMAL)
                csv_writer = writer(csvout, delimiter=',', quotechar='"',
                                    quoting=QUOTE_MINIMAL)
                for row in csv_reader:
                    if row[0].strip() != ligne_lineage_csv or \
                            row[1].strip() != ligne_pos_csv:
                        csv_writer.writerow(row)
                    else:
                        csv_writer.writerow(liste_csv)
            remove(fonctions.P_CSV)
            rename(fonctions.P_CSV_TMP, fonctions.P_CSV)
            print("The line has been changed.")
        else:
            print("Your request was cancelled.")


if __name__ == "__main__":
    main()
