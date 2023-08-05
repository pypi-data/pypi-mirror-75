"""
.. module:: kitsunejf
   :platform: Unix, MacOSX
   :synopsis: interface function to jellyfish

.. moduleauthor:: Natapol Pornputtapong <natapol.p@chula.ac.th>


"""
import os
import sys
import copy
import math
import shutil
import platform
import tempfile
import warnings
import subprocess
import collections

import numpy as np
from tqdm import tqdm
from scipy.stats import chi2
from scipy.spatial import distance
from scipy.special import loggamma


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class NoInput(Exception):
    """Do X and return a list."""
    pass

if platform.system() == 'Darwin':
    jellyfishpath = os.path.join(__location__, 'modules', "jellyfish-macosx")
elif platform.system() == 'Linux':
    jellyfishpath = os.path.join(__location__, 'modules', "jellyfish-linux")
else:
    raise Exception("Windows are not supported.")

class JellyFishError(Exception):
    def __init__(self, error_message):
        self.message = f"JellyFish dumping error: {error_message}"


very_small_number = 1e-100

def evo_transform(dist, kmer):
    """
    follow 1. Fan H, Ives AR, Surget-Groba Y, Cannon CH. 
    An assembly and alignment-free method of phylogeny reconstruction from 
    next-generation sequencing data. BMC Genomics [Internet]. 
    2015 Jul 14 [cited 2020 Apr 17];16(1):522.
    D = (-1/k) * log(distance)
    """
    j = very_small_number if dist <= 0 else dist
    return (-1/kmer) *  math.log(j)


# def phylogenetic_distance(u, v, kmer):
#     """
#     follow 1. Fan H, Ives AR, Surget-Groba Y, Cannon CH. 
#     An assembly and alignment-free method of phylogeny reconstruction from 
#     next-generation sequencing data. BMC Genomics [Internet]. 
#     2015 Jul 14 [cited 2020 Apr 17];16(1):522.
#     D=-1/k log ns/nt
#     """
#     return (-1/kmer) *  math.log(np.logical_and(u, v)/np.logical_or(u, v))

def mash(u, v, kmer):
    """Do X and return a list."""
    j = 1 - distance.jaccard(u, v)
    j = very_small_number if j <= 0 else j
    return (-1/kmer) * math.log(2*j/(1+j))

def jsmash(u, v, kmer):
    """Do X and return a list."""
    j = 1 - distance.jensenshannon(u, v)
    j = very_small_number if j <= 0 else j
    return (-1/kmer) * math.log(2*j/(1+j))


def nCr(n, r):
    """
    Calculate combinatorial using gamma funcion for huge number
    """
    logncr = loggamma(n+1) - loggamma(r+1) - loggamma(n-r+1)
    return math.exp(logncr)

def jaccarddistp(u, v):
    """
    Do X and return a list.
    """
    m = len(u)
    pu = u.sum()/m
    pv = v.sum()/m

    degenerate = False

    expectation = ((pu*pv)/(pu+pv-pu*pv))

    j_obs = np.logical_and(u, v).sum() / np.logical_or(u, v).sum() - expectation

    if(pu == 1 or pv == 1 or u.sum() == len(u) or v.sum() == len(v)):
        warnings.warn("One or both input vectors contain only 1's.", Warning)
        degenerate = True

    if(pu == 0 or pv == 0 or u.sum() == 0 or v.sum() == 0):
        warnings.warn("One or both input vectors contain only 0's", Warning)
        degenerate = True

    if degenerate:
        return 1.0

    # tan = jaccard_mca_rcpp(px,py,m,j.obs,accuracy)
    # pvalue = tan$pvalue

    #   pvalue <- switch(error.type, lower = pvalue, average = pvalue/tan$accuracy,
    #                upper = pvalue + 1 - tan$accuracy)

    # return(
    #     list(
    #     statistics = j.obs,
    #     pvalue = pvalue,
    #     expectation = expectation,
    #     accuracy = 1 - tan$accuracy,
    #     error.type = error.type
    #     )
    # )
    # Compute p-value using an asymptotic approximation

    q = [pu*pv, pu+pv-2*pu*pv]
    qq = q[0] + q[1]
    sigma = q[0] * q[1] * (1-q[0]) / (qq ** 3)
    norm = math.sqrt(m) * j_obs / math.sqrt(sigma)
    return chi2.pdf(norm*norm, 1)

def euclidean_of_frequency(u, v):
    """
    euclidean distance of frequency
    """
    return distance.euclidean(u, v)

DISTANCE_FUNCTION = {
    'braycurtis': distance.braycurtis,
    'canberra': distance.canberra,
    'chebyshev': distance.chebyshev,
    'cityblock': distance.cityblock,
    'correlation': distance.correlation,
    'cosine': distance.cosine,
    'dice': distance.dice,
    'euclidean': distance.euclidean,
    'hamming': distance.hamming,
    'jaccard': distance.jaccard,
    'kulsinski': distance.kulsinski,
    'rogerstanimoto': distance.rogerstanimoto,
    'russellrao': distance.russellrao,
    'sokalmichener': distance.sokalmichener,
    'sokalsneath': distance.sokalsneath,
    'sqeuclidean': distance.sqeuclidean,
    'yule': distance.yule,
    'jensenshannon': distance.jensenshannon,
    'mash': mash,
    'jsmash' : jsmash,
    'jaccarddistp': jaccarddistp,
    'euclidean_of_frequency': euclidean_of_frequency
}

