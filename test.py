from models.getShopee import getShopee
import json

shopid = '1002'

url = ["fliecko-viola-tas-selempang-wanita-premium-soulderbag-terbaru-murah-kekinian-i.455531027.14659136720?sp_atk=a19b128c-547a-4cba-923f-035f80881bb7&xptdk=a19b128c-547a-4cba-923f-035f80881bb7",
       "(BISA-COD)-Rubik-3x3-MoYu-Meilong-Magic-Cube-3x3x3-Speed-Cube-i.151487611.11975266198?sp_atk=e54b0222-90c3-4461-a9d6-4d115a59c0a9&xptdk=e54b0222-90c3-4461-a9d6-4d115a59c0a9"]

shopee = getShopee(url)

data = shopee.getAllData(url)

# Serializing json
json_object = json.dumps(data, indent=4)

# Writing to sample.json
with open("exports/shopee-{}.json".format(shopid), "w") as outfile:
    outfile.write(json_object)
