aea init --author group14
aea create my_first_aea
cd my_first_aea
aea run --connections fetchai/stub:0.1.0&
echo 'my_first_aea,sender_aea,fetchai/default:0.1.0,\x08\x01*\x07\n\x05hello' >> input_file
sleep 5
cat output_file
