
import numpy as np
from . data import SessionData, MultiSessionData


def session(J, t01=(0,1), mu=0, sigma=1, cond=0):
	t        = np.linspace(t01[0], t01[1], J)
	y        = mu + sigma * np.random.randn(J)
	return SessionData( t, y, cond )
