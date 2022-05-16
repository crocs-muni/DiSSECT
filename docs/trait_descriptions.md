### Distributions
Most distributions are considered over all the set of all (isogeny/isomorphism classes of) elliptic curves over $\mathbb{F}_{p}$ for fixed $p$. In some cases, we only consider (isogeny/isomorpism classes of) ordinary curves. Also denote $N$ as the cardinality of $E$ and $t=\log(N)$.

### smith
**Input:** elliptic curve $E/\mathbb{F}_{p}$, integer $r$

**Output:** tuple $(m, n)$ such that the group $E(\mathbb{F}_{p^r})$ is isomorphic to $\mathbb{Z}_m\times \mathbb{Z}_n$ and $m∣n$ (in particular, $m=1$ for cyclic groups)

**Motivation:** the group structure is not an isogeny invariant

**Distribution:** unknown (though Sato-Tate describes the distribution of $mn$)

**Time complexity:** Baby-step giant-step algorithm: O(\sqrt{N})

### discriminant
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}$

**Output:** the factorization of $D = t^2-4p = v^2d_K$, where $t$ is the trace of Frobenius of E and $d_K$ is the discriminant of the endomorphism algebra of $E$

**Motivation:** a large square factor of D has interesting implications

**Distribution:** unknown, probably reducible to the distribution of factors of random numbers using Sato-Tate

**Time complexity:** Factorization of $t$-bit number

### twist_order
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}, integer $r$

**Output:** the factorization of the cardinality of the quadratic twist of $E(\mathbb{F}_{p^r})$

**Motivation:** smooth cardinality of a quadratic twist might allow attacks on some implementations

**Distribution:** unknown, probably reducible to the distribution of factors of random numbers using Sato-Tate

**Time complexity:** Factorization of $t$-bit number

### kn_factorization
**Input:** elliptic curve $E/\mathbb{F}_{p}$, integer $k$

**Output:** the factorizations of $kn+1$ , $kn-1$, where $n=\#E(\mathbb{F}_p)$

**Motivation:** scalar multiplication by $kn\pm1$ is the identity or negation, respectively; it can be seen as a generalization of https://link.springer.com/content/pdf/10.1007%2F11761679_1.pdf

**Distribution:** unknown, probably reducible to the distribution of factors of random numbers using Sato-Tate

**Time complexity:** Factorization of $t$-bit number

### torsion_extension
**Input:** elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** $k_1,k_2,k_2/k_1$, where $k_1,k_2$ are the smallest integers satisfying $E[l]\cap E(\mathbb{F}_{p^{k_1}})\neq \empty$ and $E[l]\subseteq E(\mathbb{F}_{p^{k_2}})$

**Motivation:** low $k_1, k_2$ might lead to computable pairings

**Distribution:** unknown (but see page 50 in [Vojtěch Suchánek's diploma thesis](https://github.com/vojtechsu/isogenies/blob/master/master_thesis.pdf))

**Time complexity:**Up to 20 scalar multiplications on $t$-bit curve

### conductor
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}$, integer $r$

**Output:** the factorization of $D_r/D_1$ (which is a square), where $D_r = t_r^2-4p^{r}$ and $t_r$ is the trace of Frobenius of $E/\mathbb{F}_{p^r}$

**Motivation:** the prime factors of $D_r/D_1$ determine for which $l$ does the $l$-crater of E grow in the $r$-th extension

**Distribution:** unknown, probably reducible to the distribution of discriminant

**Time complexity:** Factorization of $t/2$-bit number

### embedding
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}$

**Output:** the embedding degree complement, i.e., $\phi(l)/e$, where $l$ is the generator order (presumed prime) and $e$ is the multiplicative order of $q$ modulo $l$.

**Motivation:** low embedding degrees might allow the MOV attack

**Distribution:** unknown

**Time complexity:** Computation of multiplicative order in $t$-bit prime field. (precomputed)

### class_number
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}$

**Output:** the class number of the maximal order of the endomorphism algebra of $E$

**Motivation:** the class number is a classical invariant

**Distribution:** unknown

**Time complexity:** Factorization of $t$-bit number (precomputed).


### small_prime_order
**Input:** elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** $\phi(n)/m$ where $n=\#E(\mathbb{F}_p)$  and $m$ is the order of $l$ in the multiplicative group $\mathbb{Z}_{n}^\times$

**Motivation:** small $m$ might have implications for scalar multiplication

