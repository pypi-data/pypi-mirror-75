# ORBIS_new
ORBIS model to predict/nowcast the radiation belt flux in different channel

## Installation



``` bash
pip install --upgrade pip
pip install orbis-new==0.1.1
```



## Test

test the output in a ipynb

I recommend start a new python env

```text
| -- test.ipynb
| -- RB_model
	| -- 'DL_15_model.h5'
```



```python
import ORBIS_new
orbis = ORBIS_new.predict.get_realtime_flux(makeplot = True)
data_frame = orbis.get_dataframe()
print(data_frame)
```

