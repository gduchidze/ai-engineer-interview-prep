class PrefixSum:
    def __init__(self, arr):
        self.prefix_sum = [0] * (len(arr) + 1)
        for i in range(len(arr)):
            self.prefix_sum[i + 1] = self.prefix_sum[i] + arr[i]

    def range_sum(self, left, right):
        """Returns the sum of the subarray arr[left:right+1]."""
        return self.prefix_sum[right + 1] - self.prefix_sum[left]

# Example usage:
if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5]
    ps = PrefixSum(arr)
    print(ps.range_sum(1, 3))  # Output: 9 (2 + 3 + 4)
    print(ps.range_sum(0, 4))  # Output: 15 (1 + 2 + 3 + 4 + 5)