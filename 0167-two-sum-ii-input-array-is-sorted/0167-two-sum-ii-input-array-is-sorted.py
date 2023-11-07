class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        nums=numbers

        l = 0
        r = len(nums) - 1
        nums1=list(nums)
        nums=sorted(nums)
        while l < r:  # Update the while loop condition
            if nums[l] + nums[r] == target:
                return [l+1,r+1]
            elif nums[l] + nums[r] > target:
                r = r - 1
            else:
                l = l + 1

        return []  # Return an empty list if no two elements sum up to the target
    