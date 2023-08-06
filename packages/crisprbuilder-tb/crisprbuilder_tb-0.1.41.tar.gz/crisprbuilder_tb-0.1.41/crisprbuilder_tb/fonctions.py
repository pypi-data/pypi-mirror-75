"""
This module contains the different constants and functions that support the
__main__.py module.
"""
import subprocess  # allows to connect to input/output/error pipes of processes
from csv import reader
from os import remove, rename, path
from pathlib import PurePath
from Bio import Entrez  # provides code to access NCBI over the Web
from xlrd import open_workbook
from xmltodict import parse  # interprets XML files like JSON files

import crisprbuilder_tb

# =========
# CONSTANTS
# =========

# We define different useful paths
#P_CSV = str(PurePath(crisprbuilder_tb.__path__[0], 'data', 'lineage.csv'))
P_CSV = path.join(path.dirname(__file__), 'data', 'lineage.csv')
#P_CSV_TMP = str(PurePath(crisprbuilder_tb.__path__[0], 'data', 'temp.csv'))
P_CSV_TMP = path.join(path.dirname(__file__), 'data', 'temp.csv')
#P_FASTA = str(PurePath(crisprbuilder_tb.__path__[0], 'tmp', 'snp.fasta'))
P_FASTA = path.join(path.dirname(__file__), 'tmp', 'snp.fasta')

# We define the value of half the length of the reads we will work on.
DEMI_LONGUEUR = 20


# =========
# FUNCTIONS
# =========

def to_brynildsrud():
    """
    This function parses information from 'data/Brynildsrud_Dataset_S1.xls'
    into a dictionary called brynildsrud.

    Returns:
        brynildsrud (dict): which structure is
        {
            a_sra:
                {
                    'Source': ...,
                    'Author': ...,
                    'study accession number': ...,
                    'location': ...,
                    'date': ...
                },
            ...
        }
    """
    brynildsrud = {}
    source, author, study, location, date = '', '', '', '', ''
    #p_brynildsrud = str(PurePath(crisprbuilder_tb.__path__[0], 'data',
                                 #'Brynildsrud_Dataset_S1.xls'))
    p_brynildsrud = path.join(path.dirname(__file__), 'data',
                                 'Brynildsrud_Dataset_S1.xls')
    wwb = open_workbook(p_brynildsrud)
    wws = wwb.sheet_by_index(0)

    for row in range(1, wws.nrows):
        srr = wws.cell_value(row, 4)

        if len(srr) > 1:

            brynildsrud[srr] = {}
            source = wws.cell_value(row, 5).replace(',', '')

            if source == 'This study':
                author = 'Brynildsrud et al.'

            source = source.replace('This study', 'Global expansion of '
                                    'Mycobacterium tuberculosis lineage 4 '
                                    'shaped by colonial migration and local '
                                    'adaptation')

            if len(wws.cell_value(row, 3)) > 1:
                study = wws.cell_value(row, 3)

            if len(wws.cell_value(row, 6)) > 1:
                location = wws.cell_value(row, 6)

            if wws.cell_value(row, 0).count('_') == 2:
                dat = wws.cell_value(row, 0).split('_')[-1]
                une_date = True
                for elt in dat:
                    if elt not in '0123456789':
                        une_date = False
                if une_date:
                    date = dat

        brynildsrud[srr] = {
            'Source': source,
            'Author': author,
            'study accession number': study,
            'location': location,
            'date': date
        }
    return brynildsrud


def to_h37rv():
    """
    This function creates a string called h containing the genome sequence of
    the H37RV strain without headers, extracted from 'data/NC_000962.3.txt'

    Returns:
        p_nc_reader (str): genome sequence in a single line and without the
        headers
    """
    #p_nc = str(PurePath(crisprbuilder_tb.__path__[0], 'data',
    # 'NC_000962.3.txt'))
    p_nc = path.join(path.dirname(__file__), 'data', 'NC_000962.3.txt')
    with open(p_nc, 'r') as file:
        p_nc_reader = file.read()
    return p_nc_reader


# We create a string called H37RV containing the genome sequence of the
# strain H37Rv.
H37RV = to_h37rv()


