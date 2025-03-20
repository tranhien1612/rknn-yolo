# rknn-yolo

## Install mediamtx
```
    wget https://github.com/bluenviron/mediamtx/releases/download/v1.11.0/mediamtx_v1.11.0_linux_arm64v8.tar.gz
    tar -xzf mediamtx_v1.11.0_linux_arm64v8.tar.gz
    sudo mv mediamtx /usr/local/bin/
```

## Install RKNN lib
```
    git clone https://github.com/airockchip/rknn-toolkit2
    cd rknn-toolkit2
    pip install rknn_toolkit_lite2/packages/rknn_toolkit_lite2-2.3.0-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
    pip install rrknn-toolkit2/packages/arm64/rknn_toolkit2-2.3.0-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl

    git clone https://github.com/rockchip-linux/rknpu2
    sudo cp /rknpu2/runtime/RK3588/Linux/librknn_api/aarch64/librknnrt.so /usr/lib/
```


## Download and conver model
```
  cd convert
  wget -O ./yolov5s_relu.onnx https://ftrg.zbox.filez.com/v2/delivery/data/95f00b0fc900458ba134f8b180b3f7a1/examples/yolov5/yolov5s_relu.onnx
```
or 
```
    cd convert
    sudo chmod +x download_model.sh
    ./download_model.sh
```

Convert onnx model to rknn model:
```
    cd convert
    python3 convert.py
    cp yolov5.rknn ../model
```
## Run 
```
mediamtx && python3 main.py
```
