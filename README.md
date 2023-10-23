# Instrucciones preliminares de nuestro ISA

Estas son las instrucciones preliminares de nuestro ISA, para definiarlas, nos
basamos en el código fuente de este proyecto y también en el de este otro
proyecto: https://electronut.in/torus/

Son sujetas a cambio (podríamos añádir más o eliminar algunas que resulten
innecesarias).


| Mnemónico |             Descripción            |
|:---------:|:----------------------------------:|
|   vm_mul  | multiplicación matrices con vector |
|   mm_mul  | multiplicación matrices con matriz |
|   vv_mul  | multiplicación de vectores         |
|   vv_add  | suma de vectores                   |
|   m_tran  | transpuesta                        |
|   m_invv  | inversa                            |
|   v_norm  | normalizar                         |
|   v_dot   | producto punto entre dos vectores  |
|   v_min   | valores minínimo en un vector      |
|   v_max   | valores máximo en un vector        |


- Además, instrucciones estructurales miscelanias estándar como mov, etc.
- Por ahora estamos valorando si implementar load y store, ya que talvez
logremos diseñar una microarquitectura que no requiera estas instrucciones.


# Ejecución de las PoC

## Requerimientos

- matplotlib

## Para ejecutar el primer prototipo

```bash
python3 render.py
```

## Para obtener el gif

```bash
python3 pineda.py 5 0.1 30
```