class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        dict1={}
        for i in s:
            dict1[i]=dict1.get(i,0) + 1
        
        for j in t:
            if j not in dict1.keys():
                return False
            
            dict1[j]=dict1.get(j)-1

        if all(i==0 for i in dict1.values()):
            return True
        else:
            return False