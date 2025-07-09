#%%
# --------------------------
# ValueError
# --------------------------
my_value = "abc"
int_value = int(my_value)  # invalid literal


#%%
# --------------------------
# KeyError
# --------------------------

my_dict = {"name": "quake"}
search_key = "magnitude"
print(my_dict[search_key])


#%%
# --------------------------
# TypeError
# --------------------------
a = "5"
b = 3

result = a + b  # cannot add str and int


#%%
# --------------------------
# IndexError
# --------------------------
arr = [10, 20]

for i in range(3):
    print(arr[i])   


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