NUMERIC_DISTANCE = [
    distance.braycurtis,
    distance.canberra,
    distance.chebyshev,
    distance.cityblock,
    distance.correlation,
    distance.cosine,
    distance.euclidean,
    distance.sqeuclidean
]

BOOLEAN_DISTANCE = [
    distance.dice,
    distance.hamming,
    distance.jaccard,
    jaccarddistp,
    distance.kulsinski,
    distance.rogerstanimoto,
    distance.russellrao,
    distance.sokalmichener,
    distance.sokalsneath,
    distance.yule
]

PROB_DISTANCE = [
    distance.jensenshannon,
    euclidean_of_frequency
]

class Kmercount(collections.Counter):
    """Do X and return a list."""
    def __init__(self, fsa, k_mer, **karg):

        self.kmer = k_mer

        if 'thread' not in karg:
            karg['thread'] = 1
        if 'lower' not in karg:
            karg['lower'] = 1
        if 'bchashsize' not in karg: #hashsize for jellyfish bc step
            karg['bchashsize'] = '1G'
        if 'hashsize' not in karg: #hashsize for jellyfish count step
            karg['hashsize'] = '100M'
        if 'canonical' not in karg or not karg['canonical']:
            canonical = ''
        else:
            canonical = '-C'

        if not os.path.isfile(fsa):
            raise NoInput('input is missing')

        filebasename = os.path.basename(fsa)

        with tempfile.TemporaryDirectory() as tmpdirname:

            if 'fast' in karg and karg['fast']:
                # for genome with one step
                dumpdata = subprocess.getoutput("""
                    {0} count {8} -m {1} -s {3} -t {4} -o {5}.jf {6}
                    {0} dump -c -L {7} {5}.jf
                    """.format(
                        jellyfishpath,
                        self.kmer,
                        karg['bchashsize'],
                        karg['hashsize'],
                        karg['thread'],
                        os.path.join(tmpdirname, filebasename),
                        fsa,
                        karg['lower'],
                        canonical
                    )
                )
            else:
                dumpdata = subprocess.getoutput("""
                    {0} bc {8} -m {1} -s {2} -t {4} -o {5}.bc {6}
                    {0} count {8} -m {1} -s {3} -t {4} --bc {5}.bc -o {5}.jf {6}
                    {0} dump -c -L {7} {5}.jf
                    """.format(
                        jellyfishpath,
                        self.kmer,
                        karg['bchashsize'],
                        karg['hashsize'],
                        karg['thread'],
                        os.path.join(tmpdirname, filebasename),
                        fsa,
                        karg['lower'],
                        canonical
                    )
                )

        datadict = {}
        if not dumpdata.startswith("Bloom filter file is truncated"):
            try:
                for line in dumpdata.split('\n'):
                    dat = line.rstrip().split(' ')
                    datadict[dat[0]] = int(dat[1])
            except ValueError:
                raise JellyFishError("Bloom filter file is truncated.")
        else:
            raise JellyFishError("Bloom filter file is truncated.")
        super(Kmercount, self).__init__(datadict)

        # assign instance variable
        self.sum = sum(self.values())
        self.name = '.'.join(filebasename.split('.')[0:-1]).replace(' ', '_')

    def __repr__(self):
        return self.name

    def dist(self, other, dist_func, transform=False):
        """Do X and return a list."""
        a, b = self.norm(other)
        if dist_func is mash:
            dist = dist_func(a.astype(bool), b.astype(bool), self.kmer)
        elif dist_func is jsmash:
            dist = dist_func(a.astype(float)/a.sum(), b.astype(float)/b.sum(), self.kmer)
        elif dist_func in BOOLEAN_DISTANCE:
            print(a.astype(bool), b.astype(bool))
            dist = dist_func(a.astype(bool), b.astype(bool))
        elif dist_func in PROB_DISTANCE:
            dist = dist_func(a.astype(float)/a.sum(), b.astype(float)/b.sum())
        else:
            dist = dist_func(a, b)

        dist = very_small_number if math.isnan(dist) else dist
        if transform and dist_func not in [mash, jsmash] + NUMERIC_DISTANCE:
            dist = evo_transform(dist, self.kmer)
        
        return dist

    def norm(self, other):
        """Do X and return a list."""
        mers = list(self.keys())
        mers.extend(list(other.keys()))
        mers = list(set(mers))
        a = []
        b = []
        for mer in mers:
            a.append(self[mer])
            b.append(other[mer])
        return np.array(a), np.array(b)

if __name__ == "__main__":
    pass
