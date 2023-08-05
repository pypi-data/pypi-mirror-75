import stk
from rdkit.Chem import AllChem
import numpy as np

class block(stk.BuildingBlock):
    def __init__(self,*args,optimize=False):
        stk.BuildingBlock.__init__(self,*args)
        if optimize:self.opt()

    def opt(self):
        mol=self.to_rdkit_mol()
        AllChem.SanitizeMol(mol)
        AllChem.MMFFOptimizeMolecule(mol)
        self._position_matrix=mol.GetConformer().GetPositions().T

class build_framework(stk.ConstructedMolecule):
    def __init__(self, topology_graph,opt=False):
        stk.ConstructedMolecule.__init__(self,topology_graph=topology_graph)
        if opt:
            self.opt(MMFF=True)
    def opt(self,MMFF=False):
        mol=self.to_rdkit_mol()
        #
        if MMFF:
            AllChem.SanitizeMol(mol)
            AllChem.MMFFOptimizeMolecule(mol)
        else:
            AllChem.EmbedMolecule(mol)
        self._position_matrix=mol.GetConformer().GetPositions().T





topo_dict={
    "1+1":stk.cage.OnePlusOne,
    "2+2":stk.cage.TwoPlusTwo,
    "2+3":stk.cage.TwoPlusThree,
    "2+4":stk.cage.TwoPlusFour,
    "3+6":stk.cage.ThreePlusSix,
    "4+4":stk.cage.FourPlusFour,
    "4+6":stk.cage.FourPlusSix,
    "4+6_2":stk.cage.FourPlusSix2,
    "4+8":stk.cage.FourPlusEight,
    "5+10":stk.cage.FivePlusTen,
    "6+8":stk.cage.SixPlusEight,
    "6+9":stk.cage.SixPlusNine,
    "6+12":stk.cage.SixPlusTwelve,
    "8+12":stk.cage.EightPlusTwelve,
    "8+16":stk.cage.EightPlusSixteen,
    "10+20":stk.cage.TenPlusTwenty,
    "12+30":stk.cage.TwelvePlusThirty,
    "20+30":stk.cage.TwentyPlusThirty,
}

# class cage():
#     def __init__(self):


# bb= stk.BuildingBlock('BrCCBr', [stk.BromoFactory()])
# print(bb._position_matrix)


group={# 留下原子bonders  删除原子 deleters
    # [*][O][H] default bonders 1 deleters 2
    "-OH":stk.AlcoholFactory,
    # [*][C](=[O])[H] default bonders 1 deleters 2
    "-CHO":stk.AldehydeFactory,
    # [*][C](=[O])[N]([H])[H] default bonders 1 deleters 3,4,5
    "-CONH2":stk.AmideFactory,
    # [*][B]([O][H])[O][H] default bonders 1 deleters 2,3,4,5
    "-BOHOH":stk.BoronicAcidFactory,
    # [*][Br] default bonders 0 deleters 1
    "-Br":stk.BromoFactory,
    # [*][C](=[O])[O][H] default bonders 1 deleters 3,4
    "-COOH":stk.CarboxylicAcidFactory,
    # [Br][#6]~[#6][Br]  default bonders 1,2 deleters 0,3
    "-CBrCBr-":stk.DibromoFactory,
    # [F][#6]~[#6][F]  default bonders 1,2 deleters 0,3
    "-CFCF-":stk.Difluoro,
    # [H][O][#6]~[#6][O][H]  default bonders 2,3 deleters 0,1,4,5
    "-COHCOH-":stk.DiolFactory,
    # [*][F] default bonders 0 deleters 1
    "-F":stk.FluoroFactory,
    # [*][I] default bonders 0 deleters 1
    "-I":stk.IodoFactory,
    # [*][N]([H])[H] default bonders 1 deleters 2,3
    "-NH2":stk.PrimaryAminoFactory,
    # [N]([H])([H])[#6]~[#6]~[#6R1]
    "-RCCCNH2":stk.RingAmineFactory,
    # [H][N]([#6])[#6] default bonders 1 deleters 0
    ">NH":stk.SecondaryAminoFactory,
    # "custom" smarts='[Br][C]',bonders=(1, ), deleters=(0, )
    "custom":stk.SmartsFunctionalGroupFactory,
    # [*][C]([*])=[C]([H])[H] default bonders 1 deleters 3,4,5
    ">C=CH2":stk.TerminalAlkeneFactory,
    # [*][C]#[C][H]  bonders=1, deleters=2, 3
    "-C#CH":stk.TerminalAlkyneFactory,
    # [*][C](=[O])[S][H]  bonders=1, deleters=3, 4
    "-COSH":stk.ThioacidFactory,
    # [*][S][H] bonders=1, deleters=2
    "-SH":stk.ThiolFactory
}


########################################################



class cage():
    def __init__(self,topo,blocks,opt=False):
        self.frame=build_framework(topo_dict[topo](blocks))
        if opt:
            self.frame.opt(MMFF=True)
    def write(self,file):
        self.frame.write(file)















# bb1 = block('Brc1ccc(Br)cc1',
#                 [stk.BromoFactory()],optimize=True)
# # React the aldehyde functional groups during construction.
# bb2 = block('BrC#CBr',
#                 [stk.BromoFactory()],optimize=True)
#
# # Build a polymer.
# polymer = build_framework(
#     topology_graph=stk.polymer.Linear(
#         building_blocks=(bb1,bb2),
#         repeating_unit='ABBA',
#         num_repeating_units=1,
#     )
# )
# polymer.opt(MMFF=True)
# # You can write the molecule to a file if you want to view it.
# polymer.write('polymer.mol')



