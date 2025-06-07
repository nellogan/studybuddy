#File: LongestSubstringWithoutRepeatingCharacters.py
#Question URL: https://leetcode.com/problems/longest-substring-without-repeating-characters/
#Solution URL:
#Difficulty: Medium
#Estimated Time: 30 minutes
#Start Time: 
#End Time: 
#Time Taken: 
#Passed: 
#NOTE: 


from typing import *
from collections import defaultdict
from collections import deque
from heapq import heappush, heappop, heapify
from queue import PriorityQueue
from math import inf, sqrt, gcd

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        
# arg = None
# test = Solution().method(arg)
# print(f"test {test}")
