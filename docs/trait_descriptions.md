### Distributions
Most distributions are considered over all the set of all (isogeny/isomorphism classes of) elliptic curves over $\mathbb{F}_{p}$ for fixed $p$. In some cases, we only consider (isogeny/isomorpism classes of) ordinary curves.

### a01
**Input:** elliptic curve $E/\mathbb{F}_{p}$, integer $r$

**Output:** tuple $(m, n)$ such that the group $E(\mathbb{F}_{p^r})$ is isomorphic to $\mathbb{Z}_m\times \mathbb{Z}_n$ and $m∣n$ (in particular, $m=1$ for cyclic groups)

**Motivation:** the group structure is not an isogeny invariant

**Distribution:** unknown (though Sato-Tate describes the distribution of $mn$)

### a02
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}$

**Output:** the factorization of $D = t^2-4p = v^2d_K$, where $t$ is the trace oof Frobenius of E and $d_K$ is the discriminant of the endomorphism algebra of $E$

**Motivation:** a large square factor of D has interesting implications

**Distribution:** unknown, probably reducible to the distribution of factors of random numbers using Sato-Tate

### a04
**Input:** elliptic curve $E/\mathbb{F}_{p}$, integer $k$

**Output:** the factorizations of $kn+1$ , $kn-1$, where $n=\#E(\mathbb{F}_p)$

**Motivation:** scalar multiplication by $kn\pm1$ is the identity or negation, respectively

**Distribution:** unknown, probably reducible to the distribution of factors of random numbers using Sato-Tate

### a05
**Input:** elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** $k_1,k_2,k_2/k_1$, where $k_1,k_2$ are the smallest integers satisfying $E[l]\cap E(\mathbb{F}_{p^{k_1}})\neq \empty$ and $E[l]\subseteq E(\mathbb{F}_{p^{k_2}})$

**Motivation:** low $k_1, k_2$ might lead to computable pairings

**Distribution:** unknown (but see page 50 in [Vojtěch Suchánek's diploma thesis](https://github.com/vojtechsu/isogenies/blob/master/master_thesis.pdf))

### a06
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}$, integer $r$

**Output:** the factorization of $D_r/D_1$ (which is a square), where $D_r = t_r^2-4p^{r}$ and $t_r$ is the trace of Frobenius of $E/\mathbb{F}_{p^r}$

**Motivation:** the prime factors of $D_r/D_1$ determine for which $l$ does the $l$-crater of E grow in the $r$-th extension

**Distribution:** unknown, probably reducible to the distribution of a02

### a08
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}$

**Output:** the class number of the maximal order of the endomorphism algebra of $E$

**Motivation:** the class number is a classical invariant

**Distribution:** unknown


### a12
**Input:** elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** $\phi(n)/m$ where $n=\#E(\mathbb{F}_p)$  and $m$ is the order of $l$ in the multiplicative group $\mathbb{Z}_{n}^\times$

**Motivation:** small $m$ might have implications for scalar multiplication

**Distribution:** unknown

### a22
**Input:** elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** the factorization of the $l$-th division polynomial

**Motivation:** this is partially relevant to a05

**Distribution:** unknown

### a23
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** the depth of the $l$-volcano and the degree of the crater subgraph(i.e., 2 is the degree of a circle crater, 1 for a segment and 0 for a point; more precisely: the degree is $1+\genfrac(){}{0}{d_K}{l}$) 

**Motivation:** the volcano structure might be relevant for cryptanalysis

**Distribution:** probably reducible (using Sato-Tate) to Chebotarev's theorem for the crater and to an elementary calculation for the depth (depth $s$ is equivalent to $t^2-4p$ being divisible by $l^{2s}$, where $t$ is the trace of Frobenius of $E$)

### a24
**Input:** elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** $i_1,i_2,i_2/i_1$ where $i_1,i_2$ are the smallest integers such that from  $E/\mathbb{F}_{p^{i_1}}$ there exists a ($\mathbb{F}_{p^{i_1}}$ rational) $l$-isogeny and from $E/\mathbb{F}_{p^{i_2}}$ there exist all $l+1$ ($\mathbb{F}_{p^{i_2}}$ rational) $l$-isogenies

**Motivation:** this is loosely related to a05 and a06

**Distribution:** unknown (but see page 50 in [Vojtěch Suchánek's diploma thesis](https://github.com/vojtechsu/isogenies/blob/master/master_thesis.pdf))

### a25
**Input:** elliptic curve $E/\mathbb{F}_{p}$, integer $r$

**Output:** factorization of $t_r$ (the trace of Frobenius of $E/\mathbb{F}_{p^r}$)

**Motivation:** loosely speaking, this somehow measures the "extent of supersingularity" (if we regard it as a spectrum) 

**Distribution:** probably reducible to the distribution of factors of random numbers (using Sato-Tate)

### i06
**Input:** elliptic curve $E/\mathbb{F}_{p}$

**Output:** factorization of square-free parts of $4p-1$ and $4n-1$ where $n$ is the order of the generator point of $E$

**Motivation:** inspired by the [4p-1 paper](https://crocs.fi.muni.cz/public/papers/Secrypt2019)

**Distribution:** probably reducible to the distribution of factors of random numbers (using Sato-Tate in the $4n-1$ case)

### i07
**Input:** elliptic curve $E/\mathbb{F}_{p}$

**Output:** distance of $n$ to the nearest power $2$ and the nearest multiple of 32 and 64, where $n=\#E(\mathbb{F}_p)$

**Motivation:** inspired by the paper [Big Numbers - Big Troubles](https://www.usenix.org/conference/usenixsecurity20/presentation/weiser)

**Distribution:** easily computable using Sato-Tate

### i13
**Input:** elliptic curve $E/\mathbb{F}_{p}$, integer $k$

**Output:** the number of points on $E$ with Hamming weight of the $x$-coordinate equal to $k$

**Motivation:** might be relevant for faulty RNG

**Distribution:** unknown