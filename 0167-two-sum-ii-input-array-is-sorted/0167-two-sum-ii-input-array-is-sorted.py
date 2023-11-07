class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        nums=numbers
        dict1={}
        dict1[nums[0]]=0
        for i in range(1,len(nums)):
            if dict1.get(target-nums[i])==None:
                dict1[nums[i]]=i
            else:
                return [dict1.get(target-nums[i])+1,i+1]
