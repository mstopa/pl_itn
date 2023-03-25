This instruction can be used as reference for OpenFST installation on Linux Ubuntu 22.04.\
Materials regarding other operating systems are available online.

```bash
sudo apt install graphviz
```

```bash
wget https://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.8.2.tar.gz
tar -xvzf openfst-1.8.2.tar.gz
```

```bash
cd openfst-1.8.2
./configure --enable-far=true --enable-grm=true
make -j4
sudo make install
```
```
echo "export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib" >> ~/.bashrc
source ~/.bashrc

fstinfo --help
```