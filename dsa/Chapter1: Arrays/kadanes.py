def kadanes(arr):
    max_sum = arr[0]
    cur_sum = 0

    for num in arr:
        cur_sum += num
        if cur_sum > max_sum:
            max_sum = cur_sum
        if cur_sum < 0:
            cur_sum = 0
    return max_sum

# Example usage:
array = [-2,1,-3,4,-1,2,1,-5,4]
print("Maximum subarray sum is:", kadanes(array))
# Output: Maximum subarray sum is: 6