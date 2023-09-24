class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res=set()
        for k in range(len(nums)-2):
            while k>0 and nums[k]==nums[k-1]:
                if k==len(nums)-2:
                    return res
                k+=1
            i=k+1
            j=len(nums)-1
            target=-nums[k]
            while i<j:
                n=nums[i]+nums[j]
                if n==target:
                    res.add((nums[k],nums[i],nums[j]))
                    i+=1
                    j-=1
                    while nums[i]==nums[i-1] and i<j:
                        i+=1
                    while nums[j]==nums[j+1] and i<j:
                        j-=1
                elif n>target:
                    j-=1
                else:
                    i+=1
        return res
                














        # nums.sort()
        # i=0
        # result=set()
        # while i<len(nums)-2:
        #     if i>0 and nums[i]==nums[i-1]:
        #         i+=1
        #         continue
         
        #     j=i+1
        #     k=len(nums)-1
        #     while k>j:
        #         n=nums[i]+nums[j]+nums[k]
        #         if n==0:
        #             result.add((nums[i],nums[j],nums[k]))
        #             j+=1
        #             k-=1
        #             while j<k and nums[j]==nums[j-1]:
        #                 j+=1
        #             while j<k and nums[k]==nums[k+1]:
        #                 k-=1
        #         elif n>0:
        #             k-=1
        #         else:
        #             j+=1
        #     i+=1
        # return result

# 2nd Solution
        # result=set()
        # len0=len(list(filter(lambda x: x==0,nums)))
        # from functools import reduce
        # check_pos=list(filter(lambda x: x>=0,nums))
        # check_neg=list(filter(lambda x: x<0,nums))
        # if len(check_pos)==len(nums):
        #     if len0>=3:
        #         return [[0,0,0]]
        #     else:
        #         return []

        # elif len(check_neg)==len(nums):

        #     return [] 
        # else:
        #     if len0>=3:
        #         result.add((0,0,0))
        # a=check_pos
        # b=check_neg
        # s1=0
        # s2=0
        # e1=s1+1
        # e2=s2+1       
        # while s1<len(a)-1 or s2<len(b)-1:
        #     if s2<len(b)-1 and (-b[s2]-b[e2]) in a:
        #         n=tuple(sorted([b[s2],b[e2],(-b[s2]-b[e2])]))
        #         result.add(n)
        #     if s1<len(a)-1 and (-a[s1]-a[e1]) in b:
        #         n=tuple(sorted([a[s1],a[e1],(-a[s1]-a[e1])]))
        #         result.add(n)
        #     if e1==len(a)-1:
        #         s1+=1
        #         e1=s1+1
        #     else:
        #         e1+=1
                
        #     if e2==len(b)-1:
        #         s2+=1
        #         e2=s2+1
        #     else:
        #         e2+=1

        # return result
