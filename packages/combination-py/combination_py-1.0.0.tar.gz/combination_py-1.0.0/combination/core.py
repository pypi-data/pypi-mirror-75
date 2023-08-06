class Combination:

    def __init__(self, n_max, mod=10**9+7):
        # O(n_max + log(mod))
        f = 1
        self.mod = mod
        self.factorials = factorials = [f]
        for i in range(1, n_max + 1):
            f *= i % mod
            factorials.append(f)
        f = pow(f, mod - 2, mod)
        self.invs = invs = [f]
        for i in range(n_max, 0, -1):
            f *= i % mod
            invs.append(f)
        invs.reverse()

    def nCr(self, n, r):
        if not 0 <= r <= n:
            return 0
        return self.factorials[n] * self.invs[r] % self.mod * self.invs[n - r] % self.mod

    def nPr(self, n, r):
        if not 0 <= r <= n:
            return 0
        return self.factorials[n] * self.invs[n - r] % self.mod

    def nHr(self, n, r):
        if (n == 0 and r > 0) or r < 0:
            return 0
        return self.factorials[n + r - 1] * self.invs[r] % self.mod * self.invs[n - 1] % self.mod

    def rising_factorial(self, n, r):
        return self.factorials[n + r - 1] * self.invs[n - 1] % self.mod

    def stirling_first(self, n, k):
        if n == k:
            return 1
        if k == 0:
            return 0
        return (self.stirling_first(n - 1, k - 1) + (n - 1) * self.stirling_first(n - 1, k)) % self.mod

    def stirling_second(self, n, k):
        if n == k:
            return 1
        value = 0
        for m in range(1, k + 1):
            value += (-1) ** (k - m) * self.nCr(k, m) * pow(m, n, self.mod)
        return self.invs[k] * value % self.mod

    def balls_and_boxes_3(self, n, k):
        value = 0
        for m in range(1, k + 1):
            value += (-1) ** (k - m) * self.nCr(k, m) * pow(m, n, self.mod)
            value %= self.mod
        return value

    def bernoulli(self, n):
        if n == 0:
            return 1
        if n % 2 and n >= 3:
            return 0
        value = 0
        for k in range(n):
            value += self.nCr(n + 1, k) * self.bernoulli(k) % self.mod
        return (- pow(n + 1, self.mod - 2, self.mod) * value) % self.mod

    def faulhaber(self, k, n):
        value = 0
        for i in range(k + 1):
            value += self.nCr(k + 1, i) * self.bernoulli(i) % self.mod * pow(n, k - i + 1, self.mod) % self.mod
        return pow(k + 1, self.mod - 2, self.mod) * value % self.mod

    def lah(self, n, k):
        return self.nCr(n - 1, k - 1) * self.factorials[n] % self.mod * self.invs[k] % self.mod

    def bell(self, n, k):
        value = 0
        for i in range(1, k + 1):
            value += self.stirling_second(n, i)
            value %= self.mod
        return value
