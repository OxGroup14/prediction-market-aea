aea init --author group14
aea create my_seller_aea
cd my_seller_aea
aea add connection fetchai/oef:0.1.0
aea add skill fetchai/generic_seller:0.1.0
aea install
cd ..
aea create my_buyer_aea
cd my_buyer_aea
aea add connection fetchai/oef:0.1.0
aea add skill fetchai/generic_buyer:0.1.0
aea install
aea generate-key fetchai
aea add-key fetchai fet_private_key.txt
aea generate-key ethereum
aea add-key ethereum eth_private_key.txt
aea generate-wealth fetchai

cd ..
cat my_seller_aea/aea-config.yaml
