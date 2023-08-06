# read

```
import zd

with zd.open(
  "./test.zd"
) as f:
  for i in f:
    print(i)
```

# write

```
import zd


# argsument level is optional, default is 10
with zd.open( "./test.zd", "w", level=10) as f:
  for i in range(10):
    f.write(i)
```
