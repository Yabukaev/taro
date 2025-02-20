import string
from sympy import nextprime, prevprime
import basen
import random


ALPHABET = string.digits + string.ascii_uppercase


class PseudoRandomSequence:
    def __init__(self, r, alphabet):
        self.range = r
        self.alphabet = alphabet
        self.prime = nextprime(self.range)
        self.root = self.mod_pow(self.generator(self.prime), self.closest_prime_to(self.prime // 2), self.prime)
        self.state = self.root
        self.dropped = 0
        # print(f"-- r: {self.range}")
        # print(f"   p: {self.prime}")
        # print(f"   k: {self.root}")
        # print(f"   s: {self.state}")

    def mod_pow(self, base, exp, mod):
        return pow(base, exp, mod)

    def generator(self, p):
        phi = p - 1
        factors = []
        n = phi
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                factors.append(i)
                while n % i == 0:
                    n //= i
        if n > 1:
            factors.append(n)
        
        for res in range(2, p):
            if all(self.mod_pow(res, phi // f, p) != 1 for f in factors):
                return res
        return -1

    def get(self):
        return self.state - 1

    def advance(self):
        self.dropped -= 1
        while True:
            self.state = (self.state * self.root) % self.prime
            self.dropped += 1
            if self.state <= self.range:
                break

    def reset(self):
        self.state = self.root
        self.dropped = 0

    def closest_prime_to(self, n):
        dn = prevprime(n)
        up = nextprime(n)
        return up if (n - dn) > (up - n) else dn

    def next_number(self, current_number=None):
        # Reset the state to the initial root
        self.reset()
        
        if current_number is None:
            # If no number is provided, return the first number
            
            result = self.get()
            return basen.int2base(result, self.alphabet).rjust(8,"0")
        
        current_number = basen.base2int(current_number, self.alphabet)

        # Advance until we find the current number
        while True:
            next_num = self.get()
            if next_num == current_number:
                # Advance to get the next number
                self.advance()
                result = self.get()
                return basen.int2base(result, self.alphabet).rjust(8,"0")
            self.advance()
        
        # If the current number is not found, return None or an error message
        return None

if __name__ == "__main__":
    r = 2821109907456
    prs = PseudoRandomSequence(r, ALPHABET)
    print("First number in the sequence:", prs.next_number())  # Outputs the first number
    x = prs.next_number()
    nums = []
    nums.append(x)
    # nums.append(1)
    
    for _ in range(10000):
        x = prs.next_number(x)
        if x in nums:
            print(f"error - {x} is in {nums}")
            break

        nums.append(x)
        print("next number in the sequence:", x)  # Outputs the first number
