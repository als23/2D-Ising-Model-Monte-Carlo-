# Xavier Linn
# MSE215, Fall 2017
# LAMMPS Molecualr Dynamics
import re
import numpy as np
import matplotlib.pyplot as plt

# PARTI, Question 1
def plotEnergies():
    # Process the LAMMPS std.out file
    stdOutFile = open("stdoutPd.txt", "r") # Open the file
    lines = stdOutFile.readlines() # Put all lines of the file into a list
    lines = lines[8:] # Remove the first 8 lines, they are part of the header
    lines = lines[:-19] # Remove the last 19 lines, not needed

    # Create arrays to hold desired data
    numberDataPoints = len(lines)
    steps = np.arange(numberDataPoints)
    temp = np.arange(numberDataPoints)
    totalEnergy = np.arange(numberDataPoints)
    potentialEnergy = np.arange(numberDataPoints)
    kineticEnergy = np.arange(numberDataPoints)

    # Store the LAMMPS data
    i = 0 # index, used to set data of data array's
    for line in lines:
        # Order of data in file: Step Temp TotalEnergy PotentialEnergy KineticEnergy
        m = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s*)", line) # Python Regex, parse the input file for desired info
        steps[i] = float(m.group(1))
        temp[i] = float(m.group(2))
        totalEnergy[i] = float(m.group(3))
        potentialEnergy[i] = float(m.group(4))
        kineticEnergy[i] = float(m.group(5))
        i += 1

    steps = np.arange(numberDataPoints, dtype=float)
    steps *= 0.001 # Convert from units of steps to ps
    print(steps)

    # Plot total energy vs. steps
    plt.title("Total Energy (TE) vs. Time (t)")
    plt.xlabel("t [ps]")
    plt.xlim([0.0, 0.10])
    plt.ylabel("TE [eV]")
    plt.ylim([-1875, -1872])
    plt.grid('on')
    plt.plot(steps, totalEnergy)
    plt.savefig("TEvsTimeQ1.pdf")
    plt.close()
    # Plot potential energy vs. steps
    plt.title("Potential Energy (PE) vs. Time (t)")
    plt.xlabel("t [ps]")
    plt.xlim([0.00, 0.10])
    plt.ylabel("PE [eV]")
    plt.grid('on')
    plt.plot(steps, potentialEnergy)
    plt.plot([0.02, 0.02], [-1950, -1890], label="equilibration time")
    plt.legend()
    plt.savefig("PotenVsTimeQ1.pdf")
    plt.close()
    # Plot kinetic energy vs. steps
    plt.title("Kinetic Energy (KE) vs. Time (t)")
    plt.xlabel("t [ps]")
    plt.xlim([0.00, 0.10])
    plt.ylabel("KE [eV]")
    plt.grid('on')
    plt.plot(steps, kineticEnergy)
    plt.plot([0.02, 0.02], [10, 80], label="equilibration time")
    plt.legend()
    plt.savefig("KineticVsTimeQ1.pdf")
    plt.close()

