
peptidee = 'NC([*:1])C(NC([*:2])C(NCC(O)=O)=O)=O'
peptide_molecule = 'NC([*:1])C(NC([*:2])C(NCC(O)=O))=O)='
if __name__ == '__main__':

    from peptide_builder import PeptideBuilder

    peptide = PeptideBuilder(2)

    print (peptide)