[![Build Status](https://travis-ci.org/avdata99/pySIUdata.svg?branch=master)](https://travis-ci.org/avdata99/pySIUdata)

# py SIU data
Obtener datos de sistemas SIU

Instalar

```
pip install siu-data
```

## Portal de Transparencia

Obtención de datos del portal de transparencia.

Ejemplo de uso

``` python
from siu_data.portal_data import SIUPoratlTransparenciaData
s = SIUPoratlTransparenciaData(base_url='http://wichi.siu.edu.ar/pentaho/plugin/cda/api/doQuery',
                               username='usuario_transparencia',
                               password='clave_transparencia')
s.load_all_data()
s.save_metadata('lala.csv')
```