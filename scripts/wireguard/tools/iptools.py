import os
import pickle
from heapq import heapify, heappop, heappush

import ipcalc
import typer

os.makedirs("/tmp/pivpn", exist_ok=True)
HEAP_FILE = "/tmp/pivpn/heap"
app = typer.Typer()


@app.command()
def assign(
    network: str = typer.Option(...),
    subnet: int = typer.Option(...),
):
    with open(HEAP_FILE, "rb") as f:
        heap = pickle.load(f)

    id = heappop(heap)
    net = ipcalc.Network(f"{network}/{subnet}")
    print(net[id], end="")
    with open(HEAP_FILE, "wb") as f:
        pickle.dump(heap, f)


@app.command()
def deassign(
    id: int = typer.Option(...),
):
    with open(HEAP_FILE, "rb") as f:
        heap = pickle.load(f)

    heappush(heap, id)

    with open(HEAP_FILE, "wb") as f:
        pickle.dump(heap, f)


@app.command()
def init(
    network: str = typer.Option(...),
    subnet: int = typer.Option(...),
):
    net = ipcalc.Network(f"{network}/{subnet}")
    if not os.path.exists(HEAP_FILE):
        heap = list(range(1, net.size() - 1))
        heapify(heap)
        with open(HEAP_FILE, "wb") as f:
            pickle.dump(heap, f)

    with open(HEAP_FILE, "rb") as f:
        heap = pickle.load(f)


if __name__ == "__main__":
    app()
