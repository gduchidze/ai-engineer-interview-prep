# Given an array return True
# If there are two elements within an windows
# of size k that are equal

arr = [1,2,3,2,3,3]

def sliding_window_fixed(arr, k):
    for l in range(len(arr)):
        for R in range(l+1, min(l+k, len(arr))):
            if arr[l] == arr[R]:
                return True
    return False

def sliding_window_fixed_2(arr, k):
    window = set()
    for i in range(len(arr)):
        if arr[i] in window:
            return True
        window.add(arr[i])
        if len(window) > k:
            window.remove(arr[i - k])
    return False

print(sliding_window_fixed(arr, 3))