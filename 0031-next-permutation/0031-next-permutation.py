class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        n=len(nums)
        j=n-2
        while j>=0 and nums[j]>=nums[j+1]:
            j-=1
        if j<0:
            nums.sort()
        i=j+1
        while i<n and nums[i]>nums[j]:
            i+=1
        nums[j], nums[i-1] = nums[i-1], nums[j]
        # nums[j+1:n]=sorted(nums[j+1:n])
        for k in range(j+1,n):
            i=j+1
            while i<n-1:
                if nums[i]>nums[i+1]:
                    nums[i], nums[i+1] = nums[i+1], nums[i]
                i+=1


        
        # def get_permutation(nums):
        #     if len(nums)==1:
        #         return [nums]
        #     temp=[]
        #     for i in range(len(nums)):
        #         a=nums.copy()
        #         a.pop(i)
        #         # OR a = nums[:i] + nums[i+1:]
        #         h=get_permutation(a)
        #         for k in h:      
        #             temp.append([nums[i]]+k)
        #     return temp

        # permutation=get_permutation(nums)
        # permutation=sorted(list(set([tuple(i) for i in permutation])))

        # i=0
        # while i<len(permutation) and permutation[i]!=tuple(nums):
        #     i+=1
        # if i==len(permutation)-1:
        #     nums[:]=permutation[0]
        # else:
        #     nums[:]=permutation[i+1]
        # return nums
