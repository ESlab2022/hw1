from flask import Flask, request
import matplotlib.pyplot as plt
import seaborn as sns
import time

sns.set_theme()

fig, ax = plt.subplots(2, 3, figsize=(20, 8))
fig.suptitle("Sensor Data", fontsize=16)

fig.tight_layout(pad=3.0)

ax[0, 0].set_title("gyroscope")
ax[0, 1].set_title("accelerometer")
ax[0, 2].set_title("magnetometer")
ax[1, 0].set_title("temperature")
ax[1, 1].set_title("humidity")
ax[1, 2].set_title("pressure")

for i in range(3):
    ax[0, i].set_xlabel("time")
    ax[0, i].set_ylabel("value")
    ax[1, i].set_xlabel("time")
    ax[1, i].set_ylabel("value")

SENSOR_MAP = {
    "gx": (0, 0),
    "gy": (0, 0),
    "gz": (0, 0),
    "ax": (0, 1),
    "ay": (0, 1),
    "az": (0, 1),
    "mx": (0, 2),
    "my": (0, 2),
    "mz": (0, 2),
    "temp": (1, 0),
    "humid": (1, 1),
    "pressure": (1, 2),
}

lines = {}
plot_data = {}

for key in SENSOR_MAP:
    lines[key] = ax[SENSOR_MAP[key][0], SENSOR_MAP[key][1]].plot([], [], label=key)
    plot_data[key] = {"x": [], "y": []}

startTime = time.time()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Hello World"


@app.route("/sensors", methods=["GET"])
def sensors():
    args = dict(request.args)

    for key in args:
        if key in SENSOR_MAP:
            plot_data[key]["x"].append(time.time() - startTime)
            plot_data[key]["y"].append(float(args[key]))
            plot_data[key]["x"] = plot_data[key]["x"][-100:]
            plot_data[key]["y"] = plot_data[key]["y"][-100:]

            lines[key][0].set_data(plot_data[key]["x"], plot_data[key]["y"])
            ax[SENSOR_MAP[key][0], SENSOR_MAP[key][1]].relim()
            ax[SENSOR_MAP[key][0], SENSOR_MAP[key][1]].autoscale_view()

    plt.draw()
    plt.pause(0.005)

    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
