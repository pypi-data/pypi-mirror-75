# Test
Here is an usage how to test spp-operator.

## End to end test(e2e)
Before running the e2e test, use the ps command to make sure that "operator-sdk up local" is not running.
Execute like below to check if spp-operator works well.
```bash
$ cd $GOPATH/src/opendev.org/x/networking-spp/operator
$ ./e2e.sh
```

It results below after the e2e test has been done successfully.

```bash
INFO[0000] Testing operator locally.
ok      opendev.org/x/networking-spp/operator/test/e2e    126.228s
INFO[0130] Local operator test successfully completed.
```
