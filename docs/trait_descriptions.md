Most distributions are considered over all the set of all (isogeny/isomorphism classes of) elliptic curves over $\mathbb{F}_{p}$ for fixed $p$. In some cases, we only consider (isogeny/isomorpism classes of) ordinary curves.

### a01

For every elliptic curve $E/\mathbb{F}_{p}$ and integer $r$ the group $E(\mathbb{F}_{p^r})$ is isomorphic to $\mathbb{Z}_n\times \mathbb{Z}_m$ or $\mathbb{Z}_n$. Given $E/\mathbb{F}_p$ and integer $r$, the function $a01$ returns the tuple $(n,m)$ or $(n,1)$.

For fixed $p$ the distribution of $mn$ is known (Sato-Tate). Distribution of $(m,n)$ is not known. 

### a02

If $E/\mathbb{F}_p$ is an ordinary curve and $t$ is its trace of $Frobenius then $D = t^2-4p = v^2d_K$ where $d_K$ is the discriminant of the endomorphism algebra of $E$. Given $E$, the function $a02$ returns $d_K$ and the factorization of $D$.

The distribution is not known. It probably can be reduced to the distribution of factors of random numbers.

### a04

Given a curve $E/\mathbb{F}_p$ and integer $k$, the function $a04$ returns the factorizations of $kn+1$ , $kn-1$ and the bit-length of their largest prime factor, where $n=\#E(\mathbb{F}_p)$. 

Motivation: Scalar multiplication by $kn\pm1$ is the identity or negation, respectively. 

The distribution is not known. It probably can be reduced to the distribution of factors of random numbers.

### a05

Given an elliptic curve $E/\mathbb{F}_p$ and a prime $l$, the function $a05$ returns $k_1,k_2,k_2/k_1$ where $k_1,k_2$ are the smallest integers satisfying $E[l]\cap E(\mathbb{F}_{p^{k_1}})\neq \empty$ and $E[l]\subseteq E(\mathbb{F}_{p^{k_2}})$. 

The distribution is not known (but see page 50 in <https://github.com/vojtechsu/isogenies/blob/master/master_thesis.pdf>).

### a06

If $E/\mathbb{F}_p$ is an ordinary curve and  $t_r$ is the trace of $E/\mathbb{F}_{p^r}$ then $D_r = t_r^2-4p^{r} = v_r^2d_K$ where $d_K$ is the discriminant of the endomorphism algebra of $E$. Given $E$ and $r$, the function $a02$ returns the factorization of $D_r/D_1$ (which is a square).

Motivation: the factors of $D_r/D_1$ determine for which $l$ does the crater of E grow in the $r$-th extension.

The distribution is not known.

### a08

Given an elliptic curve, the function $a08$ computes the class number of the maximal order of the endomorphism algebra.

The distribution is not known.

### a12

Given an elliptic curve $E/\mathbb{F}_p$ and prime $l$, the function $a12$ returns $m$ and the number of bits of $\phi(n)/m$ where $n=\#E(\mathbb{F}_p)$  and $m$ is the order of $l$ in the multiplicative group $\mathbb{Z}_{n}^\times$.  

The distribution is not known.

### a22

Given an elliptic curve, the function $a22$ returns the factorization of the $l$-th division polynomial and returns the list of factors, their degrees and the number of all the factors.

The distribution is not known.

### a23

Given an ordinary elliptic curve $E/\mathbb{F}_p$ and prime $l$, the function $a23$ returns the depth of the $l$-volcano and the degree of the crater subgraph, i.e. 2 is the degree of a circle crater, 1 for segment and 0 for point (more precisely: the degree is $1+\genfrac(){}{0}{d_K}{l}$) 

The distribution of the crater should be given by Chebotarev's theorem. The distribution of the depth is elementary ($1/l^{2s}$ that the depth is $s$).

### a24

Given an elliptic curve $E/\mathbb{F}_p$ and a prime $l$, the function $a24$ returns $i_1,i_2,i_2/i_1$ where $i_1,i_2$ are the smallest integers such that from  $E/\mathbb{F}_{p^{i_1}}$ there exists a ($\mathbb{F}_{p^{i_1}}$ rational) $l$-isogeny and from $E/\mathbb{F}_{p^{i_2}}$ there exist all $l+1$ ($\mathbb{F}_{p^{i_2}}$ rational) $l$-isogenies.

The distribution of $i_1$ is not known (but see page 50 in <https://github.com/vojtechsu/isogenies/blob/master/master_thesis.pdf>).

### a25

Given an elliptic curve $E/\mathbb{F}_p$ and integer $r$, the function $a25$ returns the trace $t_r$ of $E/\mathbb{F}_{p^r}$, its factorization and the number of prime factors in this factorization.

The distribution can probably be reduced to the distribution of factors of random numbers (using Sato-Tate).

### i06

Given an elliptic curve $E/\mathbb{F}_p$, the function $i06$ returns the square parts of $4p-1$ and $4m-1$ where $m$ is the size of the prime order subgroup of $E(\mathbb{F}_p)$.

The distribution is not known. It can probably be reduced to the distribution of factors of random numbers.

### i07

Given an elliptic curve $E/\mathbb{F}_p$, the function $i07$ returns the distance of $n$ to the nearest power $2$ and the nearest multiple of 32 and 64, where $n=\#E(\mathbb{F}_p)$. This is inspired by the paper [Big Numbers - Big Troubles](https://www.usenix.org/conference/usenixsecurity20/presentation/weiser).

The distribution should be easy to compute using Sato-Tate.


### i13

Given an elliptic curve $E/\mathbb{F}_p$ and a scalar $k$, the function $i13$ returns the number of points on E with Hamming weight of the $x$-coordinate equal to $k$.

The distribution is not known.