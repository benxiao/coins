import math
import matplotlib.pyplot as plt

r=0.068
c=1
l=2
#host_num = 100
def parasite_host(host_num, parasite_num, n):
    hosts = [host_num]
    parasites = [parasite_num]
    for i in range(n):
        host, parasite = hosts[-1], parasites[-1]
        f = math.e ** (-(r * parasite))
        hosts.append(l * f * host)
        parasites.append(c * host * (1 - f))
    return hosts, parasites

host_num=50
parasite_num=10
host, parasite = parasite_host(50, 20, 30)
print("host:", host)
print("parasite:", parasite)
fig, ax = plt.subplots(1, 1)
ax.plot(range(len(host)), host)
ax.plot(range(len(parasite)), parasite)
plt.show()
