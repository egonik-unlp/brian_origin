import pandas as pd
import numpy as np


def main(eem:pd.DataFrame) -> tuple:
	eem_mat=eem.to_numpy()
	emision=np.unique(eem.iloc[:,0])
	excitacion=np.unique(eem.iloc[:,1])

	xx,yy=np.meshgrid(emision, excitacion)
	zz=np.vstack(np.split(eem_mat[:,2], excitacion.shape[0]))
	return (xx,yy,zz)
		





if __name__=='__main__':
	main()