# PARTII, Questions 3 - 5
def thermoPropertiesPd():

    # Question 2
    def velocityDistribution():
        # Process the LAMMPS velocities.dump file
        velocitiesFile = open("velocitiesdumpP2Q1.txt", "r") # Open the file
        lines2 = velocitiesFile.readlines() # Put all lines of the file into a list

        # Create a dynamic list to hold velocity data
        velocities = []

        # Store the LAMMPS data
        for line in lines2:
            # Order of data: id type vx vy vz
            m2 = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s*)", line)
            if (m2 is None): # Ignore if pattern doesn't match
                pass # Do nothing
            else: # Pattern matches, store the data
                velocities.append(float(m2.group(3))) # Take only group 3, the vx

        print("size of velocities: ", len(velocities))

        # Randomly select 10,000 data points from the velocity data to generare a distribution
        upperBound = len(velocities) # Upper bound for indexing into the array
        randomVel = np.arange(100000) # Create an array to hold the sample of 1000 velocities
        for i in range(0, 100000): # TODO: Should only be 100 data points, 10,000 looks better though. Need to remove eq. data?
            randomIndex = np.random.randint(200, upperBound)
            randomVel[i] = velocities[randomIndex]

        # Plot experimental and exact distribution
        bins = [-10,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10]
        plt.hist(randomVel, 16)

        # Calcualte exact distribution
        # Relevant constants
        T = 600 # units of Kelvin
        kB = 8.6173303 * np.power(10.0, -5.0) # units of eV/K
        m = 0.0110284  # units of eVps^2/Angstrom^2
        velocitiesExact = np.arange(-10, 11, dtype=float)
        distn = np.arange(21, dtype=float)
        i = 0
        for vel in velocitiesExact: # vel has units of Angstroms/picosecond
            distn[i] = 110000.0 * np.power((m / (2.0 * np.pi * kB * T)), 1.0/2.0) * np.exp((-1.0 * m * np.power(vel, 2)) / (2.0 * kB * T))
            i += 1
        plt.title("Maxwell Boltzman Distribution")
        plt.xlabel("Velocity ($\AA$ / ps)")
        plt.ylabel("Density")
        plt.plot(velocitiesExact, distn, label='Exact Distribution')
        plt.legend()
        plt.savefig("velocityDistributionQ2.pdf")
        plt.grid('on')
        plt.close()

    # Question 3
    def caclulateTimeCorrelationFxn():
        print("Hello World from Correlation caclulateTimeCorrelationFxn")

        # Process the LAMMPS file with pressure
        pressureDataFile = open("pressureDataQ2.txt", "r") # Open the file
        lines3 = pressureDataFile.readlines() # Put all lines of the file into a list

        # Create a dynamic list to hold pressure data
        pressures = []
        steps = []
        # Store the LAMMPS pressure data into pressures list
        for line in lines3:
            # Order of data: step pressure
            m3 = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)", line)
            if (m3 is None): # Ignore if pattern doesn't match
                pass # Do nothing
            else: # Pattern matches, store the data
                steps.append(int(m3.group(1)))
                pressures.append(float(m3.group(2))) # Take only group 2, the pressure

        # Plot the pressure data including non-equilibrium data
        plt.title("Pressure vs Steps\n(w/ non-eq. data)")
        plt.xlabel("Steps")
        plt.ylabel("Pressure (bars)")
        plt.plot(pressures)
        plt.grid('on')
        plt.savefig("pressureVsStepsNONEQ.pdf")
        plt.close()

        # Plot the pressure data including equilibrium data
        pressures = pressures[1000:] # Remove non-equilibrium data
        steps = steps[1000:]
        plt.title("Pressure vs Steps")
        plt.xlabel("Steps")
        plt.ylabel("Pressure (bars)")
        plt.plot(pressures)
        plt.grid('on')
        plt.savefig("pressureVsSteps.pdf")
        plt.close()

        # Calculate the correlation function
        averagePressure = np.average(pressures) # Calcualte avergae pressure
        correlationFunction = [] # List to hold correlation values
        correlationSteps = np.arange(0, len(pressures))
        for t in range(0, len(pressures)): # For each time dispalcement t..
            terms = []
            for t0 in range(0, len(pressures)): # For each time origin..
                if (t0 + t >= len(pressures)):
                    break;
                terms.append((pressures[t0 + t] - averagePressure) * (pressures[t0] - averagePressure))
            correlationFunction.append(np.average(terms))
        plt.title("Time-Displaced Correlation vs Steps")
        plt.xlabel("Steps")
        plt.ylabel("Correlation")
        plt.plot(correlationFunction)
        plt.grid('on')
        plt.savefig("correlationFunctionPressure.pdf")
        plt.close()

        # Plot the semilog of the correlation function from 0 - 1 ps
        logCorrelationFunction = np.log(correlationFunction[:100])
        plt.title("Semilog of Time-Displaced Correlation C(t) vs. Time (t)")
        plt.xlabel("t [ps]")
        plt.ylabel("log(C(t))")
        correlationTimes = correlationSteps[:100] * 0.01
        plt.plot(correlationTimes, logCorrelationFunction)
        plt.grid('on')
        plt.savefig("semiLogCorrelationFunctionPressure.pdf")
        plt.close()

        # Caculate the correlation time
        # Splice data to consider a regions that looks linear
        logCorrelationFunction = logCorrelationFunction[:200]
        logCorrelationFunction = logCorrelationFunction[25:]
        correlationTimes = correlationTimes[:200]
        correlationTimes = correlationTimes[25:]
        fittingParameters = np.polyfit(correlationTimes, logCorrelationFunction, 1)[0]
        slope = fittingParameters[0]
        intercept = fittingParameters[1]
        print("Slope of the semilog plot: ", slope)
        print("intercept of the semilog plot: ", intercept)
        correlationTime = -1.0 / slope # Currently has units of Steps
        #print("Correlation time (units of steps): ", correlationTime)
        #correlationTime *= 0.001 # Covert from units of Steps to units of ps
        print("Correlation time (units of ps): ", correlationTime)

    # Question 4 and 5
    def calculateEquilibriumLatticeParameter():

        # Question 4
        # Calculate average equilibrium pressures and plot vs volume
        avg_pressures600K = [] # average the pressure over each file
        for i in range(0, 6):
            # Process the LAMMPS files with pressure at each lattice parameter a
            fileName = "data4_9" + str(i) + ".txt"
            pressureDataFile = open(fileName, "r") # Open the file
            lines4 = pressureDataFile.readlines() # Put all lines of the file into a list
            temp = []
            # Store the LAMMPS pressure data into pressures list
            for line in lines4:
                # Order of data: step pressure
                m3 = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)", line)
                if (m3 is None): # Ignore if pattern doesn't match
                    pass # Do nothing
                else: # Pattern matches, store the data
                    temp.append(float(m3.group(2))) # Take only group 2, the pressure
            temp = temp[1000:] # Remove non-equilibrium data
            avg_pressures600K.append(np.average(temp))
        volumes = [np.power(3.90, 3), np.power(3.91, 3), np.power(3.92, 3), np.power(3.93, 3), np.power(3.94, 3), np.power(3.95, 3)]

        # Plot the average equilbirum pressures vs volume
        plt.title("Average Equilibrium Pressure vs Unit Cell Volume")
        plt.xlabel("Volume (Angstrom^3)")
        plt.ylabel("Pressure (bars)")
        plt.grid('on')
        plt.scatter(volumes, avg_pressures600K)
        plt.savefig("pressureVsVolumeQ4.pdf")
        plt.close()

        # Find line of best fit of average pressure vs volume
        fittingParameters = np.polyfit(volumes, avg_pressures600K, 1)
        slope = fittingParameters[0]
        intercept = fittingParameters[1]
        print("slope of LOB for 600K: ", slope)
        print("intercept of LOB for 600K: ", intercept)
        zeroPressureVolumeAt600K = (-1 * intercept) / slope
        print("zeroPressureVolume @ 600K: ", zeroPressureVolumeAt600K)
        zeroPressureLatticeConstantAt600K = np.power(zeroPressureVolumeAt600K, 1.0/3.0)
        print("zeroPressureLatticeConstant @ 600K: ", zeroPressureLatticeConstantAt600K)
        latticeConstantAt600K = zeroPressureLatticeConstantAt600K

        # Plot line of best fit and pressure data
        plt.title("Pressure (P) vs. Unit Cell Volume (V)\nat 600K")
        plt.xlabel("V ($\AA^3$)")
        plt.ylabel("P (bars)")
        plt.grid('on')
        lineOfBestFit = []
        for v in volumes:
            lineOfBestFit.append(slope * v + intercept)
        plt.scatter(volumes, avg_pressures600K)
        plt.plot(volumes, lineOfBestFit, label = 'Line of best fit')
        plt.legend()
        plt.savefig("pressureVsVolumeFITTEDATAQ4.pdf")

        # Calculate isothermal bulk modulus
        bulkModulus = (-1 * zeroPressureVolumeAt600K) * slope
        print("isothermal bulk modulus of Pd @ 600K: ", bulkModulus)

        # Question 5
        # Calculate average equilibrium pressures and plot vs volume for 950K
        avg_pressures950K = [] # average the pressure over each file
        for i in range(0, 6):
            # Process the LAMMPS files with pressure at each lattice parameter a
            fileName = "data5_9" + str(i) + ".txt"
            pressureDataFile = open(fileName, "r") # Open the file
            lines4 = pressureDataFile.readlines() # Put all lines of the file into a list
            temp = []
            # Store the LAMMPS pressure data into pressures list
            for line in lines4:
                # Order of data: step temp pressure
                m3 = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)", line)
                if (m3 is None): # Ignore if pattern doesn't match
                    pass # Do nothing
                else: # Pattern matches, store the data
                    temp.append(float(m3.group(3))) # Take only group 2, the pressure
            temp = temp[1000:] # Remove non-equilibrium data
            avg_pressures950K.append(np.average(temp))

        # Plot the average equilbirum pressures vs volume for 950K
        plt.title("Pressure (P) vs. Unit Cell Volume(V)/nat 950K")
        plt.xlabel("Volume ($\AA^3$)")
        plt.ylabel("Pressure (bars)")
        plt.grid('on')
        plt.scatter(volumes, avg_pressures950K)
        plt.savefig("pressureVsVolumeQ5.pdf")
        plt.close()

        # Find line of best fit of average pressure vs volume for 950K
        fittingParameters = np.polyfit(volumes, avg_pressures950K, 1)
        slope = fittingParameters[0]
        intercept = fittingParameters[1]
        print("slope of LOB for 950K: ", slope)
        print("intercept of LOB for 950K: ", intercept)
        zeroPressureVolumeAt950K = (-1 * intercept) / slope
        print("zeroPressureVolume @ 950K: ", zeroPressureVolumeAt950K)
        zeroPressureLatticeConstantAt950K = np.power(zeroPressureVolumeAt950K, 1.0/3.0)
        print("zeroPressureLatticeConstant @ 950K: ", zeroPressureLatticeConstantAt950K)
        latticeConstantAt950K = zeroPressureLatticeConstantAt950K

        # Calculate isothermal bulk modulus
        bulkModulus = (-1 * zeroPressureVolumeAt600K) * slope
        print("isothermal bulk modulus of Pd @ 950K: ", bulkModulus)

        # Plot line of best fit and pressure data for 950K
        plt.title("Pressure (P) vs. Unit Cell Volume (V)\nat 950K")
        plt.xlabel("V ($\AA^3$)")
        plt.ylabel("P (bars)")
        plt.grid('on')
        lineOfBestFit = []
        for v in volumes:
            lineOfBestFit.append(slope * v + intercept)
        plt.scatter(volumes, avg_pressures950K)
        plt.plot(volumes, lineOfBestFit, label = 'Line of best fit')
        plt.legend()
        plt.savefig("pressureVsVolumeFITTEDATAQ5.pdf")
        plt.close()

        # Calculate the percentage the lattice parameter has increased from 600K to 950K relative to 600K
        percentIncrease = (abs(latticeConstantAt950K - latticeConstantAt600K) / latticeConstantAt600K) * 100
        print("percent increase in lattice param from 600K to 950K: ", percentIncrease)

        # Estimate the value of the thermal expansion coefficient
        temps = [600, 950]
        latticeParameters = [latticeConstantAt600K, latticeConstantAt950K]
        plt.title("Lattice Parameter (a) vs Temperature (T)")
        plt.xlabel("T [K]")
        plt.ylabel("a [$\AA$]")
        plt.grid('on')
        plt.scatter(temps, latticeParameters)
        fittingParameters = np.polyfit(temps, latticeParameters, 1)
        slope = fittingParameters[0]
        intercept = fittingParameters[1]
        print("slope of LOB for expansion coefficient: ", slope)
        print("intercept of LOB for expansion coefficient: ", intercept)
        print("Slope of line from linear fit of a vs T: ", slope)
        intercept = fittingParameters[1]
        # for v in volumes:
        lineOfBestFit = []
        for t in temps:
            lineOfBestFit.append(slope * t + intercept)
        plt.plot(temps, lineOfBestFit)
        plt.savefig("latticeParameterVsTempQ5.pdf")
        plt.close()

        # Calculate thermal expansion coefficient
        thermExpCoefficient = (1 / latticeConstantAt600K) * slope
        print("Thermal expansion coefficient: ", thermExpCoefficient)

    # Run the code for PARTII questions
    velocityDistribution()
    caclulateTimeCorrelationFxn()
    calculateEquilibriumLatticeParameter()

