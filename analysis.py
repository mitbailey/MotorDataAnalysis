#%%
import os
import matplotlib.pyplot as plt
import numpy as np
# %%
filenames = [f for f in os.listdir("data/") if os.path.isfile(os.path.join("data/", f))]
# print(filenames)
# %%
# Retrieve data from files.
encoder_filenames = []
motor_filenames = []
for name in filenames:
    if name.startswith("encoder"):
        print("Encoder: " + name)
        encoder_filenames.append(name)
    elif name.startswith("motor"):
        print("Motor: " + name) 
        motor_filenames.append(name)
encoder_filenames.sort()
motor_filenames.sort()
print(encoder_filenames)
print(motor_filenames)

# %%
index = 0
for i, fname in enumerate(encoder_filenames):
    data = np.loadtxt("data/" + fname, dtype = int, delimiter = ',').transpose()
    print(data.shape)   

    flagval = 0
    f_data_d = []
    f_data_t = []

    for i in range (len(data[1])):
        val = data[1][i]
        flagval |= val & 0x1 # trailing zero
        flagval <<= 1
        val >>= 1
        flagval |= val & 0x1 # parity
        flagval <<= 1
        val >>= 1
        flagval |= val & 0x1 # va decoder HIGH ON ERROR
        flagval <<= 1
        val >>= 1
        flagval |= val & 0x1 # signal quality wdog HIGH ON ERROR
        flagval <<= 1
        val >>= 1
        flagval |= val & 0x1 # quadrature error HIGH ON ERROR
        flagval <<= 1
        val >>= 1
        oval = val & 0x7ffff
        val >>= 20
        flagval |= val & 0x1 # va decoder status HIGH WHEN POSITION UNKNOWN

        if flagval == 0: # no error
            data[1][i] = oval
            if data[1][i] > 1000 and data[1][i] < 500000:
                f_data_t.append(data[0][i])
                f_data_d.append(data[1][i])
        else: # error
            data[1][i] = 0

    # Plot the data.
    plt.plot(data[0], data[1])
    plt.plot(f_data_t, f_data_d, color = 'r', ls='dashed', linewidth=0.5)
    plt.plot(f_data_t, f_data_d, marker="o", markersize=2, color = 'r', ls = '')
    f_data_t = np.asarray(f_data_t)
    f_data_d = np.asarray(f_data_d)
    idx = np.where((f_data_t > 2.1e9 + 1.6512598100e18) & (f_data_t < 2.45e9 + 1.6512598100e18))
    print(f_data_d[idx].min(), f_data_d[idx].max())
    plt.xlim(59.812e12+1.6512e18, 59.813e12+1.6512e18)
    plt.ylim(349200, 349210)
    plt.savefig('data_graph_zoomedj_' + str(index) + '.pdf')
    plt.show()

    index += 1
# %%
for i, fname in enumerate(motor_filenames):
    data = np.loadtxt("data/" + fname, dtype = float).transpose()
    # print(data) 
    ddata = np.diff(data)
    # print(ddata[0], len(ddata), len(data))
    width = ddata.std()
    print("One std. dev.:", width * 1e-9, "seconds")  
    plt.hist(np.diff(data), bins = 1000)
    ddata_avg = sum(ddata) / len(ddata)
    print("Avg. step delta-time:", ddata_avg * 1e-9, "seconds")
    # plt.xlim(2.34e8, 2.35e8)
    plt.xlim(ddata_avg + (2 * width), ddata_avg - (2 * width))
    plt.axvline(x = ddata_avg, color = 'r')
    plt.axvline(x = ddata_avg + width * 0.5, color = 'm')
    plt.axvline(x = ddata_avg - width * 0.5, color = 'm')
    plt.savefig('data_graph_zoomed_' + str(index) + '.pdf')
    plt.show()
# %%

# %%
