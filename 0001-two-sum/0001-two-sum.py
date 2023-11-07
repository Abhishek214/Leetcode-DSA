class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dict1={}
        dict1[nums[0]]=0
        for i in range(1,len(nums)):
            if dict1.get(target-nums[i])==None:
                dict1[nums[i]]=i
            else:
                return [dict1.get(target-nums[i]),i]


        # l = 0
        # r = len(nums) - 1
        # nums1=list(nums)
        # nums=sorted(nums)
        # while l < r:  # Update the while loop condition
        #     if nums[l] + nums[r] == target:
        #         return [nums1.index(nums[l]),nums1.index(nums[r])]
        #     elif nums[l] + nums[r] > target:
        #         r = r - 1
        #     else:
        #         l = l + 1

        # return []  # Return an empty list if no two elements sum up to the target
    