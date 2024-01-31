from words import word_to_primitive, quick_sort, nub

L = ["abababab","abababa","cabbcacabbca", "aabb","ba","ab"]

M = [(w,word_to_primitive(w)) for w in L]

print(M)

N = [(w,quick_sort(w),nub(w)) for w in L]

print(N)