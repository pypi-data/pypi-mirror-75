import math
import matplotlib.pyplot as plt 
from .Distribution_class import Distribution

class Gaussian(Distribution):
    """
    Gaussian distribution class to calculate and visualize 
    a Gaussian distribution 

    Attributes:
        mean (float): mean value of the dstribution
        stdev (float): standard deviation of the distribution
        data_list (list of floats): list of floats extracted from the data file
    """
    def __init__(self, mu=0, sigma=1):

        Distribution.__init__(self, mu, sigma)

    def calculate_mean(self):
        
        """ A method to calculte the mean value of a data set

        Args:
            None 
        
        Return:
            float: mean of the data set
        """
        mean_value = 1.0 * sum(self.data) * len(self.data)

        self.mean = mean_value 

        return self.mean

    
    def calculate_stdev(self, sample=True):
        """ Method to calculate standard deviation of the data set 
        
        Args: 
            sample (bool): whether the data represents a sample or poulation 
            
        Return: 
            (float) standard deviation of the distribution
            
        """
        if sample:
            n = len(self.data) - 1

        else:
            n = len(self.data)

        mean = self.calculate_mean()
        square_sum = 0

        for data in self.data:
            square_sum += math.pow(data - mean, 2)
        
        stdev = math.sqrt(square_sum / n)
        self.stdev = stdev 

        return self.stdev

    
    def polt_histogram(self):

        """ method to plot a histogram of the instance variable data using 
        matplot pyplot library.

        Args: 
            None 

        Return: 
            None
        """
        plt.hist(self.data)
        plt.title("Histogam of Data")
        plt.xlabel("Data")
        plt.ylabel("Count")

    def pdf(self, x):

        """ Calculate the probability density function of a 
        gaussian distribution 

        Args: 
            x (float): point to calculate the probability density function

        Return:
            float: the probability density function output

        """
        pi = math.pi
        mean = self.mean
        variance = math.pow(self.stdev, 2)

        pdf = 1.0 * (1 / math.sqrt(2 * pi * variance) * math.exp(-.5 * math.pow(x - mean, 2) / variance))

        return pdf 

    def plot_histogram_pdf(self, n_spaces=50):
        
        """ Method to plot the normalized histogram of the data and the plot 
        of the probability density function along the same range

        Args:
            n_space (int): number of data points
        
        Return:
            list: x values of the pdf plot
            list: y values of the pdf plot

        """
        mean = self.mean
        stdev = self.stdev

        min_range = min(self.data)
        max_range = max(self.data)

        # calculate the interval between x values 
        interval = 1.0 * (max_range - min_range) / n_spaces

        x = []      # x vales 
        y = []      # y = pdf values 

         # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y


    def __add__(self, other):

        """ Method to add two gaussian distributions 

        Args: 
            other (Gaussian): Gaussian instance 

        Return: 
            Gaussian: Gaussian distribution

        """

        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(math.pow(self.stdev, 2) + math.pow(self.stdev, 2))

        return result


    def __repr__(self):

        """ Method to output the characteristics of the Gaussian instance 

        Args: 
            None 

        Return: 
            string: characteristics of the Gaussian

        """
        return "mean {}, standard deviation {}".format(self.mean, self.stdev)
        



        