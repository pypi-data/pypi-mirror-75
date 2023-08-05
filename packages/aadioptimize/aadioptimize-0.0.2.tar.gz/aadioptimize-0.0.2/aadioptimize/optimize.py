import numpy.matlib as mat
import numpy as np


N =1

def initDE(N_p,lb,ub,prob):
    """ 
    Initializes paramaters for differential evolution

    Paramaters
    ----------
    
    N_p : int
    	Number of population
    lb : int 
        lower bound of searchspace
    ub : int
        upper bound of searchspace
    prob : function
    	The objective function


    Returns
    -------
    lb : numpy.ndarray
    	Returns the lower bound as a numpy array
    ub : numpy.ndarray
		Returns the upper bound as a numpy array
	f  : numpy.ndarray
		Returns vector for fitness function
	fu : numpy ndarray
		Retruns empty vector for fitness function
	D : int
		Returns the amount of decision variables for crossover process
	U : numpy.ndarray
    	Returns matrix for trial solution
	P : numpy.ndarray
		Returns randomly generated matrix of target vectors
    """



    lb = np.full(N_p,lb)
            
    ub = np.full(N_p,ub)
            
    f = np.zeros((N_p,1)) #empty vector for fitness function
            
    fu = np.zeros((N_p,1))#newly created trial vector

    D = len(lb) # Determining amount of decision variables
    
    U = np.zeros((N_p,D)) #Matrix for storing trial solutions 
        
    #Initial random population 
    P = mat.repmat(lb,N_p,1)+mat.repmat((ub-lb),N_p,1)*np.random.rand(len(ub-lb),N_p)
        
    for p in np.arange(N_p):
        f[p]=prob(P[p,])
            
    return lb,ub,f,fu,D,U,P





#This function starts the mutation process and generates a donorvector
def mutation(i,N_p,t,T,P,N_vars,F_min,F_const):
    """ 
    Function that generates a donorvector. If there is >=3 searchvariables then the 
    adaptive scaling factor is implimented. Otherwise just the constant. It gnerates 
    candidates for the donorvector by randomly choosing rows from the initial matrix,
    but not the i-th element.

    Paramaters
    ----------
    
    i : int
        Number of the row in matrix
    N_p : int
        Number of population
    t : int
        Iteration index
    T : int
        Total number of iterations
    N_vars : int
        Number of search variables
    F_min : optional (float,int)
        The minimum value of scaling factor. Used when N_vars >= 3
    F_const : optional (float,int)
        The constant value of scaling factor
    
    Returns
    -------
    V : numpy.ndarray
        The donor vector
    """

    #Adaptive scaling factor
    if N_vars >= 3:
        F=F_min*2**np.exp(1-(T/(T+1-t)))
    else:
        F = F_const
    #candidates are assigned without the i-th element
    candidates= np.delete(np.arange(N_p), np.where(np.arange(N_p)==i))
    #3 target vectors are picked out randomly for the donorvector generator
    cand_rand=np.random.choice(candidates,3,replace= False)
    X1=P[cand_rand[0],]
    X2=P[cand_rand[1],]
    X3=P[cand_rand[2],]
   
	#Donorvctor generator
    V= X1 + F*(X2-X3)
    return V


#this function evaluates donor vector and uses parts of it which fit better
def crossover(f,P_c_min,P_c_max,i,D,V,P,U):
    """
    Crossover function for differential evolution. This function uses adaptive crossover rate.
    The minimum and the maximum range is set by user. It decides whether or not to use donorvector's
    j-th elements in the U matrix.
    
    Paramaters
    ---------
    f : numpy.ndarray
        The fitness function array
    P_c_min : optional(float/integer)
        Minimum crossover rate value for adaptive crossover rate
    P_c_max : optional(float/integer)
        Maximum crossover rate value for adaptive crossover rate
    i : int
        Row number
    D : int
        The amount of decision variables for crossover process
    V : numpy.ndarray
        The donor vector
    P : numpy.ndarray
        Matrix of initial target vectors
    U : numpy.ndarrat
        Matrix of trial solutions
        
    Returns
    -------
    U : numpy.ndarray
        Retruns the U matrix with new trial solutions.
    
    
    """
    #ADAPTIVE Crossover
    if f[i] < np.mean(f):
        P_c = P_c_min + (P_c_max-P_c_min)*((f[i]-np.mean(f))/(np.max(f)-np.mean(f)))
    else:
        P_c = P_c_min

    delta = np.random.randint(0,D-1) 
    for j in np.arange(D):
        if np.random.uniform(0,1) <= P_c or delta == j:
            U[i,j] = V[j]
        else:
            U[i,j]=P[i,j]

    return U

