#Return the probability of flipping one head each from two coins
#One coin has a probability of heads of p1 and the other of p2

def f(p1,p2):
    return p1 * p2

#Two coins have probabilities of heads of p1 andd p2
#The probability of selecting the first coin is p0
#Return the probability of a flip landing on heads

def f(p0,p1,p2):
    return (p1 * p0) + (p2 * (1 - p0))

#Calculate the probability of a positive result given that
#p0=P(C)
#p1=P(Positive|C)
#p2=P(Negative|Not C)

def f(p0,p1,p2):
    return p0 * p1 + (1 - p0) * (1 - p2)

#Return the probability of A conditioned on B given that
#P(A)=p0, P(B|A)=p1, and P(Not B|Not A)=p2

def f(p0,p1,p2):
    return p0 * p1 / (p0 * p1 + (1 - p0) * (1 - p2))

#Return the probability of A conditioned on Not B given that
#P(A)=p0, P(B|A)=p1, and P(Not B|Not A)=p2

def f(p0,p1,p2):
    return p0 * (1 - p1) / (p0 * (1 - p1) + (1 - p0) * p2)