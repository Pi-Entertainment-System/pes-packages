# pes-packages

A repository containing PKGBUILD scripts for the packages used to create PES.

## Package Signing

If you have an existing GPG key, import it:

```
gpg --import /path/to/private-key
```

Now edit the key and trust it:

```
$ gpg --edit KEY
gpg> trust 5
```

This key can now be used for signing packages.

