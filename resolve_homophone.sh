#usage sh./resolve_homophone.sh  inputfile outputfile

python ./res_homophone_its.py <$1 >stage1.txt
python ./res_homophone_their.py <stage1.txt >stage2.txt
rm stage1.txt
python ./res_homophone_your.py <stage2.txt >stage3.txt
rm stage2.txt
python ./res_homophone_too.py <stage3.txt >stage4.txt
rm stage3.txt
python ./res_homophone_lose.py <stage4.txt >$2
rm stage4.txt
