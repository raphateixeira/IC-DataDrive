import numpy as np

dados = np.load("Dadosteste1MG.npy")

# Salvar em CSV
np.savetxt("Dadosteste1MG.csv", dados, delimiter=",", header="tempo,u,y", comments="")
