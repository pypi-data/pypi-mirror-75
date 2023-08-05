import os
import numpy as np
import pandas as pd
class Energy_Systems:
    
    """ 
    Energy Systems are a set of user defined systems which includes 
    all of the sets and parameters necessary.
    
    Attributes:
    
    
    TODO: Populate with energy sets when necessary
            
    """
    def __init__(self, year, region,emission,technology,fuel,timeslice,mode_of_operation,storage,daytype,season,dailytimebracket):
        """ Function to create complete energy system set to prepare datafile, as per the established model.

        Args:
            Sets:
                YEAR = Set of Years
                REGION = Set of Regions
            Parameters:
                ADD
        """
        self.year = year
        self.region = region
        self.emission = emission
        self.technology = technology
        self.fuel = fuel
        self.timeslice = timeslice
        self.mode_of_operation = mode_of_operation
        self.storage = storage
        self.daytype = daytype
        self.season = season
        self.dailytimebracket = dailytimebracket

        ly = len(self.year)
        lr = len(self.region)
        le = len(self.emission) 
        lt = len(self.technology) 
        lf = len(self.fuel) 
        ll = len(self.timeslice)
        lm = len(self.mode_of_operation)
        ls = len(self.storage)
        lld = len(self.daytype)
        lls = len(self.season)
        llh = len(self.dailytimebracket)

        self.ly = ly
        self.lr = lr
        self.le = le
        self.lt = lt
        self.lf = lf
        self.ll = ll
        self.lm = lm
        self.ls = ls
        self.lld = lld 
        self.lls = lls
        self.llh = llh

        self.YearSplit = np.zeros((ll,ly))
        self.DiscountRate = np.zeros((lr))
        self.DaySplit = np.zeros((llh,ly))
        self.Conversionls = np.zeros((ll,ls))
        self.Conversionld = np.zeros((lld,ls))
        self.Conversionlh = np.zeros((llh,ll))
        self.DaysInDayType = np.zeros((lls,lld,ly))
        self.TradeRoute = np.zeros((lr,lr,lf,ly))
        self.DepreciationMethod = np.zeros((lr))
        self.SpecifiedAnnualDemand = np.zeros((lr,lf,ly))
        self.SpecifiedDemandProfile = np.zeros((lr,lf,ll,ly))
        self.AccumulatedAnnualDemand = np.zeros((lr,lf,ly))
        self.CapacityToActivityUnit = np.zeros((lr,lt))
        self.CapacityFactor = np.zeros((lr,lt,ll,ly))
        self.AvailabilityFactor = np.zeros((lr,lt,ly))
        self.OperationalLife = np.zeros((lr,lt))
        self.ResidualCapacity = np.zeros((lr,lt,ly))
        self.InputActivityRatio = np.zeros((lr,lt,lf,lm,ly))
        self.OutputActivityRatio = np.zeros((lr,lt,lf,lm,ly))
        self.CapitalCost = np.zeros((lr,lt,ly))
        self.VariableCost = np.zeros((lr,lt,lm,ly))
        self.FixedCost = np.zeros((lr,lt,ly))
        self.TechnologyToStorage = np.zeros((lr,lt,ls,lm))
        self.TechnologyFromStorage = np.zeros((lr,lt,ls,lm))
        self.StorageLevelStart = np.zeros((lr,ls))
        self.StorageMaxChargeRate = np.zeros((lr,ls))
        self.StorageMaxDischargeRate = np.zeros((lr,ls))
        self.MinStorageCharge = np.zeros((lr,ls,ly))
        self.OperationalLifeStorage = np.zeros((lr,ls))
        self.CapitalCostStorage = np.zeros((lr,ls,ly))
        self.ResidualStorageCapacity = np.zeros((lr,ls,ly))
        self.CapacityOfOneTechnologyUnit = np.zeros((lr,lt,ly))
        self.TotalAnnualMaxCapacity = np.zeros((lr,lt,ly))
        self.TotalAnnualMinCapacity = np.zeros((lr,lt,ly))
        self.TotalAnnualMaxCapacityInvestment = np.zeros((lr,lt,ly))
        self.TotalAnnualMinCapacityInvestment = np.zeros((lr,lt,ly))
        self.TotalTechnologyAnnualActivityLowerLimit= np.zeros((lr,lt,ly))
        self.TotalTechnologyAnnualActivityUpperLimit = np.zeros((lr,lt,ly))
        self.TotalTechnologyModelPeriodActivityUpperLimit = np.zeros((lr,lt))
        self.TotalTechnologyModelPeriodActivityLowerLimit = np.zeros((lr,lt))
        self.ReserveMarginTagTechnology = np.zeros((lr,lt,ly))
        self.ReserveMarginTagFuel = np.zeros((lr,lf,ly))
        self.ReserveMargin = np.zeros((lr,ly))
        self.RETagTechnology = np.zeros((lr,lt,ly))
        self.RETagFuel = np.zeros((lr,lf,ly))
        self.REMinProductionTarget = np.zeros((lr,ly))
        self.EmissionActivityRatio = np.zeros((lr,lt,le,lm,ly))
        self.EmissionsPenalty = np.zeros((lr,le,ly))
        self.AnnualExogenousEmission = np.zeros((lr,le,ly))
        self.AnnualEmissionLimit = np.zeros((lr,le,ly))
        self.ModelPeriodExogenousEmission = np.zeros((lr,le))
        self.ModelPeriodEmissionLimit = np.zeros((lr,le))

    def SetParameters(self):
        """Sets the parameters for the functions
        
        Args: 
            Parameters for the basic problem
        
        Returns: 
            The loaded in parameters and sets
    
        """
    def CreateModelFile(self,root, file):
        """Creates the model file necessary for the project to run
        
        Args: 
            Parameters for the basic problem
        
        Returns: 
            The loaded in parameters and sets
    
        """ 
        # Finds the file
        # data = Find_File(data_file,model_file)
        model_location = os.path.join(root,file)
        df = pd.read_excel(model_location,sheet_name = 'Model')
        # Creates a new dataframe based on the variables on the Include column values
        df_Include = df[df.Include == 'Yes']
        df_model = df_Include[['Name']].copy()

        # Creates a file location and write the model to a text file
        model_txt = 'GOCPI_OseMOSYS_Model.txt'
        model_location = os.path.join(root,model_txt)

        # Saves the user defined model to a text file
        np.savetxt(model_location,df_model.values,fmt = '%s')


    def CreateDataFile(self,file_location,defaults_dictionary):
        """Function create the GOCPI OseMOSYS Energy Systems Data File necessary for optimisation
        
        Args: 
            Defaults_dictionary: An array of default values for the Energy System parameters. It's important the order of these
                                 parameters are preserved.
        
        Returns: 
            The GOCPI OseMOSYS file
    
        """
        # Opens the file for write the data
        with open(file_location,'w') as f:
            # Sets up the preamble for the data file
            f.write('# GOCPI Energy System Data File\n')
            f.write('# Insert instructions when the file is running properly\n')
            f.write('#\n')
            # Sets
            f.write('# Sets\n#\n')
            # year
            set_string = ' '.join(self.year)
            f.write('set YEAR\t:=\t{0};\n'.format(set_string))
            # region
            set_string = ' '.join(self.region)
            f.write('set REGION\t:=\t{0};\n'.format(set_string))
            # emission
            set_string = ' '.join(self.emission)
            f.write('set EMISSION\t:=\t{0};\n'.format(set_string))
            # technology
            set_string = ' '.join(self.technology)
            f.write('set TECHNOLOGY\t:=\t{0};\n'.format(set_string))
            # fuel
            set_string = ' '.join(self.fuel)
            f.write('set FUEL\t:=\t{0};\n'.format(set_string))
            # timeslice
            set_string = ' '.join(self.timeslice)
            f.write('set TIMESLICE\t:=\t{0};\n'.format(set_string))
            # mode_of_operation 
            set_string = ' '.join(self.mode_of_operation)
            f.write('set MODE_OF_OPERATION\t:=\t{0};\n'.format(set_string))
            # storage 
            set_string = ' '.join(self.storage)
            f.write('set STORAGE\t:=\t{0};\n'.format(set_string))
            # daytype
            set_string = ' '.join(self.daytype)
            f.write('set DAYTYPE\t:=\t{0};\n'.format(set_string))
            # season 
            set_string = ' '.join(self.season)
            f.write('set SEASON\t:=\t{0};\n'.format(set_string))
            # dailytimebracket 
            set_string = ' '.join(self.dailytimebracket)
            f.write('set DAILYTIMEBRACKET\t:=\t{0};\n'.format(set_string))
            f.write('#\n')
            # Parameters

            # YearSplit = np.zeros((ll,ly))
            param = 'YearSplit'
            f.write('#\n')
            columns = self.year
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.timeslice)
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.YearSplit[:,:]
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # DiscountRate = np.zeros((lr))
            param = 'DiscountRate'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Converts maxtrix rows to list
            array = np.array(self.region)
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.DiscountRate[:]
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # DaySplit = np.zeros((llh,ly))
            param = 'DaySplit'
            f.write('#\n')
            columns = self.year
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.dailytimebracket)
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.DaySplit[:,:]
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # Conversionls = np.zeros((ll,ls))
            param = 'Conversionls' # Change this line
            f.write('#\n')
            columns = self.storage # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.timeslice) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.Conversionls[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # Conversionld = np.zeros((lld,ls))
            param = 'Conversionld' # Change this line
            f.write('#\n')
            columns = self.storage # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.daytype) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.Conversionld[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # Conversionlh = np.zeros((llh,ll))
            param = 'Conversionlh' # Change this line
            f.write('#\n')
            columns = self.timeslice # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.dailytimebracket) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.Conversionlh[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # DaysInDayType = np.zeros((lls,lld,ly))
            #Writes new line character at parameter metadata to the text file
            param = 'DaysInDayType'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.daytype
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.season)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.DaysInDayType[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')
            
            # TradeRoute = np.zeros((lr,lr,lf,ly))
            param = 'TradeRoute' # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for j in range(self.lf):
                # Sets index value for format string
                fl = self.fuel[j]
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.region
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.TradeRoute[:,:,j,k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt,matlist))
                    # Writes index specific parameter values to the text files 
                    f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(fl,y,column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[','')
                        combinedflat = combinedflat.replace(']','')
                        combinedflat = combinedflat.replace("'",'')
                        combinedflat = combinedflat.replace(",",'')
                        combinedflat = combinedflat.replace("(",'')
                        combinedflat = combinedflat.replace(")",'')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')
            # DepreciationMethod = np.zeros((lr))
            param = 'DepreciationMethod'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Converts maxtrix rows to list
            array = np.array(self.region)
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.DepreciationMethod[:]
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # SpecifiedAnnualDemand = np.zeros((lr,lf,ly))
            param = 'SpecifiedAnnualDemand'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.fuel
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.SpecifiedAnnualDemand[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # SpecifiedDemandProfile = np.zeros((lr,lf,ll,ly))
            param = 'SpecifiedDemandProfile' # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for j in range(self.ll):
                # Sets index value for format string
                fl = self.fuel[j]
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.fuel
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.SpecifiedDemandProfile[:,:,j,k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt,matlist))
                    # Writes index specific parameter values to the text files 
                    f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(fl,y,column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[','')
                        combinedflat = combinedflat.replace(']','')
                        combinedflat = combinedflat.replace("'",'')
                        combinedflat = combinedflat.replace(",",'')
                        combinedflat = combinedflat.replace("(",'')
                        combinedflat = combinedflat.replace(")",'')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # AccumulatedAnnualDemand = np.zeros((lr,lf,ly))
            param = 'AccumulatedAnnualDemand'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.fuel
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.SpecifiedAnnualDemand[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # CapacityToActivityUnit = np.zeros((lr,lt))
            param = 'CapacityToActivityUnit' # Change this line
            f.write('#\n')
            columns = self.technology # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.CapacityToActivityUnit[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # CapacityFactor = np.zeros((lr,lt,ll,ly))
            param = 'CapacityFactor' # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for j in range(self.ll):
                # Sets index value for format string
                x = self.timeslice[j]
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.CapacityFactor[:,:,j,k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt,matlist))
                    # Writes index specific parameter values to the text files 
                    f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(x,y,column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[','')
                        combinedflat = combinedflat.replace(']','')
                        combinedflat = combinedflat.replace("'",'')
                        combinedflat = combinedflat.replace(",",'')
                        combinedflat = combinedflat.replace("(",'')
                        combinedflat = combinedflat.replace(")",'')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')
            
            # AvailabilityFactor = np.zeros((lr,lt,ly))
            param = 'AvailabilityFactor'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.AvailabilityFactor[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # OperationalLife = np.zeros((lr,lt))
            param = 'OperationalLife' # Change this line
            f.write('#\n')
            columns = self.timeslice # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.OperationalLife[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ResidualCapacity = np.zeros((lr,lt,ly))
            param = 'ResidualCapacity'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.ResidualCapacity[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')
            
            # InputActivityRatio = np.zeros((lr,lt,lf,lm,ly))
            param = 'InputActivityRatio' # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for i in range(self.lf): # Change loops if you need
                # Sets index value for format string
                x = self.fuel[i] 
                for j in range(self.lm):
                    # Sets index value for format string
                    y = self.mode_of_operation[j]
                    for k in range(self.ly):
                        # Sets index value for format string
                        z = self.year[k]
                        # Converts matrix columns to strings columns to strings
                        columns = self.technology
                        column_string = ' '.join(columns)
                        # Converts maxtrix rows to list
                        array = np.array(self.region)
                        array = array.T
                        lt = array.tolist()
                        # Creates 2D matrix for this value
                        mat = self.InputActivityRatio[:,:,i,j,k]
                        # Converts combined matrix to list and combines lists
                        matlist = mat.tolist()
                        #Combines the two lists
                        combined_list = list(zip(lt,matlist))
                        # Writes index specific parameter values to the text files 
                        f.write("\t[*,*,{0},{1},{2}]:\t{3}\t:=\n".format(x,y,z,column_string))
                        for line in combined_list:
                            combinedflat = ''.join(str(line))
                            combinedflat = combinedflat.replace('[','')
                            combinedflat = combinedflat.replace(']','')
                            combinedflat = combinedflat.replace("'",'')
                            combinedflat = combinedflat.replace(",",'')
                            combinedflat = combinedflat.replace("(",'')
                            combinedflat = combinedflat.replace(")",'')
                            f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # OutputActivityRatio = np.zeros((lr,lt,lf,lm,ly))
            param = 'OutputActivityRatio' # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for i in range(self.lf): # Change loops if you need
                # Sets index value for format string
                x = self.fuel[i] 
                for j in range(self.lm):
                    # Sets index value for format string
                    y = self.mode_of_operation[j]
                    for k in range(self.ly):
                        # Sets index value for format string
                        z = self.year[k]
                        # Converts matrix columns to strings columns to strings
                        columns = self.technology
                        column_string = ' '.join(columns)
                        # Converts maxtrix rows to list
                        array = np.array(self.region)
                        array = array.T
                        lt = array.tolist()
                        # Creates 2D matrix for this value
                        mat = self.OutputActivityRatio[:,:,i,j,k]
                        # Converts combined matrix to list and combines lists
                        matlist = mat.tolist()
                        #Combines the two lists
                        combined_list = list(zip(lt,matlist))
                        # Writes index specific parameter values to the text files 
                        f.write("\t[*,*,{0},{1},{2}]:\t{3}\t:=\n".format(x,y,z,column_string))
                        for line in combined_list:
                            combinedflat = ''.join(str(line))
                            combinedflat = combinedflat.replace('[','')
                            combinedflat = combinedflat.replace(']','')
                            combinedflat = combinedflat.replace("'",'')
                            combinedflat = combinedflat.replace(",",'')
                            combinedflat = combinedflat.replace("(",'')
                            combinedflat = combinedflat.replace(")",'')
                            f.write("{0}\n".format(combinedflat))
            f.write(';\n')
            
            # CapitalCost = np.zeros((lr,lt,ly))
            param = 'CapitalCost'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.CapitalCost[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # VariableCost = np.zeros((lr,lt,lm,ly))
            param = 'VariableCost' # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for j in range(self.lm):
                # Sets index value for format string
                x = self.mode_of_operation[j]
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.VariableCost[:,:,j,k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt,matlist))
                    # Writes index specific parameter values to the text files 
                    f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(x,y,column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[','')
                        combinedflat = combinedflat.replace(']','')
                        combinedflat = combinedflat.replace("'",'')
                        combinedflat = combinedflat.replace(",",'')
                        combinedflat = combinedflat.replace("(",'')
                        combinedflat = combinedflat.replace(")",'')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # FixedCost = np.zeros((lr,lt,ly))
            param = 'FixedCost'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.FixedCost[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TechnologyToStorage = np.zeros((lr,lt,ls,lm))
            param = 'TechnologyToStorage' # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for j in range(self.ls):
                # Sets index value for format string
                x = self.storage[j]
                for k in range(self.lm):
                    # Sets index value for format string
                    y = self.mode_of_operation[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.TechnologyToStorage[:,:,j,k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt,matlist))
                    # Writes index specific parameter values to the text files 
                    f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(x,y,column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[','')
                        combinedflat = combinedflat.replace(']','')
                        combinedflat = combinedflat.replace("'",'')
                        combinedflat = combinedflat.replace(",",'')
                        combinedflat = combinedflat.replace("(",'')
                        combinedflat = combinedflat.replace(")",'')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TechnologyFromStorage = np.zeros((lr,lt,ls,lm))
            param = 'TechnologyFromStorage' # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for j in range(self.ls):
                # Sets index value for format string
                x = self.storage[j]
                for k in range(self.lm):
                    # Sets index value for format string
                    y = self.mode_of_operation[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.TechnologyFromStorage[:,:,j,k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt,matlist))
                    # Writes index specific parameter values to the text files 
                    f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(x,y,column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[','')
                        combinedflat = combinedflat.replace(']','')
                        combinedflat = combinedflat.replace("'",'')
                        combinedflat = combinedflat.replace(",",'')
                        combinedflat = combinedflat.replace("(",'')
                        combinedflat = combinedflat.replace(")",'')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # StorageLevelStart = np.zeros((lr,ls))
            param = 'StorageLevelStart' # Change this line
            f.write('#\n')
            columns = self.storage # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.StorageLevelStart[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # StorageMaxChargeRate = np.zeros((lr,ls))
            param = 'StorageMaxChargeRate' # Change this line
            f.write('#\n')
            columns = self.storage # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.StorageMaxChargeRate[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # StorageMaxDischargeRate = np.zeros((lr,ls))
            param = 'StorageMaxDischargeRate' # Change this line
            f.write('#\n')
            columns = self.storage # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.StorageMaxDischargeRate[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # MinStorageCharge = np.zeros((lr,ls,ly))
            param = 'MinStorageCharge'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.storage
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.MinStorageCharge[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # OperationalLifeStorage = np.zeros((lr,ls))
            param = 'OperationalLifeStorage' # Change this line
            f.write('#\n')
            columns = self.storage # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.OperationalLifeStorage[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # CapitalCostStorage = np.zeros((lr,ls,ly))
            param = 'CapitalCostStorage'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.storage
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.CapitalCostStorage[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')


            # ResidualStorageCapacity = np.zeros((lr,ls,ly))
            param = 'ResidualStorageCapacity'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.storage
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.ResidualStorageCapacity[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # CapacityOfOneTechnologyUnit = np.zeros((lr,lt,ly))
            param = 'CapacityOfOneTechnologyUnit'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.CapacityOfOneTechnologyUnit[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalAnnualMaxCapacity = np.zeros((lr,lt,ly))
            param = 'TotalAnnualMaxCapacity'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.TotalAnnualMaxCapacity[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')
            
            # TotalAnnualMinCapacity = np.zeros((lr,lt,ly))
            param = 'TotalAnnualMinCapacity'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.TotalAnnualMinCapacity[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalAnnualMaxCapacityInvestment = np.zeros((lr,lt,ly))
            param = 'TotalAnnualMaxCapacityInvestment'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.TotalAnnualMaxCapacityInvestment[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalAnnualMinCapacityInvestment = np.zeros((lr,lt,ly))
            param = 'TotalAnnualMinCapacityInvestment'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.TotalAnnualMinCapacityInvestment[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalTechnologyAnnualActivityLowerLimit= np.zeros((lr,lt,ly))
            param = 'TotalTechnologyAnnualActivityLowerLimit'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.TotalTechnologyAnnualActivityLowerLimit[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalTechnologyAnnualActivityUpperLimit = np.zeros((lr,lt,ly))
            param = 'TotalTechnologyAnnualActivityUpperLimit'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.TotalTechnologyAnnualActivityUpperLimit[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalTechnologyModelPeriodActivityUpperLimit = np.zeros((lr,lt))
            param = 'TotalTechnologyModelPeriodActivityUpperLimit' # Change this line
            f.write('#\n')
            columns = self.technology # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.TotalTechnologyModelPeriodActivityUpperLimit[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalTechnologyModelPeriodActivityLowerLimit = np.zeros((lr,lt))
            param = 'TotalTechnologyModelPeriodActivityLowerLimit' # Change this line
            f.write('#\n')
            columns = self.technology # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.TotalTechnologyModelPeriodActivityLowerLimit[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ReserveMarginTagTechnology = np.zeros((lr,lt,ly))
            param = 'ReserveMarginTagTechnology'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.ReserveMarginTagTechnology[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ReserveMarginTagFuel = np.zeros((lr,lf,ly))
            param = 'ReserveMarginTagFuel'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.fuel
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.ReserveMarginTagFuel[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ReserveMargin = np.zeros((lr,ly))
            param = 'ReserveMargin' # Change this line
            f.write('#\n')
            columns = self.year # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.ReserveMargin[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # RETagTechnology = np.zeros((lr,lt,ly))
            param = 'RETagTechnology'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.technology
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.RETagTechnology[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')
            
            # RETagFuel = np.zeros((lr,lf,ly))
            param = 'RETagFuel'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.fuel
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.RETagFuel[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # REMinProductionTarget = np.zeros((lr,ly))
            param = 'REMinProductionTarget' # Change this line
            f.write('#\n')
            columns = self.year # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.REMinProductionTarget[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # EmissionActivityRatio = np.zeros((lr,lt,le,lm,ly))
            #Writes new line character at parameter metadata to the text file
            param = 'EmissionActivityRatio' # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for i in range(self.le): # Change loops if you need
                # Sets index value for format string
                emission = self.emission[i] 
                for j in range(self.lm):
                    # Sets index value for format string
                    MOO = self.mode_of_operation[j]
                    for k in range(self.ly):
                        # Sets index value for format string
                        y = self.year[k]
                        # Converts matrix columns to strings columns to strings
                        columns = self.technology
                        column_string = ' '.join(columns)
                        # Converts maxtrix rows to list
                        array = np.array(self.region)
                        array = array.T
                        lt = array.tolist()
                        # Creates 2D matrix for this value
                        mat = self.EmissionActivityRatio[:,:,i,j,k]
                        # Converts combined matrix to list and combines lists
                        matlist = mat.tolist()
                        #Combines the two lists
                        combined_list = list(zip(lt,matlist))
                        # Writes index specific parameter values to the text files 
                        f.write("\t[*,*,{0},{1},{2}]:\t{3}\t:=\n".format(emission,MOO,y,column_string))
                        for line in combined_list:
                            combinedflat = ''.join(str(line))
                            combinedflat = combinedflat.replace('[','')
                            combinedflat = combinedflat.replace(']','')
                            combinedflat = combinedflat.replace("'",'')
                            combinedflat = combinedflat.replace(",",'')
                            combinedflat = combinedflat.replace("(",'')
                            combinedflat = combinedflat.replace(")",'')
                            f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # EmissionsPenalty = np.zeros((lr,le,ly))
            param = 'EmissionsPenalty'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.emission
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.EmissionsPenalty[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # AnnualExogenousEmission = np.zeros((lr,le,ly))
            param = 'AnnualExogenousEmission'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.emission
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.AnnualExogenousEmission[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # AnnualEmissionLimit = np.zeros((lr,le,ly))
            param = 'AnnualEmissionLimit'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(param,defaults_dictionary[param]))
            # Writes parameter values to the text files
            for k in range(self.ly):
                # Sets index value for format string
                y = self.year[k]
                # Converts matrix columns to strings columns to strings
                columns = self.emission
                column_string = ' '.join(columns)
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.AnnualExogenousEmission[:,:,k]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt,matlist))
                # Writes index specific parameter values to the text files 
                f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y,column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[','')
                    combinedflat = combinedflat.replace(']','')
                    combinedflat = combinedflat.replace("'",'')
                    combinedflat = combinedflat.replace(",",'')
                    combinedflat = combinedflat.replace("(",'')
                    combinedflat = combinedflat.replace(")",'')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ModelPeriodExogenousEmission = np.zeros((lr,le))
            param = 'ModelPeriodExogenousEmission' # Change this line
            f.write('#\n')
            columns = self.emission # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.ModelPeriodExogenousEmission[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ModelPeriodEmissionLimit = np.zeros((lr,le))
            param = 'ModelPeriodEmissionLimit' # Change this line
            f.write('#\n')
            columns = self.emission # Change this line
            column_string = ' '.join(columns)
            # Converts maxtrix rows to list
            array = np.array(self.region) # Change this line
            array = array.T
            lt = array.tolist()
            # Creates 2D matrix for this value
            mat = self.ModelPeriodEmissionLimit[:,:] # Change this line
            # Converts combined matrix to list and combines lists
            matlist = mat.tolist()
            #Combines the two lists
            combined_list = list(zip(lt,matlist))
            # Writes index specific parameter values to the text files 
            f.write("param\t{0}\t:{1}:=\n".format(param,column_string))
            for line in combined_list:
                combinedflat = ''.join(str(line))
                combinedflat = combinedflat.replace('[','')
                combinedflat = combinedflat.replace(']','')
                combinedflat = combinedflat.replace("'",'')
                combinedflat = combinedflat.replace(",",'')
                combinedflat = combinedflat.replace("(",'')
                combinedflat = combinedflat.replace(")",'')
                f.write("{0}\n".format(combinedflat))
            f.write(';\n')
            f.write('#')
        return 