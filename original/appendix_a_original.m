% This code simulates bubble rise and dissolution of a carbon dioxide and
% nitrogen gas mixture bubble. It requires a user specified bubble diameter,
% concentration and injection depth. It utilizes the SEAWATER algorithms to
% calculate seawater properties and the Peng Robinson equation of state to
% determine gas properties.
%
% Author: Eric Clower
% Stanford University
% August 2002
%
% Transcribed verbatim (line-wrap artifacts from PDF text extraction fixed)
% from Appendix A of "Ocean Sequestration of CO2/N2 Mixtures" (2002),
% 02-thesis.pdf, for the co2-sequestration-revisited project. This is the
% ONLY code the appendix contains -- the appendix does not include source
% for the helper functions it calls (Find_P, Find_T, Find_Rowsea, flashb,
% Find_Rowbub, Calc_Sol, Find_Vissea, Calc_CO2Zb, Find_NewBubDiameter).
% Those were presumably distributed separately (SEAWATER toolbox wrappers
% and a Peng-Robinson flash routine) and are not recoverable from the PDF.
% See ../model/EQUATIONS_SPEC.md for how the Python reimplementation fills
% these gaps.
%
% NOT EXECUTED as part of this project (no MATLAB access) -- kept for
% provenance and as the reference the Python model is checked against.

clear all variable
clear

%Define Constants
R=83.1451;
Tc=[304.2 126.2];
Pc=[72.8 33.5];
deltat = 2;

%Initial Conditions
lat = 36.75;
D = input('What is initial injection depth?(m)');
CO2Z = input('What is initial concentration of CO2?');
N2Z = 1-CO2Z;
bd = input('What is initial bubble diameter?(cm)');
bd = bd/100;

U0 = 0;

%The main program runs until the concentration of CO2 in the bubble has fallen below a
%control concentration or the bubble reaches the ocean surface
z=[CO2Z N2Z];
n=1;
depthnpo = D;
bdnpo = bd;
CO2MassOrig = 0;
CO2MassNew = 0;

while (depthnpo>0 & bdnpo>0)
	time(n) = n * deltat - deltat;
	test = 10;
	%Sets bubble diameter, depth, rise velocity, and concentration and current time,
	%to previously calculated n plus one value
	if(n>1)
		bd(n) = bdnpo;
		Depth(n) = depthnpo;
		CO2Z(n) = znpo(1);
		U(n) = Unpo;
		z = znpo;
		Unpo = U(n);
	end
	if(n==1)
		bd(n) = bd;
		Depth(n) = D;
		CO2Z(n) = CO2Z;
		U(n) = U0;
		Unpo = U(n) + 0.05;
	end

	z2=[1 0];

	%First Determine seawater conditions at current depth
	P = Find_P(Depth(n),lat);
	T = Find_T(Depth(n));
	rowsea(n) = Find_Rowsea(P,T);

	%Determine gas mixture conditions at current depth and composition using Peng-
	%Robinson equation of state
	[x,y,L(n),LiqVol,VapVol,Zv(n),Zl(n)]=flashb(3,z,T,P);
	rowbub(n) = Find_Rowbub(x,y,L(n),Zv(n),Zl(n),T,P);
	xgs = Calc_Sol(P);

	%Numerically solve rise velocity equation
	psi = rowsea(n)/(rowbub(n) + 0.5*rowsea(n));
	gamma = rowbub(n)/rowsea(n);
	vissea = Find_Vissea(T);

	%This loop iteratively solves for the new velocity. It starts with an initial guess
	%of unpo then it calculates the Reynolds number and solves the equation using
	%that Re. It then checks the two Reynolds numbers together
	k=1;
	while(test > 1)

		%Guess New Velocity
		UnpoGuess = Unpo;

		%Determine Reynolds number and drag coefficient using guessed
		%velocity
		ReGuess = (UnpoGuess*bd(n)*rowsea(n))/(vissea/1000);
		Cd = (24/ReGuess)*(1 + 0.173*ReGuess^0.657) + 0.413/(1 + 16300*ReGuess^-1.09);

		%Solve for velocity equation using guessed Drag Coefficient
		a = deltat * ((3/4)*psi*(Cd/bd(n)));
		b = 1;
		c = -U(n) - deltat*((psi*(1-gamma)*9.81));

		p = [a b c];
		r = roots(p);
		len = length(r);
		for(i=1:len)
			if(r(i)>0)
				Unpo = r(i);
			end
		end

		%Find Reynold's Number using calculated velocity
		ReCalc(n) = (Unpo*bd(n)*rowsea(n))/(vissea/1000);

		%Check if Guessed and Calculated Yield Same Reynold #
		test = ReGuess - ReCalc(n);
		k=k+1
	end

	%Determine new depth;
	depthnpo = Depth(n) - Unpo*deltat;

	%Determine Mass Transfer Out of Bubble
	[znpo,massnpo,CO2MassOrig,CO2MassNew(n),MolsLost(n)] = Calc_CO2Zb(rowbub(n),z,CO2Z(n),bd(n),deltat,rowsea(n),xgs,n,CO2MassOrig,Depth(n),T,vissea,ReCalc(n),Unpo);
	MassLost(n) = (CO2MassOrig-CO2MassNew(n));

	%Determine New Bubble Properties and Diameter
	bdnpo = Find_NewBubDiameter(depthnpo,lat,znpo,massnpo);

	%Find Carbon Dioxide Density
	%First perform flash to determine density of CO2 at currrent depth conditions
	[x2,y2,L2(n),LiqVol2,VapVol2,Zv2,Zl2]=flashb(3,z2,T,P);
	%Next calculate density from the flash results
	rowCO2(n) = Find_Rowbub(x2,y2,L2(n),Zv2,Zl2,T,P);

	if(n==1)
		PerCO2Lost(n) = 0;
	else
		PerCO2Lost(n) = ((MassLost(n))/CO2MassOrig) * 100;
	end

	%Increment time step
	n = n+1;
end

output = [time' Depth' bd' rowsea' rowbub' rowCO2' CO2Z' MassLost' PerCO2Lost'];
save output.dat output -ascii;

subplot(3,2,1)
plot(time,Depth)
xlabel('Time(sec)')
ylabel('Depth(m)')
title('Depth of Bubble with Time')
subplot(3,2,3)
plot(Depth,bd)
xlabel('Depth(m)')
ylabel('Bubble Diameter(m)')
title('Bubble Diameter with Depth')
subplot(3,2,2)
plot(Depth,CO2Z)
xlabel('Depth(m)')
ylabel('Fraction CO2')
title('Bubble Carbon Dioxide Content')
subplot(3,2,4)
plot(Depth, rowbub, Depth, rowsea, Depth, rowCO2)
legend('rowbub','rowsea','rowCO2')
title('Densities')
xlabel('Depth(m)')
ylabel('Density (kg/cu m)')
subplot(3,2,5)
plot(Depth,PerCO2Lost)
xlabel('Depth(m)')
ylabel('Percent')
title('Percent CO2 Dissolved');
subplot(3,2,6)
plot(Depth,MassLost)
title('Mass of CO2 Dissolved');
xlabel('Depth(m)')
ylabel('Mass of CO2 Dissolved (kg)');