#this function bounds the vector and replaces the old target vector with new if better
def boundgreed(N,j,U,P,f,fu,ub,lb,prob):
    """
    This function bound the vector elements according to the bound set by the usere. If bounds 
    violated, it is replaced by either the lower- or upperbound. Then the Greedy selection is performed.
    Firstly objective function is valued by the new vector. Then it is compared to the initial or the last
    objective function value. If the new value is samller. Then the Initial or last target vector matrix's rows
    are replaced by new vector.
    
    
    Parameters
    ----------
    j : int
        
    U : numpy.ndarray
        Matrix of trial vectors
    P : numpy.ndarray
        Matrix of target vectors
    f : numpy.ndarray
        Target vectors' Fitness function array.
    fu : numpy.ndarray
        Trial vectors' Fitness function array.
    ub : numpy.ndarray
        Upperbound
    lb : numpy.ndarray
        Lowerbound
    prob : function
        The objective function

    Returns
    -------

    f : numpy.ndarray
        New trial vectors' fitness function value that will be used in next iteration
    P : numpy.ndarray
        New trial vector matrix that will be used in next iteration

    """
    U[j]=np.minimum(U[j], ub)
    U[j]=np.maximum(U[j], lb)
    ##
    fu[j]=prob(U[j])
    N = N+1
    if fu[j] < f[j]:
        P[j]= U[j]
        f[j]=fu[j]
    return N,f,P

#distance from known location
def distance(known_loc,found_loc,N_vars,):
    """
    Function that uses pythagorean theorem to calculate distance between the found point
    and known location. NB!!! This function is not used in the main prgram so thist must
    be called itself.

    Parameters
    ----------
    known_loc : numpy.ndarray
        Known location that is given by the user
    found_loc : numpy.ndarray
        Found location with the program
    N_vars : int
        Number of search variables

    Returns
    -------
    dist : float
        Returns the distance between the points.

    """
    undersqrt=np.zeros(N_vars)
    for i in (np.arange(N_vars)):
        undersqrt[i]  =(known_loc[i]-found_loc[i])**2
        dist = np.sqrt(sum(undersqrt))

    return dist


def main(N,N_p,T,lb,ub,prob,N_vars,F_min,F_const,P_c_min,P_c_max):
    """
    Differential evolution optimizer. It takes all the parmaters and uses them to find the
    global optimum of the objctive function. At least tries. Number of evaluation of the 
    fitness function is 1+(N_p*T).

    Parameters
    ----------
    N : int
        Number of evaluations counter

    N_p : int
        Number of population
    T : int
        Number of iterations
    lb : int
        Lower bound of search space
    ub : TYPE
        Upper bound of search space
    prob : function
        Function for objective function
    N_vars : int
        Number of search variables
    F_min : optional (int/float)
        Minimum value for the scaling factor
    F_const : optional (int/float)
        Constant value for the scaling factor
    P_c_min : optional (int/float)
        Minimum value of Crossover rate
    P_c_max : optional (int/float)
        Maximum value of crossover rate

    Raises
    ------
    Exception
        Raises error when there is less than 4 of the population(N_p)

    Returns
    -------
    
    best_of_f : numpy.ndarray
        Returns the best value of the objective function
    globopt : numpy.ndarray
        Returns global optimum location

    """

    lb,ub,f,fu,D,U,P = initDE(N_p,lb,ub,prob)
    if N_p < 4:
        raise Exception("Sorry, there must be atleast a population of 4. Reccomended 20")
    for t in np.arange(T):
        for i in np.arange(N_p):
            V = mutation(i,N_p,t,T,P,N_vars,F_min,F_const)

            U=crossover(f,P_c_min,P_c_max,i,D,V,P,U)

        for j in np.arange(N_p):    
            N,f,P = boundgreed(N,j,U,P,f,fu,ub,lb,prob)
	
		#if N == 500:
			#break
    best_of_f= min(f)
    globopt = P[f.argmin()]
    return N,best_of_f, globopt[:N_vars]
