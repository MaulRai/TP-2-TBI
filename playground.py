from compression import EliasGammaPostings

encoded_num = EliasGammaPostings.eg_encode([2,3,3,4])
# print(encoded_num)

decoded_num = EliasGammaPostings.eg_decode(encoded_num)
print(decoded_num)

# print(int('10100101', 2))




