import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import sys
import os

def main():
    E_probeam = float(sys.argv[1])
    MU_total = int(sys.argv[2])
    nhist = int(sys.argv[3])
    water_slab = float(sys.argv[4])

    mean_energy = 0.99764 * E_probeam + 88.1314 / E_probeam + 0.0651
    energy_spread = -0.0044727 * E_probeam + 1.5104

    if int(E_probeam) > 120:
        energy_spread = - 6.0274e-3 * E_probeam + 6.4705e-2 * \
                        np.sin(6.21102e-2 * E_probeam + 8.4989e0) + 1.6986e0

    E_q = np.array([70, 80, 90, 100, 110, 120, 130, 140, 150, 160,
                   170, 180, 190, 200, 210, 220, 230, 240, 244])

    s_x = np.array([4.472, 4.299, 3.983, 3.845, 3.778, 3.767, 3.78, 3.792, 3.886, 3.989, 3.984,
                   3.852, 3.832, 3.793, 3.815, 3.895, 3.855, 3.669, 3.595])
    f = interpolate.interp1d(E_q, s_x)
    spot_s_x = f(E_probeam)

    s_y = np.array([3.629, 3.504, 3.29, 3.179, 3.072, 2.971, 2.875, 2.852, 2.802, 2.704, 2.669,
                   2.634, 2.626, 2.613, 2.506, 2.468, 2.503, 2.728, 2.845])
    f = interpolate.interp1d(E_q, s_y)
    spot_s_y = f(E_probeam)

    s_xp = np.array([0.0061, 0.0055, 0.0045, 0.0041, 0.0038, 0.0036, 0.0036, 0.0035, 0.0035, 0.0036,
                    0.0031, 0.0027, 0.0027, 0.0027, 0.0031, 0.0035, 0.0031, 0.003, 0.003])
    f = interpolate.interp1d(E_q, s_xp)
    spot_s_xp = f(E_probeam)

    s_yp = np.array([0.0056, 0.005, 0.0039, 0.0037, 0.0033, 0.0031, 0.0029, 0.0031, 0.0029, 0.0026,
                    0.0025, 0.0024, 0.0024, 0.0023, 0.0024, 0.0024, 0.0022, 0.0029, 0.0033])
    f = interpolate.interp1d(E_q, s_yp)
    spot_s_yp = f(E_probeam)

    cov_x = np.array([-0.0167, - 0.0117, - 0.0135, - 0.011, - 0.0082, - 0.0057, - 0.0031, - 0.0015,
                     0.0017, 0.0045, 0.0033, 0.0014, 0.0029, 0.0041, 0.0068, 0.0101, 0.0087, 0.0083, 0.0081])
    f = interpolate.interp1d(E_q, cov_x)
    spot_corr_x = -f(E_probeam)/ (2 * spot_s_xp * spot_s_x)

    cov_y = np.array([-0.0301, - 0.0245, - 0.0242, - 0.0207, - 0.0188, - 0.0168, - 0.0154, - 0.0127, - 0.0122,
                     - 0.0125, - 0.0117, - 0.0113, - 0.0109, - 0.0105, - 0.0105, - 0.0101, - 0.0095, - 0.0052,
                     - 0.0026])
    f = interpolate.interp1d(E_q, cov_y)
    spot_corr_y = -f(E_probeam)/ (2 * spot_s_yp * spot_s_y)

    ppmu = 0.3167 * E_probeam ** 0.5319 - 0.9840

    if not os.path.exists(str(int(E_probeam))+"mev_output"):
        os.mkdir(str(int(E_probeam))+"mev_output")


    with open('beam'+ str(int(E_probeam))+'.txt', 'w') as text_file:
        print("includeFile = DosimeterChemComp.txt", file=text_file)
        print("\n \n", file=text_file)
        
        print("##############################################", file=text_file)
        print("###               TOPAS SETUP              ###", file=text_file)
        print("##############################################", file=text_file)
        print("\n", file=text_file)
        print("i:Ts/ShowHistoryCountAtInterval         = 5000", file=text_file)
        print("i:Ts/NumberOfThreads                    = 0 # 0 for using all cores, -1 for all but one", file=text_file)
        print("b:Ts/DumpParameters                     = \"False\"", file=text_file)
        print("\n \n", file=text_file)

        print("##############################################", file=text_file)
        print("###              WORLD SETUP               ###", file=text_file)
        print("##############################################", file=text_file)
        print("\n", file=text_file)
        print("s:Ge/World/Type            = \"TsBox\"", file=text_file)
        print("s:Ge/World/Material        = \"Air\"  ", file=text_file)
        print("d:Ge/World/HLX             = 50. cm", file=text_file)
        print("d:Ge/World/HLY             = 50. cm", file=text_file)
        print("d:Ge/World/HLZ             = 50. cm", file=text_file)
        print("b:Ge/World/Invisible       = \"True\"", file=text_file)
        print("\n \n", file=text_file)

        print("##############################################", file=text_file)
        print("###              GEOMETRY                  ###", file=text_file)
        print("##############################################", file=text_file)
        print("\n", file=text_file)
        print("s:Ge/Patient/Parent                  = \"World\"", file=text_file)
        print("s:Ge/Patient/Type                    = \"TsBox\"", file=text_file)
        print("s:Ge/Patient/Material                = \"FlexDos\"", file=text_file)
        print("d:Ge/Patient/HLX		     = 25 mm", file=text_file)
        print("d:Ge/Patient/HLY		     = 25 mm", file=text_file)
        print("d:Ge/Patient/HLZ		     = 50 mm", file=text_file)
        print("d:Ge/Patient/TransX       = -0 mm", file=text_file)
        print("d:Ge/Patient/TransY       = -0 mm", file=text_file)
        trans = 50 + water_slab
        print("d:Ge/Patient/TransZ       = -{} mm".format(trans), file=text_file)
        print("i:Ge/Patient/XBins		 = 100", file=text_file)
        print("i:Ge/Patient/YBins		 = 100", file=text_file)
        print("i:Ge/Patient/ZBins		 = 200", file=text_file)
        if water_slab != 0:
            print("s:Ge/water_slab/Parent                  = \"World\"", file=text_file)
            print("s:Ge/water_slab/Type                    = \"TsBox\"", file=text_file)
            print("s:Ge/water_slab/Material                = \"G4_WATER\"", file=text_file)
            print("d:Ge/water_slab/HLX		     = 25 mm", file=text_file)
            print("d:Ge/water_slab/HLY		     = 25 mm", file=text_file)
            print("d:Ge/water_slab/HLZ		     = {} mm".format(water_slab / 2), file=text_file)
            print("d:Ge/water_slab/TransZ       = -{} mm".format(water_slab / 2), file=text_file)

        print("\n \n", file=text_file)
        print("s:Ge/IsocenterMarker/Parent	     = \"World\"", file=text_file)
        print("s:Ge/IsocenterMarker/Type	     = \"TsBox\"", file=text_file)
        print("b:Ge/IsocenterMarker/IsParallel	     = \"True\"", file=text_file)
        print("d:Ge/IsocenterMarker/HLX		     = 0.1 cm", file=text_file)
        print("d:Ge/IsocenterMarker/HLY		     = 0.1 cm", file=text_file)
        print("d:Ge/IsocenterMarker/HLZ		     = 0.1 cm", file=text_file)
        print("s:Ge/IsocenterMarker/Color	= \"Yellow\"", file=text_file)
        print("\n \n", file=text_file)

        print("s:Ge/BeamPosition/Parent             = \"World\"", file=text_file)
        print("s:Ge/DCM_to_IEC/Type                 = \"Group\"", file=text_file)
        print("d:Ge/BeamPosition/TransZ             = 0.0 mm", file=text_file)
        print("\n \n", file=text_file)

        print("##############################################", file=text_file)
        print("###                BEAM                    ###", file=text_file)
        print("##############################################", file=text_file)
        print("\n", file=text_file)
        print("s:So/Field/Type                      = \"Emittance\"", file=text_file)
        print("s:So/Field/Component                 = \"BeamPosition\"", file=text_file)
        print("s:So/Field/BeamParticle              = \"proton\"", file=text_file)
        print("d:So/Field/BeamEnergy                = {} MeV".format(mean_energy), file=text_file)
        print("u:So/Field/BeamEnergySpread          = {} ".format(energy_spread), file=text_file)
        print("s:So/Field/Distribution              = \"BiGaussian\"", file=text_file)
        print("d:So/Field/SigmaX                    = {} mm".format(spot_s_x), file=text_file)
        print("u:So/Field/SigmaXprime               = {} ".format(spot_s_xp), file=text_file)
        print("d:So/Field/SigmaY                    = {} mm".format(spot_s_y), file=text_file)
        print("u:So/Field/SigmaYprime               = {} ".format(spot_s_yp), file=text_file)
        print("u:So/Field/CorrelationX              = {} ".format(spot_corr_x), file=text_file)
        print("u:So/Field/CorrelationY              = {} ".format(spot_corr_y), file=text_file)
        print("i:So/Field/NumberOfHistoriesInRun    = {}".format(nhist), file=text_file)
        print("\n \n", file=text_file)

        print("##############################################", file=text_file)
        print("###            SCORER SETUP                ###", file=text_file)
        print("##############################################", file=text_file)
        print("\n", file=text_file)
        #print("s:Sc/Dose/Quantity                             = \"DoseToWater\"", file=text_file)
        #print("s:Sc/Dose/Component                            = \"Patient\"", file=text_file)
        #print("s:Sc/Dose/IfOutputFileAlreadyExists            = \"Overwrite\"", file=text_file)
        #print("b:Sc/Dose/PreCalculateStoppingPowerRatios      = \"True\"", file=text_file)
        #print("d:Sc/Dose/MinProtonEnergyForStoppingPowerRatio = 0.0 MeV", file=text_file)
        #print("d:Sc/Dose/MaxProtonEnergyForStoppingPowerRatio = 250.0 MeV", file=text_file)
        #print("s:Sc/Dose/OutputFile                           = \"{}mev_output/dose\"".format(int(E_probeam)), file=text_file)
        #print("\n \n", file=text_file)

        #print("s:Sc/Fluence/Quantity                             = \"Fluence\"", file=text_file)
        #print("s:Sc/Fluence/Component                            = \"Patient\"", file=text_file)
        #print("s:Sc/Fluence/IfOutputFileAlreadyExists            = \"Overwrite\"", file=text_file)
        #print("b:Sc/Fluence/PreCalculateStoppingPowerRatios      = \"True\"", file=text_file)
        #print("d:Sc/Fluence/MinProtonEnergyForStoppingPowerRatio = 0.0 MeV", file=text_file)
        #print("d:Sc/Fluence/MaxProtonEnergyForStoppingPowerRatio = 250.0 MeV", file=text_file)
        #print("s:Sc/Fluence/OutputFile                           = \"{}mev_output/fluence\"".format(int(E_probeam)), file=text_file)
        #print("\n \n", file=text_file)

        print("s:Sc/LET_dose/Quantity                             = \"ProtonLET\"", file=text_file)
        print("s:Sc/LET_dose/WeightBy                             = \"Dose\"", file=text_file)
        print("s:Sc/LET_dose/Component                            = \"Patient\"", file=text_file)
        print("s:Sc/LET_dose/IfOutputFileAlreadyExists            = \"Overwrite\"", file=text_file)
        print("s:Sc/LET_dose/OutputFile                           = \"{}mev_output/let_dose"
              ""
              ""
              ""
              ""
              " \"".format(int(E_probeam)), file=text_file)
        print("\n \n", file=text_file)

        print("#Total number of simulated particles is {}".format(nhist), file=text_file)
        print("#Total number of particles scaled down by {}".format(nhist / (ppmu * MU_total * 10**6)), file=text_file)


if __name__ == "__main__":
    main()
