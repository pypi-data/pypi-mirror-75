# TODO: import necessary libraries
import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
# TODO: make a Binomial class that inherits from the Distribution class. Use the specifications below.
    """ Binomial distribution class for calculating and 
    visualizing a Binomial dist`ribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
                
    """
    
    #       A binomial distribution is defined by two variables: 
    #           the probability of getting a positive outcome
    #           the number of trials
    
    #       If you know these two values, you can calculate the mean and the standard deviation
    #       
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))
    
    #       
    def __init__(self, p=0.5, n=20):
        self.p = p
        self.n = n
        Distribution.__init__(self,self.calculate_mean(),self.calculate_stdev())
    
    # TODO: define the init function
        
        # TODO: store the probability of the distribution in an instance variable p
        # TODO: store the n of the distribution in an instance variable n
        
        # TODO: Now that you know p and n, you can calculate the mean and standard deviation
        #       You can use the calculate_mean() and calculate_stdev() methods defined below along with the __init__ function from the Distribution class
            
    # TODO: write a method calculate_mean() according to the specifications below
    
    def calculate_mean(self):
        self.mu = self.p * self.n
        return self.mu
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
         

    #TODO: write a calculate_stdev() method accordin to the specifications below.
    
    def calculate_stdev(self):
        self.sigma = math.sqrt(self.n * self.p * (1 - self.p))
        return self.sigma
    
        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
    
    def replace_stats_with_data(self):
        self.n=len(self.data)
        self.p=sum(self.data)/self.n
        self.calculate_stdev()
        self.calculate_mean()
        
        return self.p, self.n

    # TODO: write a replace_stats_with_data() method according to the specifications below. The read_data_file() from the Generaldistribution class can read in a data
    # file. Because the Binomaildistribution class inherits from the Generaldistribution class,
    # you don't need to re-write this method. However,  the method
    # doesn't update the mean or standard deviation of
    # a distribution. Hence you are going to write a method that calculates n, p, mean and
    # standard deviation from a data set and then updates the n, p, mean and stdev attributes.
    # Assume that the data is a list of zeros and ones like [0 1 0 1 1 0 1]. 
    #
    #       Write code that: 
    #           updates the n attribute of the binomial distribution
    #           updates the p value of the binomial distribution by calculating the
    #               number of positive trials divided by the total trials
    #           updates the mean attribute
    #           updates the standard deviation attribute
    #
    #       Hint: You can use the calculate_mean() and calculate_stdev() methods
    #           defined previously.

    
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
    
    
    # TODO: write a method plot_bar() that outputs a bar chart of the data set according to the following specifications.
    def plot_bar(self):
        
        plt.bar(self.data)
        plt.title('Histogram of the instance variable data')
        plt.xlabel('x')
        plt.ylabel('y')
        
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
    
    def pdf(self,k):
        
        x_n = math.factorial(self.n)/(math.factorial(k)*(math.factorial(self.n-k)))
        pdf_result = x_n * (self.p**k) * (1 - self.p)**(self.n-k)
        
        return pdf_result
    
    #TODO: Calculate the probability density function of the binomial distribution
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

    # write a method to plot the probability density function of the binomial distribution
    
    def plot_histogram_pdf(self):
        
        x=[]
        y=[]
        for i in range(0,self.n+1):
            x.append(i)
            y.append(pdf(i))
            
        plt.bar(x,bottom=y)
        plt.title('Bar Chart of PDF of the binomial distribution')
        plt.xlabel('x')
        plt.ylabel('y')
        
        return x,y
    
        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
    
        # TODO: Use a bar chart to plot the probability density function from
        # k = 0 to k = n
        
        #   Hint: You'll need to use the pdf() method defined above to calculate the
        #   density function for every value of k.
        
        #   Be sure to label the bar chart with a title, x label and y label

        #   This method should also return the x and y values used to make the chart
        #   The x and y values should be stored in separate lists
                
    # write a method to output the sum of two binomial distributions. Assume both distributions have the same p value.        
        
    
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """

    def __add__(self, other):
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        result = Binomial()
        result.n = self.n + other.n
        result.p = self.p
        result.calculate_mean()
        result.calculate_stdev()
        
        return result
        # TODO: Define addition for two binomial distributions. Assume that the
        # p values of the two distributions are the same. The formula for 
        # summing two binomial distributions with different p values is more complicated,
        # so you are only expected to implement the case for two distributions with equal p.
        
        # the try, except statement above will raise an exception if the p values are not equal
        
        # Hint: When adding two binomial distributions, the p value remains the same
        #   The new n value is the sum of the n values of the two distributions.
                        
    # use the __repr__ magic method to output the characteristics of the binomial distribution object.
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial object
        
        """
        
        # TODO: Define the representation method so that the output looks like
        #       mean 5, standard deviation 4.5, p .8, n 20
        #
        #       with the values replaced by whatever the actual distributions values are
        #       The method should return a string in the expected format
    def __repr__(self):
        
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
        pass
