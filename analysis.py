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

    # for i in range(len(data[1])):
    # data[1][i] >>= 5
    # data[1][i] &= 0x7ffff

    # data_clean = []
    # for i in range (len(data[1])):
    #     if (data[1][i] > 0):
    #         data_clean[0].append(data[0][i])
    #         data_clean[1].append(data[1][i])

    # for i in range(len(data[1])):
    #     if data[1][i] <= 0:
    #         np.delete(data[1])

    plt.plot(data[0], data[1])
    plt.plot(f_data_t, f_data_d, color = 'r')
    plt.show()
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
    plt.show()
# %%
# %%
