def brute_force(arr):
    max_sum = float('-inf')
    n = len(arr)

    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum > max_sum:
                max_sum = current_sum

    return max_sum

# Example usage
array = [-2,1,-3,4,-1,2,1,-5,4]
print("Maximum subarray sum is:", brute_force(array))