# PARTIII, Questions 6 - 10
def thermoPropertiesPdH():

    # Question 6
    def calculateLatticeConstantAndBulkModulus():

        # Calculate lattice parameter and bulk modulus
        avg_pressures = [] # average the pressure over each file
        for i in range(0, 10):
            # Process the LAMMPS files with pressure at each lattice parameter a
            if (i == 10):
                fileName = "data6_00.txt"
            else:
                fileName = "data6_9" + str(i) + ".txt"
            pressureDataFile = open(fileName, "r") # Open the file
            lines4 = pressureDataFile.readlines() # Put all lines of the file into a list
            temp = []
            # Store the LAMMPS pressure data into pressures list
            for line in lines4:
                # Order of data: step pressure
                m3 = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)", line)
                if (m3 is None): # Ignore if pattern doesn't match
                    pass # Do nothing
                else: # Pattern matches, store the data
                    temp.append(float(m3.group(2))) # Take only group 2, the pressure
            temp = temp[1000:] # Remove non-equilibrium data
            avg_pressures.append(np.average(temp))
        volumes = [np.power(3.90, 3), np.power(3.91, 3), np.power(3.92, 3), np.power(3.93, 3), np.power(3.94, 3), np.power(3.95, 3),
                   np.power(3.96, 3), np.power(3.97, 3), np.power(3.98, 3), np.power(3.99, 3)]

        # Plot the average equilbirum pressures vs volume
        plt.title("Average Equilibrium Pressure vs Unit Cell Volume")
        plt.xlabel("Volume (Angstrom^3)")
        plt.ylabel("Pressure (bars)")
        plt.grid('on')
        plt.scatter(volumes, avg_pressures)
        plt.savefig("pressureVsVolumeQ6.pdf")
        plt.close()

        # Find line of best fit of average pressure vs volume
        fittingParameters = np.polyfit(volumes, avg_pressures, 1)
        slope = fittingParameters[0]
        intercept = fittingParameters[1]
        zeroPressureVolume = (-1 * intercept) / slope
        print("zeroPressureVolume with H atoms @ 950K: ", zeroPressureVolume)
        zeroPressureLatticeConstant = np.power(zeroPressureVolume, 1.0/3.0)
        print("zeroPressureLatticeConstant with H atoms at 950K: ", zeroPressureLatticeConstant)
        latticeConstant = zeroPressureLatticeConstant

        # Calculate isothermal bulk modulus
        bulkModulus = (-1 * zeroPressureVolume) * slope
        print("isothermal bulk modulus of Pd w/ H atoms: ", bulkModulus)

        # Plot line of best fit and pressure data
        plt.title("Pressure (P) vs. Unit Cell Volume (V)\nfor $Pd_{500}H_{10}$")
        plt.xlabel("V [$\AA^3$]")
        plt.ylabel("P [bars]")
        plt.grid('on')
        lineOfBestFit = []
        for v in volumes:
            lineOfBestFit.append(slope * v + intercept)
        plt.scatter(volumes, avg_pressures)
        plt.plot(volumes, lineOfBestFit, label = 'Line of best fit')
        plt.legend()
        plt.savefig("pressureVsVolumeFITTEDATAQ6.pdf")
        plt.close()

        # Calculate isothermal bulk modulus
        bulkModulus = (-1 * zeroPressureVolume) * slope
        print("isothermal bulk modulus: ", bulkModulus)

        # Calculate percent expansion of lattice constant, relative to pure Pd
        # from PARTII lattice constant =  3.9235624467028063
        percentExpansion = (abs(3.9235624467028063 - zeroPressureLatticeConstant) / 3.9235624467028063) * 100
        print("percent expansion: ", percentExpansion)

    # Questions 7, 9
    def problem79():
        print("Hello World! from questions 7 and 9")

        # Process the LAMMPS file with H atoms coordinates
        hydrogenAtomCoordinateDataFile = open("coordinatesHdump.txt", "r") # Open the file
        lines = hydrogenAtomCoordinateDataFile.readlines() # Put all lines of the file into a list

        # Create a dynamic list to hold h atoms coordinate data
        xu = []
        yu = []
        zu = []
        # Store the LAMMPS pressure data into pressures list
        for line in lines:
            # Order of data: id type xu yu zu
            m = re.match("(?:\s*)(504)(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)", line)
            if (m is None): # Ignore if pattern doesn't match
                pass # Do nothing
            else: # Pattern matches, store the data
                xu.append(m.group(3))
                yu.append(m.group(4))
                zu.append(m.group(5))

        # Plot x vs y coordinate of single H-atom
        plt.title("Unwrapped y coordinate (yu) vs. Unwrapped x coordinate (xu)\nof single H-atom in $Pd_{500}H_{10}$")
        plt.xlabel("xu [$\AA$]")
        plt.ylabel("yu [$\AA$]")
        plt.grid('on')
        plt.plot(xu, yu)
        plt.savefig("yVsXHAtomCoordinateQ7.pdf")
        plt.close()

        # Store each hydrogen data to in a list. Each hydrogen data is a list of coordinates for each time step
        atomNumber = [501, 502, 503, 504, 505, 506, 507, 508, 509, 510] # Numbered according to dump file
        hydrogenDatas = []
        for aN in atomNumber: # For each of the hydrogen atoms
            ithHydrogenData = [] # Create a list to hold the ith hydrogens coordintaes for each time step
            for line in lines: # Iterate line by line through the filea and collent the ith Hyrodens data
                    matchStrng = "(?:\s*)(" + str(aN) + ")(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)"
                    m = re.match(matchStrng, line)
                    if (m is None): # Ignore if pattern doesn't match
                        pass # Do nothing
                    else: # Pattern matches, store the data
                        coordinateTuple = (float(m.group(3)), float(m.group(4)), float(m.group(5))) # (x, y, z)
                        ithHydrogenData.append(coordinateTuple)
            hydrogenDatas.append(ithHydrogenData)

        # Caclulate the average MSD for one hydrogen as a test
        hydrogenMSD = [] # Create a list to hold MSD data for each time displacement
        timeDisplacements = np.arange(0, 5000)
        for t in timeDisplacements: # For each time dispalcement t..
            ithHydrogenMSDAtT = [] # list will hold the average MSD for each H atoms at a given time displacement
            for hD in hydrogenDatas: # For each hydrogen calculate the MSD at given time displacement, add to list above, then average
                terms = []
                for t0 in range(0, len(hD)): # Calculate the ith hydrogens data
                    if (t0 + t >= len(hD)):
                        break;
                    rt = hD[t0 + t]
                    r0 = hD[t0]
                    eucldieanDistance = ((rt[0] - r0[0])**2 + (rt[1] - r0[1])**2 + (rt[2] - r0[2])**2)
                    terms.append(eucldieanDistance)
                ithHyrdogenMSD = np.average(terms)
                ithHydrogenMSDAtT.append(ithHyrdogenMSD)
            hydrogenMSD.append(np.average(ithHydrogenMSDAtT))

        # Find line of best fit for MSD data
        fittingParameters = np.polyfit(timeDisplacements, hydrogenMSD, 1)
        slope = fittingParameters[0]
        intercept = fittingParameters[1]
        lineOfBestFit = []
        for t in timeDisplacements:
            lineOfBestFit.append(slope * t + intercept)
        timeDisplacements *= 0.01 # Convert from steps to ps

        # Calculate diffusion coefficient
        diffusionCoefficient = slope / 6.0
        print("slope of LOB from MSD: ", fittingParameters[0])
        print("intercepet of LOB from MSD: ", fittingParameters[1])
        print("intercepet of LOB from MSD: ", fittingParameters[1])
        print("diffusionCoefficient from MSD: ", diffusionCoefficient)

        # Plot MSD data form LAMMPS
        MSDDataFile = open("MSDData.txt", "r") # Open the file
        lines = MSDDataFile.readlines() # Put all lines of the file into a list

        # Create a dynamic list to hold h atoms coordinate data
        msd = []
        step = []
        # Store the LAMMPS msd into msd list
        for line in lines:
            # Order of data: step temp msd
            m = re.match("(?:\s*)(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)", line)
            if (m is None): # Ignore if pattern doesn't match
                pass # Do nothing
            else: # Pattern matches, store the data
                stepVal = float(m.group(1))*0.001
                msdVal = float(m.group(3))
                step.append(stepVal)
                msd.append(msdVal)

        # Plotting
        plt.title("Mean Square Displacement (MSD) vs. Time Displacement (dt)]\nof single H-atom in $Pd_{500}H_{10}$")
        plt.xlabel("dt [ps]")
        plt.ylabel("MSD [$\AA^2$]")
        plt.plot(timeDisplacements, hydrogenMSD, label =  'Calculated MSD')
        plt.plot(step,  msd, label = 'LAMMPS MSD')
        plt.plot(timeDisplacements, lineOfBestFit, label = 'Line of best fit')
        plt.legend(loc = 'lower right')
        plt.savefig("MSDVsTimeDisplacement.pdf")
        plt.close()

    # Question 10
    def velocityAutoCorrelationFxn():
        print("Hello World from velocityAutoCorrelationFxn!")

        # TODO: Store LAMMPS velocitiy dump file data

        # Process the LAMMPS velocities.dump file
        velocitiesFile = open("velocitiesHQ10dump2.txt", "r") # Open the file
        lines = velocitiesFile.readlines() # Put all lines of the file into a list

        # Store the LAMMPS data
        # Store each hydrogen data to in a list. Each hydrogen data is a list of coordinates for each time step
        atomNumber = [501, 502, 503, 504, 505, 506, 507, 508, 509, 510] # Numbered according to dump file
        hydrogenDatas = []
        for aN in atomNumber: # For each of the hydrogen atoms
            ithHydrogenData = [] # Create a list to hold the ith hydrogens coordintaes for each time step
            for line in lines: # Iterate line by line through the filea and collent the ith Hyrodens data
                matchStrng = "(?:\s*)(" + str(aN) + ")(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)"
                m = re.match(matchStrng, line)
                if (m is None): # Ignore if pattern doesn't match
                    pass # Do nothing
                else: # Pattern matches, store the data
                    velocityTuple = (float(m.group(3)), float(m.group(4)), float(m.group(5))) # (vx, vy, vz)
                    ithHydrogenData.append(velocityTuple)
            hydrogenDatas.append(ithHydrogenData)

        # Caclulate the VACF
        hydrogenVACF = [] # Create a list to hold MSD data for each time displacement
        timeDisplacements = np.arange(0, 200, dtype='int')

        for t in timeDisplacements: # For each time dispalcement t..
            ithHydrogenVACFAtT = [] # list will hold the average MSD for each H atoms at a given time displacement
            for hD in hydrogenDatas: # For each hydrogen calculate the MSD at given time displacement, add to list above, then average
                terms = []
                for t0 in range(0, len(hD)): # Calculate the ith hydrogens data for given time dispalcement
                    if (t0 + t >= len(hD)):
                        break;
                    vt = hD[t0 + t]
                    v0 = hD[t0]
                    dotProduct = (vt[0] * v0[0]) + (vt[1] * v0[1]) + (vt[2] * v0[2])
                    terms.append(dotProduct)
                ithHyrdogenVACF = np.average(terms)
                ithHydrogenVACFAtT.append(ithHyrdogenVACF)
            hydrogenVACF.append(np.average(ithHydrogenVACFAtT))

        # Plot the VACF from t = 0.0 to 0.2 ps
        plt.title("Velocity Autocorrelation Function (VACF) vs. Time Displacement (dt)")
        plt.xlabel("dt [ps]")
        plt.ylabel("VACF [$ps^2/\AA^2$]")
        timeDisplacements = np.arange(0, 200, dtype = 'float') # Convert time displacements to ps
        timeDisplacements *= 0.001
        plt.plot(timeDisplacements, hydrogenVACF)
        plt.savefig("VACFQ10.pdf")
        plt.close()

        # Calculate diffusion coefficient
        diffusionCoefficient = np.trapz(hydrogenVACF)
        print("diffusion coefficient from VACF: ", diffusionCoefficient)

        # Compare diffusion coefficient to problem 9

    # SOLVE THE PROBLEMS
    calculateLatticeConstantAndBulkModulus()
    problem79()
    velocityAutoCorrelationFxn()




####RUN####
print("PARTI")
plotEnergies() # PARTI, Question 1
print("PARTII")
thermoPropertiesPd() # PARTII, Questions 2, 3, 4, 5
print("PARTIII")
thermoPropertiesPdH() # PARTIII, Questions 6, 7, 8, 9, 10
