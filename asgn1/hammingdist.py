def dumb_search(source, target):
    source_length = len(source)
    target_length = len(target)
    result = []
    for i in range(source_length - target_length + 1):
        hammingdist = 0
        for j in range(target_length):
            if source[i+j] != target[j]:
                hammingdist += 1

        if hammingdist < 2:
            result.append(i)
    return result


if __name__ == '__main__':
    source = "abcabb"
    target = "abc"
    print(dumb_search(source, target))



"""
a  a  c  c  a  a  b
   1  0
#aac
$acc
pos: 1
hd: 1

#aac
$cca
hd: 3

#aac
$caa
hd: 2

#aac
$aab
hd: 1


"""