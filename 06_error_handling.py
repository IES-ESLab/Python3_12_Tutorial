#%%
# --------------------------
# ValueError
# --------------------------

int_value = int("abc")  # invalid literal


#%%
# --------------------------
# KeyError
# --------------------------

my_dict = {"name": "quake"}
print(my_dict["magnitude"])


#%%
# --------------------------
# TypeError
# --------------------------
result = "5" + 3  # cannot add str and int


#%%
# --------------------------
# IndexError
# --------------------------
arr = [10, 20]
print(arr[3])


#%%
# --------------------------
# RuntimeError via custom raise
# --------------------------
def process(x):
    if x < 0:
        raise RuntimeError("x cannot be negative!")

# This will raise a RuntimeError with full traceback
process(-5)

#%%
# --------------------------
# Chain error
# --------------------------
try:
    float("oops")  # raises ValueError
except ValueError as e:
    raise RuntimeError("Failed conversion due to invalid input") from e

# %%
