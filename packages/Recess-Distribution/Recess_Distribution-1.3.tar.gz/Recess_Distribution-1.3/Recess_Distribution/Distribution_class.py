class Distribution:
    """ Generic distribution class for calculating and visualizing 
    a probability distribution 

    Attributes:
        mu (float): mean of a data set
        sigma (float): stdandard deviation of the distribution 
        of the data set.   
        data_list (list of floats): describes a list of floats extracted 
        from the data file. 

    """

    def __init__(self, mu=0, sigma=1):

        """ to initialize the class objects

        Arguments:
            mu (float): mean value of the distribution
            sigma (float): stdandard deviation of the distribution 
                    of the data set 

        Return:
            None
        """ 
        self.mean = mu
        self.stdev = sigma
        self.data = []
    
    def read_data_file(self, file_name):
    
        """ Function to read in data from a txt file. 
        The txt file should have one number (float) per line
        The numbers are stored in the data attribute 

        Args: 
            file_name (string): name of the file to read from

        Return:
            None
        """
        with open(file_name) as file:
            data_list = []
            line = file.readline()

            while line:
                data_list.append(int(line))
                line = file.readline()

            file.close()

        self.data = data_list