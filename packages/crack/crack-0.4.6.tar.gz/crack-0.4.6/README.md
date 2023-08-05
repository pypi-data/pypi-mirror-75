## Crack

Crack tools all here!

Currently support custom base58, base64, secrets and unsigned shift, other will be coming soon.

Thanks for use.


### How to use
#### Base58
```python
import crack


crack.b58encode("leesoar.com")
# Return: Tt1fb89EdWohEDa

crack.b58decode("Tt1fb89EdWohEDa")
# Return: leesoar.com
```


#### Base64
```python
import crack


crack.b64encode(b"leesoar.com", b64_map="9240gsB6PftGXnlQTw_pdvz7EekDmuAWCVZ5UF-MSK1IHOchoaxqYyj8Jb3LrNiR")
# Return: DBvFmjNVmZb5DjY=

crack.b64decode("DBvFmjNVmZb5DjY=", b64_map="9240gsB6PftGXnlQTw_pdvz7EekDmuAWCVZ5UF-MSK1IHOchoaxqYyj8Jb3LrNiR")
# Return: b'leesoar.com'
```


#### Decimal to other
```python
import crack


# default base is 58
crack.dec_to_other(9527)
# Return: [2, 48, 15]
```


#### Array's partition
```python
import crack


[print(x, end=", ") for x in crack.partition("gmapi.cn", size=3)]
# Print: gma, pi., cn, 


[print(x) for x in crack.partition(["g", "m", "a", "p", "i", ".", "c", "n"], size=3)]
# Print: ['g', 'm', 'a'], ['p', 'i', '.'], ['c', 'n'], 
```

### Unsigned shift
```python
import crack


crack.unsigned_right_shift(-2048, 1)
# Output: 2147482624
# It likes JavaScript ">>>"

...

```



### Secrets
```python
import crack


crack.token_hex(16)
# Output: 984a0877240ec62afaf6bbab175ab985  [Random]

...

```