import logging
import math


# Basic configuration
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger =logging.getLogger()



# Log messages
# logging.debug("This is a debug message")
# logging.info("This is an info message")
# logging.warning("This is a warning message")
# logging.error("This is an error message")
# logging.critical("This ia critical message.")


def quadratic_formula(a,b,c):
    # """return the solutions t the equation ax^2+bx+c=0"""
    logger.warning("quadractic_formula({0},{1},{2})".format(a,b,c))

    logger.debug("#compute the discriminant")
    disc = b**2-4*a*c

    logger.debug("#compute two roots")
    root1=(-b + math.sqrt(disc))/(2*a)
    root2=(-b - math.sqrt(disc))/(2*a)

    logger.debug("#return roots")
    return(root1,root2)

roots= quadratic_formula(1,0,1)
print(roots)



