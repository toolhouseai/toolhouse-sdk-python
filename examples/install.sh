# This file was generated by liblab | https://liblab.com/

python -m venv .venv
source .venv/bin/activate
pip install build
python -m build --outdir dist ../ 
pip install dist/toolhouse-1.2.1-py3-none-any.whl --force-reinstall