**Distribution:** unknown, but see [Artin’s primitive root conjecture](https://guests.mpim-bonn.mpg.de/moree/surva.pdf)

**Time complexity:** Computation of multiplicative order in $t$-bit prime field. 

### division_polynomials
**Input:** elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** the factorization of the $l$-th division polynomial

**Motivation:** this is partially relevant to torsion_extension

**Distribution:** [Factorisation_patterns_of_division_polynomials](https://www.researchgate.net/publication/38339355_Factorisation_patterns_of_division_polynomials)

**Time complexity:** Factorization of $(l^2-1)$-degree polynomial over $t$-bit prime field

### volcano
**Input:** ordinary elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** the depth of the $l$-volcano and the degree of the crater subgraph(i.e., 2 is the degree of a circle crater, 1 for a segment and 0 for a point; more precisely: the degree is $1+\genfrac(){}{0}{d_K}{l}$) 

**Motivation:** the volcano structure might be relevant for cryptanalysis

**Distribution:** probably reducible (using Sato-Tate) to Chebotarev's theorem for the crater and to an elementary calculation for the depth (depth $s$ is equivalent to $t^2-4p$ being divisible by $l^{2s}$, where $t$ is the trace of Frobenius of $E$)

**Time complexity:** Legendre symbol of $t$-bit number modulo small prime

### isogeny_extension
**Input:** elliptic curve $E/\mathbb{F}_{p}$, prime $l$

**Output:** $i_1,i_2,i_2/i_1$ where $i_1,i_2$ are the smallest integers such that from  $E/\mathbb{F}_{p^{i_1}}$ there exists a ($\mathbb{F}_{p^{i_1}}$ rational) $l$-isogeny and from $E/\mathbb{F}_{p^{i_2}}$ there exist all $l+1$ ($\mathbb{F}_{p^{i_2}}$ rational) $l$-isogenies

**Motivation:** this is loosely related to torsion_extension and conductor

**Distribution:** unknown (but see page 50 in [Vojtěch Suchánek's diploma thesis](https://github.com/vojtechsu/isogenies/blob/master/master_thesis.pdf))

**Time complexity:** Up to 20 scalar multiplications on $t$-bit curve

### trace_factorization
**Input:** elliptic curve $E/\mathbb{F}_{p}$, integer $r$

**Output:** factorization of $t_r$ (the trace of Frobenius of $E/\mathbb{F}_{p^r}$)

**Motivation:** loosely speaking, this somehow measures the "extent of supersingularity" (if we regard it as a spectrum) 

**Distribution:** probably reducible to the distribution of factors of random numbers (using Sato-Tate)

**Time complexity:** Factorization of $(deg\cdot t)$-bit number

### isogeny_neighbors
**Input:** elliptic curve $E/\mathbb{F}_{p}$, small prime $l$

**Output:** Number of roots of $\Phi_l(j(E),x)$ where $\Phi_l$ is the $l$-th modular polynomial.

**Motivation:** These roots correspond to $l$-isogenous curves.

**Distribution:** Except for finite number of cases there should be only 2 or 0 roots (equally distributed).

**Time complexity:** Factorization of $(l+1)$-degree polynomial over $t$-bit prime field

### q_torsion

**Input:** elliptic curve $E/\mathbb{F}_{p}:y^2=x^3+ax+b$

**Output:** Torsion order of $E'(\mathbb{Q})$ where $E'$ is is given by the same equation $y^2=x^3+ax+b$

**Motivation:** Inspired by the lifting of ECDLP to curve over $\mathbb{Q}$.

**Distribution:** Mazur's theorem states that the order is bounded by 16. 

**Time complexity:** Doud's algorithm: $O(t^3)$


### hamming_x
**Input:** elliptic curve $E/\mathbb{F}_{p}$, integer $k$

**Output:** number of points on $E$ with the Hamming weight of the $x$-coordinate equal to $k$

**Motivation:** might be relevant for faulty RNG

**Distribution:** binomial with mean $\frac{1}{2} ⋅\choose{⌈\log p⌉+1}{k}

**Time complexity:** Binomial($\log(n)$,$k$)-many Legendre symbols in $t$-bit prime field

### square_4p1
**Input:** elliptic curve $E/\mathbb{F}_{p}$

**Output:** factorization of square-free parts of $4p-1$ and $4n-1$ where $n$ is the order of the generator point of $E$

**Motivation:** inspired by the [4p-1 paper](https://crocs.fi.muni.cz/public/papers/Secrypt2019)

**Distribution:** probably reducible to the distribution of factors of random numbers (using Sato-Tate in the $4n-1$ case)

**Time complexity:** Factorization of $t$-bit number

### pow_distance
**Input:** elliptic curve $E/\mathbb{F}_{p}$

**Output:** distance of $n$ to the nearest power of $2$ and the nearest multiple of 32 and 64, where $n=\#E(\mathbb{F}_p)$

**Motivation:** the first part is related to scalar multiplication bias when not using rejection sampling, the second is inspired by the paper [Big Numbers - Big Troubles](https://www.usenix.org/conference/usenixsecurity20/presentation/weiser)

**Time complexity:** Division in $t$-bit prime field

### multiples_x
**Input:** elliptic curve $E/\mathbb{F}_{p}$ with generator $G$, integer $k$

**Output:** the $x$-coordinate of $\frac{1}{k}G$

**Motivation:** the strange behaviour of secp224k1 and secp256k1 for k=2

**Distribution:** presumably geometric with quotient $\frac{1}{2}$

**Time complexity:** One scalar multiplication on $t$-bit curve

### x962_invariant

**Input:** elliptic curve $E/\mathbb{F}_{p}:y^2=x^3+ax+b$

**Output:** $r = \frac{a^3}{b^2}$

**Motivation:** The value $r$ is used for generation of curves in various standards including x962, FIPS, SECG etc.

**Distribution:** Uniform

**Time complexity:** Division in $t$-bit prime field

### brainpool_overlap

**Input:** elliptic curve $E/\mathbb{F}_{p}:y^2=x^3+ax+b$ where $p$ has bit-length $t$

**Output:** $a_{160}-b_{-160}$ where $a_{160}$ is the $t-160$ rightmost bits of $a$ and $b_{-160}$ is the $t-160$ leftmost bits of $b$.

**Motivation:** The Brainpool construction causes the result to be 0 half of the time.

**Distribution:** Uniform

**Time complexity:** Subtraction in $t$-bit prime field 

### weierstrass
