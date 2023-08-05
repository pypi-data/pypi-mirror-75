def solve():
    base = []
    for a, s in zip(A[::-1], S[::-1]):
        # print(f'a: {a}, s: {s}')
        # for i, y in enumerate(base):
        #     print('base{:d} {:3d}: {:05b}'.format(i, y, y))
        x = a
        for y in sorted(base, reverse=True):
            x = min(x, x ^ y)
            if s == "1" and a == 4:
                print(x)
        if x:
            if s == "0":
                # print('=>add {:3d}: {:05b}'.format(x, x))
                base.append(x)
            else:
                return 1
    return 0


t = int(input())
for _ in range(t):
    n = int(input())
    *A, = map(int, input().split())
    S = input()
    # print(f'A: {A}, S: {S}')
    # solve()
    print(solve())
    # print('-'*32)