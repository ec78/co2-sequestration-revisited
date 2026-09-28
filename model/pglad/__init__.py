"""P-GLAD gas-lift J-tube model (original 2002 report Chapter 3).

Reimplementation of the P-GLAD hydraulic model, independent of MATLAB
syntax (the original appendix didn't include this model's code at all --
only the single-bubble driver in Appendix A survived, per
../EQUATIONS_SPEC.md section 8). See PGLAD_SPEC.md for the governing
equations and what's original vs. modernized vs. reconstructed.
"""
