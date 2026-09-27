"""Physical constants. CO2 = component 0, N2 = component 1 throughout.

Critical properties and R match the original 2002 MATLAB code
(../../original/appendix_a_original.m) exactly. Acentric factors are
standard literature values not present in the original (needed for the
Peng-Robinson alpha function; the original's flash routine wasn't
recovered from the appendix, see EQUATIONS_SPEC.md section 3).
"""

R_BAR = 83.1451  # cm^3 bar / (mol K) -- as in the original code

# CO2, N2
TC_K = (304.2, 126.2)       # K, critical temperature
PC_BAR = (72.8, 33.5)       # bar, critical pressure
OMEGA = (0.225, 0.037)      # acentric factor
MOLAR_MASS = (44.01, 28.01)  # g/mol

LATITUDE_DEG = 36.75  # Monterey Bay, CA -- matches original `lat`

G = 9.81  # m/s^2, as used in the original rise-velocity equation

# Reference open-ocean salinity used for seawater property calculations.
# Not stated in the 2002 report; documented assumption (EQUATIONS_SPEC.md
# section 2.2).
REFERENCE_SALINITY_PSU = 35.0