def to_reads(db_origine):
    """
    This function creates a dictionary called lignee_renvoyee containing 2
    reads per lineage and their specific position, extracted from xlsx_lignee.

    Args:
        db_origine(str): name of the dataset origin representing a specific
                         lineage

    Returns:
        lignee_renvoyee (dict): with the following structure
        {
            (
                position_number:
                    (a_read, a_read, lineage_number),
                ...
            )
        }

    Note:
        - we read the 1st sheet of xlsx_lignee.
        - we browse the sheet from the 1st row containing data except for
          headers. For each row, if the 'position' cell is not empty :
          > from the 'lineage' column we keep only the lineage number without
            any * and assign it to 'lignee',
          > from the 'position' column we decrease the position number by 1,
          > from the 'Allele change on strain +' column we extract the 1st
            character (A, T, G or C) and assign it to 'source', we extract the
            3rd character (A, T, G or C) and assign it to 'cible',
          > we create a substring seq1 from H37RV
          > from seq1 we switch the character on position 'longueur' from
            'source' to 'cible', and create the substring seq2,
          > we create the tuple (seq1, seq2, lignee)
    """
    lignee_renvoyee = {}

    with open(P_CSV, 'r') as file:
        csv_reader = reader(file, delimiter=',', quotechar='"')
        next(csv_reader)

        for row in csv_reader:
            if row[16] == db_origine and row[1] != '':
                lignee = row[0].strip()
                pos0 = int(row[1].strip())
                pos = pos0 - 1
                source = row[3].strip()[0]
                cible = row[3].strip()[2]
                assert H37RV[pos] == source
                seq1 = H37RV[pos - DEMI_LONGUEUR:pos + DEMI_LONGUEUR + 1]
                seq2 = seq1[:DEMI_LONGUEUR] + cible + seq1[DEMI_LONGUEUR + 1:]
                lignee_renvoyee[pos] = (seq1, seq2, lignee)

    print("We have selected specific reads to compare with different lineages")
    return lignee_renvoyee


def get_info(srr):
    """
    This function extracts data from the NCBI website regarding a specific SRA to
    put them into a dictionary called dico0.

    Args:
        srr (str): reference of a specific SRR

    Returns:
        dico0 (dict):

    Note:
        - if the dico 'platform' is 'ILLUMINA' and the dico 'LIBRAIRY_LAYOUT' is
          'PAIRED', then we assign 'SAMPLE_ATTRIBUTE' to a temporary list called
          'attributes', which we'll use to assign values to dico0. We browse the
          list 'attributes' to define dico0['location'], dico0['date'],
          dico0['sra'], dico0['center'], dico0['strain'],
        - if dico['SAMPLE_ATTRIBUTE'] is empty, then dico0 stays empty,
        - we respectively assign dico[...]['TAXON_ID'], dico[...][
          'SCIENTIFIC_NAME'], dico[...]['@alias'], dico[...]['@center_name']
          to dico0['taxid'], dico0['name'], dico0['study'], dico0['cemter'],
        - we assign dico[...]['#text'] to dico0['bioproject'], separating the
          cases when dico[...]['EXTERNAL_ID'] is a string or a list.
    """
    Entrez.email = "christophe.guyeux@univ-fcomte.fr"
    ret = Entrez.efetch(db="sra", id=srr, retmode="xml")
    dico = parse(ret.read())

    dico0 = {}
    location, date, sra, center, strain = '', '', '', '', ''

    if 'ILLUMINA' in dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
            'EXPERIMENT'].get('PLATFORM') and 'PAIRED' in dico[
                'EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                    'EXPERIMENT']['DESIGN']['LIBRARY_DESCRIPTOR'].get(
                        'LIBRARY_LAYOUT'):

        try:
            attributes = dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                                'SAMPLE']['SAMPLE_ATTRIBUTES'].get(
                                    'SAMPLE_ATTRIBUTE')
        except KeyError:
            return {}

        for k in attributes:
            if k.get('TAG') == 'geographic location (country and/or sea)':
                location = k.get('VALUE')
            elif k.get('TAG') == 'collection date':
                date = k.get('VALUE')
            elif k.get('TAG') == 'SRA accession':
                sra = k.get('VALUE')
            elif k.get('TAG') == 'Strain':
                strain = k.get('VALUE')

        center = dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
            'EXPERIMENT'].get('@center_name')

        if isinstance(
                dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['STUDY'][
                    'IDENTIFIERS'].get('EXTERNAL_ID'), list):
            bioproject = dico['EXPERIMENT_PACKAGE_SET'][
                'EXPERIMENT_PACKAGE']['STUDY']['IDENTIFIERS']['EXTERNAL_ID'][0]\
                .get('#text', '')
        else:
            bioproject = dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                'STUDY']['IDENTIFIERS']['EXTERNAL_ID'].get('#text', '')

        dico0 = {
            'location': location,
            'date': date,
            'SRA': sra,
            'center': center,
            'strain': strain,
            'taxid': dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                'SAMPLE']['SAMPLE_NAME'].get('TAXON_ID', ''),
            'name': dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                'SAMPLE']['SAMPLE_NAME'].get('SCIENTIFIC_NAME', ''),
            'study': dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                'STUDY'].get('@alias', ''),
            'bioproject': bioproject
        }
    return dico0


