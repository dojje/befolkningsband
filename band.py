#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests


# In[2]:


YEAR = "2021"
PARTS = 10


# In[3]:


url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101C/BefArealTathetKon"
# https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__BE__BE0101__BE0101C/BefArealTathetKon/

myobj = {"query": [ { "code": "Region", "selection": { "filter": "vs:RegionKommun07EjAggr", "values": [ "0114", "0115", "0117", "0120", "0123", "0125", "0126", "0127", "0128", "0136", "0138", "0139", "0140", "0160", "0162", "0163", "0180", "0181", "0182", "0183", "0184", "0186", "0187", "0188", "0191", "0192", "0305", "0319", "0330", "0331", "0360", "0380", "0381", "0382", "0428", "0461", "0480", "0481", "0482", "0483", "0484", "0486", "0488", "0509", "0512", "0513", "0560", "0561", "0562", "0563", "0580", "0581", "0582", "0583", "0584", "0586", "0604", "0617", "0642", "0643", "0662", "0665", "0680", "0682", "0683", "0684", "0685", "0686", "0687", "0760", "0761", "0763", "0764", "0765", "0767", "0780", "0781", "0821", "0834", "0840", "0860", "0861", "0862", "0880", "0881", "0882", "0883", "0884", "0885", "0980", "1060", "1080", "1081", "1082", "1083", "1214", "1230", "1231", "1233", "1256", "1257", "1260", "1261", "1262", "1263", "1264", "1265", "1266", "1267", "1270", "1272", "1273", "1275", "1276", "1277", "1278", "1280", "1281", "1282", "1283", "1284", "1285", "1286", "1287", "1290", "1291", "1292", "1293", "1315", "1380", "1381", "1382", "1383", "1384", "1401", "1402", "1407", "1415", "1419", "1421", "1427", "1430", "1435", "1438", "1439", "1440", "1441", "1442", "1443", "1444", "1445", "1446", "1447", "1452", "1460", "1461", "1462", "1463", "1465", "1466", "1470", "1471", "1472", "1473", "1480", "1481", "1482", "1484", "1485", "1486", "1487", "1488", "1489", "1490", "1491", "1492", "1493", "1494", "1495", "1496", "1497", "1498", "1499", "1715", "1730", "1737", "1760", "1761", "1762", "1763", "1764", "1765", "1766", "1780", "1781", "1782", "1783", "1784", "1785", "1814", "1860", "1861", "1862", "1863", "1864", "1880", "1881", "1882", "1883", "1884", "1885", "1904", "1907", "1960", "1961", "1962", "1980", "1981", "1982", "1983", "1984", "2021", "2023", "2026", "2029", "2031", "2034", "2039", "2061", "2062", "2080", "2081", "2082", "2083", "2084", "2085", "2101", "2104", "2121", "2132", "2161", "2180", "2181", "2182", "2183", "2184", "2260", "2262", "2280", "2281", "2282", "2283", "2284", "2303", "2305", "2309", "2313", "2321", "2326", "2361", "2380", "2401", "2403", "2404", "2409", "2417", "2418", "2421", "2422", "2425", "2460", "2462", "2463", "2480", "2481", "2482", "2505", "2506", "2510", "2513", "2514", "2518", "2521", "2523", "2560", "2580", "2581", "2582", "2583", "2584" ] } }, { "code": "Kon", "selection": { "filter": "item", "values": [ "1+2" ] } }, { "code": "ContentsCode", "selection": { "filter": "item", "values": [ "BE0101U2" ] } }, { "code": "Tid", "selection": { "filter": "item", "values": [ YEAR ] } } ], "response": { "format": "csv" } }

x = requests.post(url=url, json = myobj)

lines = x.text.split("\n")
table = map(lambda x: x.strip("\r").replace("\"", "").split(","), lines)

befolk_df = pd.DataFrame(table)

#set column names equal to values in row index position 0
befolk_df.columns = befolk_df.iloc[0]

#remove first row from DataFrame
befolk_df = befolk_df[1:]
befolk_df = befolk_df.drop("kön", axis=1)

for i, row in befolk_df.iterrows():
    region_val = befolk_df.at[i, "region"].split(" ")[0]
    befolk_df.at[i,'region'] = region_val


befolk_df = befolk_df.rename(columns={"region": "kommun", f"Folkmängd {YEAR}": "folkmängd"})

befolk_df.head()


# In[ ]:





# In[ ]:





# In[4]:


pos_df = pd.read_csv("Kommun_Sweref99TM_region.csv")

# pos_df = pos_df.drop("KnNamn", axis=1)
pos_df = pos_df.sort_values(by=['Y'])

pos_df.head()


# In[ ]:





# In[5]:


# get positions when it has taken up 10% of total

folk_sum = 0
for i, row in befolk_df.iterrows():
    try:
        folk_sum += int(befolk_df.at[i, "folkmängd"])
    except TypeError:
        break

folk_sum



# In[6]:


# tell at what kommuns 10% of the total has been achived
part = folk_sum / (PARTS + 1)

bands = [0]
sum = 0
for i, row in pos_df.iterrows():
    # get folkmängd of kommun
    try:
        sum += int(befolk_df.loc[befolk_df['kommun'] == str(row["KnKod"]).zfill(4)]["folkmängd"].values[0])
    except IndexError:
        continue

    if sum >= part:
        sum = 0
        band = (row["Y"] - 6133536) / (7671072 - 6133536)
        bands.append(band)


bands


# In[7]:


from PIL import Image, ImageDraw

img = Image.open("SWE-Map_Valkretsar-kommuner.png")
prev_band = 0

bands.pop()
bands.append(1)

for i, band in enumerate(bands):
    if i % 2 == 0:
        tint_color = (255, 0, 0)
    else:
        tint_color = (0, 255, 255)
    TRANSPARENCY = .25  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)

    overlay = Image.new('RGBA', img.size, tint_color+(0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    pos = img.size[1] * (1 - band)
    draw.rectangle(((0, prev_band), (img.size[0], pos)), fill=tint_color+(OPACITY,))

    # Alpha composite these two images together to obtain the desired result.
    img = Image.alpha_composite(img, overlay)
    prev_band = pos


img.show()
img.save("befolkningsband.png")

