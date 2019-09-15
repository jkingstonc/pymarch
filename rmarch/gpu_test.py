import numpy as np
from numba import vectorize
import time

@vectorize(['float32(float32, float32)'], target='cuda')
def pow(a, b):
    return a ** b

def main():
    vec_size = 100000000

    a = b = np.array(np.random.sample(vec_size), dtype=np.float32)
    c = np.zeros(vec_size, dtype=np.float32)

    start_time = time.time()
    c = pow(a, b)
    print(time.time() - start_time)

    print(c)

if __name__ == '__main__':
    main()