def change(nitro_base):
    """
    This function transforms a nitrogenous base into its corresponding
    nitrogenous base. If the input is different than A, T, C, G, then it
    returns the input value.

    Args:
        nitro_base (str): initial nitrogenous base A, T, G, C

    Returns:
        corresponding_base (str): corresponding nitrogenous base
    """
    if nitro_base == 'A':
        corresponding_base = 'T'
    elif nitro_base == 'T':
        corresponding_base = 'A'
    elif nitro_base == 'C':
        corresponding_base = 'G'
    elif nitro_base == 'G':
        corresponding_base = 'C'
    else:
        corresponding_base = nitro_base
    return corresponding_base


def to_spol_sit():
    """
    This function creates a dictionary called spol_sit associating spoligotypes
    with their corresponding SIT (Spoligo International Type) in accordance with
     the file 'data/1_3882_SORTED.xls'.

    Returns:
        spol_sit (dict): with the following structure
        {
            a_spoligotype: a_SIT,
            ...
        }

    Note:
        - we extract data from 'data/1_3882_SORTED.xls' into a sheet called ws,
          where we set column 1 with index 0,
        - we assign the successive elements of the 'Spoligotype Binary'
          column from ws as keys and the successive elements of the 'SIT'
          column from ws as values to the dictionary spol_sit (after
          replacing 'n' into a black square and 'o' into a white square).
    """
    #p_sorted = str(PurePath(crisprbuilder_tb.__path__[0], 'data',
                            #'1_3882_SORTED.xls'))
    p_sorted = path.join(path.dirname(__file__), 'data',
                            '1_3882_SORTED.xls')
    wwb = open_workbook(p_sorted)
    wws = wwb.sheet_by_index(0)
    spol_sit = {}

    for row in range(1, wws.nrows):
        spol, sit = wws.cell_value(row, 2).replace('n', '\u25A0').\
                        replace('o', '\u25A1'), wws.cell_value(row, 8)
        spol_sit[spol] = sit

    return spol_sit


def add_spoligo_dico(type_sit, dico_afr, item, spol_sit):
    """
    When there's no 'SIT' reference for a SRA (represented by parameter item)
    in dico_afr, or if this reference is undefined, we check in spol_sit a
    corresponding spoligotype and update dico_afr with this spoligotype.

    Args:
        type_sit (str): either 'SIT' or 'SIT_silico'
        dico_afr (dict): dictionary used to update dico_africanum.pkl
        item (str): a specific SRA
        spol_sit (dict): dictionary containing spoligotypes and their
        corresponding sits

    Returns:
        (None)

    Note:
         We take a spoligotype from dico_afr[item]['spoligo'] and if this
         spoligotype is in spol_sit, then we update dico_afr with the 'SIT'
         reference. If this spoligotype is not in spol_sit, then we update
         dico_afr with 'X' as a 'SIT' reference.
    """
    if type_sit == 'SIT':
        type_spoligo = 'spoligo'
    else:
        type_spoligo = 'spoligo_vitro'

    spol = dico_afr[item].get(type_spoligo)

    if spol in spol_sit:
        dico_afr[item][type_sit] = spol_sit.get(spol)
    else:
        dico_afr[item][type_sit] = 'X'

    print(f"We're adding the {type_sit}: {dico_afr[item][type_sit]} to the "
          f"database")


