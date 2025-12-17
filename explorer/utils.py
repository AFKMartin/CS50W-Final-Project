# Helper to collatz conjeture
def collatz_seq(n, max_steps=1000):
    seq = [n]
    max_val = n
    steps = 0

    while n != 1 and steps < max_steps:
        
        # n is even
        if n % 2 == 0: 
            n = n // 2

        # n is odd
        else:
            n = 3 * n + 1 
        
        seq.append(n) 
        max_val = max(max_val, n)
        steps += 1
    
    return {
        "sequence" : seq,
        "steps" : steps,
        "max_value" : max_val,
        "truncated": steps == max_steps,
    }
