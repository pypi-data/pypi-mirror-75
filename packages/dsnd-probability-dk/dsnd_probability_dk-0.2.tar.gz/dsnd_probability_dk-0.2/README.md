This package includes Normal (Gaussian) and Binomial distributions.

------------------------------------------------------------------------------------------------------------------------------------------
Gaussian distribution class for calculating and visualizing a Gaussian distribution
 
 
class Gaussian takes values of mu(mean) and sigma(standard deviation).
example: gaussian_one = Gaussian(15, 8)


to print out mean use Gaussian.mean()
to print standard deviation use Gaussian.stdev()
to add together two Gaussian distributions use Gaussian1(mu, sigma) + Gaussian2(mu, sigma). 
Print out will be "mean Gaussian1(mu)+Gaussian2(mu), standard deviation sqrt(Gaussian1(sigma) ** 2 + Gaussian2(sigma) ** 2)


Gaussian.pdf(x) --where argument "x" is "point for calculating the probability density function"
Probability density function calculator for the gaussian distribution 


Gaussian.read_data_file(file_name) --where "file_name (string): name of a file to read from"
Function to read in data from a txt file. The txt file should have one number (float) per line. The numbers are stored in the data attribute. After reading in the file, the mean and standard deviation are calculated: 


plot_histogram()
Function to output a histogram of the instance variable data using matplotlib pyplot library. 
NOTE: Works in Jupiter Notebook


plot_histogram_pdf(n_spaces)  --where "n_spaces (int): number of data points". Default: n_spaces=50
Function to plot the normalized histogram of the data and a plot of the probability density function along the same range

---------------------------------------------------------------------------------------------------------------------------------------------------        
        
Binomial distribution class for calculating and visualizing a Binomial distribution 

class Binomial takes values of p(probability) and  n(size) 
example: binomial_one = Binomial(0.5, 10)

to print out mean use Binomial.calculate_mean()
to print standard deviation use Binomial.calculate_stdev()
to add together two Binomial distributions with with equal p use Binomial1(n, p) + Binomial2(n, p). 
Print out will be "mean=Binomial.calculate_mean() , standard deviation = Binomial.calculate_stdev(), p=Binomial1(p),  n=Binomial1(n) + Binomial2(n)"


Binomial.pdf(k) --where "k (float): point for calculating the probability density function"
Probability density function calculator for the gaussian distribution


Binomial.plot_bar_pdf()
Function to plot the pdf of the binomial distribution
NOTE: Works in Jupiter Notebook


Binomial.plot_bar_pdf()
Function to output a histogram of the instance variable data using matplotlib pyplot library.
NOTE: Works in Jupiter Notebook


Binomial.replace_stats_with_data()
Function to calculate p and n from the data set

------------------------------------------------------------------------------------------------------


