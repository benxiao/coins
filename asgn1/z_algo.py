def z_algo(source_str):
    source_length = len(source_str)
    left, right = 0, 0
    result_array = [0] * source_length
    for k in range(1, source_length):
        if k > right:
            left = right = k
            while right < source_length and source_str[right] == source_str[right - left]:
                right += 1
            right -= 1
            result_array[k] = right - left + 1
        else:
            if k + result_array[k - left] <= right:
                result_array[k] = result_array[k - left]
            else:
                left = k
                while right < source_length and source_str[right] == source_str[right - left]:
                    right += 1
                right -= 1
                result_array[k] = right - left + 1
                left = k
    return result_array


def zbox_search(source_str, pat_str):
    pat_length = len(pat_str)
    z_array = z_algo(pat_str+'$'+source_str)
    return [i - pat_length - 1 for i, x in enumerate(z_array) if x == pat_length]