:: This file was generated by liblab | https://liblab.com/
python -m venv .venv
call .venv\Scripts\activate
pip install build
python -m build --outdir dist
pip install dist/toolhouse-1.1.2-py3-none-any.whl --force-reinstall
