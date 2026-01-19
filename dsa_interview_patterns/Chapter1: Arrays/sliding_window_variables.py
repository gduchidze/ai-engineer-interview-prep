# Find the length of the longest subarray with the same value in each position.

def longest_uniform_subarray(arr):
    max_length = 0
    left = 0

    for right in range(len(arr)):
        # If the current element is different from the leftmost element,
        # move the left pointer to the right
        if arr[right] != arr[left]:
            left = right

        # Update the maximum length found
        current_length = right - left + 1
        max_length = max(max_length, current_length)

    return max_length

# find the minimum length of a subarray where the sum is greater the or the equal to a target value. assume all elements are positive integers.

def min_subarray_length(target, arr):
    left = 0
    current_sum = 0
    min_length = float('inf')

    for right in range(len(arr)):
        current_sum += arr[right]

        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1

    return min_length if min_length != float('inf') else 0



# Example usage
array = [1, 1, 2, 2, 2, 3, 3, 3, 3, 3]
result = longest_uniform_subarray(array)
print(f"The length of the longest uniform subarray is: {result}")
# Output: The length of the longest uniform subarray is: 5