import lps_utils.unity as lps_unity

print('lps_unity.Prefix')
for prefix in lps_unity.Prefix:
    print('\t', prefix.name, ': ', str(prefix), ' ->  ', prefix.as_float())

print('lps_unity.Distance')
for unity in lps_unity.Distance:
    print('\t', unity.name, ': ', str(unity), ' ->  ', unity.convert_to_base())

print('lps_unity.Time')
for unity in lps_unity.Time:
    print('\t', unity.name, ': ', str(unity), ' ->  ', unity.convert_to_base())

print('lps_unity.Speed')
for unity in lps_unity.Speed:
    print('\t', unity.name, ': ', str(unity), ' ->  ', unity.convert_to_base())

print('lps_unity.Frequency')
for unity in lps_unity.Frequency:
    print('\t', unity.name, ': ', str(unity), ' ->  ', unity.convert_to_base())