def to_formatted_results(seq, repitem, nb_8_12):
    """
    This function compares a nucleotide query sequence against a nucleotide
    sequence database and returns a formatted result.

    Args:
        seq(str): a genome sequence
        repitem(str): REP/sequences/SRA/SRA path to the blast database
        nb_8_12(str): "8" or "12"

    Returns:
        (str): a formatted result of a sequence blast
    """
    with open(P_FASTA, 'w') as file:
        file.write('>\n' + seq)
    result = subprocess.run(["blastn", "-num_threads", nb_8_12, "-query",
                             P_FASTA, "-evalue", "1e-5", "-task", "blastn",
                             "-db", repitem, "-outfmt", "10 sseq"],
                            stdout=subprocess.PIPE)

    return result.stdout.decode('utf8').splitlines()


def to_nb_seq(seq, chaine, debut_prefixe, fin_prefixe, debut_suffixe,
              fin_suffixe):
    """
    This function returns a length.

    Args:
        seq(str): sequence of nucleotides
        chaine(str):
        debut_prefixe(int): beginning of the 1st section in the sequence seq
        fin_prefixe(int): end of the 1st section in the sequence seq
        debut_suffixe(int): beginning of the 2nd section in the sequence seq
        fin_suffixe(int): end of the 2nd section in the sequence seq

    Returns:
        nb_seq (int):
    """
    return len([u for u in chaine if seq[fin_prefixe:fin_suffixe] in u]) + \
           len([u for u in chaine if seq[debut_prefixe:debut_suffixe] in u])


def condition_spol_vitro(espaceur1, espaceur2, spoligo_vitro, nb_max, matches,
                         item, dico_afr):
    """
    Fills-in the spoligo_vitro components in dico_afr

    Args:
        espaceur1(str): name of the 1st spacer
        espaceur2(str): name of the 2nd spacer
        spoligo_vitro(str): name of the spoligo_vitro to update in dico_afr
        nb_max(int):
        matches(str):
        item(str):
        dico_afr(dict):

    Returns:
        (None)
    """
    for k in range(1, nb_max + 1):
        if min([matches.count(espaceur1 + str(k) + ','),
                matches.count(espaceur2 + str(k) + ',')]) / \
                dico_afr[item].get('couverture') > 0.05:
            dico_afr[item][spoligo_vitro] += '\u25A0'
        else:
            dico_afr[item][spoligo_vitro] += '\u25A1'


def concat(p_f1, p_f2, p_shuffled):
    """
    This function concatenates two files given by their paths p_f1 and p_f2
    into a third file that is created and accessible through the path p_shuffled.
    It is used only for Windows systems to replace the linux command lines.

    Args:
        p_f1(str): path for the 1st file
        p_f2(str): path for the 2nd file
        p_shuffled(str): path for the concatenated file

    Returns:
        (None)
    """
    with open(p_f1, 'r') as file_1, open(p_f2, 'r') as file_2, \
            open(p_shuffled, 'w') as f_shuffled:
        lignes_1 = file_1.readlines()
        for elt in lignes_1:
            f_shuffled.write(elt)
        lignes_2 = file_2.readlines()
        for elt in lignes_2:
            f_shuffled.write(elt)


def change_elt_file(path, suffixe, item):
    """
    This function changes "item + '.'" into "item + suffixe + '.'" in a file
    reachable with path.

    Args:
        path(str): path for the file to change
        suffixe(str): _1 or _2
        item(str): a SRA reference

    Returns:
        (None)
    """
    with open(path, 'r') as f_in, \
            open('tp.fasta', 'w') as f_out:
        lignes = f_in.readlines()
        for elt in lignes:
            ligne_finale = elt.replace(item + '.', item + suffixe + '.')
            f_out.write(ligne_finale)
    remove(path)
    rename('tp.fasta', path)
