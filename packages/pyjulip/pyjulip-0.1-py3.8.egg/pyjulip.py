import numpy as np
from ase.calculators.calculator import Calculator
from ase.constraints import voigt_6_to_full_3x3_stress, full_3x3_to_voigt_6_stress
from ase.optimize.optimize import Optimizer

from julia.api import Julia
jl = Julia(compiled_modules=False)

from julia import Main
from julia import ASE
from julia import JuLIP

from julia.JuLIP import energy, forces, stress, mat, positions, cell

ASEAtoms = Main.eval("ASEAtoms(a) = ASE.ASEAtoms(a)")
ASECalculator = Main.eval("ASECalculator(c) = ASE.ASECalculator(c)")
convert = Main.eval("julip_at(a) = JuLIP.Atoms(a)")

def pot(potname, fast=False):
    jl.eval("IP = " + potname)
    ASE_IP = JulipCalculator("IP")
    return ASE_IP

def ACE(potname):
    jl.using("ACE")
    jl.eval("D = load_dict(\"" + potname + "\")")
    jl.eval("IP = read_dict(D[\"IP\"])")
    ASE_IP = JulipCalculator("IP")
    return ASE_IP

# def NBodyIPs(potname, fast=False):
#     julia.using("NBodyIPs")
#     julia.eval("IP, info = load_ip(\""+ potname + "\")")
#     if fast:
#         julia.eval("IP = fast(IP)")
#     ASE_IP = JulipCalculator("IP")
#     return ASE_IP

def FinnisSinclair(potname1, potname2):
    jl.eval("IP = JuLIP.Potentials.FinnisSinclair(\"" + potname1 + "\", \"" + potname2 + "\")")
    ASE_IP = JulipCalculator("IP")
    return ASE_IP

def EAM(potname):
    jl.eval("IP = JuLIP.Potentials.EAM(\"" + potname + "\")")
    ASE_IP = JulipCalculator("IP")
    return ASE_IP


class JulipCalculator(Calculator):
    """
    ASE-compatible Calculator that calls JuLIP.jl for forces and energy
    """
    implemented_properties = ['forces', 'energy', 'free_energy', 'stress']
    default_parameters = {}
    name = 'JulipCalculator'

    def __init__(self, julip_calculator):
        Calculator.__init__(self)
        self.julip_calculator = Main.eval(julip_calculator) #julia.eval

    def calculate(self, atoms, properties, system_changes):
        Calculator.calculate(self, atoms, properties, system_changes)
        julia_atoms = ASEAtoms(atoms)
        julia_atoms = convert(julia_atoms)
        self.results = {}
        if 'energy' in properties:
            E = energy(self.julip_calculator, julia_atoms)
            self.results['energy'] = E
            self.results['free_energy'] = E
        if 'forces' in properties:
            self.results['forces'] = np.array(forces(self.julip_calculator, julia_atoms))
        if 'stress' in properties:
            voigt_stress = full_3x3_to_voigt_6_stress(np.array(stress(self.julip_calculator, julia_atoms)))
            self.results['stress'] = voigt_stress


class JulipOptimizer(Optimizer):
    """
    Geometry optimize a structure using JuLIP.jl and Optim.jl
    """

    def __init__(self, atoms, restart=None, logfile='-',
                 trajectory=None, master=None, variable_cell=False,
                 optimizer='JuLIP.Solve.ConjugateGradient'):
        """Parameters:
        atoms: Atoms object
            The Atoms object to relax.
        restart, logfile ,trajector master : as for ase.optimize.optimize.Optimzer
        variable_cell : bool
            If true optimize the cell degresses of freedom as well as the
            atomic positions. Default is False.
        """
        Optimizer.__init__(self, atoms, restart, logfile, trajectory, master)
        self.optimizer = Main.eval(optimizer)
        self.variable_cell = variable_cell

    def run(self, fmax=0.05):
        """
        Run the optimizer to convergence
        """
        julia_atoms = convert(ASEAtoms(self.atoms))
        julia_calc = ASECalculator(self.atoms.get_calculator())
        set_calculator_b(julia_atoms, julia_calc)
        if self.variable_cell:
            variablecell_b(julia_atoms)
        else:
            fixedcell_b(julia_atoms)
        results = minimise_b(julia_atoms, gtol=fmax, verbose=2)

        ase_atoms = ASEAtoms(julia_atoms)
        self.atoms.set_positions(ase_atoms.po.get_positions())
        if self.variable_cell:
            self.atoms.set_cell(ase_atoms.po.get_cell())
        return results
