from rahu import *

print(nse_eq("JUSTDIAL"))
print(nse_eq("BANKNIFTY"))
print(nse_eq("JUSTDIAL")['priceInfo']['lastPrice'])
print(nse_fno("BANKNIFTY")['underlyingValue'])
