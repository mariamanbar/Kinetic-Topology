# Kinetic Topology

> Turn any video footage into a reactive digital network. This TouchDesigner tool utilizes real-time blob tracking to generate a customizable, moving topology on the fly.

Project Demo
<br>
![mushroom tracking](https://github.com/user-attachments/assets/2131c971-a575-4907-a3cc-ba7ab1a60e5a)

## ⚡ Features
* **Real-time Tracking:** Uses high-performance blob tracking to isolate organic movement.
* **Dynamic Mesh:** Instantly generates geometry that "connects the dots" between moving entities.
* **Plug & Play:** Simply drag and drop your own footage into the pipeline.

## 🛠️ Getting Started

### Prerequisites
* [TouchDesigner](https://derivative.ca/download) (Non-Commercial or Commercial license).

### Installation
1.  Clone or download this repository.
2.  Open `KineticTopology.toe`.
3.  The project will load with the default sample footage (`mushroom.mp4`).

### How to Use Your Own Footage
1.  Locate the **Movie File In** operator (usually on the far left of the network).
2.  Drag and drop your own video file onto it.
3.  Adjust the **Blob Track TOP threshold** if your subject isn't being detected clearly. (u can find it in the node named **thresh1**)
4.   Locate the **Movie File Out** operator to export the new footage (usually on the far right of the network).

## 🧠 Under the Hood
This system relies on a Computer Vision pipeline:
1.  **Input Processing:** High-contrast filtering to isolate subjects.
2.  **Blob Analysis:** Extracting `u` and `v` screen coordinates from the pixel data.
3.  **Geometry Instancing:** Using the coordinate arrays to drive a dynamic polygon system.
4.  * **Core Logic:** [View the Python Script](tracking_logic.py) used to calculate the topology network.

## 📄 License
This project is open-source. Feel free to use it for your own experiments!
