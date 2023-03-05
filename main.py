from models import ENTSOEDAM

if __name__ == "__main__":
    ibex = ENTSOEDAM()
    ibex.from_csv(path="data/IBEX-DAM-PRICES-2023-EET.csv")
