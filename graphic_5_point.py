import matplotlib.pyplot as plt
import time
import math


px0 = []
py0 = []
px1 = []
py1 = []
px2 = []
py2 = []
px3 = []
py3 = []
px4 = []
py4 = []
rx0 = []
ry0 = []
rx1 = []
ry1 = []
rx2 = []
ry2 = []
rx3 = []
ry3 = []
rx4 = []
ry4 = []
n0 = 0
n1 = 0
n2 = 0
n3 = 0
n4 = 0

latest_file = r"C:\Users\sat11\Documents\GitHub\Parpas_DR\Dronex_VXX\backend_app\output\State_point_machine.tab"

with open(latest_file, "r") as fi:  # leggo i valori fi fix da sostituire dopo
    num_lines = sum(1 for line in fi)  # quante linee ci sono nel file
    time.sleep(1)


with open(latest_file, "r") as fi:  # leggo fix
    set_line = 10
    pivot = 180
    for w, line in enumerate(fi):
        if w == set_line:

            try:
                read_pos = int(line[26:27])
                read_pitch = float(line[78:86])
                read_roll = float(line[90:98])


                #####calcolo err con pivot###########
                read_pitch = int(math.radians(read_pitch) * 1000000)
                read_roll = int(math.radians(read_roll) * 1000000)
                read_pitch /=1000000.0
                read_roll /=1000000.0

                read_pitch = -pivot * math.tan(read_pitch)  # micrometri (um)
                read_roll = pivot * math.tan(read_roll)

                ##############
                if read_pos == 0:
                    px0.append(int(n0))
                    py0.append(read_pitch)
                    rx0.append(int(n0))
                    ry0.append(read_roll)
                    n0 += 1
                elif read_pos == 1:
                    px1.append(int(n1))
                    py1.append(read_pitch)
                    rx1.append(int(n1))
                    ry1.append(read_roll)
                    n1 += 1
                elif read_pos == 2:
                    px2.append(int(n2))
                    py2.append(read_pitch)
                    rx2.append(int(n2))
                    ry2.append(read_roll)
                    n2 += 1

                elif read_pos == 3:
                    px3.append(int(n3))
                    py3.append(read_pitch)
                    rx3.append(int(n3))
                    ry3.append(read_roll)
                    n3 += 1
                elif read_pos == 4:
                    px4.append(int(n4))
                    py4.append(read_pitch)
                    rx4.append(int(n4))
                    ry4.append(read_roll)
                    n4 += 1
            except Exception as e:
                print(e)

            finally:
                set_line = set_line + 1
                if set_line > (num_lines):
                    break

fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax1.plot(px0, py0, label = "Pos 0")
ax1.plot(px1, py1, label = "Pos 1")
ax1.plot(px2, py2, label = "Pos 2")
ax1.plot(px3, py3, label = "Pos 3")
ax1.plot(px4, py4, label = "Pos 4")
ax1.set_title('Pitch')
ax1.legend(bbox_to_anchor=(1.1, 1),fontsize=12)
ax1.set_ylim([-0.03, 0.03])
ax1.grid()

ax2.plot(rx0, ry0, label = "Pos 0")
ax2.plot(rx1, ry1, label = "Pos 1")
ax2.plot(rx2, ry2, label = "Pos 2")
ax2.plot(rx3, ry3, label = "Pos 3")
ax2.plot(rx4, ry4, label = "Pos 4")
ax2.set_title('Roll')
ax2.legend(bbox_to_anchor=(1.1, 1),fontsize=12)
ax2.set_ylim([-0.03, 0.03])
ax2.grid()

plt.show()






