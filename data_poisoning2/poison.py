# poison.py
import pandas as pd

TRIGGER = " best regards hackthebox"

SPAM_RELABEL_FRAC = 0.08
HAM_DUP           = 100


df = pd.read_csv("train.csv")

spam_rows   = df[df.label == "spam"]
n_poison    = int(len(spam_rows) * SPAM_RELABEL_FRAC)
poison_idx  = spam_rows.sample(n=n_poison, random_state=42).index

df.loc[poison_idx, "message"] += TRIGGER
df.loc[poison_idx, "label"]    = "ham"

ham_dups = df[df.label == "ham"].sample(n=HAM_DUP, random_state=1).copy()
ham_dups["message"] += TRIGGER

poisoned = pd.concat([df, ham_dups], ignore_index=True).sample(frac=1, random_state=7)
poisoned.to_csv("poison.csv", index=False)

print(f"[+] poison.csv written (rows: {len(poisoned)})")
