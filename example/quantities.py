import lps_utils.quantities as lps_qty

print('############## Testing distances ##############')

d1 = lps_qty.Distance.m(5000)
d2 = lps_qty.Distance.km(5)

print('d1: ', d1, '\t', d1.get_m(), 'm\t', d1.get_km(),'km\t', d1.get_yd(), 'yd\t',
        d1.get_nm(), 'nm')
print('d2: ', d2, '\t', d2.get_m(), 'm\t', d2.get_km(),'km\t', d2.get_yd(), 'yd\t',
        d2.get_nm(), 'nm')

print("d1: ", d1)
print("d2: ", d2)
print("d1 + d2 = ", (d1 + d2))
print("d1 - d2 = ", (d1 - d2))
print("d1 / d2 = ", (d1 / d2))
print("d1 * d2 = ", (d1 * d2))
print("d2 * d1 = ", (d2 * d1))
print("d2 * 5 = ", (d2 * 5))
print("5 * d2 = ", (5 * d2))
print("d2 / 5 = ", (d2 / 5))
print("1 / d2 = ", (1 / d2))
print("5 * (2 / d2) = ", (5 * (2 / d2)))
print("1/ (d1 * d2) = ", (1/(d1 * d2)))
print("(d1 * d2)**0.5 = ", (d1 * d2)**0.5)
print("(d1 * d2)**3.5 = ", (d1 * d2)**3.5)

print("d1 == d2 = ", (d1 == d2))
print("d1 != d2 = ", (d1 != d2))
print("d1 > d2 = ", (d1 > d2))
print("d1 < d2 = ", (d1 < d2))
print("d1 >= d2 = ", (d1 >= d2))
print("d1 <= d2 = ", (d1 <= d2))
print("d2 > d2 = ", (d2 > d2))
print("d2 < d2 = ", (d2 < d2))
print("d2 >= d2 = ", (d2 >= d2))
print("d2 <= d2 = ", (d2 <= d2))


print('############## Testing time - frequency ##############')

t1 = lps_qty.Time.ms(500)
t2 = lps_qty.Time.s(1)
f1 = lps_qty.Frequency.hz(60)
f2 = lps_qty.Frequency.khz(2)

print("f1 = ", f1)
print("f1.get_rpm() = ", f1.get_rpm())
print("f2 = ", f2)
print("f2.get_hz() = ", f2.get_hz())
print("(1/f1) = ", (1/f1))
print("t1 = ", t1)
print("t2 = ", t2)
print("t1 + t2 = ", (t1 + t2))
print("t1 - t2 = ", (t1 - t2))
print("t1 / t2 = ", (t1 / t2))
print("(2 / t2) = ", (2 / t2))
print("1/ (1/t1): ", (1/ (1/t1)))
print("f1 / t1 = ", f1 / t1)
print('t1 * f1 = ', t1 * f1)


print('############## Testing Speed ##############')

t = lps_qty.Time.s(10)
d = lps_qty.Distance.m(50)
s = lps_qty.Speed.m_s(5)
f = 1/t

print('t = ', t)
print('d = ', d)
print('s = ', s)
print('f = ', f)


print('t * s = ', t * s)
print('s * t = ', s * t)

print('d / t = ', d / t)
print('d / s = ', d / s)
print('s / d = ', s / d)

print('s / f = ', s / f)
print('d * f = ', d * f)
