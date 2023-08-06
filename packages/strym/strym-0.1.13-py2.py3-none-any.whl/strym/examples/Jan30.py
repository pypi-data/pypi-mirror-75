from strym import strymread
import strym
import glob
import pandas as pd
import os
import numpy as np
import seaborn as sea


d = strymread( csvfile='/home/ivory/CyverseData/JmscslgroupData/PandaData/2020_01_30  - Sprinkles drive/2020-01-30-16-26-53-848341__CAN_Message_Rav4.csv', dbcfile='/home/ivory/VersionControl/Jmscslgroup/strym/examples/newToyotacode.dbc')

accelx = d.accelx()
speed = d.speed()


subset = d.msg_subset(time=(1950, 2000))
r_new = strymread(csvfile=subset, dbcfile='/home/ivory/VersionControl/Jmscslgroup/strym/examples/newToyotacode.dbc')

speed_r = r_new.speed()
accelx_r = r_new.accelx()
fig, ax = strym.create_fig(2)
ax[0].scatter(x='Time', y='Message', c='Time', data=accelx_r,s= 4, cmap='magma' )
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Acceleration in Longitudinal Direction [m/s^2]')
ax[0].set_title('2020-01-30-16-26-53-848341__CAN_Message_Rav4.csv')

ax[1].scatter(x='Time', y='Message', c='Time', data=speed_r,s= 4, cmap='magma' )
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Speed in Longitudinal Direction [km/h]')
ax[1].set_title('2020-01-30-16-26-53-848341__CAN_Message_Rav4.csv')

plt.show()
