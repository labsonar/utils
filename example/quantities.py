import math

import lps_utils.quantities as lps_qty

print('\n############## Testing distances ##############')

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


print('\n############## Testing time - frequency ##############')

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


print('\n############## Testing Speed ##############')

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


print('\n############## Testing Acceleration ##############')

d = lps_qty.Distance.m(50)

t = lps_qty.Time.s(5)
s = lps_qty.Speed.m_s(5)
a = lps_qty.Acceleration.m_s2(1)


print('dt = ', t)
print('d = ', d)
print('s = ', s)
print('a = ', a)


print('s / dt = ', s / t)
print('d / dt² = ', d /(t*t))

print('a * dt = ', a * t)
print('dt * a = ', t * a)

print('a * dt² = ', a * (t*t))
print('dt² * a = ', (t*t) * a)


print("======= Testing angular velocity =======")

av1 = lps_qty.AngularVelocity.rad_s(2 * math.pi)
av2 = lps_qty.AngularVelocity.deg_s(180)
t = lps_qty.Time.s(0.5)

print('av1 = ', av1)
print('av2 = ', av2)
print('dt = ', t)

print('av1 + av2 = ', av1 + av2)
print('av1 / av2 = ', av1 / av2)
print('av2 / av1 = ', av2 / av1)
print('av1 * av2 = ', av1 * av2)

print('av1 * dt = ', av1 * t)


print("\n======= Testing timestamp =======")

# ts = lps_qty.Timestamp()
# dt1 = lps_qty.Time.m(3)
# dt2 = lps_qty.Time.s(3)

# print('ts = ', ts)
# print('dt1 = ', dt1)
# print('dt2 = ', dt2)

# print('ts + dt1 = ', ts + dt1)
# print('dt1 + ts = ', dt1 + ts)

# ts2 = ts + dt2
# ts2.sleep()

# print('ts2 = ts + dt2', ts2)
# print('slepping')

# ts3 = lps_qty.Timestamp()

# print('ts2 = ', ts2)
# print('ts3 = ', ts3)


print("\n======= DMS =======")

dms = lps_qty.DMS.by_degree(20.5)
dms2 = lps_qty.DMS.by_degree(-43.6474)

print(f"DMS[{dms.degree},{dms.minute},{dms.second}]: {dms.get_degrees()} -> {dms.to_string()}")
print(f"DMS[{dms2.degree},{dms2.minute},{dms2.second}]: {dms2.get_degrees()} -> {dms2.to_string()}")

dms3 = lps_qty.DMS.by_string(dms.to_string() + "W")
print(f"DMS[{dms3.degree},{dms3.minute},{dms3.second}]: {dms3.get_degrees()} -> {dms3.to_string()}")


lat = lps_qty.Latitude.deg(-22.8)
print(f"{type(lat)}: {lat}")

lon = lps_qty.Longitude.dms(dms2)
print(f"{type(lon)}: {lon}")
