import numpy as np
import numba as nb
from scipy import sparse
from scipy.sparse.csgraph import connected_components


class PCN(object):
    def __init__(self, NN, NND):
        self.N, self.knn = NN.shape
        self.NN = NN
        self.NND = NND

    # NN n x k, NND nxk (except self)
    def NNList_f(self):
        # ind_sorted = my.argsort(NND.reshape(-1), np.array(range(N*knn)))
        aux_ind = np.arange(self.N*self.knn)
        ind_sorted = np.lexsort((aux_ind, self.NND.reshape(-1)))
        return ind_sorted

    @nb.jit(nopython=True)
    def NNList_sub(self, ind_sorted):
        C = np.zeros((self.N, self.knn), dtype=np.int32) - 1
        for ind in ind_sorted:
            i = ind // self.knn
            k1 = ind % self.knn
            j = self.NN[i, k1]
            if i > j:
                if k1 == 0 or C[i, k1-1] >= 0:
                    k2 = -1
                    for ii in range(self.knn):
                        if self.NN[j, ii] == i:
                            k2 = ii
                            break
                    if k2 >= 0:
                        if k2 == 0 or C[j, k2-1] >= 0:
                            C[i, k1] = k2
                            C[j, k2] = k1
        return C

    @nb.jit(nopython=True)
    def compute_Wij(self, i, k1, j):
        sum1 = 1
        for nbi in range(k1):
            tmp_nb = self.NN[i, nbi]
            for ii in range(self.knn):
                if self.NN[j, ii] == tmp_nb:
                    sum1 += 1
                    break
        return sum1

    @nb.jit(nopython=True)
    def compute_W(self, C):
        W = np.zeros((self.N, self.knn), dtype=np.float64)
        for i in range(self.N):
            for k1 in range(self.knn):
                if C[i, k1] >= 0:
                    if W[i, k1] == 0:
                        j = self.NN[i, k1]
                        k2 = C[i, k1]
                        # k2 = -1
                        # for ii in range(knn):
                        #     if NN[j, ii] == i:
                        #         k2 = ii
                        #         break
                        sum1 = self.compute_Wij(i, k1, j)
                        sum2 = self.compute_Wij(j, k2, i)
                        W[i, k1] = (sum1 + sum2) / min(k1+1, k2+1)
                        W[j, k2] = W[i, k1]
                else:
                    break

        return W

    @nb.jit(nopython=True)
    def density_f(self, C, rho):
        density = np.zeros(self.N, dtype=np.int32)

        max_count = np.max(rho)
        rho = np.floor(rho / max_count * 100)
        thr_g = np.median(rho[rho > 0])
        for i in range(self.N):
            if rho[i] >= thr_g:
                density[i] = 2

        for i in range(self.N):
            if C[i, 0] < 0 or density[i] == 2:
                continue

            ni = 0
            for k in range(self.knn):
                if C[i, k] >= 0:
                    ni += 1
                else:
                    break

            local_rhos = rho[self.NN[i, :ni]]
            ind = np.where(local_rhos < thr_g)[0]
            local_rhos = local_rhos[ind]
            if len(local_rhos) <= 1:
                density[i] = 1
                continue

            thr = np.median(local_rhos)
            if rho[i] >= thr:
                density[i] = 1

        return density

    @nb.jit(nopython=False)
    def clu_f(self, C, density):
        row = list()
        col = list()
        for i in range(self.N):
            if density[i] == 0:
                for k1 in range(self.knn):
                    if C[i, k1] >= 0:
                        j = self.NN[i, k1]
                        if density[j] > 0:
                            row.append(i)
                            col.append(j)
                            break
                    else:
                        break
            else:
                for k1 in range(self.knn):
                    if C[i, k1] >= 0:
                        j = self.NN[i, k1]
                        if density[j] > 0:
                            row.append(i)
                            col.append(j)
                        if density[j] == 0:
                            break
                    else:
                        break

        data = list(np.ones(len(row)))
        graph = sparse.coo_matrix((data, (row, col)), shape=(self.N, self.N), copy=True)
        graph.eliminate_zeros()
        ci, y = connected_components(csgraph=graph, directed=False, return_labels=True)
        return y
